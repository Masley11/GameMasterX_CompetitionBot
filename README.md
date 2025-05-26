# GameMasterX Competition Bot

Ce projet met à jour automatiquement les scores des compétitions e-sport toutes les 15 minutes depuis PandaScore.

## Déploiement

1. Lier ce dépôt à Railway
2. Ajouter les variables d'environnement :
   - PANDASCORE_TOKEN
   - DB_HOST
   - DB_USER
   - DB_PASS
   - DB_NAME

3. Railway exécutera le script automatiquement via GitHub Actions.
