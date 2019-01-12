""" This file contains formatting or output functions used by http_header_fuzzer.py """
import csv
import os


def parse_to_csv(data, csv_name=None):
    """ Takes a list of lists and outputs to a csv file """
    csv_name = 'results.csv' if not csv_name else csv_name
    if not os.path.isfile(csv_name):
        csv_file = open(csv_name, 'w', newline='')
        csv_writer = csv.writer(csv_file)
        top_row = ['URL', 'Test Type', 'Header', 'Value', 'Status code', 'Length', 'Response Time', 'Reflection', 'Reflection context', 'Notes']
        csv_writer.writerow(top_row)
        print('\n[+] The file {} does not exist. New file created!\n'.format(csv_name))
    else:
        try:
            csv_file = open(csv_name, 'a', newline='')
        except PermissionError:
            print("\n[-] Permission denied to open the file {}. Check if the file is open and try again.\n".format(csv_name))
            exit()
        csv_writer = csv.writer(csv_file)
        print('\n[+]  {} exists. Appending to file!\n'.format(csv_name))
    
    for line in data:
        csv_writer.writerow(line)
        
    csv_file.close()


def normalize_urls(urls):
    """ Accepts a list of urls and formats them so they will be accepted.
    Returns a new list of the processed urls """
    url_list = []
    http_port_list = ['80', '280', '81', '591', '593', '2080', '2480', '3080', 
                  '4080', '4567', '5080', '5104', '5800', '6080',
                  '7001', '7080', '7777', '8000', '8008', '8042', '8080',
                  '8081', '8082', '8088', '8180', '8222', '8280', '8281',
                  '8530', '8887', '9000', '9080', '9090', '16080']                    
    https_port_list = ['832', '981', '1311', '7002', '7021', '7023', '7025',
                   '7777', '8333', '8531', '8888']
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
