import threading
from threading import Thread, Event
import re
import json
import time

quiet = False


# This event will be used for signaling (not utilized here)
parser_done_event = threading.Event()

class ParserThread(Thread):
    def __init__(self, input_file, output_file=None):
        super().__init__()
        self.stop_event = Event()
        self.input_file = input_file
        self.output_file = output_file

    def run(self):
        output_handle = open(self.output_file, 'a') if self.output_file else None
        try:
            for log in ParserThread.parse_logs(self.input_file):
            # for log in parse_logs(self.input_file):
                if self.stop_event.is_set():
                    break
                json_log = json.dumps(log)
                if output_handle:
                    output_handle.write(json_log + '\n')
                    print(str(json_log)[1:-1] + '\n') # my addition
                    output_handle.flush()
                else:
                    print(json_log)
        finally:
            if output_handle:
                output_handle.close()

    def stop(self):
        self.stop_event.set()



    @staticmethod
    def parse_logs(log_file: str) -> dict:
        """
        Parse an apache access log file.
        :Param log_file: file to read logs from
        :return: generator that yields a dictionary
        """
        regex = re.compile(r'^.*ABS:([\d.]+).*DEL:([\d.]+).*LEN:([\d.]+).*RSSI:(\[.*?\]).*$', re.IGNORECASE)
        for groups in ParserThread.get_matches(log_file, regex):
            try:
                yield {'ABS': groups[0], 'DEL': groups[1], 'LEN': groups[2], 'RSSI': groups[3]}
            except IndexError as e:
                print(f"{type(e).__name__}: {e}")
                sys.exit()


    @staticmethod
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
                        ParserThread.print_message(f'Warning, unable to parse: {line}')
                last_pos = f.tell()
            time.sleep(0.1)  # Adjust polling interval (TBD - to oupdate as needed)

    @staticmethod
    def print_message(message: str): # printing a warning message when encounter a line that is not parse applicalble
        """
        Print message to STDOUT if the quiet option is set to False (this is the default).
        :param message: message to print
        :return: None
        """
        global quiet
        if not quiet:
            print(message) # this is the STDOUT print as in the default case



def print_shai():
    print("shai")

my_parser = ParserThread('./log.txt', './koko.txt')



def main():

    x = threading.Thread(target=my_parser.run, args=())
    # x = threading.Thread(target=run_parser, args=('./log.txt', './koko.txt'))
    y = threading.Thread(target=print_shai, args=())
    x.start()
    y.start()
    # x.join()
    # y.join()


if __name__ == "__main__":
    main()





