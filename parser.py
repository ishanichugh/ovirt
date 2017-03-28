#!/usr/bin/python
"""
This script is a parser for the logs in a logfile.
It takes one line of log as argument and converts it into a log object.
"""
import re
import time
import calendar
from vdsm_logs import VDSMLog
from engine_logs import EngineLog
class Parser(object):
    """
    Takes input on line of log and parses it.
    Creates log objects.
    """
    def __init__(self, line):
        self.line = line

    def get_timestamp(self):
        """
        Input: Line of Log
        Output: None(If no timestamp is present)
                Timestamp in epoch time(milliseconds)
        """
        # print self.line
        pattern = re.compile(r'^[ 0-9:+\.\-TZ,.]{19,28}')
        timestamp = pattern.search(self.line)
        if timestamp is None:
            return None
        timestamp = timestamp.group()
        if 'Z' in timestamp:
            milliseconds = int(timestamp.split(',')[1][0:3])
            timestamp = calendar.timegm(time.strptime(timestamp.partition(',')[0], "%Y-%m-%d %H:%M:%S"))
            epoch_time = timestamp*1000 + milliseconds
            return epoch_time

        separator = '+' if '+' in timestamp else '-'
        milliseconds = int(timestamp.split(',')[1].split(separator)[0])
        offset_type = 1 if separator == '-' else -1
        offset = (int(timestamp.split(',')[1].split(separator)[1])/100)*3600 + (int(timestamp.split(',')[1].split(separator)[1])%100)*60
        timestamp = calendar.timegm(
            time.strptime(timestamp.partition(',')[0], "%Y-%m-%d %H:%M:%S")) + offset_type*offset
        epoch_time = timestamp*1000 + milliseconds
        return epoch_time

    def get_message_level(self):
        """
        Returns the Message Level in a line of log.
        """
        message_level = ["TRACE", "DEBUG", "INFO", "WARNING", "ERROR"]
        message_level = self.line.split(' ')[2]
        return message_level

    def get_thread_name(self):
        """
        Extracts Thread Name from a line of log
        """
        stack = []
        pattern = re.compile(r"\((.*?)\)")
        start_pos = re.search(pattern, self.line).start()
        for index in range(start_pos, len(self.line)):
            if self.line[index] == '(':
                stack.append(index)
            elif self.line[index] == ')':
                if len(stack) == 1:
                    return self.line[stack[0]+1:index]
                stack.pop()

    def get_message(self):
        """
        Returns line of log.
        """
        return self.line

    def get_sender(self):
        """
        Retrieves sender from line of log.
        """
        stack = []
        pattern = re.compile(r"\[(.*?)\]")
        start_pos = re.search(pattern, self.line).start()
        for index in range(start_pos, len(self.line)):
            if self.line[index] == '[':
                stack.append(index)
            elif self.line[index] == ']':
                if len(stack) == 1:
                    return self.line[stack[0]+1:index]
                stack.pop()

    def get_vdsm_module(self):
        """
        Takes line of VDSM log and retrieves module name and line number
        """
        pattern = re.compile(r"\((.*?)\)")
        string = re.findall(pattern, self.line)[-1]
        try:
            return string.split(':')[0], string.split(':')[1]
        except:
            return None, None

    def engine_parser(self):
        """
        Total Parser for log from engine
        Returns EngineLog object
        """
        timestamp = self.get_timestamp()
        # print "VDSM", timestamp
        if timestamp is None:
            return None
        epoch_time = timestamp
        thread_name = self.get_thread_name()
        sender = self.get_sender()
        message_level = self.get_message_level()
        message = self.get_message()
        return EngineLog(epoch_time, thread_name, sender, message_level, message)

    def vdsm_parser(self):
        """
        Total parser for log from VDSM
        Returns VDSMLog object
        """
        engine_log = self.engine_parser()
        if engine_log is None:
            return None
        # print engine_log.time, engine_log.sender, engine_log.thread_name, engine_log.message_level, engine_log.message
        module, line_no = self.get_vdsm_module()
        return VDSMLog(engine_log.time, engine_log.thread_name, engine_log.sender, engine_log.message_level, engine_log.message, module, line_no)

# engineFile ="/home/ishani/ovirt/logs/engine.log"
# a = []
# counter = 0
# line_n=0
# with open(engineFile,'r') as f:
#     for log in f:
#   #print log
#         line_n+=1
#         # print line_n,
#         ob = Parser(log)
#         x = ob.engine_parser()
#         if x is not None:
#             counter+=1
# print "Size",counter
# ob = Parser(line)
# print ob.vdsmParser()
# ob2 = Parser(line2)
# print ob2.engineparser()
# log_array = []
# vdsm_file = "/home/ishani/ovirt/logs/engine.log"
# with open(vdsm_file, 'r') as f:
#     log = None
#     for line in f:
#         x = Parser(line).engine_parser()
#         if x is not None:
#             log_array.append(x)
#             log = x
#         if x is None and log is not None:
#             log.message = log.message + line

# print "log array size",len(log_array)
# # print log_array[345]

# for log in log_array:
#     if "Caused" in log.message:
#         print log.message
#         break
