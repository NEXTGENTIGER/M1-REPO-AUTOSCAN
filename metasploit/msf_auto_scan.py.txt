import subprocess
import os
import re
import json

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
    # On redirige stdout/stderr dans un fichier spool.txt
    spool_path = 'metasploit/results/spool.txt'
    os.makedirs('metasploit/results', exist_ok=True)
    cmd = ['msfconsole', '-q', '-r', rc_path]
    with open(spool_path, 'w') as f:
        subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT)
    print(f"Metasploit terminé. Spool enregistré dans {spool_path}")
    return spool_path

def parse_spool_to_json(spool_path, json_out_path='metasploit/results/msf_report.json'):
    with open(spool_path, 'r') as f:
        lines = f.readlines()

    results = []
    current_host = None

    # Exemple: parser lignes avec "Host: <ip> Port: <port>/tcp State: open"
    for line in lines:
        host_match = re.search(r'Host: (\d+\.\d+\.\d+\.\d+)', line)
        port_match = re.search(r'Port: (\d+)/tcp', line)
        state_match = re.search(r'State: (\w+)', line)
        service_match = re.search(r'Service: (\w+)', line)

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

    with open(json_out_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Rapport JSON généré dans {json_out_path}")

def main():
    ip = get_local_ip()
    if not ip:
        print("IP locale non trouvée, arrêt.")
        return
    print(f"IP locale détectée: {ip}")

    rc_path = generate_rc_file(ip)
    spool_path = run_msfconsole(rc_path)
    parse_spool_to_json(spool_path)

if __name__ == "__main__":
    main()
