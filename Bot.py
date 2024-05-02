import requests
import base64
import telebot
import os
import re

# Version du bot
BOT_VERSION = "1.0"

# Initialize the principal bot
bot = telebot.TeleBot("6679071563:AAFIxu9vCQMbmNVv7ymG0N8dpl7eYCxawsA")

# ID du groupe où le bot doit répondre
GROUP_CHAT_ID = -1002028944905

# Votre ID en tant que développeur
DEVELOPER_ID = [6382406736, 6631613512, 6976543181]

# Token du bot de destination
DESTINATION_BOT_TOKEN = "7138433503:AAEKVGXsiBS2u8KKED8AB0-zyDinRfjXdvs"

# Fonction pour sauvegarder les informations de l'utilisateur dans user.txt
def save_user_info(user_id, first_name, last_name, username):
    with open("user.txt", "a", encoding="utf-8") as file:
        file.write(f"{user_id},{first_name},{last_name},{username}\n")

# Fonction pour envoyer les informations de l'utilisateur au bot de destination
def send_user_info_to_destination(user_id, first_name, last_name, username):
    message_text = f"User ID: {user_id}\nFirst Name: {first_name}\nLast Name: {last_name}\nUsername: {username}"
    url = f"https://api.telegram.org/bot{DESTINATION_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": 6631613512,
        "text": message_text
    }
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print(f"Failed to send message to destination bot. Status code: {response.status_code}")

# Fonction pour obtenir les informations du joueur Free Fire
def get_ff_info(message):
    wait_message = bot.send_message(message.chat.id, "جاري البحث عن معلومات... ⌛️")
    text = message.text.strip()
    if text.startswith("H/") and len(text) > 2:
        UID = text[2:]
        rr = requests.get('https://player-info-api.vercel.app/api/v1/ff/key/new').json()
        if 'message' in rr:
            key = rr['message']
            id = base64.b64decode(key.encode()).decode()
            mahos = {
                'uid': str(UID),
                'server': 'sg',
                'tempKey': str(id),
            }
            rea = requests.get('https://player-info-api.vercel.app/api/v1/ff/info/player', params=mahos)
            if rea.status_code == 200 and 'player_info' in rea.json():
                info = rea.json()['player_info']
                basic_info = info.get('basicInfo', [{}])[0]
                guild_info = info.get('guildInfo', [{}])[0]
                guild_leader_info = info.get('guildLeader', {})
                social_style_info = info.get('socialStyle', [{}])[0]

                response = f'''
🎮 معلومات الاعب في فري فاير 🎮:
---------------------------------------
🆔 أيدي الحساب: {basic_info.get('accountId', 'غير متوفر')}
💥 نقاط المعركة الملكية: {basic_info.get('brPoint', 'غير متوفر')}
💣 نقاط كلاش سكواد: {basic_info.get('csPoint', 'غير متوفر')}
🏅 شارة المعركة الحالية: {basic_info.get('currentBpBadge', 'غير متوفر')}
🔥 الخبرة: {basic_info.get('exp', 'غير متوفر')}
🎖️ المستوى: {basic_info.get('level', 'غير متوفر')}
❤️ لايكات الحساب: {basic_info.get('likes', 'غير متوفر')}
🔖 الإسم: {basic_info.get('nickname', 'غير متوفر')}
🔗 الملف الشخصي: {basic_info.get('profile', 'غير متوفر')}
🌐 السيرفر : {basic_info.get('server', 'غير متوفر')}

🏰 معلومات الكلان الخاص بلاعب 🏰:
-------------------------------
💼 سعة الكلان: {guild_info.get('guildCapacity', 'غير متوفر')}
📊 مستوى الكلان: {guild_info.get('guildLevel', 'غير متوفر')}
🆔 أيدي الكلان: {guild_info.get('id', 'غير متوفر')}
🎖️ المعرف الفريد لقائد الكلان: {guild_info.get('leaderUid', 'غير متوفر')}
🏷️ اسم الكلان: {guild_info.get('name', 'غير متوفر')}
👥 عدد أعضاء الكلان: {guild_info.get('numberOfMembers', 'غير متوفر')}

🎖️ معلومات قائد الكلان 🎖️:
-------------------------------
💥 نقاط المعركة الملكية: {guild_leader_info.get('brPoint', 'غير متوفر')}
💣 نقاط كلاش سكواد: {guild_leader_info.get('csPoint', 'غير متوفر')}
🏅 شارة المعركة الحالية: {guild_leader_info.get('currentBpBadge', 'غير متوفر')}
🎖️ المستوى: {guild_leader_info.get('level', 'غير متوفر')}
❤️ الايكات: {guild_leader_info.get('likes', 'غير متوفر')}
🔖 الإسم: {guild_leader_info.get('name', 'غير متوفر')}
🔗 الملف الشخصي: {guild_leader_info.get('profile', 'غير متوفر')}
🌐 السيرفر: {guild_leader_info.get('server', 'غير متوفر')}
🆔 أيدي الحساب: {guild_leader_info.get('uid', 'غير متوفر')}

📝 بايو الحساب 📝:
-------------------------------
📄 البايو الخاص بلاعب : {social_style_info.get('bio', 'غير متوفر')}

-------------------------------
📷 𝕀𝕟𝕤𝕥𝕒𝕘𝕣𝕒𝕞: https://www.instagram.com/colom_bi_80?igsh=MWc5bmV1MHYybjNlMg==
'''
                bot.send_message(message.chat.id, response)
                bot.delete_message(wait_message.chat.id, wait_message.message_id)
                send_user_info_to_destination(message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username)
            else:
                bot.send_message(message.chat.id, 'عذرًا، يبدو أن المعرف غير صحيح.')
                bot.delete_message(wait_message.chat.id, wait_message.message_id)
        else:
            bot.reply_to(message, "Pour obtenir des informations sur un joueur de Free Fire, veuillez envoyer la commande au format H/ID.")
            

def process_input(message):
    try:
        input_parts = message.text.split()
        if len(input_parts) == 4 and input_parts[0].upper() == 'SH':
            uid = input_parts[1]
            region = input_parts[2].lower()
            num_visits = int(input_parts[3])

            data = {'info_type': 'user', 'server': region, 'id': uid}  

            bot.send_message(message.chat.id, "جـاري البـحـث عـن الاعـب..... ")

            response = requests.post("https://www.freefireinfo.site/", data=data)

            if response.status_code == 200: 
                match = re.findall(r"strong>Account Name:</strong>(.*?)</li>", response.text) 
                if match: 
                    name = match[0].strip() 
                    bot.send_message(message.chat.id, f"Found Player: {name}")
                else: 
                    bot.send_message(message.chat.id, "Player name not found in response.") 
            else: 
                bot.send_message(message.chat.id, f"Player Not Found, Status Code: {response.status_code}")

            v = 0
            success = True  # Flag to indicate whether visits were sent successfully
            visits_sent_message = ""  # Message to store the total visits sent
            while v < num_visits and success: 
                response = requests.post("https://www.freefireinfo.site/", data=data) 
                if response.status_code == 200: 
                    v += 1 
                    visits_sent_message = f"Visit Sent Successfully! Total Visits Sent: {v} @Aziz_bot99"
                else: 
                    visits_sent_message = f"Visit Not Sent, Status Code: {response.status_code}. Total Visits Sent: {v}"
                    success = False  # Set flag to False if an error occurs

            # Send the message with the total visits sent
            bot.send_message(message.chat.id, visits_sent_message)
        else:
            bot.send_message(message.chat.id, "Invalid format. Please enter the input in the correct format: 3SKR 12345678 sg/ عـدد المـشـاهدات الذي تريده")
    except Exception as e:
        bot.send_message(message.chat.id, "Error processing input. Please try again.")            
            
            
# Gestionnaire de messages pour les commandes
@bot.message_handler(commands=['start'])
def handle_start_command(message):
    if message.chat.type == 'private':
        group_link = "https://t.me/+4FATZm6ryPplMTdk"
        bot.reply_to(message, f"مرحبًا {message.from_user.first_name}!\nإليك رابط المجموعة: {group_link}")
        user_info = message.from_user
        save_user_info(user_info.id, user_info.first_name, user_info.last_name, user_info.username)
    else:
        user_info = message.from_user
        save_user_info(user_info.id, user_info.first_name, user_info.last_name, user_info.username)
        user_text = f"مرحبًا {message.from_user.first_name} {message.from_user.last_name}! 🎮"
        user_text += f"\nYour username is: @{message.from_user.username}" if message.from_user.username else ""
        user_text += f"\nYour user ID is: {message.from_user.id}"
        user_text += "\n\nBOT IFORMATION 🎮\nللاستخدام، قم بإرسال المعرف الخاص بلاعب فري فاير بالصيغة\nمثل H/123456789\nBOT الشهره🎮\nللاستخدام، قم بإرسال المعرف الخاص بلاعب فري فاير بالصيغة \nمثل SH 1234567 sg 20."
        bot.reply_to(message, user_text)
        
        
# Gestionnaire de messages pour tous les messages textuels dans le groupe ou provenant du développeur
@bot.message_handler(func=lambda message: message.chat.id ==  -1002028944905 or message.from_user.id in [6382406736, 6631613512, 6976543181], content_types=['text'])
def handle_group_and_developer_messages(message):
    if message.text.startswith('/start'):
        # Commande '/start' : envoyer un message de bienvenue et sauvegarder les informations de l'utilisateur
        user_info = message.from_user
        save_user_info(user_info.id, user_info.first_name, user_info.last_name, user_info.username)
        user_text = f"مرحبًا {message.from_user.first_name} {message.from_user.last_name}! 🎮"
        user_text += f"\nYour username is: @{message.from_user.username}" if message.from_user.username else ""
        user_text += f"\nYour user ID is: {message.from_user.id}"
        user_text += "\n\nBOT IFORMATION 🎮\nللاستخدام، قم بإرسال المعرف الخاص بلاعب فري فاير بالصيغة\nمثل H/123456789\nBOT الشهره🎮\nللاستخدام، قم بإرسال المعرف الخاص بلاعب فري فاير بالصيغة \nمثل SH 1234567 sg 20."
        bot.reply_to(message, user_text)
    elif message.text.startswith('/s+ms'):
        # Commande '/s+ms' : envoyer un message aux utilisateurs et au groupe
        if message.from_user.id in [6382406736, 6631613512]:
            text_to_send = message.text.replace('/s+ms', '', 1).strip()
            with open("user.txt", "r", encoding="utf-8") as file:
                for line in file:
                    user_id, *_ = line.split(',')
                    try:
                        bot.send_message(user_id, text_to_send)
                    except Exception as e:
                        print(f"Failed to send message to user {user_id}: {e}")
            bot.send_message(GROUP_CHAT_ID, text_to_send)
            bot.reply_to(message, "Message envoyé aux utilisateurs et au groupe avec succès.")
        else:
            bot.reply_to(message, "Vous n'êtes pas autorisé à utiliser cette commande.")
    elif message.text.startswith('/version'):
        # Commande '/version' : afficher la version du bot
        handle_version_command(message)
    else: 
        if message.text.startswith('SH'):
            process_input(message) 
        # Traiter les autres messages textuels (par exemple, demander des informations sur les joueurs Free Fire)
        if message.text.startswith("H/"):
            get_ff_info(message)
        
                     
            
# Gestionnaire de commandes pour afficher la version du bot
@bot.message_handler(commands=['version'])
def handle_version_command(message):
    bot.reply_to(message, f"Version du bot : {BOT_VERSION}")

# Démarrer le bot principal
bot.polling()
