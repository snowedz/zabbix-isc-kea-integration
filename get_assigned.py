#!/usr/bin/env python3

import json
import sys
import subprocess
#This command gets the status of the leases and we'll use it to get the number of assigned IPs by subnet.
command = '''echo '{"command": "stat-lease4-get"}' | sudo -S /usr/bin/socat - UNIX-CONNECT:/run/kea/kea4-ctrl-socket '''
result = subprocess.run(command, shell=True, capture_output=True, text=True)
status = json.loads(result.stdout)

f = open('/etc/zabbix/zabbix_agent2.d/scripts/isc-kea-server/subnets.json', 'r')
subnets_name = json.load(f)

def find_row_by_subnet_id(subnet_id):
    rows = status['arguments']['result-set']['rows']
    for row in rows:
        if row[0] == subnet_id:
            return row

def signed_ips(sn):
    subnet_id = subnets_name[sn]
    row = find_row_by_subnet_id(subnet_id)
    return row[3]

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Wrong VLAN name')
        sys.exit(1)
    sn = sys.argv[1]

print(signed_ips(sn))
