# xss_fuzzer.py
This tools used fuzzing technique


Requirement

go install github.com/tomnomnom/qsreplace@latest

go install github.com/rix4uni/xsschecker@latest

usage: xss_fuzzer.py [-h] -u URLS -p PAYLOADS [--threads THREADS] [-s] [-o OUTPUT]

XSS Fuzzer Tool

options:
  -h, --help            show this help message and exit
  
  -u URLS, --urls URLS  File containing vulnerable URLs
  
  -p PAYLOADS, --payloads PAYLOADS
  
                        File containing XSS payloads
  --threads THREADS     Maximum number of threads (default: 10)
  
  -s, --silent          Hide non-vulnerable results
  
  -o OUTPUT, --output OUTPUT
  
                        Output file to save vulnerable URLs
