#!/usr/bin/env python

# Copyright (c) 2015, Ales Cernivec. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""
Proto Local address                  Remote address                 Status        PID    Program name         Location 1           Location 2          
tcp   127.0.0.1:17603                -                              LISTEN        2988   dropbox              local                local               
tcp   172.16.93.140:58723            52.21.87.43:443                ESTABLISHED   29165  firefox              "United States"      "North America"     
tcp   127.0.0.1:44680                127.0.0.1:2222                 ESTABLISHED   9135   ssh                  local                local               
tcp   127.0.0.1:44088                127.0.0.1:43662                ESTABLISHED   29281  GoogleTalkPlugi      local                local               
tcp6  :::22                          -                              LISTEN        -      ?                    local                local               
udp   0.0.0.0:1196                   -                              NONE          -      ?                    local                local               
tcp   172.16.93.140:45608            74.125.136.189:443             ESTABLISHED   29165  firefox              "United States"      "North America"     
tcp   172.16.93.140:53025            91.217.255.47:443              ESTABLISHED   31424  storagesync          Slovenia             Europe              
tcp   172.16.93.140:36656            148.251.181.44:7615            ESTABLISHED   7720   islpronto            Germany              Europe              
tcp   172.16.93.140:45030            91.217.255.47:443              ESTABLISHED   31433  storagesync          Slovenia             Europe              
...
"""

import socket
from socket import AF_INET, SOCK_STREAM, SOCK_DGRAM
import ipaddress
import psutil

GEOIP_COUNTRY_DIR = "../database"
GEOIP_CITY_DIR = "../database"
AD = "-"
AF_INET6 = getattr(socket, 'AF_INET6', object())
proto_map = {
    (AF_INET, SOCK_STREAM): 'tcp',
    (AF_INET6, SOCK_STREAM): 'tcp6',
    (AF_INET, SOCK_DGRAM): 'udp',
    (AF_INET6, SOCK_DGRAM): 'udp6',
}

def read_geoip_countries():
    seq=( GEOIP_COUNTRY_DIR,"country-blocks-en.csv" )
    fname="/".join( seq )
    content = [line.rstrip('\n') for line in open(fname)]
    ipdict = dict()
    for line in content:
        sline = line.split(",")
        if sline[0] != "network":
            ipdict[sline[0]]=sline[1]
    return ipdict 

def read_geoip_country_names(type='cities'):
    if type == 'cities':
        seq=( GEOIP_CITY_DIR,"city-locations-en.csv" )
    elif type == 'countries':
        seq=( GEOIP_COUNTRY_DIR,"country-locations-en.csv" )
    fname="/".join( seq )
    content = [line.rstrip('\n') for line in open(fname)]
    ipdict = dict()
    for line in content:
        sline = line.split(",")
        if sline[0] != "geoname_id":
            if type == "cities":
                ipdict[sline[0]]= {'name1': sline[5], 'name2' : sline[10]}
            elif type == 'countries':
                ipdict[sline[0]]= {'name1': sline[5], 'name2' : sline[3]}
    ipdict['local'] = {"name1": "local", "name2": "local"}
    return ipdict 

def return_country_id(ipdict, ip):
    try:
        ip_addr = ipaddress.IPv4Address(ip)
    except ipaddress.AddressValueError:        
        return "local"    
    if ip_addr.is_private:
        return 'local'
    for net in ipdict:
        try:
            if ip_addr in ipaddress.IPv4Network(net.decode('unicode-escape')):
                return ipdict[net]
        except ipaddress.AddressValueError:
            print "err %s %s" % (net, ipdict[net])
            raise "Can not parse the address in return_country_id"

def main():
    ipcity = read_geoip_country_names('countries')
    ipdict = read_geoip_countries()
    templ = "%-5s %-30s %-30s %-13s %-6s %-20s %-20s %-20s"
    print_out_str = []
    print_out_str.append(templ % (
        "Proto", "Local address", "Remote address", "Status", "PID",
        "Program name", "Location 1", "Location 2"))
    proc_names = {}
    for p in psutil.process_iter():
        try:
            proc_names[p.pid] = p.name()
        except psutil.Error:
            pass
    for c in psutil.net_connections(kind='inet'):
        laddr = "%s:%s" % (c.laddr)
        raddr = ""
        if c.raddr:
            raddr = "%s:%s" % (c.raddr)
        if c.raddr:
            country_id = return_country_id(ipdict, c.raddr[0].decode('unicode-escape'))
            country_city = ipcity[country_id]
        else:
            country_city = {"name1": "local", "name2": "local"}
        print_out = []
        print_out.append([proto_map[(c.family, c.type)],
            laddr,
            raddr or AD,
            c.status,
            c.pid or AD,
            proc_names.get(c.pid, '?')[:15],
            country_city["name1"],
            country_city["name2"]])        
        str_line = templ % (
            proto_map[(c.family, c.type)],
            laddr,
            raddr or AD,
            c.status,
            c.pid or AD,
            proc_names.get(c.pid, '?')[:15],
            country_city["name1"],
            country_city["name2"]  
        )
        print_out_str.append(str_line)
    for i, line in enumerate(print_out_str):   
        print line

if __name__ == '__main__':
    main()