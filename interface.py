#!/usr/bin/python
"""
This script defines an Interface class which is containts all
the functionalities of tools as an abstraction.
"""
from parser import Parser
from binary_search import Searcher
class Interface(object):
    """A user interface for Tool"""
    def __init__(self, filename):
        super(Interface, self).__init__()
        self.filename = filename

    def engine_log(self):
        """
        Parses Engine File into an EngineLog object list
        """
        log_array = []
        with open(self.filename, 'r') as fileptr:
            log = None
            for line in fileptr:
                elog = Parser(line).engine_parser()
                if elog is not None:
                    log_array.append(elog)
                    log = elog
                if elog is None and log is not None:
                    log.message = log.message + line
        return log_array

    def vdsm_log(self):
        """
        Parses VDSM File into an VDSMLof object list
        """
        log_array = []
        with open(self.filename, 'r') as fileptr:
            log = None
            for line in fileptr:
                vlog = Parser(line).vdsm_parser()
                if vlog is not None:
                    log_array.append(vlog)
                    log = vlog
                if vlog is None and log is not None:
                    log.message = log.message + line
        return log_array

    def search_vdsm(self, start_time, end_time):
        """
        Search VDSM file with respect to time.
        Returns VDSMLog object list in given time range
        """
        start_time = Parser(start_time).get_timestamp()
        end_time = Parser(end_time).get_timestamp()
        logs = Searcher(self.filename).find(start_time, end_time)
        log_array1 = []
        log = None
        for line in logs:
            vlog = Parser(line).vdsm_parser()
            if vlog is not None:
                log_array1.append(vlog)
                log = vlog
            if vlog is None and log is not None:
                log.message = log.message + line
        return log_array1

    def search_engine(self, start_time, end_time):
        """
        Search engine file with respect to time.
        Returns EngineLog object list in given time range
        """
        start_time = Parser(start_time).get_timestamp()
        end_time = Parser(end_time).get_timestamp()
        logs = Searcher(self.filename).find(start_time, end_time)
        log_array = []
        log = None
        for line in logs:
            elog = Parser(line).engine_parser()
            if elog is not None:
                log_array.append(elog)
                log = elog
            if elog is None and log is not None:
                log.message = log.message + line
        return log_array

    def search_by_message_level(self, start_time, end_time, message_level):
        """
        Search engine file with respect to time and message level
        Returns EngineLog object list in given time range and given message level.
        """
        log_array = []
        initial_array = self.search_engine(start_time, end_time)
        for log in initial_array:
            if log.message_level in message_level:
                log_array.append(log)
        return log_array

def main():
    """
    Tesing the functionality of Interface class
    """
    engine_file = "/home/ishani/ovirt/logs/engine.log"
    vdsm_file = "/home/ishani/ovirt/logs/vdsm-1.log"
    eob = Interface(engine_file)
    vob = Interface(vdsm_file)
    start_time = "2017-02-23 09:28:30,142Z"
    end_time = "2017-02-23 09:28:30,144Z"
    log_array = eob.engine_log()
    log_array = eob.search_engine(start_time, end_time)
    log_array = vob.vdsm_log()
    log_array = vob.search_vdsm(start_time, end_time)
    log_array = vob.search_by_message_level(start_time, end_time, ['DEBUG'])

    for log in log_array:
        print log.message
        # if log.message_level == 'DEBUG':
        #     print log.message
    print len(log_array)

if __name__ == '__main__':
    main()
