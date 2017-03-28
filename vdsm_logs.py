#!/usr/bin/python
"""
This script is an object oriented representation of logs from VDSM
It inherits Log class and extends data items.
"""
from logs import Log
class VDSMLog(Log):
    """docstring for VDSMLog"""
    def __init__(self, time, thread_name, sender, message_level, message, module, line_no):
        super(VDSMLog, self).__init__(time, thread_name, sender, message_level, message)
        self.module = module
        self.line_no = line_no

    def display(self):
        """
        Display the contents of VDSMLog object
        """
        print "Time", self.time
        print "Threadname", self.thread_name
        print "Sender", self.sender
        print "message level", self.message_level
        print "mesage", self.message
        print "caller module", self.module
        print "line no", self.line_no

# ob = VDSMLog(1,'threadname','INFO',"this is message",'vdsm',123)
# ob.display()
