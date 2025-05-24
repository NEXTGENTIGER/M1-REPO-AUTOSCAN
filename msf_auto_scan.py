import subprocess
import os
import re
import json
import shutil

BASE_DIR = '/app/metasploit'

def get_local_ip():
    try:
        result = subprocess.run(['hostname', '-I'], capture_output=True, text=True)
        ip = result.stdout.strip().split()[0]
        return ip
    except Exception as e:
        print(f"Erreur pour récupérer IP: {e}")
        return None

def generate_rc_file(ip, rc_template_path=f'{BASE_DIR}/scan_template.rc', rc_out_path=f'{BASE_DIR}/scan_auto.rc'):
    with open(rc_template_path, 'r') as f:
        content = f.read()
    content = content.replace('__TARGET_IP__', ip)
    with open(rc_out_path, 'w') as f:
        f.write(content)
    return rc_out_path

def run_msfconsole(rc_path):
    if not shutil.which("msfconsole"):
        print("Erreur: msfconsole non trouvé dans le PATH.")
        return None

    print("Lancement de Metasploit...")
    spool_path = f'{BASE_DIR}/results/spool.txt'
    os.makedirs(f'{BASE_DIR}/results', exist_ok=True)
    cmd = ['msfconsole', '-q', '-r', rc_path]
    with open(spool_path, 'w') as f:
        result = subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT)
        if result.returncode != 0:
            print("Erreur lors de l'exécution de msfconsole.")
            return None
    print(f"Metasploit terminé. Spool enregistré dans {spool_path}")
    return spool_path

def parse_spool_to_json(spool_path, json_out_path=f'{BASE_DIR}/results/msf_report.json'):
    if not spool_path or not os.path.exists(spool_path):
        print("Fichier spool introuvable, impossible de parser.")
        return

    with open(spool_path, 'r') as f:
        lines = f.readlines()

    results = []
    for line in lines:
        host_match = re.search(r'Host: (\d+\.\d+\.\d+\.\d+)', line)
        port_match = re.search(r'Port: (\d+)/tcp', line)
        state_match = re.search(r'State: (\w+)', line)
        service_match = re.search(r'Service: (\w+)', line)

        if host_match and port_match and state_match:
            results.append({
                "host": host_match.group(1),
                "port": int(port_match.group(1)),
                "state": state_match.group(1),
