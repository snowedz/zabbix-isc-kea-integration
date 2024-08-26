#!/usr/bin/env python3

import json
import sys
import subprocess
#This commands gets the total number of IP's by subnet
command = '''echo '{"command": "stat-lease4-get"}' | sudo -S /usr/bin/socat - UNIX-CONNECT:/run/kea/kea4-ctrl-socket '''
result = subprocess.run(command, shell=True, capture_output=True, text=True)
status = json.loads(result.stdout)

f = open('/etc/zabbix/zabbix_agent2.d/scripts/isc-kea-server/subnets.json', 'r')
subnets_name = json.load(f)

def total_ips(sn):
    subnet_id = subnets_name[sn]
    print(f"{(status['arguments']['result-set']['rows'][subnet_id - 1][1])}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Wrong VLAN name')
        sys.exit(1)
    sn = sys.argv[1]

total_ips(sn)

