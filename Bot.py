import telebot
from datetime import datetime, timedelta

# Initialisation du bot avec le token d'accès
bot = telebot.TeleBot("6494867003:AAH0RxRvczkUk6hDV6bdZ1hwHYrFPOiw5UQ")

# Identifiant du développeur
developer_id = 6631613512  # Identifiant du développeur spécifié

# Fonction pour gérer la commande /start
@bot.message_handler(commands=['start'])
def start(message):
    # Vérifier si l'utilisateur est le développeur
    if message.from_user.id == developer_id:
        bot.reply_to(message, "Bienvenue! S'il vous plaît, entrez votre date de naissance au format JJ/MM/AAAA.")
    else:
        bot.reply_to(message, "Désolé, je ne suis configuré que pour répondre au développeur\n developer: @lion_souhail")

# Fonction pour gérer les messages contenant la date de naissance
@bot.message_handler(func=lambda message: True)
def age(message):
    # Vérifier si l'utilisateur est le développeur
    if message.from_user.id == developer_id:
        # Obtention de la date de naissance saisie par l'utilisateur
        dob_str = message.text
        try:
            # Convertir la chaîne en objet de date
            dob = datetime.strptime(dob_str, '%d/%m/%Y')

            # Calcul de la date de son prochain anniversaire
            today = datetime.today()
            next_birthday = datetime(today.year, dob.month, dob.day)
            if today > next_birthday:
                next_birthday = datetime(today.year + 1, dob.month, dob.day)

            # Calcul du jour de la semaine, la date et l'heure de l'anniversaire
            formatted_birthday = next_birthday.strftime("%A, %d %B %Y, %H:%M:%S")

            # Calcul de l'âge actuel
            age_now = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

            # Calcul de l'âge le jour de son prochain anniversaire
            age_next_birthday = next_birthday.year - dob.year

            # Calcul de la durée jusqu'à son prochain anniversaire
            time_until_birthday = next_birthday - today

            # Formater la date actuelle
            current_time = datetime.now()
            formatted_current_time = current_time.strftime("%A, %d %B %Y, %H:%M:%S")

            # Répondre à l'utilisateur avec les informations demandées
            response = "🎉 Il vous reste {} jours jusqu'à votre prochain anniversaire.\n".format(time_until_birthday.days)
            response += "🎂 Vous avez actuellement {} ans.\n".format(age_now)
            response += "🎁 Vous aurez {} ans le jour de votre prochain anniversaire.\n".format(age_next_birthday)
            response += "📅 Votre prochain anniversaire est prévu pour : {}\n".format(formatted_birthday)
            response += "⏰ La date et l'heure actuelles sont : {}".format(formatted_current_time)
            bot.reply_to(message, response)
        except ValueError:
            # Gérer les erreurs de format de date
            bot.reply_to(message, "❌ Format de date invalide. Veuillez saisir votre date de naissance au format JJ/MM/AAAA.")
    else:
        bot.reply_to(message, "Désolé, je ne suis configuré que pour répondre au développeur.\n developer: @lion_souhail")

# Lancer le bot
bot.polling()
