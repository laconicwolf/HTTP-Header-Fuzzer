import string
import random


def get_header_values(test, header):
    ''' Accepts the name of an HTTP header and returns the contents of a 
    function containing a list of header values associated with the header
    name.
    '''
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


def get_random_useragent():
    ''' Returns a randomly chosen User-Agent string.
    '''
    win_edge = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
    win_firefox = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/43.0'
    win_chrome = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
    lin_firefox = 'Mozilla/5.0 (X11; Linux i686; rv:30.0) Gecko/20100101 Firefox/42.0'
    mac_chrome = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.38 Safari/537.36'
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
    ''' Returns a random string consisting of lowercase letters.
    '''
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def get_host_header_values(test):
    ''' Returns host headers values.
    '''
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
    return values


def get_useragent_header_values(test):
    ''' Returns header values.
    '''
    values = []
    if test == 'reflection':
        random_string = get_random_string(40)
        values.append(random_string)
    if test == 'length':
        for i in range(50, 500, 50):
            random_string = get_random_string(i)
            values.append(random_string)
    if test == 'authorization':
        mobile_user_agents = ['Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
                              'Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36',]
        values += [ua for ua in mobile_user_agents] 
    return values


def get_forwarded_header_values(test):
    ''' Returns header values.
    '''
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
    return values


def get_X_forwarded_for_header_values(test):
    ''' Returns header values.
    '''
    values = []
    if test == 'reflection':
        random_string = get_random_string(10)
        values.append(random_string)
    if test == 'length':
        for i in range(50, 500, 50):
            random_string = get_random_string(i)
            values.append(random_string)
    if test == 'authorization':
        addresses = ['127.0.0.1', 'localhost', '10.10.1.1']
        values += [addr for addr in addresses]
    return values


def get_from_header_values(test):
    ''' Returns header values.
    '''
    values = []
    if test == 'reflection':
        random_string = get_random_string(10)
        values.append(random_string)
    if test == 'length':
        for i in range(50, 500, 50):
            random_string = get_random_string(i)
            values.append(random_string)
    return values


def get_connection_header_values(test):
    ''' Returns header values.
    '''
    values = []
    if test == 'reflection':
        random_string = get_random_string(10)
        values.append(random_string)
    if test == 'length':
        for i in range(50, 500, 50):
            string_val = 'A' * i
            values.append(string_val)
    return values


def get_referer_header_values(test):
    ''' Returns header values.
    '''
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
    return values