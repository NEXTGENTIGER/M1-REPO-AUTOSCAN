import subprocess
import os
import re
import json
import sys

def get_local_ip(interface='eth0'):
    try:
        result = subprocess.run(['ip', 'addr', 'show', interface], capture_output=True, text=True)
        ip_line = next(line for line in result.stdout.split('\n') if 'inet ' in line)
        ip = ip_line.strip().split(' ')[1].split('/')[0]
        return ip
    except Exception as e:
        print(f"Erreur pour récupérer IP: {e}")
        return None

def generate_rc_file(ip, rc_template_path='metasploit/scan_template.rc', rc_out_path='metasploit/scan_auto.rc'):
    with open(rc_template_path, 'r') as f:
        content = f.read()
    content = content.replace('__TARGET_IP__', ip)
    with open(rc_out_path, 'w') as f:
        f.write(content)
    return rc_out_path

def run_msfconsole(rc_path):
    print("Lancement de Metasploit...")
    spool_path = 'metasploit/results/spool.txt'
    os.makedirs('metasploit/results', exist_ok=True)
    cmd = ['/usr/src/metasploit-framework/msfconsole', '-q', '-r', rc_path]
    with open(spool_path, 'w') as f:
        subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT)
    print(f"Metasploit terminé. Spool enregistré dans {spool_path}")
    return spool_path

def test_spool_content(spool_path):
    with open(spool_path, 'r') as f:
        content = f.read()
    if "Host:" in content:
        print("Le fichier spool contient des résultats exploitables.")
    else:
        print("Aucun résultat de scan détecté dans le fichier spool.")

def parse_spool_to_json(spool_path, json_out_path='metasploit/results/msf_report.json'):
    with open(spool_path, 'r') as f:
        lines = f.readlines()

    results = []
    exploits = []

    for line in lines:
        host_match = re.search(r'Host: (\d+\.\d+\.\d+\.\d+)', line)
        port_match = re.search(r'Port: (\d+)/tcp', line)
        state_match = re.search(r'State: (\w+)', line)
        service_match = re.search(r'Service: (\w+)', line)

        exploit_match = re.search(r'\[\*\] Meterpreter session (\d+) opened.*?(\d+\.\d+\.\d+\.\d+)', line)
        user_match = re.search(r'Username\s+:\s+(\w+)', line)
        platform_match = re.search(r'Platform\s+:\s+(\w+)', line)

        if host_match and port_match and state_match:
            host = host_match.group(1)
            port = int(port_match.group(1))
            state = state_match.group(1)
            service = service_match.group(1) if service_match else ""

            results.append({
                "host": host,
                "port": port,
                "state": state,
                "service": service
            })

        elif exploit_match:
            session_id = int(exploit_match.group(1))
            host = exploit_match.group(2)

            exploits.append({
                "exploit_module": "exploit/windows/smb/ms08_067_netapi",
                "payload": "windows/meterpreter/reverse_tcp",
                "status": "success",
                "session": {
                    "type": "meterpreter",
                    "session_id": session_id,
                    "user": user_match.group(1) if user_match else "unknown",
                    "platform": platform_match.group(1) if platform_match else "unknown",
                    "host": host
                }
            })

    final_output = {
        "scan_results": results,
        "exploit_results": exploits
    }

    with open(json_out_path, 'w') as f:
        json.dump(final_output, f, indent=2)
    print(f"Rapport JSON enrichi généré dans {json_out_path}")
    print(json.dumps(final_output, indent=2))
    return final_output

def main(ip_cible=None):
    if ip_cible is None:
        ip_cible = get_local_ip()
        if not ip_cible:
            print("IP locale non trouvée, arrêt.")
            return
        print(f"IP locale détectée: {ip_cible}")
    else:
        print(f"IP cible fournie: {ip_cible}")

    rc_path = generate_rc_file(ip_cible)
    spool_path = run_msfconsole(rc_path)
    test_spool_content(spool_path)
    parse_spool_to_json(spool_path)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
