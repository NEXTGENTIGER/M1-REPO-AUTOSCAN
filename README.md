----------------------------------------------------------------------------------------------------------------
À la racine de ton projet (là où est ton docker-compose.yml), lance simplement :

docker-compose up --build

Cela va :
    builder les images si besoin (ton image nmapscanner sera buildée)
    lancer tous les services (metasploit, zap, tshark, nmapscanner)
    ton nmapscanner va exécuter son script automatiquement au démarrage
    les autres services démarreront aussi normalement
    
----------------------------------------------------------------------------------------------------------------
Si tu préfères supprimer tous les conteneurs arrêtés en une seule commande (à utiliser avec précaution) :

docker container prune

----------------------------------------------------------------------------------------------------------------
