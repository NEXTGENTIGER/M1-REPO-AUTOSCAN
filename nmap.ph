import nmap
import json
import sys
import os

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "scanme.nmap.org"
    scanner = nmap.PortScanner()

    # Scan complet : SYN scan, version, OS, scripts, tous les ports TCP
    options = "-sS -sV -O -A -p 1-65535"

    print(f"Lancement du scan complet sur {target}...")

    scanner.scan(target, arguments=options)

    results = {}

    for host in scanner.all_hosts():
        host_info = {
            "state": scanner[host].state(),
            "hostname": scanner[host].hostname(),
            "protocols": {},
            "osmatch": scanner[host].get('osmatch', [])
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
                    "reason": scanner[host][proto][port].get('reason', ''),
                    "conf": scanner[host][proto][port].get('conf', ''),
                }
            host_info["protocols"][proto] = ports_info
        results[host] = host_info

    os.makedirs("/app/results", exist_ok=True)
    output_file = "/app/results/result.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"Scan terminé. Résultats sauvegardés dans {output_file}")

if __name__ == "__main__":
    main()
