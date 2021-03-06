# mastrobot_example2.py
import datetime
import math
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

STATE = None
NIU = 1
OPCIO = 2
TEST = 3
ELECCIO = 4
ESCOLLIR = 5

# function to handle the /start command
def inici(update, context):
    first_name = update.message.chat.first_name
    update.message.reply_text(f"Hola {first_name}. Benvingut a la plataforma de la UAB per a realitzar qüestionaris.")
    demanar_niu(update, context)

def demanar_niu(update, context):
    global STATE
    STATE = NIU
    update.message.reply_text(
        f"A continuació introdueix el teu NIU per a tenir accés al menú principal.")

def obtenir_estadistiques():
    url = "https://tfgbd-7eb0.restdb.io/rest/estadistiques"
    headers = {
        'content-type': "application/json",
        'x-apikey': "a797522efb0f9291cdf8f52c3ba6e3e79b047",
        'cache-control': "no-cache"
    }
    coleccio_estadistiques = requests.request("GET", url, headers=headers)
    return coleccio_estadistiques


def accedir_niu(update, context):
    global STATE
    id_est = 0
    # Funcio que retorni objecte niu de estadistiques
    estadistiques = obtenir_estadistiques()
    print("has arribat aqui")
    identifiacio = ""
    global ultima_id
    fila_nius = len(estadistiques.json())
    count = 0
    niu_existent = False
    niu_introduit = int(update.message.text)
    while count < fila_nius:
        niu_bd = estadistiques.json()[count].get('niu')
        if niu_introduit == niu_bd:
            niu_existent = True
            identifiacio = str(estadistiques.json()[count].get('_id'))
            update.message.reply_text(f"S'ha trobat el NIU {niu_introduit} a la Base de Dades.")
            menu_principal = "Benvingut al menu principal: \n" \
                             "Opcions: \n" \
                             "1 -> Realitzar test \n"  \
                            "2 -> Escollir test \n"
            update.message.reply_text(menu_principal)
            STATE = OPCIO
        count = count + 1
    if niu_existent == False:
        missatge_niu_no_trobat = "No s'ha trobat el NIU, torna a introduir-lo"
        update.message.reply_text(missatge_niu_no_trobat)

    return identifiacio


def triar_opcio(update, context):
    global STATE
    try:
        eleccio = int(update.message.text)
        update.message.reply_text(f"La teva opció ha sigut {eleccio}.")
        if eleccio == 1:
            STATE = TEST
            update.message.reply_text(f"Estàs accedint a l'opció 'Realitzar Test'.")
        if eleccio == 2:
            STATE = ELECCIO
            update.message.reply_text(f"Escriu la contrasenya de professor per a poder accedir a l'opció 'Escollir Test'.")
    except:
        update.message.reply_text("Has introduït un valor incorrecte")

def contrasenya_escollir_test(update, context):
    global STATE
    contrasenya_correcta = False
    while (contrasenya_correcta == False):
        contrasenya = int(update.message.text)
        if contrasenya == 1234:
            correcta = "Contrasenya correcta"
            update.message.reply_text(correcta)
            missatge_resposta = "Selecciona el test que vols que els alumnes visualitzin \n" \
                                "1 -> Tema 1 \n" \
                                "2 -> Tema 2 \n" \
                                "3 -> Tema 3 \n"
            update.message.reply_text(missatge_resposta)
            contrasenya_correcta = True
            STATE = ESCOLLIR
    if contrasenya_correcta == False:
        incorrecta = "Contrasenya incorrecta, torna a introduir-la"
        update.message.reply_text(incorrecta)

def received_birth_month(update, context):
    global STATE

    try:
        today = datetime.date.today()
        month = int(update.message.text)

        if month > 12 or month < 1:
            raise ValueError("invalid value")

        context.user_data['birth_month'] = month
        update.message.reply_text(f"great! And now, the day...")
    except:
        update.message.reply_text(
            "it's funny but it doesn't seem to be correct...")

def received_birth_day(update, context):
    global STATE

    try:
        today = datetime.date.today()
        dd = int(update.message.text)
        yyyy = context.user_data['birth_year']
        mm = context.user_data['birth_month']
        birthday = datetime.date(year=yyyy, month=mm, day=dd)

        if today - birthday < datetime.timedelta(days=0):
            raise ValueError("invalid value")

        context.user_data['birthday'] = birthday
        STATE = None
        update.message.reply_text(f'ok, you born on {birthday}')

    except:
        update.message.reply_text(
            "it's funny but it doesn't seem to be correct...")

# function to handle the /help command
def help(update, context):
    update.message.reply_text('help command received')

# function to handle errors occured in the dispatcher
def error(update, context):
    update.message.reply_text('an error occured')

# function to handle normal text
def text(update, context):
    global STATE

    if STATE == NIU:
        return accedir_niu(update, context)

    if STATE == OPCIO:
        return triar_opcio(update, context)

    if STATE == TEST:
        return received_birth_month(update, context)

    if STATE == ELECCIO:
        return contrasenya_escollir_test(update, context)

    if STATE == ESCOLLIR:
        return received_birth_month(update, context)

# This function is called when the /biorhythm command is issued
def biorhythm(update, context):
    print("ok")
    user_biorhythm = calculate_biorhythm(
        context.user_data['birthday'])

    update.message.reply_text(f"Phisical: {user_biorhythm['phisical']}")
    update.message.reply_text(f"Emotional: {user_biorhythm['emotional']}")
    update.message.reply_text(f"Intellectual: {user_biorhythm['intellectual']}")

def calculate_biorhythm(birthdate):
    today = datetime.date.today()
    delta = today - birthdate
    days = delta.days

    phisical = math.sin(2*math.pi*(days/23))
    emotional = math.sin(2*math.pi*(days/28))
    intellectual = math.sin(2*math.pi*(days/33))

    biorhythm = {}
    biorhythm['phisical'] = int(phisical * 10000)/100
    biorhythm['emotional'] = int(emotional * 10000)/100
    biorhythm['intellectual'] = int(intellectual * 10000)/100

    biorhythm['phisical_critical_day'] = (phisical == 0)
    biorhythm['emotional_critical_day'] = (emotional == 0)
    biorhythm['intellectual_critical_day'] = (intellectual == 0)

    return biorhythm

def main():
    TOKEN = "1682062953:AAHBVabPLYS6MNNbdWONd5lGbkrh0ARDC3s"

    # create the updater, that will automatically create also a dispatcher and a queue to
    # make them dialoge
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # add handlers for start and help commands
    dispatcher.add_handler(CommandHandler("start", inici))
    dispatcher.add_handler(CommandHandler("help", help))
    # add an handler for our biorhythm command
    dispatcher.add_handler(CommandHandler("biorhythm", biorhythm))

    # add an handler for normal text (not commands)
    dispatcher.add_handler(MessageHandler(Filters.text, text))

    # add an handler for errors
    dispatcher.add_error_handler(error)

    # start your shiny new bot
    updater.start_polling()

    # run the bot until Ctrl-C
    updater.idle()


if __name__ == '__main__':
    main()