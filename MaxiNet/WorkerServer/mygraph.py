
import os, sys, json, subprocess, re, argparse
import time
import logging

class MyTopoGraph(object):

    def  __init__(self, graph_dict = None,host_links=None,switch_links=None,sw_port_mapping=None):
        """ Initialized a graph object 
            If no dictionary or None is given,
            an empty dictionary will be used
        """

        if graph_dict == None:
            graph_dict = {}
        self.__graph_dict = graph_dict
        self.host_links = []
        self.switch_links = []
        self.myhost_list = []
        self.myswitch_list = []
        self.my_allowed_paths = []
        self.sw_port_mapping = {}

    def vertices(self):
        """ returns the vertices of a graph """
        return list(self.__graph_dict.keys())

    def edges(self):
        """ returns the edges of a graph """
        return self.__generate_edges()


    def add_vertex(self,vertex):
        """ If the vertex is no in self.graph.dict
            a key vertex with an empty list is added
            to the dictionary. Otherwise nothing has
            to be done.
        """
        if vertex not in self.__graph_dict:
            self.__graph_dict[vertex] = []
            # logging.debug("vertex being initialized ..", vertex)
        else:
            # logging.debug("vertex not added ..", vertex)
            pass

    def add_edge(self, edge):
        """ assumes that edge is of type set, tuple or list
            between two vertices can be multiple edges !
        """
        edge = set(edge)
        (vertex1, vertex2) = tuple(edge)
        if vertex1 not in self.__graph_dict:
            self.__graph_dict[vertex1] = []
            dbg_str = "Vertex being initialized .." + str(vertex1)
            # logging.debug(dbg_str)
        if vertex2 not in self.__graph_dict:
            self.__graph_dict[vertex2] = []
            dbg_str = "Vertex being initialized .." + str(vertex2)
            # logging.debug(dbg_str)
        if vertex2 not in self.__graph_dict[vertex1]:
            self.__graph_dict[vertex1].append(vertex2)
            dbg_str = "Appending .. " + str(vertex2), "to ->" +str(vertex1)
            # logging.debug(dbg_str)

        if vertex1 not in self.__graph_dict[vertex2]:
            self.__graph_dict[vertex2].append(vertex1)
            dbg_str = "Appending .. " + str(vertex1), "to ->" +str(vertex2)
            # logging.debug(dbg_str)

    def dump_graph(self):
        """ A static method generating the edges of the graph "graph"
            Edges are represented as sets with one (a loopback to the vertex)
            or two vertices
        """

        edges = []
        for vertex in self.__graph_dict:
            mylist = list(vertex)
            logging.debug("mylist : ", mylist)

    def dump_vertex(self, vertex):
        """ A static method generating the edges of the graph "graph"
            Edges are represented as sets with one (a loopback to the vertex)
            or two vertices
        """

        mylist = self.__graph_dict[vertex]
        logging.debug( "** Mylist : ", mylist)

    def __generate_edges(self):
        """ A static method generating the edges of the graph "graph"
            Edges are represented as sets with one (a loopback to the vertex)
            or two vertices
        """

        edges = []
        for vertex in self.__graph_dict:
            for neighbour in self.__graph_dict[vertex]:
                if {neighbour, vertex} not in edges:
                    edges.append( {vertex,neighbour} )
        return edges


    def __str__(self):
        res = "vertices: "
        for k in self.__graph_dict:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.__generate_edges():
            res += str(edge) + " "
        return res


    def find_isolated_vertices(self):
        """ returns list of isolated vertices """
        graph = self.__graph_dict
        isolated = []
        for vertex in graph:
            # print(isolated,vertex)
            if not graph[vertex]:
                isolated += [vertex]
        return isolated

    def find_path(self, start_vertex, end_vertex, path=[]):
        """ find a path from start vertex to end vertex in graph """

        graph = self.__graph_dict
        path = path + [start_vertex]
        if start_vertex == end_vertex:
            return path

        if start_vertex not in graph:
            return None

        for vertex in graph[start_vertex]:
            if vertex not in path:
                extended_path = self.find_path(vertex, end_vertex,path)
                if extended_path:
                    return extended_path
        return None

    def find_all_path(self, start_vertex, end_vertex, path=[]):
        """ find all paths from start vertex to end vertex in graph """

        graph = self.__graph_dict
        path = path + [start_vertex]
        if start_vertex == end_vertex:
            return [path]

        if start_vertex not in graph:
            return []

        paths = []
        for vertex in graph[start_vertex]:
            if vertex not in path:
                extended_paths = self.find_all_path(vertex, end_vertex,path)
                for p in extended_paths:
                    paths.append(p)
        return paths

    def is_connected(self, vertices_encountered = None, start_vertex=None):
        """ Determines if the graph is connected """

        if vertices_encountered is None:
            vertices_encountered = set()
        gdict = self.__graph_dict
        vertices = list(gdict.keys())  # list is necessary in python 3
        # if empty list return
        if len(vertices) == 0 :
            return False
        if not start_vertex:
            # Choose a vertex vertex from graph as starting point
            start_vertex = vertices[0]
        vertices_encountered.add(start_vertex)
        if len(vertices_encountered) != len(vertices):
            for vertex in gdict[start_vertex]:
                if vertex not in vertices_encountered:
                    if self.is_connected(vertices_encountered,vertex):
                        return True
        else:
            return True
        return False

    def get_switch(self,host):
        """ Gets the switch number to which this host is connected.
            Assumption is that host is connected to only 1 switch.
            This switch also would occur as 1st element in the list,
            that corresponds to host as vertex in graph_dict
        """
        switch_list = self.__graph_dict[host]
        switch_num = switch_list[0]
        return switch_num

    def get_switch_port_mapping(self,switch_name):
        """ Gets the Port mapping of the given switch name as input .
        """
        switch_list = []
        switch_list = self.__graph_dict[switch_name]
        return switch_list

    def diameter(self):
        """ Calculates the diameter of the graph """

        v = self.vertices()
        pairs = [ (v[i],v[j]) for i in range(len(v)-1) for j in range(i+1, len(v))]
        smallest_paths = []
        for (s,e) in pairs:
            paths = self.find_all_path(s,e)
            smallest = sorted(paths, key=len)[0]
            smallest_paths.append(smallest)

        smallest_paths.sort(key=len)

        # Print the list smallest_paths

        # Longest path is at the end of list
        # ie diameter corresponds to length of this path

        diameter = len(smallest_paths[-1]) -1
        return diameter

    def add_switch_port(self,sw, node2):
        if sw not in self.sw_port_mapping:
            self.sw_port_mapping[sw] = []
        # portno = len(self.sw_port_mapping[sw])+1
        # print "Switch ..", sw, "Adding node ..", node2 
        # print "Port ..", portno
        # self.sw_port_mapping[sw].append((portno, node2))
        self.sw_port_mapping[sw].append( node2 )


    def get_switch_port_map(self,switch_name):
        """ Gets the Port mapping of the given switch name as input .
        """

        # Now do a sort and return a map having port nos & connected devices
        myswitch_pmap = []
        self.sw_port_mapping[switch_name].sort()
        idx = 1
        for swname in self.sw_port_mapping[switch_name]:
           myswitch_pmap.append( (idx, swname) )
           idx = idx + 1
        return myswitch_pmap

    def printPortMapping(self):
        print "Switch port mapping:"
        for sw in sorted(self.sw_port_mapping.keys()):
            self.sw_port_mapping[sw].sort()
            print "%s: " % sw,
            idx = 1
            for node2 in self.sw_port_mapping[sw]:
                print "%d" % idx,
                print "%s\t" % node2,
                idx = idx + 1
            print


    def init_graph_from_topofile(self, fname):


        # Load Json file into graph
    
        with open(fname) as data_file:
            data = json.load(data_file)

        hnames = data["hosts"]
        hlen = len(hnames)
        for x in range(0,hlen) :
            tmp = str(hnames[x])
            # self.add_vertex(tmp)

        for key, value in dict.items(data["switches"]):
            for value1, value2 in dict.items(data["switches"][key]):
                tmp = str(key)
                # self.add_vertex(tmp)

        hnames = data["links"]
        hlen = len(hnames)
        self.host_links = []
        self.switch_links = []
        tmp = " "
        tmp1 = " "
        for x in range(0,hlen) :
             tmp = str(hnames[x][0])
             tmp1 = str(hnames[x][1])
             # self.add_vertex(tmp)
             # self.add_vertex(tmp1)
             self.add_edge( [ tmp, tmp1 ] )
             if( tmp[0] == 's' and tmp1[0] == 's'):
                 # This is switch link
                 self.switch_links.append(hnames[x])
             else:
                 self.host_links.append(hnames[x])

        # Process allowed_paths
        for item in dict.items( data["allowed_paths"] ):
            self.my_allowed_paths.append(item)

        # Print the Host links here...

        self.host_links.sort()
        # print "Host links ..."
        # print self.host_links

        # Print the Host links here...

        # print "Switch links ..."
        self.switch_links.sort()
        # print self.switch_links

        # print("Edges of graph :")
        edgs = self.edges()
        # print edgs
        # print "------"
        ln = len(edgs)
        tmp_host_list = []
        self.myswitch_list = []
        for x in range(0,ln):
            # print edgs[x]
            tmp = list(edgs)[x]
            for y in edgs[x] :
                tmp1 = str(y)
                if tmp1[0] == 'h':
                    # print "Host ..", tmp1
                    if tmp1 not in tmp_host_list:
                        tmp_host_list.append(tmp1)
                else:
                    # print "Switch ..", tmp1
                    if tmp1 not in self.myswitch_list:
                        self.myswitch_list.append(tmp1)

        # logic to compute IP address of host
        # IP addr is formed by varied the 3rd byte in the address
        # logic to compute mac address of host
        # Mac address is formed by using the switch num & host number for bytes 5,6


        cnt = 1
        host_ipaddr = []
        mac_addr = []
        self.myhost_list = []
        for i in tmp_host_list:
            # print "** Host :", i
            host = str(i)
            tmp_host = host[1:]
            host_num = int(tmp_host)
            tmp_host_ipaddr = "10.0." + str(host_num) + ".10"

            switch_name = self.get_switch(host)
            tmp_sw = switch_name[1:]
            sw_num = int(tmp_sw)
            tmp_mac_addr = "00:00:00:00:" 
            swtch = "%02x:" % sw_num
            hnum = "%02x" % host_num
            tmp_mac_addr = tmp_mac_addr + str(swtch) + str(hnum)

            self.myhost_list.append( (i, tmp_host_ipaddr, tmp_mac_addr) )
            cnt = cnt + 1

        self.myhost_list.sort()
        # print "Final Host List ..."
        # print self.myhost_list

        host_name = " "
        host_sw = " "
        for tmp_link in self.host_links:
            h_name = tmp_link[0]
            sw_name = tmp_link[1]
            if( len(tmp_link) > 2):
                lat = tmp_link[2]

            # Ignore Latency, BW parameters, that may be set for hosts
            # Since this is purely for graph to find shortest path.

            if (h_name[0] == 'h') :
                host_name = h_name
                host_sw = sw_name
            else:
                host_sw   = h_name
                host_name = sw_name

            # print "Graph Add Host Name ...", host_name
            # print "Graph Add Switch Name ...", host_sw
            # print "Host Name ...", host_name
            # print "Switch Name ...", host_sw
            # host_num = int(host_name[1:])
            # sw_num   = int(host_sw[1:])
            # host_ip = "10.0.%d.10" % (host_num)
            # host_ip = "10.0.%d.%d" % (sw_num, host_num)
            # host_mac = '00:00:00:00:%02x:%02x' % (sw_num, host_num)
            # Each host IP should be /24, so all exercise traffic will use the
            # default gateway (the switch) without sending ARP requests.
            self.add_switch_port(host_sw,host_name)

        for link in self.switch_links:
            self.add_switch_port(link[0], link[1])
            self.add_switch_port(link[1], link[0])

        self.printPortMapping()

        if( len(self.my_allowed_paths) > 0) :
            self.generate_selective_switch_commands()
        else:
            self.generate_full_switch_commands()

    def generate_selective_switch_commands( self ):     

        print "New Function Generate Selective Switch Programming ..."
        for swname in self.myswitch_list:

            print "\n**** Writting Switch Command File :   ",
            fname = str(swname) + "-cmnds.txt"
            print " ", fname
            f_handle = open(fname,"w") 

            # We have to write the rules for programming the switch to the file:

            st = "table_set_default send_frame _drop"
            print >> f_handle,st
            st = "table_set_default forward _drop"
            print >> f_handle,st
            st = "table_set_default ipv4_lpm _drop"
            print >> f_handle,st
            st = "  "
            print >> f_handle,st

            for hname, ipaddr,macaddr in self.myhost_list :
               st = "table_add send_frame rewrite_mac "
               hst_num = hname[1:]
               st = st + str(hst_num) + str(" => ")
               tmp_mac_addr = str(macaddr)
               st = st + str(tmp_mac_addr)
               print >> f_handle,st

            st = " "
            print >> f_handle,st

            for hname, ipaddr,macaddr in self.myhost_list :
               st = "table_add forward set_dmac "
               st = st + str(ipaddr)
               st = st + " => "
               tmp_mac_addr = str(macaddr)
               st = st + str(tmp_mac_addr)
               print >> f_handle,st

            st = " "
            print >> f_handle,st

            # Here we are beginning to write selective entries for allowed path

            file_next_hop_list=[]
            for key, value in self.my_allowed_paths :
                for hname in value :
                    # print "Find Shortest Path between...", key, "->", hname

                    all_paths = []
                    all_paths = self.find_all_path(key,hname,all_paths)

                    path_len = 99999  # A Big number
                    next_hop_list = []
                    for pname in all_paths:
                        tmp_len = len(pname)
                        if tmp_len < path_len:
                            path_len = tmp_len
                            next_hop_list = pname

                    # print "Shortest Path ","host ",key, "-> ",hname, next_hop_list ,
                    # If the current switch is in the shortest path list
                    # then we have to write an entry for this host in the
                    # switch commands file.

                    found = 0
                    for tmp_sw in next_hop_list:
                        if( found == 1 ):
                            next_hop_node = tmp_sw
                            break
                        elif( tmp_sw == swname ):
                            found = 1

                    if (found == 1): 
                        # print "Next Hop Node ...", next_hop_node
                        print "Add Entry for host route ", key, "->", hname,
                        print "in the commands.txt file for Switch",swname

                        for tmp_hname, ipaddr,macaddr in self.myhost_list :
                            if( tmp_hname != hname) :
                                continue
                            else:
                                break
                        # nxt_hop_switch = next_hop_list[1]
                        # print "Next Hop Switch :", nxt_hop_switch,
                        nxt_hop_port_num = 0

                        sw_map = self.get_switch_port_map(swname)
                        # print "sw map of swname...", sw_map

                        sw_map_len = len(sw_map)
            
                        n = 0
                        for n in range(0,sw_map_len) :

                            # This is a tuple with following structure 
                            # ( portno, nodename, ip addr, mac addr
                            # So we have to compare element at index 1

                            # print "Comparing with ", sw_map[n][1], "at index", n
                            if(sw_map[n][1] == next_hop_node ):
                                nxt_hop_port_num = sw_map[n][0]
                                break

                        # print " Next Hop Switch Port num :", nxt_hop_port_num

                        st = "table_add ipv4_lpm set_nhop " 
                        st = st + str(ipaddr)
                        st = st + "/32 => "
                        st = st + str(ipaddr)
                        nhop_port = str(nxt_hop_port_num)
                        st = st + " " + nhop_port

                        if (st not in file_next_hop_list ):
                            file_next_hop_list.append(st)
                        # print >> f_handle,st

                    else : 
                        pass
                        # print "Skip Entry for host route ", key, "->", hname,
                        # print "in the commands.txt file for Switch",swname

            # From this switch, if there is need to add return path to the
            # source host, we need to add it here, before writing the whole
            # file content
            for hname, value in self.my_allowed_paths :
                # print "Computing All Paths from switch ", swname, "to : ", hname
                all_paths = []
                all_paths = self.find_all_path(swname,hname,all_paths)

                path_len = 99999  # A Big number
                next_hop_list = []
                for pname in all_paths:
                    tmp_len = len(pname)
                    if tmp_len < path_len:
                        path_len = tmp_len
                        next_hop_list = pname

                # print "Shortest Path : ",next_hop_list ,
                # print "Path Len :", path_len
                # print next_hop_list

                # Here find out the 2nd element in the list
                # In the list 1st element is source switch itself

                nxt_hop_switch = next_hop_list[1]
                # print "Next Hop Switch :", nxt_hop_switch,
                nxt_hop_port_num = 0

                # sw_map = my_pmap[swname]
                sw_map_len = len(sw_map)
            
                n = 0
                for n in range(0,sw_map_len) :

                    # This is a tuple with following structure 
                    # ( portno, nodename, ip addr, mac addr
                    # So we have to compare element at index 1

                    # print "Comparing with ", sw_map[n][1], "at index", n
                    if(sw_map[n][1] == nxt_hop_switch ):
                        # We are assigning n+1 because on the switch port numbering
                        # starts from 1, and it is not zero based.
                        # nxt_hop_port_num = (n + 1)
                        nxt_hop_port_num = sw_map[n][0] # Modified by RB
                        break

                # print " Next Hop Switch Port num :", nxt_hop_port_num

                # This loop is being done to calculate IPaddr of source host

                for tmp_hname, ipaddr,macaddr in self.myhost_list :
                    if( tmp_hname != hname) :
                        continue
                    else:
                        break

                st = "table_add ipv4_lpm set_nhop " 
                st = st + str(ipaddr)
                st = st + "/32 => "
                st = st + str(ipaddr)
                nhop_port = str(nxt_hop_port_num)
                st = st + " " + nhop_port

                if (st not in file_next_hop_list ):
                    file_next_hop_list.append(st)

            for st in file_next_hop_list :
                print >> f_handle,st
            f_handle.close()

    def generate_full_switch_commands( self ):     

        for swname in self.myswitch_list:

            print "**** Writting Switch Command File :   ",
            fname = str(swname) + "-cmnds.txt"
            print " ", fname
            f_handle = open(fname,"w") 

            # We have to write the rules for programming the switch to the file:

            st = "table_set_default send_frame _drop"
            print >> f_handle,st
            st = "table_set_default forward _drop"
            print >> f_handle,st
            st = "table_set_default ipv4_lpm _drop"
            print >> f_handle,st
            st = "  "
            print >> f_handle,st

            for hname, ipaddr,macaddr in self.myhost_list :
               st = "table_add send_frame rewrite_mac "
               hst_num = hname[1:]
               st = st + str(hst_num) + str(" => ")
               tmp_mac_addr = str(macaddr)
               st = st + str(tmp_mac_addr)
               print >> f_handle,st

            st = " "
            print >> f_handle,st


            for hname, ipaddr,macaddr in self.myhost_list :
               st = "table_add forward set_dmac "
               st = st + str(ipaddr)
               st = st + " => "
               tmp_mac_addr = str(macaddr)
               st = st + str(tmp_mac_addr)
               print >> f_handle,st

            st = " "
            print >> f_handle,st


            # Now the important logic corresponding to forwarding comes

            print "**** Switch Port Mappings of ***** ", swname
            # print "** Switch Map of :", swname
            sw_map = self.get_switch_port_map(swname)
            print sw_map

            host_cnt = 0
            for hname, ipaddr,macaddr in self.myhost_list :
                # print "Computing All Paths from switch ", swname, "to : ", hname
                all_paths = []
                all_paths = self.find_all_path(swname,hname,all_paths)

                path_len = 99999  # A Big number
                next_hop_list = []
                for pname in all_paths:
                    tmp_len = len(pname)
                    if tmp_len < path_len:
                        path_len = tmp_len
                        next_hop_list = pname

                # print "Shortest Path : ",next_hop_list ,
                # print "Path Len :", path_len
                # print next_hop_list

                # Here find out the 2nd element in the list
                # In the list 1st element is source switch itself

                nxt_hop_switch = next_hop_list[1]
                # print "Next Hop Switch :", nxt_hop_switch,
                nxt_hop_port_num = 0

                # sw_map = my_pmap[swname]
                sw_map_len = len(sw_map)
            
                n = 0
                for n in range(0,sw_map_len) :

                    # This is a tuple with following structure 
                    # ( portno, nodename, ip addr, mac addr
                    # So we have to compare element at index 1

                    # print "Comparing with ", sw_map[n][1], "at index", n
                    if(sw_map[n][1] == nxt_hop_switch ):
                        # We are assigning n+1 because on the switch port numbering
                        # starts from 1, and it is not zero based.
                        # nxt_hop_port_num = (n + 1)
                        nxt_hop_port_num = sw_map[n][0] # Modified by RB

                # print " Next Hop Switch Port num :", nxt_hop_port_num

                st = "table_add ipv4_lpm set_nhop " 
                st = st + str(ipaddr)
                st = st + "/32 => "
                st = st + str(ipaddr)
                nhop_port = str(nxt_hop_port_num)
                st = st + " " + nhop_port

                print >> f_handle,st
                host_cnt = host_cnt + 1

            f_handle.close()
        

if __name__ == "__main__" :

    graph = MyTopoGraph()
    print(graph)
    graph.init_graph_from_topofile('in_topo.json')
