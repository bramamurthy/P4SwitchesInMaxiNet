#!/usr/bin/python2

import os
import sys
import json


def main():

    parse_experiment_config()

def parse_experiment_config():

    with open('/tmp/experiment.cfg', 'r') as f:
        for t1 in f:
            tmp = t1.strip('\n')
            data = tmp.split("=")
            print "Key :", data[0],
            print "Value :", data[1]

        
    # print "Topo file name ...", cfg_val["topo_file_name"] 
    # print "Switch Log Dir ...", cfg_val["swlog_dir"]
    # print "Switch Pcap Dir ...", cfg_val["pcap_dir"]
    # print "Switch Json file ...", cfg_val["p4_switch_json"]
    # print "Switch Executable ...", cfg_val["bmv2_exe"]
    # print "Invoke Mininet CLI ...", cfg_val['Invoke_mininet_cli']

    print "*** ######## "
    print "Topo file name ...", get_exp_topo_fname()
    print "Switch Log Dir ...", get_exp_swlog_dir()
    print "Switch Pcap Dir ...", get_exp_pcap_dir()
    print "Switch Json file ...", get_exp_switch_json()
    print "Switch Executable ...", get_exp_switch_exe()
    print "Invoke Mininet CLI ...", get_exp_mininet_cli()
    print "P4 Switch Initialization ...", get_exp_p4switch_init()

def get_exp_topo_fname():

    with open('/tmp/experiment.cfg', 'r') as f:
        for t1 in f:
            tmp = t1.strip('\n')
            data = tmp.split("=")
            key = data[0]
            value = data[1]
            if( key == "topo_file_name" ):
                return value

def get_exp_swlog_dir():

    with open('/tmp/experiment.cfg', 'r') as f:
        for t1 in f:
            tmp = t1.strip('\n')
            data = tmp.split("=")
            key = data[0]
            value = data[1]
            if( key == "swlog_dir" ):
                return value

def get_exp_pcap_dir():

    with open('/tmp/experiment.cfg', 'r') as f:
        for t1 in f:
            tmp = t1.strip('\n')
            data = tmp.split("=")
            key = data[0]
            value = data[1]
            if( key == "pcap_dir" ):
                return value

def get_exp_switch_json():

    with open('/tmp/experiment.cfg', 'r') as f:
        for t1 in f:
            tmp = t1.strip('\n')
            data = tmp.split("=")
            key = data[0]
            value = data[1]
            if( key == "p4_switch_json" ):
                return value

def get_exp_switch_exe():

    with open('/tmp/experiment.cfg', 'r') as f:
        for t1 in f:
            tmp = t1.strip('\n')
            data = tmp.split("=")
            key = data[0]
            value = data[1]
            if( key == "bmv2_exe" ):
                return value

def get_exp_mininet_cli():

    with open('/tmp/experiment.cfg', 'r') as f:
        for t1 in f:
            tmp = t1.strip('\n')
            data = tmp.split("=")
            key = data[0]
            value = data[1]
            if( key == "Invoke_mininet_cli" ):
                return value

def get_exp_p4switch_init():

    with open('/tmp/experiment.cfg', 'r') as f:
        for t1 in f:
            tmp = t1.strip('\n')
            data = tmp.split("=")
            key = data[0]
            value = data[1]
            if( key == "p4_switch_initialization" ):
                return value


if __name__ == '__main__':
    main()
