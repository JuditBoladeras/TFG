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
                missatge_niu_trobat = "S'ha trobat el NIU " + niu_introduit +  " a la Base de Dades"
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

def menu_principal(usuari):
    global idchat
    # Funcio que retorni objecte niu de estadistiques
    response = obtenir_estadistiques()
    index = 0
    print(usuari)
    count = 0
    filasusuaris = len(response.json())
    while count < filasusuaris:
        if usuari == str(response.json()[count].get('_id')):
            if (response.json()[count].get('admin') == True):
                menu_principal = "Benvingut al menú principal \n" \
                                 "Opcions: \n" \
                                 "T -> Realitzar Test \n" \
                                 "E -> Escollir Test \n" \
                                 "P -> Visualitzar Puntuacions Globals \n"
            else:
                menu_principal = "Benvingut al menú principal \n" \
                                 "Opcions: \n" \
                                 "T -> Realitzar Test \n" \
                                 "P -> Visualitzar Puntuació \n"
            enviar_mensaje(idchat, menu_principal)

        count = count + 1


def triar_opcio(missatge, usuari):
    opcio_triada = ""
    opcio_escollida = False
    global ultima_id

    for i in missatge["result"]:

        # Llamar a la funcion "leer_mensaje()"
        idchat, nombre, missage_enviat, id_update = leer_mensaje(i)

        # Si la ID del mensaje es mayor que el ultimo, se guarda la ID + 1
        if id_update > (ultima_id - 1):
            ultima_id = id_update + 1

        # Funcio que retorni objecte niu de estadistiques
        response = obtenir_estadistiques()
        index = 0
        print(usuari)
        count = 0
        filasusuaris = len(response.json())
        while count < filasusuaris:
            if usuari == str(response.json()[count].get('_id')):
                if (response.json()[count].get('admin') == True):

                    #eleccio = "Has escollit la opció " + missage_enviat
                    #enviar_mensaje(idchat,eleccio)
                    if missage_enviat == "T" or missage_enviat =="t":
                        eleccio = "Estàs accedint a l'opció 'Realitzar Test'"
                        enviar_mensaje(idchat, eleccio)
                        test(usuari)
                        print("Sembla que funciona")
                        opcio_escollida = True

                    if missage_enviat == "E" or missage_enviat == "e":
                        eleccio = "Estàs accedint a l'opció 'Escollir Test'"
                        enviar_mensaje(idchat, eleccio)
                        contrasenya_escollir_test(usuari)
                        opcio_escollida = True

                    if missage_enviat == "P" or missage_enviat == "p":
                        eleccio = "Estàs accedint a l'opció 'Visualitzar Puntuacions Globals'"
                        enviar_mensaje(idchat, eleccio)
                        visualitzar_puntuacions_professor(usuari)
                        opcio_escollida = True
                else:
                    # eleccio = "Has escollit la opció " + missage_enviat
                    # enviar_mensaje(idchat,eleccio)
                    if missage_enviat == "T" or missage_enviat == "t":
                        eleccio = "Estàs accedint a l'opció 'Realitzar Test'"
                        enviar_mensaje(idchat, eleccio)
                        test(usuari)
                        print("Sembla que funciona")
                        opcio_escollida = True

                    if missage_enviat == "P" or missage_enviat == "p":
                        eleccio = "Estàs accedint a l'opció 'Visualitzar Puntuació'"
                        enviar_mensaje(idchat, eleccio)
                        visualitzar_puntuacions_alumne(usuari)
                        opcio_escollida = True

            count = count + 1

        """if opcio_escollida == False and mensajes_diccionario["result"] != []:
            eleccio = "No has escollit una opció correcta." + "\n" + "Torna a introduïr l'opció que vols realitzar."
            enviar_mensaje(idchat, eleccio)"""



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

def contrasenya_escollir_test(usuari):
    ultima_id = 0
    obviar = 0
    contrasenya_correcta = False
    missatge_resposta = "Escriu la contrasenya de professor per a poder accedir a aquesta opció."
    enviar_mensaje(idchat, missatge_resposta)
    while (contrasenya_correcta == False):
        mensajes_diccionario = update(ultima_id)
        for i in mensajes_diccionario["result"]:
            # Llamar a la funcion "leer_mensaje()"
            id, nombre, solucio, id_update = leer_mensaje(i)
            if obviar == 0:
                print("obviar")
            else:
                if solucio == "1234":
                    eleccio = "Contrasenya correcta"
                    enviar_mensaje(id, eleccio)
                    contrasenya_correcta = True
                    escollir_test(usuari)
                else:
                    eleccio = "Contrasenya incorrecta. Introduiex-la de nou."
                    enviar_mensaje(id, eleccio)

        obviar = obviar + 1
        if id_update > (ultima_id - 1):
            ultima_id = id_update + 1

def escollir_test(usuari):
    ultima_id = 0
    obviar = 0
    test_escollit = False
    missatge_resposta = "Selecciona el test que vols que els alumnes visualitzin \n" \
                        "1 -> Tema 1 \n" \
                        "2 -> Tema 2 \n" \
                        "3 -> Tema 3 \n"
    enviar_mensaje(idchat, missatge_resposta)
    while (test_escollit == False):
        mensajes_diccionario = update(ultima_id)
        for i in mensajes_diccionario["result"]:
            # Llamar a la funcion "leer_mensaje()"
            id, nombre, solucio, id_update = leer_mensaje(i)
            if obviar == 0:
                print("obviar")
            else:
                if solucio == "1" or solucio == "2" or solucio == "3":
                    missatge_resposta = "Has seleccionat el qüestionari del Tema " + solucio +\
                                        "\n" + "Aquest serà el qüestionari que podran realitzar els alumnes en l'opció 'Realitzar Test'."
                    enviar_mensaje(idchat, missatge_resposta)
                    url = "https://tfgbd-7eb0.restdb.io/rest/tema"+solucio
                    print(url)
                    headers = {
                        'content-type': "application/json",
                        'x-apikey': "a797522efb0f9291cdf8f52c3ba6e3e79b047",
                        'cache-control': "no-cache"
                    }
                    test = requests.request("GET", url, headers=headers)
                    print(test.json()[0].get('enunciat'))
                    test_escollit = True
                    filesorigen = len(test.json())
                    print(filesorigen)
                    i = 0

                    urlget = "https://tfgbd-7eb0.restdb.io/rest/test"

                    headersget = {
                        'content-type': "application/json",
                        'x-apikey': "a797522efb0f9291cdf8f52c3ba6e3e79b047",
                        'cache-control': "no-cache"
                    }

                    responseget = requests.request("GET", urlget, headers=headersget)
                    filesdesti = len(responseget.json())

                    if filesdesti > 0 :


                        while (i < filesdesti):

                            id = responseget.json()[i].get('_id')

                            url = "https://tfgbd-7eb0.restdb.io/rest/test/" + id

                            headers = {
                                'content-type': "application/json",
                                'x-apikey': "a797522efb0f9291cdf8f52c3ba6e3e79b047",
                                'cache-control': "no-cache"
                            }

                            resp = requests.request("DELETE", url, headers=headers)
                            i = i + 1

                    i = 0
                    while (i < filesorigen):

                        e = test.json()[i].get('enunciat')
                        resp1 = test.json()[i].get('r1')
                        resp2 = test.json()[i].get('r2')
                        resp3 = test.json()[i].get('r3')
                        resp4 = test.json()[i].get('r4')
                        val1 = test.json()[i].get('v1')
                        val2 = test.json()[i].get('v2')
                        val3 = test.json()[i].get('v3')
                        val4 = test.json()[i].get('v4')
                        #POST
                        url = "https://tfgbd-7eb0.restdb.io/rest/test"

                        payload = json.dumps({"enunciat": e, "r1": resp1, "r2": resp2, "r3": resp3, "r4": resp4, "v1": val1, "v2": val2, "v3": val3, "v4": val4})
                        headers = {
                            'content-type': "application/json",
                            'x-apikey': "a797522efb0f9291cdf8f52c3ba6e3e79b047",
                            'cache-control': "no-cache"
                        }

                        response = requests.request("POST", url, data=payload, headers=headers)
                        print(response.text)
                        i = i+1


        obviar = obviar + 1
        if id_update > (ultima_id - 1):
            ultima_id = id_update + 1
    menu_principal(usuari)


def test(usuari):
    ultima_id = 0
    print(usuari)
    url = "https://tfgbd-7eb0.restdb.io/rest/test"
    headers = {
        'content-type': "application/json",
        'x-apikey': "a797522efb0f9291cdf8f52c3ba6e3e79b047",
        'cache-control': "no-cache"
    }
    response = requests.request("GET", url, headers=headers)
    id = response.json()[index].get('_id')
    print(id)
    filas = len(response.json())
    print("El numero de filas es de: " + str(filas))

    # GET per treure el nombre de files que hi ha en el objecte
    respondre_test = 0
    vuelta = -1
    # mensajes_diccionario = update(ultima_id)
    while (vuelta != filas):

        lista = update(ultima_id)
        # lista = []
        if (vuelta + 1) != 5:
            enunciat = response.json()[vuelta + 1].get('enunciat')
            resposta1 = response.json()[vuelta + 1].get('r1')
            resposta2 = response.json()[vuelta + 1].get('r2')
            resposta3 = response.json()[vuelta + 1].get('r3')
            resposta4 = response.json()[vuelta + 1].get('r4')
            bloc_pregunta = enunciat + "\n\n" + "1. " + resposta1 + "\n\n" + "2. " + resposta2 + "\n\n" + "3. " + resposta3 + "\n\n" + "4. " + resposta4

        for i in lista["result"]:

            # Llamar a la funcion "leer_mensaje()"
            idchat, nombre, solucio, id_update = leer_mensaje(i)

            # vuelta = "Vuelta numero: " + vuelta
            if respondre_test == 0:
                print("no tenir en compte")
            else:
                if solucio == "1" or solucio == "2" or solucio == "3" or solucio == "4":
                    valor = "Has triat la resposta " + str(solucio)
                    enviar_mensaje(idchat, valor)
                    tupla = ("v", str(solucio))
                    puntuacio = "".join(tupla)
                    print(puntuacio)
                    puntuacio = response.json()[vuelta].get(puntuacio)
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
                        resposta_encert = "La teva resposta ha estat correcta."
                        enviar_mensaje(idchat, resposta_encert)
                    else:
                        actualitza_puntuacio(usuari, "errors", 1)
                        resposta_error = "La teva resposta ha estat incorrecta."
                        enviar_mensaje(idchat, resposta_error)

                    print(puntuacio)
                    print("V1 te: " + str(response.json()[vuelta].get("v1")))
                    print("V2 te: " + str(response.json()[vuelta].get("v2")))
                    print("V3 te: " + str(response.json()[vuelta].get("v3")))
                    print("V4 te: " + str(response.json()[vuelta].get("v4")))
                    resposta_punts = "Has obtingut " + str(puntuacio) + " punts."
                    enviar_mensaje(idchat, resposta_punts)

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
    menu_principal(usuari)


def actualitza_puntuacio(id_usuari, parametre_a_modificar,valor):
    url = "https://tfgbd-7eb0.restdb.io/rest/estadistiques"

    headers = {'content-type': "application/json",
                'x-apikey': "a797522efb0f9291cdf8f52c3ba6e3e79b047",
                'cache-control': "no-cache"}

    response = requests.request("GET", url, headers=headers)
    index = 0
    print(id_usuari)

    url1 = "https://tfgbd-7eb0.restdb.io/rest/estadistiques/" + id_usuari
    print(url1)
    variable_a_modificar = parametre_a_modificar

    count = 0
    index_desitjat = -1
    filasusuaris = len(response.json())
    while count < filasusuaris:
        if id == str(response.json()[count].get('_id')):
            index_desitjat = count
        count = count + 1

    valor_a_incrementar = valor + response.json()[index_desitjat].get(parametre_a_modificar)
    # payload2 = "{\"edat\":\"50\"}"
    part1 = "{\""
    part2 = str(parametre_a_modificar)
    part3 = "\":\""
    part4 = str(valor_a_incrementar)
    part5 = "\"}"

    payload = part1 + part2 + part3 + part4 + part5

    #payload = "".join(latupla)
    #payload = "{\"puntuacio\":\"100\"}"
    print(f'{payload}')
    response = requests.request("PUT", url1, data=payload, headers=headers)

def visualitzar_puntuacions_alumne(usuari):
    # Funcio que retorni objecte niu de estadistiques
    response = obtenir_estadistiques()
    index = 0
    print(usuari)
    count = 0
    filasusuaris = len(response.json())
    while count < filasusuaris:
        if usuari == str(response.json()[count].get('_id')):
            num_niu = str(response.json()[count].get("niu"))
            num_encerts = str(response.json()[count].get("encerts"))
            num_errors = str(response.json()[count].get("errors"))
            num_punts = str(response.json()[count].get("puntuacio"))
            estadistiques = "Els resultats obtinguts pel NIU " + num_niu +  " són els següents: " \
                            + "\n" + "Número d'encerts : " + num_encerts \
                            + "\n" + "Número d'errors : " + num_errors \
                            + "\n" + "Puntuació total : " + num_punts

            enviar_mensaje(idchat, estadistiques)
        count = count + 1
    menu_principal(usuari)


def visualitzar_puntuacions_professor(usuari):
    # Funcio que retorni objecte niu de estadistiques
    response = obtenir_estadistiques()
    index = 0
    print(usuari)
    count = 0
    filasusuaris = len(response.json())
    while count < filasusuaris:
        num_niu = str(response.json()[count].get("niu"))
        num_encerts = str(response.json()[count].get("encerts"))
        num_errors = str(response.json()[count].get("errors"))
        num_punts = str(response.json()[count].get("puntuacio"))
        estadistiques = "Els resultats obtinguts pel NIU " + num_niu +  " són els següents: " \
                        + "\n" + "Número d'encerts : " + num_encerts \
                        + "\n" + "Número d'errors : " + num_errors \
                        + "\n" + "Puntuació total : " + num_punts

        enviar_mensaje(idchat, estadistiques)
        count = count + 1
    menu_principal(usuari)

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
    #global niu
    mensajes_diccionario = update(ultima_id)
    # hola(mensajes_diccionario)

    if id == "" and benvingut == True:
        id = demanar_niu(mensajes_diccionario)

    if id != "" and benvingut == True:
        # Acces a fer test per que ja s'ha donat la benvinguda i s'ha guardat el id corresponent al NIU
        menu_principal(id)

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
        #triar = True

    #if triar == True and opcio == "0":
        #test(id)

    mensajes_diccionario = []


while (True):
    mensajes_diccionario = update(ultima_id)
    for i in mensajes_diccionario["result"]:
        # Llamar a la funcion "leer_mensaje()"
        idchat, nombre, solucio, id_update = leer_mensaje(i)
        if id == "":
            identificacio()
        else:
            opcions()