import argparse
from sys import version
from colorama import init
from HttpHeaderFuzzer.header_fuzzer import *


def parse_arguments(parser):
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
    parser.add_argument("-ah", "--all_headers", help="Fuzz all headers", action="store_true")
    parser.add_argument("-at", "--all_tests", help="Run all tests", action="store_true")
    parser.add_argument("-uf", "--url_file", help="Specify a file containing urls formatted http(s)://addr:port.")
    parser.add_argument("-rt", "--reflection_test", help="Test if header values appear in HTTP response",
                        action="store_true")
    parser.add_argument("-lt", "--length_test", help="Test how the length of a header value affects the HTTP response",
                        action="store_true")
    parser.add_argument("-aut", "--authorization_test",
                        help="Test how a header value handles different IP addresses affects the HTTP response",
                        action="store_true")
    parser.add_argument("-et", "--error_tests",
                        help="Test how the application handles special characters as header values.",
                        action="store_true")
    parser.add_argument("-ct", "--command_injection_tests",
                        help="Test how the application handles commands as header values.", action="store_true")
    parser.add_argument("-hh", "--host_header", help="Fuzz the host header.", action="store_true")
    parser.add_argument("-auh", "--authorization_header", help="Fuzz the authorization header.", action="store_true")
    parser.add_argument("-uah", "--user_agent_header", help="Fuzz the user agent header.", action="store_true")
    parser.add_argument("-conh", "--connection_header", help="Fuzz the user Connection header.", action="store_true")
    parser.add_argument("-f", "--forwarded_header", help="Fuzz the Forwarded header", action="store_true")
    parser.add_argument("-xffh", "--x_forwarded_for_header", help="Fuzz the X-Forwarded-For header",
                        action="store_true")
    parser.add_argument("-fr", "--from_header", help="Fuzz the from header", action="store_true")
    parser.add_argument("-r", "--referer_header", help="Fuzz the Referer header", action="store_true")
    parser.add_argument("-pr", "--proxy", help="Specify a proxy to use (-p 127.0.0.1:8080)")
    parser.add_argument("-c", "--credentials",
                        help='Specify credentials to submit. Must be quoted. '
                             'Example: -c "Authorization: Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==". '
                             'Example: -c "Cookie: SESS=Aid8eUje8&3jdolapf"')
    parser.add_argument("-t", "--threads", nargs="?", type=int, default=5, help="Specify number of threads (default=5)")
    parser.add_argument("-to", "--timeout", nargs="?", type=int, default=10,
                        help="Specify number of seconds until a connection timeout (default=5)")
    parser.add_argument("-csv", "--csv", nargs='?', const='http_header_fuzzing_results.csv',
                        help="Specify the name of a csv file to write to. "
                             "If the file already exists it will be appended"),
    parser.add_argument("-u", "--urls", default=None, help="Specify the urls to fuzz. If the url file argument is also"
                                                            "being passed, then it will be ignored.")

    return parser.parse_args()


def header_args_valid(arguments):
    """ If the all headers flag is not specified, then check and see if any of the acceptable headers are passed """
    if not arguments.all_headers:
        valid_headers = ['host_header', 'user_agent_header', 'forwarded_header', 'from_header', 'referer_header'
                         'connection_header', 'x_forwarded_for_header', 'from_header', 'authorization_header']
        for header in valid_headers:
            if hasattr(arguments, header):
                return True
            if header == valid_headers[-1]:
                return False
    return True


def get_urls():
    """ If a problem occurs in regards to the url file, then allow the user to manually specify urls to attack.
     Otherwise, load the url file and return the content. This function also validates urls passed via the -u flag """
    def terminate_if_no_urls(urls_list):
        if len(urls_list) == 0:
            print(Fore.RED + '[-]  You did not pass any urls; can not continue. Terminating script.')
            exit()

    def get_urls_from_input():
        input_urls = input(Fore.LIGHTGREEN_EX + 'Enter the urls to test: ').replace(' ', '').split(',')
        terminate_if_no_urls(input_urls)
        return input_urls

    if args.urls:  # If a url file is passed AND the urls flag is passed, then the url file will be ignored.
        passed_urls = args.urls.replace(' ', '').split(',')
        terminate_if_no_urls(passed_urls)
        return passed_urls

    if not args.url_file:
        print(Fore.RED + '[-]  No urlfile was specified via -uf.')
        return get_urls_from_input()

    url_file = args.url_file
    if os.path.exists(url_file):
        return open(url_file).read().splitlines()
    else:
        print(Fore.RED + '[-]  The url file either cannot be found, '
                         'or you do not have permission to open the file.')
        return get_urls_from_input()


def main():
    """ Normalizes the URLs and starts multi-threading """
    fuzzer = HeaderFuzzer(args)
    if not version.startswith('3'):
        print(Fore.YELLOW + 'This script has only been tested with Python 3. '
              'If an error is encountered, please try with Python 3.')
        sleep(3)

    fuzzer.start(urls)


if __name__ == '__main__':
    init()
    print(Fore.LIGHTCYAN_EX + 'HTTP Header Fuzzer - https://github.com/laconicwolf/HTTP-Header-Fuzzer')
    arg_parser = argparse.ArgumentParser()
    args = parse_arguments(arg_parser)
    urls = get_urls()
    if not header_args_valid(args):
        print(Fore.RED + '[-]  No headers were specified. Please specify header(s) and test(s). '
              'Use -ah to test all headers and -at to run all tests. Script will now terminate.')
        exit()
    main()
