# Importar librerias
import json
import requests

# Variables para el Token y la URL del chatbot
TOKEN = "1682062953:AAHBVabPLYS6MNNbdWONd5lGbkrh0ARDC3s"  # Cambialo por tu token
URL = "https://api.telegram.org/bot" + TOKEN + "/"

# Variable para almacenar la ID del ultimo mensaje procesado


def update(offset):
    # Llamar al metodo getUpdates del bot, utilizando un offset
    respuesta = requests.get(URL + "getUpdates" + "?offset=" + str(offset))
    # Telegram devolvera todos los mensajes con id IGUAL o SUPERIOR al offset

    # Decodificar la respuesta recibida a formato UTF8
    mensajes_js = respuesta.content.decode("utf8")

    # Convertir el string de JSON a un diccionario de Python
    mensajes_diccionario = json.loads(mensajes_js)

    # Devolver este diccionario
    return mensajes_diccionario


def leer_mensaje(mensaje):
    # Extraer el texto, nombre de la persona e id del último mensaje recibido
    texto = mensaje["message"]["text"]
    persona = mensaje["message"]["from"]["first_name"]
    id_chat = mensaje["message"]["chat"]["id"]

    # Calcular el identificador unico del mensaje para calcular el offset
    id_update = mensaje["update_id"]

    # Devolver las dos id, el nombre y el texto del mensaje
    return id_chat, persona, texto, id_update


def enviar_mensaje(idchat, texto):
    # Llamar el metodo sendMessage del bot, passando el texto y la id del chat
    requests.get(URL + "sendMessage?text=" + texto + "&chat_id=" + str(idchat))

def obtenir_estadistiques():
    url = "https://tfgbd-7eb0.restdb.io/rest/estadistiques"
    headers = {
        'content-type': "application/json",
        'x-apikey': "a797522efb0f9291cdf8f52c3ba6e3e79b047",
        'cache-control': "no-cache"
    }
    coleccio_estadistiques = requests.request("GET", url, headers=headers)
    return coleccio_estadistiques

def demanar_niu(missatge):
    id_est = 0
    #Funcio que retorni objecte niu de estadistiques
    estadistiques = obtenir_estadistiques()
    print("has arribat aqui")

    identifiacio = ""
    global ultima_id
    for i in missatge["result"]:

        # Llamar a la funcion "leer_mensaje()"
        idchat, nombre, niu_introduit, id_update = leer_mensaje(i)

        # Si la ID del mensaje es mayor que el ultimo, se guarda la ID + 1
        if id_update > (ultima_id - 1):
            ultima_id = id_update + 1

        # Generar una respuesta a partir de la informacion del mensaje
        fila_nius = len(estadistiques.json())
        count = 0
        niu_existent = False
        while count < fila_nius:
            niu_bd = estadistiques.json()[count].get('niu')
            if niu_introduit == str(niu_bd):
                niu_existent = True
                missatge_niu_trobat = "S'ha trobat el NIU: " + niu_introduit
                identifiacio = str(estadistiques.json()[count].get('_id'))
                enviar_mensaje(idchat, missatge_niu_trobat)
            count = count + 1
        if niu_existent == False:
            missatge_niu_no_trobat = "No s'ha trobat el NIU, torna a introduir-lo"
            enviar_mensaje(idchat, missatge_niu_no_trobat)

    return identifiacio



ultima_id = 0
benvingut = False
id = ""
opcio = ""
triar = False
mensajes_diccionario = []

def benvinguda(missatge):

    global ultima_id
    for i in missatge["result"]:

        # Llamar a la funcion "leer_mensaje()"
        idchat, nombre, texto, id_update = leer_mensaje(i)

        # Si la ID del mensaje es mayor que el ultimo, se guarda la ID + 1
        if id_update > (ultima_id - 1):
            ultima_id = id_update + 1

        # Generar una respuesta a partir de la informacion del mensaje
        text_de_benvingutda_generic = "Hola " + nombre + "!" + " Benvingut a la plataforma de la UAB per a realitzar qüestionaris."
        text_instruccions = " A continuació introdueix el teu NIU per a tenir accés al menú principal. "
        # Enviar la respuesta
        enviar_mensaje(idchat, text_de_benvingutda_generic)
        enviar_mensaje(idchat, text_instruccions)

def menu_principal(missatge):
    global ultima_id
    for i in missatge["result"]:

        # Llamar a la funcion "leer_mensaje()"
        idchat, nombre, texto, id_update = leer_mensaje(i)

        # Si la ID del mensaje es mayor que el ultimo, se guarda la ID + 1
        if id_update > (ultima_id - 1):
            ultima_id = id_update + 1

        menu_principal = "Benvingut al menu principal: \n" \
                         "Opcions: \n" \
                         "0 -> Realitzar test \n"
        enviar_mensaje(idchat, menu_principal)

def triar_opcio(missatge, usuari):
    opcio_triada = ""
    global ultima_id
    for i in missatge["result"]:

        # Llamar a la funcion "leer_mensaje()"
        idchat, nombre, missage_enviat, id_update = leer_mensaje(i)

        # Si la ID del mensaje es mayor que el ultimo, se guarda la ID + 1
        if id_update > (ultima_id - 1):
            ultima_id = id_update + 1

        eleccio = "La teva opcio ha sigut " + missage_enviat
        enviar_mensaje(idchat,eleccio)
        if missage_enviat == "0":
            opcio_triada = missage_enviat
            #test(usuari)
            print("Sembla que funciona")
    return opcio_triada

def obtenir_test():
    url_tema1 = "https://tfgbd-7eb0.restdb.io/rest/tema1"
    headers = {
        'content-type': "application/json",
        'x-apikey': "a797522efb0f9291cdf8f52c3ba6e3e79b047",
        'cache-control': "no-cache"
    }
    coleccio_test = requests.request("GET", url_tema1, headers=headers)
    return coleccio_test

index = 0
def test(missatge, usuari):
    test = obtenir_test()

    global ultima_id


    id_t1 = test.json()[index].get('_id')
    print(id_t1)
    filas = len(test.json())
    print("El numero de filas es de: " + str(filas))

    # GET per treure el nombre de files que hi ha en el objecte
    respondre_test = 0
    vuelta = -1
    # mensajes_diccionario = update(ultima_id)
    while (vuelta != filas):

        if (vuelta + 1) != 5:
            enunciat = test.json()[vuelta + 1].get('enunciat')
            resposta1 = test.json()[vuelta + 1].get('r1')
            resposta2 = test.json()[vuelta + 1].get('r2')
            resposta3 = test.json()[vuelta + 1].get('r3')
            resposta4 = test.json()[vuelta + 1].get('r4')
            bloc_pregunta = enunciat + "\n\n" + "1. " + resposta1 + "\n\n" + "2. " + resposta2 + "\n\n" + "3. " + resposta3 + "\n\n" + "4. " + resposta4

        for i in missatge["result"]:
            # Llamar a la funcion "leer_mensaje()"
            idchat, nombre, resposta_introduida, id_update = leer_mensaje(i)

            # Si la ID del mensaje es mayor que el ultimo, se guarda la ID + 1
            if id_update > (ultima_id - 1):
                ultima_id = id_update + 1


            # vuelta = "Vuelta numero: " + vuelta
            if respondre_test == 0:
                print("no tenir en compte")
            else:
                if resposta_introduida == "1" or resposta_introduida == "2" or resposta_introduida == "3" or resposta_introduida == "4":
                    valor = "Has triat el valor: " + str(resposta_introduida)
                    enviar_mensaje(idchat, valor)
                    tupla = ("v", str(resposta_introduida))
                    puntuacio = "".join(tupla)
                    print(puntuacio)
                    """"
                    puntuacio = test.json()[vuelta].get(puntuacio)
                    urlget = "https://tfgbd-7eb0.restdb.io/rest/estadistiques"
                    urlput = "https://tfgbd-7eb0.restdb.io/rest/estadistiques/" + usuari
                    headersget = {
                        'content-type': "application/json",
                        'x-apikey': "a797522efb0f9291cdf8f52c3ba6e3e79b047",
                        'cache-control': "no-cache"
                    }
                    headersput = {
                        'content-type': "application/json",
                        'x-apikey': "a797522efb0f9291cdf8f52c3ba6e3e79b047",
                        'cache-control': "no-cache"
                    }
                    response1 = requests.request("GET", urlget, headers=headersget)
                    filasusuaris = len(response1.json())
                    count = 0
                    index_desitjat = -1
                    while count < filasusuaris:
                        if usuari == str(response1.json()[count].get('_id')):
                            index_desitjat = count
                        count = count + 1
                    if puntuacio == 100:
                        actualitza_puntuacio(usuari, "puntuacio", 100)
                        actualitza_puntuacio(usuari, "encerts", 1)

                    else:
                        actualitza_puntuacio(usuari, "errors", 1)
                    """
                    print(puntuacio)
                    print("V1 te: " + str(test.json()[vuelta].get("v1")))
                    print("V2 te: " + str(test.json()[vuelta].get("v2")))
                    print("V3 te: " + str(test.json()[vuelta].get("v3")))
                    print("V4 te: " + str(test.json()[vuelta].get("v4")))

                else:
                    resposta_error = "Has introduit un valor no valid"
                    enviar_mensaje(idchat, resposta_error)


            # enviar_mensaje(idchat, vuelta)
            if (vuelta + 1) != 5:
                enviar_mensaje(idchat, bloc_pregunta)

            vuelta = vuelta + 1
            if id_update > (ultima_id - 1):
                ultima_id = id_update + 1
        respondre_test = respondre_test + 1


def hola(missatge):

    global ultima_id
    for i in missatge["result"]:

        # Llamar a la funcion "leer_mensaje()"
        idchat, nombre, texto, id_update = leer_mensaje(i)

        # Si la ID del mensaje es mayor que el ultimo, se guarda la ID + 1
        if id_update > (ultima_id - 1):
            ultima_id = id_update + 1

        # Generar una respuesta a partir de la informacion del mensaje
        if "Hola" in texto:
            texto_respuesta = "Hola, " + nombre + "!"
        elif "Adios" in texto:
            texto_respuesta = "Hasta pronto!"
        else:
            texto_respuesta = "Has escrito: \"" + texto + "\""

        # Enviar la respuesta
        enviar_mensaje(idchat, texto_respuesta)
menu_mostrat = False
def identificacio():
    global benvingut
    global id
    mensajes_diccionario = update(ultima_id)
    # hola(mensajes_diccionario)

    if id == "" and benvingut == True:
        id = demanar_niu(mensajes_diccionario)

    if id != "" and benvingut == True:
        # Acces a fer test per que ja s'ha donat la benvinguda i s'ha guardat el id corresponent al NIU
            menu_principal(mensajes_diccionario)

    if benvingut == False and mensajes_diccionario["result"] != []:
        print(mensajes_diccionario["result"])
        benvinguda(mensajes_diccionario)
        benvingut = True

    mensajes_diccionario = []

def opcions():
    global triar
    global opcio
    global id

    mensajes_diccionario = update(ultima_id)

    if triar == False and mensajes_diccionario["result"] != []:
        opcio = triar_opcio(mensajes_diccionario, id)
        triar = True

    if triar == True and opcio == "0":
        test(mensajes_diccionario, id)

    mensajes_diccionario = []


while (True):
    if id == "":
        identificacio()
    else:
        opcions()