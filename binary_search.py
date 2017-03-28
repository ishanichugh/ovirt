#!/usr/bin/python
"""
This script defines a Searcher class which is used to perform 
binary search in a log file.
"""
from parser import Parser
class Searcher(object):
    """
    Provides functionality for searching through a a logfile taking input
    as start time and end time.
    """
    def __init__(self, filename):
        self.fptr = open(filename, 'rb')
        self.fptr.seek(0, 2)
        self.length = self.fptr.tell()

    def find(self, starttime, endtime):
        """
        Binary Search in file
        Input: Start time, End time(Format: Epoch milliseconds)
        Output: All logs in given time range
        """
        low = 0
        high = self.length
        pos = 0
        while low < high:
            mid = (low+high)/2
            pos = mid
            line = ''
            while pos >= 0:
                self.fptr.seek(pos)
                if self.fptr.read(1) == '\n':
                    line = self.fptr.readline()
                    timestamp = Parser(line.split('\n')[0]).get_timestamp()
                    if timestamp is not None:
                        # print line, timestamp
                        break
                pos -= 1
            if pos < 0:
                self.fptr.seek(0)
            epoch = Parser(line.split('\n')[0]).get_timestamp()
            if epoch < starttime-1:
                low = mid+1
            elif epoch > mid:
                high = mid
            # print starttime, epoch, low, high
        self.fptr.seek(pos+1)
        if epoch > starttime:
            while pos >= 0:
                self.fptr.seek(pos)
                if self.fptr.read(1) == '\n':
                    line = self.fptr.readline()
                    timestamp = Parser(line.split('\n')[0]).get_timestamp()
                    if timestamp is not None and timestamp < epoch:
                        break
                pos -= 1
        self.fptr.seek(pos+1)
        epoch = Parser(line.split('\n')[0]).get_timestamp()
        total_logs = []
        while epoch <= endtime and self.fptr.tell() < self.length:
            line = self.fptr.readline()
            if Parser(line.split('\n')[0]).get_timestamp() is not None:
                epoch = Parser(line.split('\n')[0]).get_timestamp()
            total_logs.append(line)
        return total_logs


# def main():
#   engineFile ="/home/ishani/ovirt/logs/vdsm-1.log"
#   searchtime =  Parser("2017-02-23 09:11:45,342+0100").get_timestamp()
#   endtime =  Parser("2017-02-23 10:13:59,071+0100").get_timestamp()
#   ob = Searcher(engineFile)
#   ob.find(searchtime,endtime)
#   #   pass
#       # print line

# if __name__ == '__main__':
#   main()
