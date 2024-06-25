import telebot
from datetime import datetime
from telebot import types

# Remplacez 'YOUR_TOKEN_HERE' par votre token de bot Telegram
bot = telebot.TeleBot("6494867003:AAH0RxRvczkUk6hDV6bdZ1hwHYrFPOiw5UQ")

# Dictionnaire pour stocker la langue préférée des utilisateurs
user_languages = {}

# Dictionnaires de traductions
translations = {
    'start': {
        'fr': "Bonjour! Envoyez-moi votre date de naissance au format JJ-MM-AAAA.",
        'it': "Ciao! Inviami la tua data di nascita nel formato GG-MM-AAAA.",
        'en': "Hello! Send me your birth date in the format DD-MM-YYYY.",
        'es': "¡Hola! Envíame tu fecha de nacimiento en el formato DD-MM-AAAA.",
        'ar': "مرحبًا! أرسل لي تاريخ ميلادك بالصيغة يوم-شهر-سنة."
    },
    'invalid_date': {
        'fr': "Format de date invalide. Veuillez envoyer la date au format JJ-MM-AAAA.",
        'it': "Formato di data non valido. Si prega di inviare la data nel formato GG-MM-AAAA.",
        'en': "Invalid date format. Please send the date in the format DD-MM-YYYY.",
        'es': "Formato de fecha no válido. Envíe la fecha en el formato DD-MM-AAAA.",
        'ar': "تنسيق تاريخ غير صالح. يرجى إرسال التاريخ بصيغة يوم-شهر-سنة."
    },
    'response': {
        'fr': (
            "Votre date de naissance exacte est le {day:02d}-{month:02d}-{year}. "
            "Votre signe astrologique est {zodiac_sign}.\n{zodiac_traits}\n\n"
            "🎉 Il vous reste {days_until_birthday} jours jusqu'à votre prochain anniversaire.\n"
            "🎂 Vous avez actuellement {current_age_years} ans et {current_age_months} mois.\n"
            "🎁 Vous aurez {age_next_birthday} ans le jour de votre prochain anniversaire.\n"
            "📅 Votre prochain anniversaire est prévu pour : {next_birthday:%A, %d %B %Y, %H:%M:%S}\n"
            "⏰ La date et l'heure actuelles sont : {now:%A, %d %B %Y, %H:%M:%S}"
        ),
        'it': (
            "La tua data di nascita esatta è il {day:02d}-{month:02d}-{year}. "
            "Il tuo segno zodiacale è {zodiac_sign}.\n{zodiac_traits}\n\n"
            "🎉 Mancano {days_until_birthday} giorni al tuo prossimo compleanno.\n"
            "🎂 Attualmente hai {current_age_years} anni e {current_age_months} mesi.\n"
            "🎁 Avrai {age_next_birthday} anni al tuo prossimo compleanno.\n"
            "📅 Il tuo prossimo compleanno è previsto per: {next_birthday:%A, %d %B %Y, %H:%M:%S}\n"
            "⏰ La data e l'ora attuali sono: {now:%A, %d %B %Y, %H:%M:%S}"
        ),
        'en': (
            "Your exact birth date is {day:02d}-{month:02d}-{year}. "
            "Your zodiac sign is {zodiac_sign}.\n{zodiac_traits}\n\n"
            "🎉 There are {days_until_birthday} days left until your next birthday.\n"
            "🎂 You are currently {current_age_years} years and {current_age_months} months old.\n"
            "🎁 You will be {age_next_birthday} years old on your next birthday.\n"
            "📅 Your next birthday is scheduled for: {next_birthday:%A, %d %B %Y, %H:%M:%S}\n"
            "⏰ The current date and time are: {now:%A, %d %B %Y, %H:%M:%S}"
        ),
        'es': (
            "Tu fecha de nacimiento exacta es el {day:02d}-{month:02d}-{year}. "
            "Tu signo zodiacal es {zodiac_sign}.\n{zodiac_traits}\n\n"
            "🎉 Quedan {days_until_birthday} días hasta tu próximo cumpleaños.\n"
            "🎂 Actualmente tienes {current_age_years} años y {current_age_months} meses.\n"
            "🎁 Tendrás {age_next_birthday} años en tu próximo cumpleaños.\n"
            "📅 Tu próximo cumpleaños está previsto para: {next_birthday:%A, %d %B %Y, %H:%M:%S}\n"
            "⏰ La fecha y hora actuales son: {now:%A, %d %B %Y, %H:%M:%S}"
        ),
        'ar': (
            "تاريخ ميلادك الدقيق هو {day:02d}-{month:02d}-{year}. "
            "علامتك الفلكية هي {zodiac_sign}.\n{zodiac_traits}\n\n"
            "🎉 يتبقى {days_until_birthday} يومًا حتى عيد ميلادك القادم.\n"
            "🎂 عمرك الحالي {current_age_years} سنة و {current_age_months} أشهر.\n"
            "🎁 ستبلغ {age_next_birthday} سنة في عيد ميلادك القادم.\n"
            "📅 عيد ميلادك القادم مقرر في: {next_birthday:%A, %d %B %Y, %H:%M:%S}\n"
            "⏰ التاريخ والوقت الحاليان هما: {now:%A, %d %B %Y, %H:%M:%S}"
        )
    }
}

# Fonction pour déterminer le signe astrologique et ses détails
def get_zodiac_details(day, month):
    if (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "Capricorne", "Traits: Responsable, discipliné, maîtrise de soi, bon manager."
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "Verseau", "Traits: Progressiste, original, indépendant, humanitaire."
    elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
        return "Poissons", "Traits: Compatissant, artistique, intuitif, sage, musical."
    elif (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "Bélier", "Traits: Courageux, déterminé, confiant, enthousiaste, optimiste."
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "Taureau", "Traits: Fiable, patient, pratique, dévoué, responsable, stable."
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "Gémeaux", "Traits: Doux, affectueux, curieux, adaptable, capable d'apprendre rapidement."
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "Cancer", "Traits: Tenace, très imaginatif, loyal, émotif, sympathique, persuasif."
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "Lion", "Traits: Créatif, passionné, généreux, chaleureux, joyeux, humoristique."
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "Vierge", "Traits: Loyal, analytique, gentil, travailleur, pratique."
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "Balance", "Traits: Coopératif, diplomate, grâce, justice, sociable, charmant."
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "Scorpion", "Traits: Fidèle, ambitieux, passionné, intuitif, dynamique."
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "Sagittaire", "Traits: Aventureux, énergique, optimiste, ouvert d'esprit, généreux."
    else:
        return "Inconnu", "Traits: Mystérieux, unique, difficile à cerner."

# Fonction pour calculer les détails de l'anniversaire
def calculate_birthday_details(birth_date):
    now = datetime.now().date()  # Convertir maintenant en datetime.date
    next_birthday = birth_date.replace(year=now.year)
    if next_birthday < now:
        next_birthday = next_birthday.replace(year=now.year + 1)

    days_until_birthday = (next_birthday - now).days

    # Âge actuel en années et mois
    current_age_years = now.year - birth_date.year
    if now.month < birth_date.month or (now.month == birth_date.month and now.day < birth_date.day):
        current_age_years -= 1
    current_age_months = (now.year - birth_date.year) * 12 + now.month - birth_date.month
    if now.day < birth_date.day:
        current_age_months -= 1
    current_age_years = current_age_months // 12
    current_age_months = current_age_months % 12

    # Âge lors du prochain anniversaire
    age_next_birthday = current_age_years + 1

    return days_until_birthday, current_age_years, current_age_months, age_next_birthday, next_birthday, now

# Fonction pour extraire la langue du message
def get_language(message):
    chat_id = message.chat.id
    if chat_id in user_languages:
        return user_languages[chat_id]
    # Par défaut, retourne la langue française
    return 'fr'

# Fonction pour extraire et valider la date
def parse_date(text):
    try:
        # Analyser la date
        birth_date = datetime.strptime(text, "%d-%m-%Y").date()
        return birth_date
    except ValueError:
        return None

# Commande /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    language = get_language(message)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="🇫🇷 Français", callback_data="lang_fr"))
    markup.add(types.InlineKeyboardButton(text="🇮🇹 Italiano", callback_data="lang_it"))
    markup.add(types.InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en"))
    markup.add(types.InlineKeyboardButton(text="🇪🇸 Español", callback_data="lang_es"))
    markup.add(types.InlineKeyboardButton(text="🇦🇪 العربية", callback_data="lang_ar"))
    bot.send_message(message.chat.id, translations['start'][language], reply_markup=markup)

# Gestion des messages texte
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    language = get_language(message)
    text = message.text
    birth_date = parse_date(text)

    if birth_date:
        day = birth_date.day
        month = birth_date.month
        year = birth_date.year
        zodiac_sign, zodiac_traits = get_zodiac_details(day, month)

        days_until_birthday, current_age_years, current_age_months, age_next_birthday, next_birthday, now = calculate_birthday_details(birth_date)

        response = translations['response'][language].format(
            day=day,
            month=month,
            year=year,
            zodiac_sign=zodiac_sign,
            zodiac_traits=zodiac_traits,
            days_until_birthday=days_until_birthday,
            current_age_years=current_age_years,
            current_age_months=current_age_months,
            age_next_birthday=age_next_birthday,
            next_birthday=next_birthday,
            now=now
        )
        bot.reply_to(message, response)
    else:
        bot.reply_to(message, translations['invalid_date'][language])

# Gestion des boutons Inline
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    if call.data.startswith("lang_"):
        lang = call.data.split("_")[1]
        user_languages[chat_id] = lang
        bot.answer_callback_query(call.id, f"Langue définie sur {lang.upper()}")
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                              text=translations['start'][lang],
                              reply_markup=None)

# Démarrer le bot
bot.polling()
