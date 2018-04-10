def check_for_reflection(url, response, test_header, input_string):
    ''' Checks the contents of a response object for a specified input string
    and returns a message including attributes of the response and the response
    line where the reflection occurred.
    '''
    response_list = response.text.splitlines()
    reflection = [line for line in response_list if input_string in line]
    msg = ''  
    if reflection:
        msg += "\n[+] Reflected content for URL: {}".format(url)
        msg += "\n    {}: {}".format(test_header, input_string)
        msg += "\n    Response code: {}".format(response.status_code)
        if len(reflection) > 1:
            for item in reflection:
                msg += "\n    Response: {}".format(item.strip())
        else:
            msg += "\n    Response: {}".format(reflection[0].strip())
    return msg, reflection


def test_long_header_value(url, response, test_header, input_string):
    msg = '\n[*] URL: {}'.format(url)
    msg += '\n   {} header of {} characters'.format(test_header, len(input_string))
    msg += '\n   Status Code: {}'.format(response.status_code)
    try:
        msg += '\n   Content-Length: {}'.format(response.headers['Content-Length'])
    except KeyError:
        pass
    data = msg
    return msg, data
