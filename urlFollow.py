#!/usr/bin/env python3

import sys
import argparse
import requests
import concurrent.futures
from urllib.parse import urlparse, urlsplit
from threading import Lock, Semaphore

requests.packages.urllib3.disable_warnings()
lock = Lock()
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.171 Safari/537.36"}
semaphore = None


def parse_args():
	parser = argparse.ArgumentParser(description="endUrl.py find final url after redirection for a list of urls read from stdin")
	parser.add_argument("-i", "--input", action="store", dest="infile", help="input file [if none, stdin]", type=str, default=None)
	parser.add_argument("-o", "--outfile", action="store", dest="outfile", type=str, help="Output file to write urls [if none, only stdout]", default=None)
	parser.add_argument("-t", "--threads", action="store", dest="threads", type=int, default=4, help="Number of parallel threads [default 4]")
	parser.add_argument("-r", "--redirectsfile", action="store", dest="redirectsfile", type=str, help="File location to write redirections, \"|\" separated", default=None)

	return parser.parse_args(sys.argv[1:])


def check_url(base_url):
	resp = requests.get(base_url, headers=headers, verify=False)
	urlParts = urlsplit(resp.url)
	realurl = f"{urlParts.scheme}://{urlParts.netloc}/"

	return (base_url, realurl)


def handle_finding(future):
	global semaphore, lock, realurls, transitions

	semaphore.release()

	if future.done():
		if not future.exception():
			result = future.result()

			with lock:
				if result:
					sys.stdout.write(f"{result[1]}\n")
					if args.outfile:
						realurls.append(result[1])
					if args.redirectsfile:
						transitions.append(f"{result[0]}|{result[1]}")


args = parse_args()
semaphore = Semaphore(args.threads)
realurls = []
transitions = []
urlsToTest = []

if args.infile:
	with open(args.infile, "r") as inf:
		urlsToTest = [line.strip() for line in inf]

else:
	urlsToTest = [line.strip("\n") for line in sys.stdin]

with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as tpe:
	for line in urlsToTest:

		url = line.strip()

		semaphore.acquire()
		try:
			future = tpe.submit(check_url, url)
			future.add_done_callback(handle_finding)
		except:
			semaphore.release()

	tpe.shutdown(wait=True)

if args.outfile:
	realurls = list(set(realurls))
	with open(args.outfile, "w") as outf:
		for line in realurls:
			outf.write(f"{line}\n")

if args.redirectsfile:
	transitions = list(set(transitions))
	with open(args.redirectsfile, "w") as transf:
		for trans in transitions:
			transf.write(f"{trans}\n")