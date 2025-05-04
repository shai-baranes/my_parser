# from YouTube: https://www.youtube.com/watch?v=7Fh9K9TKFdo
# TBD try working here with Datafames after catching the idea

import argparse
import json
import re
from typing import List
import sys



quiet = False

def print_message(message: str):
	"""
	Print message to STDOUT if the quiet option is set to False (this is the default).
	:param message: message to print
	:return: None
	"""
	global quiet
	if not quiet:
		print(message) # this is the STDOUT print as in the default case



def get_matches(log_file: str, regex):  # Generic function
	"""
	Generator object to generically parse a given log file using a compiled regex pattern.
	:Param log_file: file to read logs from
	:Param regex: compiled regex pattern
	:return: a generator, which when iterated returns tuples of captures groups
	"""

	with open(log_file, 'r') as f:
		line = f.readline()
		while line:
			line = line.strip()
			matches = re.match(regex, line)
			if not matches:
				print_message(f'Warning, unable to parse log message: {line}')
				line = f.readline()
				continue
			groups = matches.groups()
			yield groups
			line = f.readline()




def parse_logs(log_file: str) -> List:
	"""
	Parse an apache access log file.
	:Param log_file: file to read logs from
	:return: list of dictionaries of fields parsed from logs
	"""
	logs = []
	regex = re.compile(r'^.*ABS:([\d.]+).*DEL:([\d.]+).*LEN:([\d.]+).*RSSI:(\[.*?\]).*$', re.IGNORECASE)
	for groups in get_matches(log_file, regex):
		# if groups[0] == 'TBD':
		# if groups[0] == '127.0.0.1'
			# continue

		try:
			log_dict = {'ABS': groups[0], 'DEL': groups[1], 'LEN': groups[2], 'RSSI': groups[3]}
		except IndexError as e:
			print(f"{type(e).__name__}: {e}")
			sys.exit()
		logs.append(log_dict)
	return logs


## from original file:
# def parse_apache_error_logs(log_file: str) -> List:
# 	"""
# 	Parse an apache error  log file.
# 	:param log_file: log file to read from
# 	:return: list of dictionaries of fields parsed from logs
# 	"""
# 	logs = []
# 	regex = re.recompile(r'TBD', re.TBD)
# 	# regex = re.recompile(r'^\[(.+)\] \[client (\d{1,3}(?:\.\d{1,3}){3})\] ([\w\s]+): (\S+)$', re.IGNORECASE)
# 	for groups in get_matches(log_file, regex):
# 		if groups[2] == 'TBD':
# 		# if groups[2] == '127.0.0.1':
# 			continue
# 		log_dict = {'datetime': groups[0], 'log_level': groups[1], 'client_ip': groups[2], 'message': groups[3]} TBD .. , 'request_path': groups[4]}
# 		logs.append(log_dict)
# 	return logs




## from original file:
# def parse_apache_logs(log_file: str) -> List:
# 	"""
# 	Parse an apache access log file.
# 	:Param log_file: file to read logs from
# 	:return: list of dictionaries of fields parsed from logs
# 	"""
# 	logs = []
# 	regex = re.compile(r'^TBD$', re.IGNORECASE)
# 	for groups in get_matches(log_file, regex):
# 		if groups[0] == 'TBD':
# 		# if groups[0] == '127.0.0.1'
# 			continue
# 		log_dict = {'client_ip': groups[0], 'datetime': groups[1], 'request_methid': groups[2],  ...}
# 		# log_dict = {TBD my dict}
# 		logs.append(log_dict)
# 	return logs





def main():
	global quiet

	parser = argparse.ArgumentParser(description='Generic log file parser application.')
	parser.add_argument('-i', '--input', required=True, help='Log file to read from')
	# parser.add_argument('-l', '--log-format', required=True, choices=['apache', 'apache_error'], help='Type of log to parse')
	parser.add_argument('-o', '--output', help='Type of log to parse')
	parser.add_argument('-q', '--quiet', help='Do not print informative message', action='store_true')
	args = parser.parse_args()
	input_file = args.input
	# log_format = args.log_format
	output = args.output
	quiet = args.quiet


	# parse_function = globals()['parse_{}_logs'.format(log_format)] # TBD replace with f" string" (although I'm not working now w/ 2 types of parsers)
	# parsed_logs = parse_function(input_file)
	parsed_logs = parse_logs(input_file)

	if output: # if output file is given via cmd line
		with open(output, 'w') as file: # of -> 'output file'
			for item in parsed_logs:
				file.write(str(item)+'\n')
	else:
		print(json.dumps(parsed_logs, indent=2))

	## as in original file to dump directly into a json file (TBD later implement using DF)
	# if output: # if output file is given via cmd line
	# 	with open(output, 'w') as of: # of -> 'output file'
	# 		json.dump(parsed_logs, of, indent=2)
	# else:
	# 	print(json.dumps(parsed_logs, indent=2))







if __name__ == "__main__":
	main()

