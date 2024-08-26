#!/usr/bin/env python3

import json
import subprocess
#This command gets the configuration of the Kea server, which includes the subnets names and their IDs, and we'll use it to store in a json file and track the status using the VLAN name.
command = ''' echo '{"command": "config-get"}' | sudo socat - UNIX-CONNECT:/run/kea/kea4-ctrl-socket '''

sn = {}
result = subprocess.run(command, shell=True, capture_output=True, text=True)
data = json.loads(result.stdout)
for lease in data['arguments']['Dhcp4']['subnet4']:
        sn[lease['user-context']['comment']]=lease['id']

with open('/etc/zabbix/zabbix_agent2.d/scripts/isc-kea-server/subnets.json','w') as f:
        json.dump(sn,f,indent=4)

# Print the list of subnets names
zabbix_data = {"data": [{"{#SUBNET}": key} for key in sn.keys()]}
print(json.dumps(zabbix_data))
