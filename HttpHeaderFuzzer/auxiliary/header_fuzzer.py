import urllib3
import threading
import requests
import csv
import os
from colorama import Fore
from queue import Queue
from time import sleep
from auxiliary.utils import *


class HeaderFuzzer:
    _args = None
    _data = []
    _url_queue = Queue()
    _processed_urls = None
    _tests_to_run = None
    _headers_to_fuzz = None
    _print_lock = threading.Lock()
    # Disable HTTPS related warnings
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def __init__(self, args):
        self._args = args
        self._tests_to_run = get_tests_to_run(args)
        self._headers_to_fuzz = get_headers_to_fuzz(args)

    def start(self, urls):
        self._processed_urls = normalize_urls(urls)
        print(Fore.YELLOW + '---------------------------------------------------------------')
        print(Fore.GREEN + '[*] Testing {} URLs'.format(len(urls)))
        print(Fore.GREEN + '[*] Testing {} headers'.format(len(self._headers_to_fuzz)))
        print(Fore.GREEN + '[*] Running {} types of tests'.format(len(self._tests_to_run)))
        print(Fore.YELLOW + '---------------------------------------------------------------')
        sleep(4)

        for i in range(self._args.threads):
            t = threading.Thread(target=self.process_queue)
            t.daemon = True
            t.start()

        for current_url in self._processed_urls:
            self._url_queue.put(current_url)

        self._url_queue.join()

        if self._args.csv:
            self.parse_to_csv(self._args.csv)

    def parse_to_csv(self, csv_name=None):
        """ Takes a list of lists and outputs to a csv file """
        csv_name = 'results.csv' if not csv_name else csv_name
        csv_file = None
        if not os.path.isfile(csv_name):
            csv_file = open(csv_name, 'w', newline='')
            csv_writer = csv.writer(csv_file)
            top_row = ['URL', 'Test Type', 'Header', 'Value', 'Status code', 'Length', 'Response Time', 'Reflection',
                       'Reflection context', 'Notes']
            csv_writer.writerow(top_row)
            print(Fore.CYAN + '\n[+] The csv file {} does not exist. New file created!\n'.format(csv_name))
        else:
            try:
                csv_file = open(csv_name, 'a', newline='')
            except PermissionError:
                print(Fore.RED + '\n[-] Permission denied while opening csv file {}. '
                                 'Results not saved.'.format(csv_name))
                exit()
            csv_writer = csv.writer(csv_file)
            print(Fore.CYAN + '\n[+]  {} exists. Appending to file!\n'.format(csv_name))

        for line in self._data:
            csv_writer.writerow(line)

        csv_file.close()

    def make_request(self, url, header=None, header_value=None):
        """ Builds a requests object, makes a request, and returns a response object """
        s = requests.Session()

        if not header == 'User-Agent':
            s.headers['User-Agent'] = get_random_useragent()

        s.headers[header] = header_value

        if self._args.credentials:
            credentials = self._args.credentials
            if 'authorization' in self._args.credentials.lower() and header != 'Authorization':
                cred_type = credentials.split(':')[0], cred_value = credentials.split(':')[1].lstrip()
                s.headers[cred_type] = cred_value
            elif self._args.credentials.lower().startswith('cookie:'):
                creds = self._args.credentials[7:].lstrip()
                cookies = creds.split(';')
                for cookie in cookies:
                    cookie_name = cookie.split('=')[0], cookie_value = '='.join(cookie.split('=')[1:]).lstrip()
                    s.cookies[cookie_name] = cookie_value

        if self._args.proxy:
            s.proxies['http'] = self._args.proxy
            s.proxies['https'] = self._args.proxy
        resp = s.get(url, verify=False, timeout=int(self._args.timeout))

        return resp

    def scanner_controller(self, url):
        """ Controls most of the logic for the script. Accepts a URL and calls various functions to make requests
        and prints output to the terminal. Returns nothing, but adds data to the data variable,
        which can be used to print to a file """
        for test in self._tests_to_run:
            with self._print_lock:
                print(Fore.LIGHTGREEN_EX + '[*] Running {} tests...'.format(test))
            for header in self._headers_to_fuzz:
                try:
                    header_values = get_header_values(test, header)
                except Exception as e:  # TODO: Print this. Also, find out why it's so broad.
                    continue
                if self._args.verbose:
                    with self._print_lock:
                        print(Fore.LIGHTGREEN_EX + '[*] Fuzzing {} header at {}'.format(header, url))
                for header_value in header_values:
                    request_data = []
                    try:
                        resp = self.make_request(url, header, header_value)
                    except Exception as e:
                        if self._args.verbose:
                            with self._print_lock:
                                print(Fore.RED + '[-] Unable to connect to site: {}'.format(url))
                                print(Fore.RED + '[*] {}'.format(e))
                        continue

                    status_code, length, reflection = self.test_headers(resp, header_value)
                    does_reflect = 'True' if reflection else 'False'
                    printable_header_value = header_value if len(header_value) < 80 else header_value[:80] + '...'
                    response_time = str(resp.elapsed.total_seconds())
                    if self._args.verbose:
                        with self._print_lock:
                            reflection_color = Fore.LIGHTCYAN_EX if does_reflect == 'True' else Fore.MAGENTA
                            print(Fore.LIGHTMAGENTA_EX + '-')
                            print(Fore.LIGHTBLUE_EX + '[+] URL: {}'.format(url))
                            print('    Test: {}'.format(test))
                            print('    Header: {}'.format(header))
                            print('    Value: {}'.format(printable_header_value))
                            if len(header_value) > 50:
                                print('    Value length: {} characters'.format(len(header_value)))
                            print('    Status Code: {}'.format(status_code))
                            print('    Response Length: {}'.format(length))
                            print('    Response Time: {}'.format(response_time))
                            print(reflection_color + '    Reflected in response: {}'.format(does_reflect))

                    if reflection:
                        if type(reflection) == list:
                            if len(reflection) < 10:
                                reflection = '\n'.join(reflection)
                            elif len(reflection) < 10:
                                reflection = "The value of the header reflected {} times. Probable false positive."
                            else:
                                reflection = reflection[0]
                    else:
                        reflection = ''
                    request_data.extend((url, test, header, header_value, status_code,
                                         length, response_time, does_reflect, reflection))
                    self._data.append(request_data)

    @staticmethod
    def test_headers(resp, header_value):
        status_code = resp.status_code
        length = str(len(resp.text))
        response_list = resp.text.splitlines()
        reflection = [line for line in response_list if header_value in line]

        return status_code, length, reflection

    def process_queue(self):
        """ Processes the URL queue and calls the scanner controller function """
        while True:
            current_url = self._url_queue.get()
            self.scanner_controller(current_url)
            self._url_queue.task_done()
