from sys import version
try:
    from queue import Queue
except ImportError as error:
    missing_module = str(error).split(' ')[-1]
    print('\nMissing module: {}'.format(missing_module))
    if not version.startswith('3'):
        print('\nThis script has only been tested with Python3. If using another version and encounter an error, try using Python3\n')
try:
    import requests
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
except ImportError as error:
    missing_module = str(error).split(' ')[-1]
    print('\nMissing module: {}'.format(missing_module))
    print('Try running "pip install {}", or do an Internet search for installation instructions.'.format(missing_module.strip("'")))
    exit()
import re
import argparse
import os
import threading
from time import sleep
from http_header_test_values import *
from http_header_tests import *
from http_header_helpers import *

if not version.startswith('3'):
    print('\nThis script has only been tested with Python3. If using another version and encounter an error, try using Python3\n')
    sleep(3)


__author__ = 'Jake Miller (@LaconicWolf)'
__date__ = '20180408'
__version__ = '0.01'
__description__ = '''Multithreaded website scanner that fuzzes HTTP
                  headers.
                  '''


def make_request(url, header=None, header_value=None):
    ''' Builds a requests object, makes a request, and returns 
    a response object.
    '''
    s = requests.Session()
    
    if not header == "User-Agent":
        s.headers['User-Agent'] = get_random_useragent()
        
    s.headers[header] = header_value
    
    if args.credentials:
        cred_type = credentials.split(':')[0]
        cred_value = credentials.split(':')[1].lstrip()
        s.headers[cred_type] = cred_value

    if args.proxy:
        s.proxies['http'] = args.proxy
        s.proxies['https'] = args.proxy
    
    resp = s.get(url, verify=False, timeout=int(args.timeout))
    return resp


def scanner_controller(url):
    ''' Controls most of the logic for the script. Accepts a URL and calls 
    various functions to make requests and prints output to the terminal.
    Returns nothing, but adds data to the data variable, which can be used 
    to print to a file. 
    '''
    global data
    for test in tests_to_run:
        with print_lock:
            print('\n[*] Running {} tests...'.format(test))
        for header in headers_to_fuzz:
            try:
                header_values = get_header_values(test, header)
            except Exception as e:
                continue
            if args.verbose:
                with print_lock:
                    print('\n[*] Fuzzing {} header at {}'.format(header, url))
            for header_value in header_values:
                request_data = []
                try:
                    resp = make_request(url, header, header_value)
                except Exception as e:
                    if args.verbose:
                        with print_lock:
                            print('[-] Unable to connect to site: {}'.format(url))
                            print('[*] {}'.format(e))
                    continue

                status_code, length, reflection = test_headers(url, test, resp, header, header_value)
                does_reflect = 'True' if reflection else 'False'
                printable_header_value = header_value if len(header_value) < 80 else header_value[:80] + '...' 
                if args.verbose:
                    with print_lock:
                        print('\n[+] URL: {}'.format(url))
                        print('    Test: {}'.format(test))
                        print('    Header: {}'.format(header))
                        print('    Value: {}'.format(printable_header_value))
                        if len(header_value) > 50:
                            print('    Value length: {} characters'.format(len(header_value)))
                        print('    Status Code: {}'.format(status_code))
                        print('    Response Length: {}'.format(length))
                        print('    Header reflected in response?: {}'.format(does_reflect))
                
                if reflection:
                    if type(reflection) == list:
                        if len(reflection) > 1:
                            reflection = '\n'.join(reflection)
                        else:
                            reflection = reflection[0]
                request_data.extend((url, test, header, header_value, status_code, length, does_reflect))
                data.append(request_data)


def process_queue():
    ''' processes the url queue and calls the scanner controller function
    '''
    while True:
        current_url = url_queue.get()
        scanner_controller(current_url)
        url_queue.task_done()


def main():
    ''' Normalizes the URLs and starts multithreading
    '''
    processed_urls = normalize_urls(urls)
    
    for i in range(args.threads):
        t = threading.Thread(target=process_queue)
        t.daemon = True
        t.start()

    for current_url in processed_urls:
        url_queue.put(current_url)

    url_queue.join()

    if args.csv:
        parse_to_csv(data, csv_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
    parser.add_argument("-ah", "--all_headers", help="Fuzz all headers", action="store_true")
    parser.add_argument("-at", "--all_tests", help="Run all tests", action="store_true")
    parser.add_argument("-uf", "--url_file", help="Specify a file containing urls formatted http(s)://addr:port.")
    parser.add_argument("-rt", "--reflection_test", help="Test if header values appear in HTTP response", action="store_true")
    parser.add_argument("-lt", "--length_test", help="Test how the length of a header value affects the HTTP response", action="store_true")
    parser.add_argument("-aut", "--authorization_test", help="Test how a header value handles different IP addresses affects the HTTP response", action="store_true")
    parser.add_argument("-et", "--error_tests", help="Test how the application handles special characters as header values.", action="store_true")
    parser.add_argument("-ct", "--command_injection_tests", help="Test how the application handles commands as header values.", action="store_true")
    parser.add_argument("-hh", "--host_header", help="Fuzz the host header.", action="store_true")
    parser.add_argument("-auh", "--authorization_header", help="Fuzz the authorization header.", action="store_true")
    parser.add_argument("-uah", "--user_agent_header", help="Fuzz the user agent header.", action="store_true")
    parser.add_argument("-conh", "--connection_header", help="Fuzz the user Connection header.", action="store_true")
    parser.add_argument("-f", "--forwarded_header", help="Fuzz the Forwarded header", action="store_true")
    parser.add_argument("-xffh", "--x_forwarded_for_header", help="Fuzz the X-Forwarded-For header", action="store_true")
    parser.add_argument("-fr", "--from_header", help="Fuzz the from header", action="store_true")
    parser.add_argument("-r", "--referer_header", help="Fuzz the Referer header", action="store_true")
    parser.add_argument("-pr", "--proxy", help="Specify a proxy to use (-p 127.0.0.1:8080)")
    parser.add_argument("-c", "--credentials", help="Specify credentials to submit. Must be quoted. Example: -c 'Authorization: Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ=='. Example: -c 'Cookie: SESS=Aid8eUje8&3jdolapf'")
    parser.add_argument("-t", "--threads", nargs="?", type=int, default=5, help="Specify number of threads (default=5)")
    parser.add_argument("-to", "--timeout", nargs="?", type=int, default=5, help="Specify number of seconds until a connection timeout (default=5)")
    parser.add_argument("-csv", "--csv", nargs='?', const='http_header_fuzzing_results.csv', help="Specify the name of a csv file to write to. If the file already exists it will be appended")
    args = parser.parse_args()

    if not args.url_file:
        parser.print_help()
        print("\n [-]  Please specify an input file containing URLs. Use -uf <urlfile> to specify the file\n")
        exit()

    if args.url_file:
        urlfile = args.url_file
        if not os.path.exists(urlfile):
            print("\n [-]  The file cannot be found or you do not have permission to open the file. Please check the path and try again\n")
            exit()
        urls = open(urlfile).read().splitlines()

    if not args.all_headers and not args.host_header and not args.user_agent_header\
        and not args.forwarded_header and not args.from_header and not args.referer_header \
        and not args.connection_header and not args.x_forwarded_for_header and not args.from_header \
        and not args.authorization_header:
        parser.print_help()
        print("\n [-]  Please specify header(s) and test(s). Use -ah to test all headers and at to run all tests.\n")
        exit()

    # Initialize the headers to be tested 
    headers_to_fuzz = []
    if args.all_headers or args.host_header:
        headers_to_fuzz.append('Host')
    if args.all_headers or args.user_agent_header:
        headers_to_fuzz.append('User-Agent')
    if args.all_headers or args.forwarded_header:
        headers_to_fuzz.append('Forwarded')
    if args.all_headers or args.x_forwarded_for_header:
        headers_to_fuzz.append('X-Forwarded-For')
    if args.all_headers or args.from_header:
        headers_to_fuzz.append('From')
    if args.all_headers or args.referer_header:
        headers_to_fuzz.append('Referer')
    if args.all_headers or args.connection_header:
        headers_to_fuzz.append('Connection')
    if args.all_headers or args.authorization_header:
        headers_to_fuzz.append('Authorization')

    # Initialize the tests to be run
    tests_to_run = []
    if args.all_tests or args. reflection_test:
        tests_to_run.append('reflection')
    if args.all_tests or args.length_test:
        tests_to_run.append('length')
    if args.all_tests or args.authorization_test:
        tests_to_run.append('authorization')
    if args.all_tests or args.error_tests:
        tests_to_run.append('error')
    if args.all_tests or args.command_injection_tests:
        tests_to_run.append('command injection')

    csv_name = args.csv

    print()
    print('[*] Loaded {} URLs'.format(len(urls)))
    print('[*] Testing {} headers'.format(len(headers_to_fuzz)))
    print('[*] Running {} types of tests'.format(len(tests_to_run)))
    sleep(4)

    # To disable HTTPS related warnings
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    print_lock = threading.Lock()
    url_queue = Queue()

    # Global variable where all data will be stored
    # The scanner_controller function appends data here
    data = []

    main()
