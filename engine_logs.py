#!/usr/bin/python
"""
This script is an object oriented representation of logs from Engine
It inherits Log class and extends data items.
"""
from logs import Log
class EngineLog(Log):
    """docstring for EngineLog"""
    def __init__(self, time, thread_name, sender, message_level, message):
        super(EngineLog, self).__init__(time, thread_name, sender, message_level, message)

    def display(self):
        print "Time", self.time
        print "Threadname", self.thread_name
        print "message level", self.message_level

    def pbmethod(self):
        """
        docstring
        """
        pass


# ob = EngineLog(1,'threadname','INFO',"this is engine message")
# ob.display()
