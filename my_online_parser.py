import time
import argparse
import json
import re
from typing import List
import sys



quiet = False

def print_message(message: str): # printing a warning message when encounter a line that is not parse applicalble
	"""
	Print message to STDOUT if the quiet option is set to False (this is the default).
	:param message: message to print
	:return: None
	"""
	global quiet
	if not quiet:
		print(message) # this is the STDOUT print as in the default case


def get_matches(log_file: str, regex): # perplexity refactoring for online file changes
    last_pos = 0
    while True:
        with open(log_file, 'r') as f:
            f.seek(last_pos)
            while True:
                line = f.readline()
                if not line:
                    break
                line = line.strip()
                matches = re.match(regex, line)
                if matches:
                    yield matches.groups()
                else:
                    print_message(f'Warning, unable to parse: {line}')
            last_pos = f.tell()
        time.sleep(0.1)  # Adjust polling interval (TBD - to oupdate as needed)


# def get_matches(log_file: str, regex):  # Generic function
# 	"""
# 	Generator object to generically parse a given log file using a compiled regex pattern.
# 	:Param log_file: file to read logs from
# 	:Param regex: compiled regex pattern
# 	:return: a generator, which when iterated returns tuples of captures groups
# 	"""

# 	with open(log_file, 'r') as f:
# 		line = f.readline()
# 		while line:
# 			line = line.strip()
# 			matches = re.match(regex, line)
# 			if not matches:
# 				print_message(f'Warning, unable to parse log message: {line}')
# 				line = f.readline()
# 				continue
# 			groups = matches.groups()
# 			yield groups
# 			line = f.readline()




def parse_logs(log_file: str) -> dict:
	"""
	Parse an apache access log file.
	:Param log_file: file to read logs from
	:return: generator that yields a dictionary
	"""
	regex = re.compile(r'^.*ABS:([\d.]+).*DEL:([\d.]+).*LEN:([\d.]+).*RSSI:(\[.*?\]).*$', re.IGNORECASE)
	for groups in get_matches(log_file, regex):
		try:
			yield {'ABS': groups[0], 'DEL': groups[1], 'LEN': groups[2], 'RSSI': groups[3]}
		except IndexError as e:
			print(f"{type(e).__name__}: {e}")
			sys.exit()


# def parse_logs(log_file: str) -> List:
# 	logs = []
# 	regex = re.compile(r'^.*ABS:([\d.]+).*DEL:([\d.]+).*LEN:([\d.]+).*RSSI:(\[.*?\]).*$', re.IGNORECASE)
# 	for groups in get_matches(log_file, regex):
# 		try:
# 			log_dict = {'ABS': groups[0], 'DEL': groups[1], 'LEN': groups[2], 'RSSI': groups[3]}
# 		except IndexError as e:
# 			print(f"{type(e).__name__}: {e}")
# 			sys.exit()
# 		logs.append(log_dict)
# 	return logs


def main():
    global quiet
    parser = argparse.ArgumentParser(description='Real-time log parser')
    parser.add_argument('-i', '--input', required=True, help='Log file to read from')
    parser.add_argument('-o', '--output', help='Output file (appends data)')
    parser.add_argument('-q', '--quiet', help='Do not print informative message', action='store_true')
    args = parser.parse_args()
    
    quiet = args.quiet
    output_handle = open(args.output, 'a') if args.output else None

    try:
        for log in parse_logs(args.input):
            json_log = json.dumps(log)
            if output_handle:
                output_handle.write(json_log + '\n')
                print(str(json_log)[1:-1] + '\n') # my addition
                output_handle.flush()
            else:
                print(json_log)
    except KeyboardInterrupt:
        if output_handle:
            output_handle.close()





if __name__ == "__main__":
	main()


# example for cmd prompt line:
# > my_online_parser.py -i log.txt -o koko.txt  # if was configured for txt file