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

----------------------------------------------LOG MAPS------------------------------------------------------------------
Directement sur ta machine (dans le dossier monté)

Si tu as bien créé le dossier results localement et que ton volume Docker est configuré correctement, tu peux juste faire :

cat /home/user/M1-REPO-AUTOSCAN/results/result.json

ou pour un affichage plus lisible :

jq . /home/user/M1-REPO-AUTOSCAN/results/result.json

(jq est un utilitaire JSON pratique, sinon tu peux juste utiliser cat)
2. Depuis le conteneur Docker

Si tu veux lire le fichier directement à l’intérieur du conteneur nmapscanner :

docker exec -it nmapscanner cat /app/results/result.json

Ou pour une lecture paginée :

docker exec -it nmapscanner less /app/results/result.json

----------------------------------------------------------------------------------------------------------------
