import os
import requests
from dotenv import load_dotenv

# 1. On charge les variables du fichier .env en mémoire
load_dotenv()

CLIENT_ID = os.getenv("FRANCE_TRAVAIL_CLIENT_ID")
CLIENT_SECRET = os.getenv("FRANCE_TRAVAIL_CLIENT_SECRET")

# URL officielle de France Travail pour demander un jeton OAuth2
URL_AUTH = "https://entreprise.francetravail.fr/connexion/oauth2/access_token"


def obtenir_jeton():
    """Se connecte à France Travail pour récupérer un jeton d'accès éphémère."""
    print("Demande de jeton d'accès à France Travail...")

    # Les paramètres requis par le protocole officiel OAuth2 Client Credentials
    params_auth = {"realm": "/partenaire"} # On est quelqu'un d'externe

    headers_auth = {"Content-Type": "application/x-www-form-urlencoded"} # format de l'envoi des données de connexion

    donnees_auth = { # données à envoyer au serveur
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "api_offresdemploiv2",  # Permet d'accéder aux offres v2
    }

    try:
        # On fait une requête POST (car on envoie nos identifiants de connexion)
        response = requests.post(
            URL_AUTH,
            params=params_auth,
            headers=headers_auth,
            data=donnees_auth,
            timeout=10,
        )

        if response.status_code == 200:
            resultat = response.json()
            jeton = resultat.get("access_token")
            print("🔑 Connexion réussie ! Jeton d'accès récupéré avec succès.")
            return jeton
        else:
            print(
                f"❌ Échec de l'authentification. Code HTTP : {response.status_code}"
            )
            print(f"Détail du message : {response.text}")
            return None

    except Exception as e:
        print(f"💥 Une erreur est survenue lors de l'authentification : {e}")
        return None


if __name__ == "__main__":
    # Test de la fonction
    token = obtenir_jeton()
    if token:
        print(f"Mon jeton commence par : {token[:15]}...")