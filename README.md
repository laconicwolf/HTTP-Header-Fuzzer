# HTTP Header Fuzzer
A multithreaded Python3 program that fuzzes HTTP headers and values and outputs the results to a CSV file. Checks HTTP responses for header reflection, HTTP response codes, attempts OS injection, uses long header values, uses special characters as header values. 
## Usage
```python3 http_header_fuzzer.py -uf <file containing urls> -at -ah -csv scan_results.csv```
### Example
```python3 http_header_fuzzer.py -v -uf urls.txt -at -ah -csv scan_results.csv```

The above command will visit each URL specified in urls.txt, and will run all tests (-at) against all headers (ah) defined in the script. The results of the script will be written to a CSV file, scan_results.csv. The verbose flag (-v) displays the results to the terminal as the requests occur. You can optionally include a threads (-t) argument (default is 5 threads) to make the scan go faster or slower. If the sites you are scanning are slow to respond, you can change the timeout options (default 5 seconds) using the -to flag (example: -to 10).
### Output
```
python3 http_header_fuzzer.py -v -uf urls.txt -at -ah -csv header_fuzzing.csv

[*] Loaded 3 URLs
[*] Testing 8 headers
[*] Running 5 types of tests

[*] Fuzzing Host header at https://laconicwolf.com/

[+] URL: http://laconicwolf.com/
    Test: reflection
    Header: Host
    Value: wbzopktwwa
    Status Code: 200
    Response Length: 111
    Header reflected in response?: False

[*] Fuzzing Host header at http://laconicwolf.net/

[+] URL: http://laconicwolf.net/
    Test: reflection
    Header: Host
    Value: owenirpeek
    Status Code: 404
    Response Length: 357
    Header reflected in response?: True
```
