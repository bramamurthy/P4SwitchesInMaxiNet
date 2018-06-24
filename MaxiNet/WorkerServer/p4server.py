#!/usr/bin/python2

import argparse
import atexit
import logging
import os
import signal
import subprocess
import sys
import tempfile
import time
from time import sleep
import json 

from mininet.node import UserSwitch, OVSSwitch
from mininet.link import Link, TCIntf
from mininet.net import Mininet
import mininet.term
import Pyro4
import threading
import traceback

from MaxiNet.tools import Tools, MaxiNetConfig
from MaxiNet.WorkerServer.ssh_manager import SSH_Manager
from p4run_exercise import ExerciseRunner

import pdb
from mygraph import MyTopoGraph   # Added by RB
# Added by RB
from parse_exp_cfg import *


class WorkerServer(object):
    """Manages the Worker

    The WorkerServer class connects to the nameserver and registers
    itself with the MaxiNetManager instance. It is used by the Cluster instances
    to start mininet instances, manage the ssh daemon and run commands etc.

    Attributes:
        logger: logging instance
        mnManager: instance of class MininetManager which is used to create mininet
            instances
        sshManager: instance of class SSH_Manager which is used to manage the ssh
            daemon.
        ssh_folder: folder which holds configuration files for the ssh daemon.
        ip: ip address of Worker
    """
    def __init__(self):
        self._ns = None
        self._pyrodaemon = None
        self.logger = logging.getLogger(__name__)
        self._manager = None
        self.mnManager = MininetManager()
        self.sshManager = None
        self.ssh_folder = tempfile.mkdtemp()
        atexit.register(subprocess.call, ["rm", "-rf", self.ssh_folder])
        logging.basicConfig(level=logging.DEBUG)
        self.ip = None
        self._shutdown = False
        #Pyro4.config.COMMTIMEOUT = 2

        #for frontend
        self._ip = None
        self._port = None
        self._password = None

        self._looping_thread = None


    def exit_handler(self, signal, frame):
        # I have absolutely no clue why but without this print atexit sometimes
        # doesn't seem to wait for called functions to finish...
        print "exiting..."
        self._shutdown = True
        sys.exit()

    @Pyro4.expose
    def monitorFrontend(self):
        """ function to monitor if the frontend is still alive.
            if not, try to reconnect.
        """
        while(not self._shutdown):
            try:
                self._manager.getStatus()
            except:
                if self._ip != None:
                    #self.ip as an indicator that this worker was connected to the frontend once.
                    print "Trying to reconnect to FrontendServer..."
                    try:
                        try:
                            self._pyrodaemon.unregister(self)
                        except:
                            pass
                        try:
                            self._pyrodaemon.unregister(self.mnManager)
                        except:
                            pass
                        try:
                            self._pyrodaemon.unregister(self.sshManager)
                        except:
                            pass
                        try:
                            self._pyrodaemon.shutdown()
                        except:
                            pass
                        try:
                            self._pyrodaemon.close()
                        except:
                            pass
                        self.start(self._ip, self._port, self._password)
                    except Exception as e:
                        traceback.print_exc(e)
                        pass
                pass
            time.sleep(5)

    @Pyro4.expose
    def start(self, ip, port, password, retry=float("inf")):
        """Start WorkerServer and ssh daemon and connect to nameserver."""
        self.logger.info("starting up and connecting to  %s:%d"
                         % (ip, port))

        #store for reconnection attempts
        self._ip = ip
        self._port = port
        self._password = password

        #Pyro4.config.HMAC_KEY = password
        tries=1
        self._ns = None
        while not self._ns:
            try:
                self._ns = Pyro4.locateNS(ip, port, hmac_key=password)
            except Pyro4.errors.NamingError:
                if tries < retry:
                    self.logger.warn("Unable to locate Nameserver. Trying again in 5 seconds...")
                    time.sleep(5)
                    tries += 1
                else:
                    self.logger.error("Unable to locate Nameserver.")
                    sys.exit()
        self.config = Pyro4.Proxy(self._ns.lookup("config"))
        self.config._pyroHmacKey=password
        self.ip = self.config.get_worker_ip(self.get_hostname())
        if(not self.ip):
            self.ip = Tools.guess_ip()
            if not self.config.has_section(self.get_hostname()):
                self.config.add_section(self.get_hostname())
            self.config.set(self.get_hostname(), "ip", self.ip)
            self.logger.warn("""FrontendServer did not know IP of this host (check configuration for hostname).
                             Guessed: %s""" % self.ip)
        self.logger.info("configuring and starting ssh daemon...")
        self.sshManager = SSH_Manager(folder=self.ssh_folder, ip=self.ip, port=self.config.get_sshd_port(), user=self.config.get("all", "sshuser"))
        self.sshManager.start_sshd()
        self._pyrodaemon = Pyro4.Daemon(host=self.ip)
        self._pyrodaemon._pyroHmacKey=password
        uri = self._pyrodaemon.register(self)
        self._ns.register(self._get_pyroname(), uri)
        uri = self._pyrodaemon.register(self.mnManager)
        self._ns.register(self._get_pyroname()+".mnManager", uri)
        uri = self._pyrodaemon.register(self.sshManager)
        self._ns.register(self._get_pyroname()+".sshManager", uri)
        atexit.register(self._stop)
        self.logger.info("looking for manager application...")
        manager_uri = self._ns.lookup("MaxiNetManager")
        if(manager_uri):
            self._manager = Pyro4.Proxy(manager_uri)
            self._manager._pyroHmacKey=self._password
            self.logger.info("signing in...")
            if(self._manager.worker_signin(self._get_pyroname(), self.get_hostname())):
                self.logger.info("done. Entering requestloop.")
                self._started = True
                self._looping_thread = threading.Thread(target=self._pyrodaemon.requestLoop)
                self._looping_thread.daemon = True
                self._looping_thread.start()
            else:
                self.logger.error("signin failed.")
        else:
            self.logger.error("no manager found.")

    def _get_pyroname(self):
        return "MaxiNetWorker_%s" % self.get_hostname()

    @Pyro4.expose
    def get_hostname(self):
        return subprocess.check_output(["hostname"]).strip()

    def _stop(self):
        self.logger.info("signing out...")
        if(self._manager):
            self._manager.worker_signout(self.get_hostname())
        self.logger.info("shutting down...")
        self._ns.remove(self._get_pyroname())
        self._ns.remove(self._get_pyroname()+".mnManager")
        self._pyrodaemon.unregister(self)
        self._pyrodaemon.unregister(self.mnManager)
        self._pyrodaemon.unregister(self.sshManager)
        self._pyrodaemon.shutdown()
        self._pyrodaemon.close()

    @Pyro4.expose
    def remoteShutdown(self):
        self._pyrodaemon.shutdown()


    @Pyro4.expose
    def stop(self):
        (signedin, assigned) = self._manager.get_worker_status(self.get_hostname())
        if(assigned):
            self.logger.warn("can't shut down as worker is still assigned to id %d" % assigned)
            return False
        else:
            self._stop()
            return True

    @Pyro4.expose
    def check_output(self, cmd):
        """Run cmd on Worker and return output

        Args:
            cmd: command to call with optional parameters

        Returns:
            Shell output of command
        """
        self.logger.debug("Executing %s" % cmd)
        return subprocess.check_output(cmd, shell=True,
                                       stderr=subprocess.STDOUT).strip()

    @Pyro4.expose
    def script_check_output(self, cmd):
        """Call MaxiNet Script and return output

        Args:
            cmd: name of script to call
        Returns:
            Shell output of script
        """
        # Prefix command by our worker directory
        cmd = Tools.get_script_dir() + cmd
        return self.check_output(cmd)

    @Pyro4.expose
    def run_cmd(self, command):
        """Call command (blocking)

        Args:
            command: command to call with optional parameters
        """
        subprocess.call(command, shell=True)

    @Pyro4.expose
    def daemonize(self, cmd):
        """Call command (non-blocking)

        Args:
            command: command to call with optional parameters
        """
        p = subprocess.Popen(cmd, shell=True)
        atexit.register(p.terminate)

    @Pyro4.expose
    def daemonize_script(self, script, args):
        """Call MaxiNet Script (non-blocking)

        Args:
            cmd: name of script to call
        """
        cmd = Tools.get_script_dir()+script+" "+args
        p = subprocess.Popen(cmd, shell=True)
        atexit.register(p.terminate)


class TCLinkParams(Link):
    """Link with symmetric TC interfaces

    Like the mininet TCLink class but with support of the params1
    and params2 arguments.
    """

    def __init__(self, node1, node2, port1=None, port2=None,
                 intfName1=None, intfName2=None,
                 addr1=None, addr2=None, params1=None,
                 params2=None, **kvargs):
        Link.__init__(self, node1, node2, port1=port1, port2=port2,
                      intfName1=intfName1, intfName2=intfName2,
                      cls1=TCIntf,
                      cls2=TCIntf,
                      addr1=addr1, addr2=addr2,
                      params1=params1,
                      params2=params2)


class MininetManager(object):

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.net = None
        self.exercise = None  # Added by RB

    @Pyro4.expose
    def create_mininet(self, topo, tunnels=[],  switch=UserSwitch,
                       controller=None, STT=False):
        if(not self.net is None):
            self.logger.warn("running mininet instance detected!\
                              Shutting it down...")
            self.destroy_mininet()

        self.logger.info("Creating mininet instance")
        # try:
            # if controller:
                # self.net = Mininet(topo=topo, intf=TCIntf, link=TCLinkParams,
                                   # switch=switch, controller=controller)
            # else:
                # self.net = Mininet(topo=topo, intf=TCIntf, link=TCLinkParams,
                                   # switch=switch)
        # except Exception, e:
            # self.logger.error("Failed to create mininet instance: %s" % traceback.format_exc())
            # raise e

        json_savetopo( topo )
        self.logger.info("Instantiating Exercise..")

        mytopo_dir = get_exp_topo_fname()
        swlog_dir = get_exp_swlog_dir()
        pcap_dir = get_exp_pcap_dir()
        switch_json = get_exp_switch_json()
        sw_exe = get_exp_switch_exe()


        exercise = ExerciseRunner( mytopo_dir, swlog_dir, pcap_dir, switch_json, sw_exe ,True)

        # exercise = ExerciseRunner( mytopo_dir, swlog_dir, pcap_dir, switch_json, '/home/rbabu/behavioral-model/targets/simple_router/simple_router',True)

        self.logger.info("Successfully Instantiated Exercise..")

        self.exercise = exercise # save this for use in switch programming 
        exercise.build_exercise_topo()

        # This would create the cmnds.txt file to program the switches
        # for the full topology. It should be okay for single worker
        # as well as multiple workers.

        graph = MyTopoGraph()
        graph.init_graph_from_topofile(exercise.topo_file) 

        # Here get the switch port map from graph formed with the input topo.
        # The switches are going to be programmed based on the graph.
        # Now build the topology in mininet as per the switch port map being
        # returned by graph. In case of tunnel also, we have to make sure
        # appropriate Tun interface is added as the proper switch port

        exercise_links = exercise.get_links_in_exercise()
        # print "Exercise links Before processing..."
        # print exercise_links

        # Here Add all Host links as per graph using sw port map
        tmp_host_links = exercise.topo.get_topo_hostlinks()
        # print "******** Topo Host Links ******", tmp_host_links

        print "Exercise Links 1st  Pass..."
        print "1st Pass Adding All hosts to the switch ..."
        for host_link_entry in tmp_host_links:
            tmp_host = host_link_entry['node1']
            sw_1 = host_link_entry['node2']
            for tmp in graph.myhost_list:
                myhost = tmp[0]
                if( myhost == tmp_host ):
                    myipaddr = tmp[1]
                    mymacaddr = tmp[2]
                    break

            # print "Adding link to Switch...",tmp_host, sw_1, host_link_entry, mymacaddr
            tmp_topo = exercise.topo
            tmp_topo.addMyHostLinkToSwitch(tmp_host, sw_1, host_link_entry,mymacaddr)

        tmp_swlist = graph.myswitch_list
        tmp_swlist.sort()

        print "2nd Pass Adding Switch links as per Switch port map ..."
        print tmp_swlist
        for sw_name in tmp_swlist:
            sw_pmap = graph.get_switch_port_map(sw_name)
            print "Sw Map for switch ..", sw_name
            print sw_pmap
            for p_entry in sw_pmap:
                portno = p_entry[0]
                nodename = p_entry[1]
                # print "Switch Name ...", sw_name
                # print "Node Name ...", nodename
                if( nodename[0] == 'h'):
                    # This is a host. So to be skipped
                    continue

                if( nodename < sw_name ):
                    # We need not add, since it would been already
                    # added by processing earlier. Switches are in sorted list
                    # A link s4<->s1, would have been added while handling s1.
                    # we can skip adding this like while we are looking at s4
                    continue
                # We have to process this entry for adding

                sw_1 = sw_name
                sw_2 = nodename
                # print "Scanning for entry ...", sw_1, sw_2
                for link_entry in exercise_links:
                    if( (( link_entry['node1'] == sw_1) and (link_entry['node2'] == sw_2))  or (( link_entry['node1'] == sw_2) and (link_entry['node2'] == sw_1)) ) :
                        break
                # print "Adding link to Switch...", sw_1, link_entry
                tmp_topo = exercise.topo
                tmp_topo.addMyLinkToSwitch(sw_1, link_entry)

        exercise.run_exercise()
        self.net = exercise.net # Initialize Mininet object for port map and tunnel to work

        # Here get the switch port map from graph formed with the input topo.
        # The switches are going to be programmed based on the graph.
        # Now build the topology in mininet as per the switch port map being
        # returned by graph. In case of tunnel also, we have to make sure
        # appropriate Tun interface is added as the proper switch port


        # Temporarily have a list of all switches of this topology in a list
        # for use in comparison in the code below.

        tmp_switch_list =[];
        for swname in topo.switches():
            tmp_switch_list.append(swname)

        tunnel_len = len(tunnels)
        if (tunnel_len > 0):
           self.logger.info("Build Mininet Topology as per parition and Tunnels ...")

           for swname in topo.switches():
               dbg_str = "*** 1st Pass Looping for Switch ...", swname 
               self.logger.info( dbg_str )
               sw_map = graph.get_switch_port_map(swname)
               print sw_map
               # for port, node in sw_map:
                   # Add Everything
                   # exercise.topo.addToSwitchAtPort(swname, port,node)

           for swname in topo.switches():
               dbg_str =  "*** 2nd Pass Looping for Switch ...", swname 
               self.logger.info( dbg_str )

               # Search in the list of switch nodes that we have for this 
               # partition. If we happen to come across a switch that is not
               # in this partition, then we need to have a tunnel for that
               # switch. Now for that switch, see which is the appropriate
               # tunnel interface and port number.

               sw_map = graph.get_switch_port_map(swname)
               print sw_map
               for port, node in sw_map:
                   if (node[0] == 's'):
                   # This is a switch. Can be added as switch port
                       found = 0
                       for tmp_sw in tmp_switch_list :
                           if (node == tmp_sw ):
                               # This happens to be a switch in our partition

                               found = 1
                               exercise.topo.addToSwitchAtPort(swname, port,node)
                               pass
                       if (found  == 0): 
                           dbg_str =  "Create Tunnel between ..", swname, node 
                           self.logger.info( dbg_str )

                           for tunnel in tunnels:
                               tun_intf_name = tunnel[0]
                               tun_switch_name = tunnel[1]

                               tun_src = tunnel[2]['node1'] 
                               tun_dst = tunnel[2]['node2']

                               if( ((tun_src == swname ) and ( tun_dst ==node)) or ((tun_src == node) and (tun_dst == swname)) ):
                                   cls = None

                                   tmp_sw_map1 = []
                                   tmp_sw_map2 = []
                                   tmp_src_port = 0
                                   tmp_dst_port = 0

                                   # We are making an assumption that tun_src
                                   # switch is greater than tun_dst switch.
                                   # Accordingly we us this logic

                                   if( swname < node):
                                       tun_src = swname
                                       tun_dst = node
                                   else:
                                       tun_src = node
                                       tun_dst = swname

                                   dbg_str =  "Tun Src ...", tun_src 
                                   self.logger.debug( dbg_str )
                                   dbg_str =  "Tun Dst ...", tun_dst 
                                   self.logger.debug( dbg_str )

                                   tmp_sw_map1 = graph.get_switch_port_map(tun_src)
                                   tmp_sw_map2 = graph.get_switch_port_map(tun_dst)

                                   for tmp_port, node1 in tmp_sw_map1:
                                       if (node1 == tun_dst):
                                           tmp_dst_port = tmp_port

                                   for tmp_port, node2 in tmp_sw_map2:
                                       if (node2 == tun_src):
                                           tmp_src_port = tmp_port

                                   dbg_str = "Tunnel interface paramters ..." 
                                   self.logger.debug( dbg_str )

                                   dbg_str = "Tunnel Source ..." , tun_src 
                                   self.logger.debug( dbg_str )

                                   dbg_str = "Tunnel Src port ..." , tmp_src_port 
                                   self.logger.debug( dbg_str )
                                   dbg_str =  "Tunnel Dst ..." , tun_dst 
                                   self.logger.debug( dbg_str )

                                   dbg_str = "Tunnel Dst Port ..." , tmp_dst_port 
                                   self.logger.debug( dbg_str )

                                  # Modify Tunnel port parameters 
                                   tunnel[2]['node1'] = tun_src
                                   tunnel[2]['node2'] = tun_dst
                                   tunnel[2]['port1'] = tmp_src_port
                                   tunnel[2]['port2'] = tmp_dst_port

                                   # We need to add tunnel to this node 
                                   dbg_str =  "Adding tunnel interface to switch",tun_switch_name,tun_intf_name 
                                   self.logger.info( dbg_str )
                                   cls = None
                                   # self.addTunnel(tunnel[0], tunnel[1], port, cls, STT=STT, **tunnel[2])
                                   self.addTunnel(tunnel[0], tunnel[1], port, cls, STT=STT )
                                   exercise.set_tunnel_delay(tun_src, tun_dst, tun_intf_name )
                               else:
                                   dbg_str =  "Skipping tunnel logic for ..",swname,node 
                                   self.logger.debug( dbg_str )
                   else:
                       exercise.topo.addToSwitchAtPort(swname, port,node)
                       pass

        else:
           # No partitioning. Single worker case. Old logic applies

           self.logger.info( "No Partition DOne ...." )
           self.logger.info( "Build Mininet Topology as per Original input ..." )
        exercise.topo.printPortMapping()

        # exercise.run_exercise()
        # self.net = exercise.net # Initialize Mininet object
        # self.net.start()  # Masked in the beginning itself by RB

        self.logger.info("Adding tunnels to mininet instance")
        for tunnel in tunnels:
            print "Tunnel Information.."
            print tunnel

            port = None
            cls = None
            if "node1" not in tunnel[2].keys():
               self.logger.info("Error! node1 is missing in tunnel metadata")
            if tunnel[2]["node1"] in topo.nodes():
               port = tunnel[2]["port1"]
            else:
               port = tunnel[2]["port2"]

            if "cls" in tunnel[2].keys():
                cls = tunnel[2]["cls"]
                del tunnel[2]["cls"]
            # self.addTunnel(tunnel[0], tunnel[1], port, cls, STT=STT, **tunnel[2])
            # self.net.start()  # Masked in beginning itself by RB

        self.logger.info("Startup complete.")
        self.x11popens = []

        # some programming that must happen after the net has started

        self.logger.info( "Starting Network .." )
        self.net.start()  # Done here for proper programming of switches by RB

        self.logger.info( "Program Hosts .." )
        exercise.program_hosts()

        self.logger.info( "Program Switches .." )
        exercise.program_switches()

        # wait for that to finish. Not sure how to do this better
        sleep(1)

        if( get_exp_mininet_cli() == "True" ):
            exercise.do_net_cli()
        return True

    @Pyro4.expose
    def destroy_mininet(self):
        """shut down mininet instance"""
        if self.net:
            for popen in self.x11popens:
                popen.terminate()
                popen.communicate()
                popen.wait()
            self.net.stop()
            self.logger.info("mininet instance terminated")
            self.net = None

    @Pyro4.expose
    def configLinkStatus(self, src, dst, status):
        self.net.configLinkStatus(src, dst, status)

    @Pyro4.expose
    def rpc(self, hostname, cmd, *params1, **params2):
        h = self.net.get(hostname)
        return getattr(h, cmd)(*params1, **params2)

    @Pyro4.expose
    def attr(self, hostname, name):
        h = self.net.get(hostname)
        return getattr(h, name)

    @Pyro4.expose
    def addHost(self, name, cls=None, **params):
        self.net.addHost(name, cls, **params)
        return name

    @Pyro4.expose
    def addSwitch(self, name, cls=None, **params):
        self.net.addSwitch(name, cls, **params)
        #TODO: This should not be done here
        self.net.get(name).start(self.net.controllers)
        return name

    @Pyro4.expose
    def addController(self, name="c0", controller=None, **params):
        self.net.addController(name, controller, **params)
        return name

    @Pyro4.expose
    def addTunnel(self, name, switch, port, intf, STT=False, **params):

        dbg_str = "Add Tunnel : Name..", name
        self.logger.debug( dbg_str )

        dbg_str =  "Switch..", switch
        self.logger.debug( dbg_str )

        dbg_str =  "Port..", port
        self.logger.debug( dbg_str )

        dbg_str =  "Intf..", intf
        self.logger.debug( dbg_str )
        dbg_str =  "Params..", params
        self.logger.debug( dbg_str )

        switch_i = self.net.get(switch)
        if not intf:
            intf = TCIntf
        if STT:
            subprocess.check_output(["ovs-vsctl","add-port", switch, name])
        else:
            intf(name, node=switch_i, port=port, link=None, **params)

    @Pyro4.expose
    def tunnelX11(self, node, display):
        node = self.net.get(node)
        (tunnel, popen) = mininet.term.tunnelX11(node, display)
        self.x11popens.append(popen)

    @Pyro4.expose
    def addLink(self, node1, node2, port1=None, port2=None, cls=None,
                **params):
        node1 = self.net.get(node1)
        node2 = self.net.get(node2)
        l = self.net.addLink(node1, node2, port1, port2, cls, **params)
        return ((node1.name, l.intf1.name), (node2.name, l.intf2.name))


    @Pyro4.expose
    def runCmdOnHost(self, hostname, command, noWait=False):
        '''
            e.g. runCmdOnHost('h1', 'ifconfig')
        '''
        h1 = self.net.get(hostname)
        if noWait:
            return h1.sendCmd(command)
        else:
            return h1.cmd(command)

    @Pyro4.expose
    def program_myswitch(self, swname):
        print "Going to Program Switch ...",swname
        tmp_exercise = self.exercise
        tmp_exercise.program_myswitch(swname)

        return


def getFrontendStatus():
    config = MaxiNetConfig(register=False)
    ip = config.get_nameserver_ip()
    port = config.get_nameserver_port()
    pw = config.get_nameserver_password()
    ns = Pyro4.locateNS(ip, port, hmac_key=pw)
    manager_uri = ns.lookup("MaxiNetManager")
    if(manager_uri):
        manager = Pyro4.Proxy(manager_uri)
        manager._pyroHmacKey=pw
        print manager.print_worker_status()
    else:
        print "Could not contact Frontend server at %s:%s" % (ip, port)


def json_savetopo( topo ):
    # print "..Save Topo in JSON .."


    f = open("/tmp/topology.json", "w")

    # 5 spaces given here
    st =  '{'
    print >>f, st
    st =  '     "hosts" : ['
    print >>f, st

    cnt = 0
    for hostName in topo.hosts():
        cnt = cnt + 1

    x = 0
    for hostName in topo.hosts():
        # print "Adding Hosts:",hostName
        # 8 spaces given here
        if x < (cnt -1) :
            st = '        "%s",' % hostName
        else :
            st = '        "%s"' % hostName
        print >>f, st
        x = x + 1

    st = '     ],'
    print >>f, st

    # 5 spaces given here
    st =  '     "switches" : {'
    print >>f, st

    cnt = 0
    for switchName in topo.switches():
         cnt = cnt + 1

    x = 0
    for switchName in topo.switches():
        # print "Adding Switch:",switchName
        if x < ( cnt -1 ) :
            bt = '        "%s": { "cli_input" : ' % switchName 
            bt1 =  ' "%s-cmnds.txt" },' %switchName
            print >>f, bt,bt1
        else :
            bt = '        "%s": { "cli_input" : ' % switchName 
            bt1 =  ' "%s-cmnds.txt" }' %switchName
            print >>f, bt,bt1
        x = x + 1

    st =  '     },'
    print >>f, st

    st =  '     "links" : ['
    print  >>f, st

    cnt = 0
    for srcName, dstName, params in topo.links(sort=True,withInfo=True):
         cnt = cnt + 1

    x = 0
    for srcName, dstName, params in topo.links(sort=True,withInfo=True):
        if x < ( cnt -1 ) :
            # print "Links :",srcName,dstName
            bt =  '          ["%s",' % srcName
            bt1 = '"%s"],' % dstName
            print >>f, bt,bt1
        else :
            # print "Links :",srcName,dstName
            bt =  '          ["%s",' % srcName
            bt1 = '"%s"]' % dstName
            print >>f, bt,bt1
        x = x + 1

    st = '     ]'
    print >>f, st

    st = '}'
    print >>f, st
    f.close()

def main():
    parser = argparse.ArgumentParser(description="MaxiNet Worker which hosts a mininet instance")
    parser.add_argument("--ip", action="store", help="Frontend Server IP")
    parser.add_argument("--port", action="store", help="Frontend Server Port", type=int)
    parser.add_argument("--password", action="store", help="Frontend Server Password")
    parser.add_argument("-c", "--config", metavar="FILE", action="store", help="Read configuration from FILE")
    parsed = parser.parse_args()

    ip = False
    port = False
    pw = False
    if (parsed.config or
            os.path.isfile("MaxiNet.cfg") or
            os.path.isfile(os.path.expanduser("~/.MaxiNet.cfg")) or
            os.path.isfile("/etc/MaxiNet.cfg")):
        if parsed.config:
            config = MaxiNetConfig(file=parsed.config,register=False)
        else:
            config = MaxiNetConfig(register=False)
        ip = config.get_nameserver_ip()
        port = config.get_nameserver_port()
        pw = config.get_nameserver_password()
    if parsed.ip:
        ip = parsed.ip
    if parsed.port:
        port = parsed.port
    if parsed.password:
        pw = parsed.password

    if os.getuid() != 0:
        print "MaxiNetWorker must run with root privileges!"
        sys.exit(1)

    if not (ip and port and pw):
        print "Please provide MaxiNet.cfg or specify ip, port and password of \
               the Frontend Server."
    else:
        workerserver = WorkerServer()

        signal.signal(signal.SIGINT, workerserver.exit_handler)

        workerserver.start(ip=ip, port=port, password=pw)
        workerserver.monitorFrontend()



if(__name__ == "__main__"):
    main()
    # print "Instantiating Exercise.."
    # exercise = ExerciseRunner("/home/rbabu/MaxiNet/MaxiNet/WorkerServer/topology.json","/home/rbabu/MaxiNet/MaxiNet/WorkerServer","/home/rbabu/MaxiNet/WorkerServer","simple_router.json",'/home/rbabu/behavioral-model/targets/simple_router/simple_router',True)
    # print "Successfully Instantiated Exercise.."
    # exercise.run_exercise()

