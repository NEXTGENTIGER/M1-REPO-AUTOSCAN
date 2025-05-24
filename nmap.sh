import nmap
import json

scanner = nmap.PortScanner()

target = "scanme.nmap.org"
options = "-sS -sV -O -A -p 1-1000"

scanner.scan(target, arguments=options)

results = {}

for host in scanner.all_hosts():
    host_info = {
        "state": scanner[host].state(),
        "protocols": {}
    }
    for proto in scanner[host].all_protocols():
        ports_info = {}
        for port in scanner[host][proto].keys():
            ports_info[port] = {
                "state": scanner[host][proto][port]['state'],
                "name": scanner[host][proto][port]['name'],
                "product": scanner[host][proto][port].get('product', ''),
                "version": scanner[host][proto][port].get('version', ''),
                "extrainfo": scanner[host][proto][port].get('extrainfo', ''),
            }
        host_info["protocols"][proto] = ports_info
    results[host] = host_info

print(json.dumps(results, indent=2))
