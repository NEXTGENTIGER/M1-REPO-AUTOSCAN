FROM python:3.11-slim

# Installer nmap
RUN apt-get update && apt-get install -y nmap

# Installer python-nmap
RUN pip install python-nmap

WORKDIR /app

# Copier ton script python
COPY nmap.py .

# Commande pour lancer le script python
CMD ["python3", "nmap.py"]
