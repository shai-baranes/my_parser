# from YouTube: https://www.youtube.com/watch?v=7Fh9K9TKFdo
# TBD try working here with Datafames after catching the idea

import argparse
import json
import re
from typing import List
import sys
import pandas as pd



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





def main():
	global quiet

	parser = argparse.ArgumentParser(description='Generic log file parser application.')
	parser.add_argument('-i', '--input', required=True, help='Log file to read from')
	parser.add_argument('-o', '--output', help='Output file (appends data)')
	parser.add_argument('-q', '--quiet', help='Do not print informative message', action='store_true')
	args = parser.parse_args()
	input_file = args.input
	output = args.output
	quiet = args.quiet


	parsed_logs = parse_logs(input_file)

	if output: # if output file is given via cmd line
		with open(output, 'w') as file: # of -> 'output file'
			json.dump(parsed_logs, file, indent=2)
			for i, item in enumerate(parsed_logs): # for each dict in list of dicts

				if i==0:

					df = pd.DataFrame([item])

				else:
					df = pd.concat([df, pd.DataFrame([item])], ignore_index=True)


			df['RSSI'] = df['RSSI'].apply(lambda a: a[1:-1].split(","))
			df['RSSI'] = df['RSSI'].apply(lambda arr: [int(a) for a in arr]) # both applies to covert '[0,0,0,80]' into ['0', '0', '0', '80'] into [0, 0, 0, 80]
			df.to_csv('koko.csv')

	else:
		print(json.dumps(parsed_logs, indent=2))



if __name__ == "__main__":
	main()



# example for cmd prompt line:
# > my_offline_parser_pandas.py -i log.txt -o koko.txt  # if was configured for txt file



# import pandas as pd
# data = {'ABS': '05958861.61421', 'DEL': '00000000.00179', 'LEN': '17', 'RSSI': '[0,0,0,80]'}
# df = pd.DataFrame(data)



