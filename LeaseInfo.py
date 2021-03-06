#!/usr/bin/python3

def split_ip(ip):
    return tuple(int(part) for part in ip.split('.'))

def ip_key(item):
    return split_ip(item[0])

def parse(fileName):

    f = open( fileName, "r" )
    output = {}
    thisIp = ""
    thisMAC = ""
    thisName = ""
    
    for line in f:
        
        # ip
        if (line.find("lease") == 0):
            if (thisIp != ""):
                output[thisIp] = thisIp + " " + thisMAC + " " + thisName
                thisMAC = ""
                thisName = ""
                
            thisIp = line[line.find(" ") +1 : line.find("{") -1]

        # mac
        if(line.find("hardware ethernet") > -1):
            thisMAC = line[line.find("ethernet") +9 : line.find(";")]
        
        # uid - will be replaced with name if it exists
        if(line.find("uid") > -1):
            thisName = line[line.find("uid") +5 : line.find(";") -1]
            
        # hostname
        if(line.find("client-hostname") > -1):
            thisName = line[line.find("hostname") +10 : line.find(";") -1]
            
    #final line
    if (thisIp != ""):
        output[thisIp] = thisIp + " " + thisMAC + " " + thisName

    #print output
    for k, v in sorted(output.items(), key=ip_key):
        print(v)

    # Close the file
    f.close()
    
#parse("/home/james/Source/LeaseInfo/dhcpd.leases")
parse("/var/lib/dhcp/dhcpd.leases")
