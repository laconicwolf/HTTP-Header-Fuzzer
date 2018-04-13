def get_response_length(response):
    return str(len(response.text))


def test_headers(url, test, resp, header, header_value):
    status_code = resp.status_code
    length = get_response_length(resp)
    response_list = resp.text.splitlines()
    reflection = [line for line in response_list if header_value in line]
    return status_code, length, reflection