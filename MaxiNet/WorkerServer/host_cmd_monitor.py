import time
import fcntl
import os
import argparse
import sys

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

my_fname=""
cmd_monitor=None

class CmdMonitorParams (object):
    def __init__( self ):
        self.cmd_file = ""
        self.my_file = None   # File Handle
        self.program_exit = 0 # Flag to check if the monitor pgm needs to exit
        self.my_cmdline=[]  # The command line that is being executed

    def set_cmd_file(self, fname):
        self.cmd_file = fname

    def start_monitor( self ):

        if os.path.exists(self.cmd_file):
            os.remove(self.cmd_file)
        self.my_file = open(self.cmd_file, "w+")
        self.my_file.truncate(0)
        self.my_file.close()
        os.chmod(self.cmd_file,0777)
        self.my_file = open(self.cmd_file, "w+")
        self.my_file.truncate(0)

    def stop_monitor( self ):
        self.my_file.close()

    def get_changed_line( self ):
        while 1:
            where = self.my_file.tell()
            line = self.my_file.readline()
            if not line:
                time.sleep(1)
                self.my_file.seek(0,where)
            else:
                tmp_line = line.strip('\n')
                self.my_cmdline = tmp_line
                return tmp_line


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        my_event = event 
        evstr = my_event.__str__()
        for ch in ['<', '>']:
            if ch in evstr:
                evstr=evstr.replace(ch,"")
        evitems = evstr.split(':')
        if(evitems[0] == "FileModifiedEvent" ):
            # print "Event Source Path ..", my_event.src_path
            # Now we have to handle the event from here...
            # if the event is being dispatched for the file I am monitoring..

            if( my_event.src_path == my_fname ):
                # print "Event Belongs to me... I have to handle.."
                my_line = cmd_monitor.get_changed_line()
                if( my_line == "QUIT") :
                    cmd_monitor.program_exit = 1
                    return
                else :
                    ret_val = os.system(my_line)
            else:
                pass
                # print "Event Does not Belong to me... Hence Skipping .."

if __name__ == "__main__" :

    parser = argparse.ArgumentParser()
    parser.add_argument('--cmd_file', dest="cmd_fname", default="/tmp/h1_cmnds.txt", help = "File Name for the host to monitor new commands")

    args = parser.parse_args()

    if args.cmd_fname:
        my_fname = str(args.cmd_fname)

    print "Command Line  My Fname ...", my_fname

    cmd_monitor = CmdMonitorParams()
    cmd_monitor.set_cmd_file(my_fname)

    cmd_monitor.start_monitor()

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path="/tmp", recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(5)
            if (cmd_monitor.program_exit == 1):
                print "Going to Exit Program ..."
                sys.exit(0)
            else:
                pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
