
import time
import fcntl
import os
import argparse
import sys
import socket
import pdb

import select


from select import *
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
        self.file_mtime = 0

    def set_cmd_file(self, fname):
        self.cmd_file = fname
        os.remove(self.cmd_file)
        self.my_file = open(self.cmd_file,"w+")
        self.my_file.close()
        os.chmod(self.cmd_file, 0777)
        self.my_file = open(self.cmd_file,"w+")
        self.file_mtime = os.path.getmtime(self.cmd_file)

    def start_monitor( self ):

        while True:
            time.sleep(5)
            file_modified = os.path.getmtime(self.cmd_file) - self.file_mtime
            if( file_modified > 0 ):
                # File is modified
                cmd = self.get_changed_line()
                if( cmd == "QUIT") :
                    cmd_monitor.program_exit = 1
                    return
                else :
                    print "Executing ... ",cmd
                    ret_val = os.system(cmd)
                    # Save the new modified time value
                    self.file_mtime = os.path.getmtime(self.cmd_file)


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
    cmd_monitor.stop_monitor()

