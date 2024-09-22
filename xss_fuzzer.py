import subprocess
import argparse
import concurrent.futures
import urllib.parse

# Function to process a single URL with a payload
def test_xss(url, payload, hide_non_vuln, output_file):
    try:
        # Replace the query string with the payload
        encoded_payload = urllib.parse.quote(payload)
        new_url = subprocess.run(['qsreplace', payload], input=url.encode(), stdout=subprocess.PIPE).stdout.decode().strip()
        
        # Run xsschecker with the new URL
        result = subprocess.run(['xsschecker', '-match', payload, '-vuln'], input=new_url.encode(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Capture the output
        output = result.stdout.decode().strip()

        if 'Vulnerable' in output:
            print(f"Vulnerable: {output}")
            if output_file:
                with open(output_file, 'a') as f:
                    f.write(f"Vulnerable: {output}\n")
        elif not hide_non_vuln:
            print(f"Testing URL: {new_url} with payload: {payload}")
    
    except Exception as e:
        print(f"Error testing URL: {url} with payload: {payload}, Error: {str(e)}")

# Main function to handle URLs and payloads
def main(url_file, payload_file, max_threads, hide_non_vuln, output_file):
    urls = []
    payloads = []
    
    # Read URLs
    with open(url_file, 'r') as uf:
        urls = [line.strip() for line in uf if line.strip()]
    
    # Read Payloads
    with open(payload_file, 'r') as pf:
        payloads = [line.strip() for line in pf if line.strip()]
    
    # Using ThreadPoolExecutor for multithreading
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = []
        for url in urls:
            for payload in payloads:
                futures.append(executor.submit(test_xss, url, payload, hide_non_vuln, output_file))
        
        # Wait for all threads to complete
        concurrent.futures.wait(futures)

# Command-line argument parser
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="XSS Fuzzer Tool")
    parser.add_argument("-u", "--urls", required=True, help="File containing vulnerable URLs")
    parser.add_argument("-p", "--payloads", required=True, help="File containing XSS payloads")
    parser.add_argument("--threads", type=int, default=10, help="Maximum number of threads (default: 10)")
    parser.add_argument("-s", "--silent", action="store_true", help="Hide non-vulnerable results")
    parser.add_argument("-o", "--output", help="Output file to save vulnerable URLs")
    
    args = parser.parse_args()
    
    # Run the main function
    main(args.urls, args.payloads, args.threads, args.silent, args.output)
