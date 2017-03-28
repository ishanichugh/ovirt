#!/usr/bin/python
"""
This script is the base class for all types of logs.
It contains attributes common to all logs
"""
class Log(object):
    """
    Defines attributes of log object
    Time is given as epoch time in milliseconds
    """
    def __init__(self, time, thread_name, sender, message_level, message):

        self.time = time
        self.thread_name = thread_name
        self.sender = sender
        self.message_level = message_level
        self.message = message

    def display(self):
        """
        Displays contents of Log object
        """
        print "Time", self.time
        print "Thread Name", self.thread_name
        print "Sender", self.sender
        print "Message Level", self.message_level
        print "Message", self.message

    