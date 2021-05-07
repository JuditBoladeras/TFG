"""
    Ejemplo 3 - Este tercer programa utiliza un offset para controlar
            los mensajes se han contestado y los que no.

    Escrito por Transductor
    www.robologs.net
"""

# Importar librerias
import json
import requests
import time

# Variables para el Token y la URL del chatbot
TOKEN = "1682062953:AAHBVabPLYS6MNNbdWONd5lGbkrh0ARDC3s"  # Cambialo por tu token
URL = "https://api.telegram.org/bot" + TOKEN + "/"


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


def enviar_mensaje(idchat, bloc_pregunta):
    # Llamar el metodo sendMessage del bot, passando el texto y la id del chat
    requests.get(URL + "sendMessage?text=" + bloc_pregunta + "&chat_id=" + str(idchat))
    #requests.get(URL + "sendMessage?text=" + instruccions + "&chat_id=" + str(idchat))
    # requests.get(URL + "sendMessage?text=" + resposta2 + "&chat_id=" + str(idchat))
    # requests.get(URL + "sendMessage?text=" + resposta3 + "&chat_id=" + str(idchat))
    # requests.get(URL + "sendMessage?text=" + resposta4 + "&chat_id=" + str(idchat))


def mostrar_coleccion():
    url = "https://tfgbd-7eb0.restdb.io/rest/prova"

    headers = {
        'content-type': "application/json",
        'x-apikey': "a797522efb0f9291cdf8f52c3ba6e3e79b047",
        'cache-control': "no-cache"
    }

    response = requests.request("GET", url, headers=headers)

    # print(response.json()[1].get('usuari'))
    # print(len(response.json()))
    # print(response.request)
    return response


def añadir_fila():
    user = input("Introdueix el nom del usuari:\n")

    print(f'You entered {user}')

    age = input("Introdueix l'edat del usuari:\n")

    print(f'You entered {age}')

    url = "https://tfgbd-7eb0.restdb.io/rest/prova"

    payload = json.dumps({"usuari": user, "edat": age})
    headers = {
        'content-type': "application/json",
        'x-apikey': "a797522efb0f9291cdf8f52c3ba6e3e79b047",
        'cache-control': "no-cache"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)


def modificar_edat():
    url = "https://tfgbd-7eb0.restdb.io/rest/prova"

    headers = {
        'content-type': "application/json",
        'x-apikey': "a797522efb0f9291cdf8f52c3ba6e3e79b047",
        'cache-control': "no-cache"
    }

    response = requests.request("GET", url, headers=headers)
    index = 1
    id = response.json()[index].get('_id')
    print(id)

    url1 = "https://tfgbd-7eb0.restdb.io/rest/prova/" + id
    print(url1)
    age = input("Introdueix l'edat del usuari:\n")

    print(f'You entered {age}')
    payload = "{\"edat\":\"50\"}"

    response = requests.request("PUT", url1, data=payload, headers=headers)

    # print(response.text)


def modificar_edat2():
    url = "https://tfgbd-7eb0.restdb.io/rest/prova"

    headers = {
        'content-type': "application/json",
        'x-apikey': "a797522efb0f9291cdf8f52c3ba6e3e79b047",
        'cache-control': "no-cache"
    }

    response = requests.request("GET", url, headers=headers)
    index = 0
    id = response.json()[index].get('_id')
    print(id)

    url1 = "https://tfgbd-7eb0.restdb.io/rest/prova/" + id
    print(url1)
    variable_a_modificar = input("Introdueix variable a modificar:\n")
    age = input("Introdueix valor:\n")

    print(f'You entered {age}')
    # payload2 = "{\"edat\":\"50\"}"
    part1 = "{\""
    part2 = variable_a_modificar
    part3 = "\":\""
    part4 = age
    part5 = "\"}"

    latupla = (part1, part2, part3, part4, part5)

    payload = "".join(latupla)

    print(f'{payload}')
    response = requests.request("PUT", url1, data=payload, headers=headers)
    # response = requests.put(url1, )

    # print(response.text)

def actualitza_puntuacio(id, parametre_a_modificar,valor):
    url = "https://tfgbd-7eb0.restdb.io/rest/estadistiques"

    headers = {'content-type': "application/json",
                'x-apikey': "a797522efb0f9291cdf8f52c3ba6e3e79b047",
                'cache-control': "no-cache"}

    response = requests.request("GET", url, headers=headers)
    index = 0
    print(id)

    url1 = "https://tfgbd-7eb0.restdb.io/rest/estadistiques/" + id
    print(url1)
    variable_a_modificar = parametre_a_modificar

    count = 0
    index_desitjat = -1
    filasusuaris = len(response.json())
    while count < filasusuaris:
        if usuari == str(response.json()[count].get('_id')):
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

    #GET per treure el nombre de files que hi ha en el objecte
    respondre_test = 0
    vuelta = -1
    #mensajes_diccionario = update(ultima_id)
    while (vuelta != filas):

        lista = update(ultima_id)
        #lista = []
        if (vuelta + 1) !=5:
            enunciat = response.json()[vuelta + 1].get('enunciat')
            resposta1 = response.json()[vuelta + 1].get('r1')
            resposta2 = response.json()[vuelta + 1].get('r2')
            resposta3 = response.json()[vuelta + 1].get('r3')
            resposta4 = response.json()[vuelta + 1].get('r4')
            bloc_pregunta = enunciat + "\n\n" + "1. " + resposta1 + "\n\n" + "2. " + resposta2 + "\n\n" + "3. " + resposta3 + "\n\n" + "4. " + resposta4

        for i in lista["result"]:

            # Llamar a la funcion "leer_mensaje()"
            idchat, nombre, solucio, id_update = leer_mensaje(i)

            #vuelta = "Vuelta numero: " + vuelta
            if respondre_test == 0:
                print("no tenir en compte")
            else:
                if solucio == "1" or solucio == "2" or solucio == "3" or solucio == "4":
                    valor = "Has triat el valor: " + str(solucio)
                    enviar_mensaje(idchat, valor)
                    tupla = ("v",str(solucio))
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
                        actualitza_puntuacio(usuari,"puntuacio",100)
                        actualitza_puntuacio(usuari,"encerts", 1)

                    else:
                        actualitza_puntuacio(usuari, "errors", 1)

                    print(puntuacio)
                    print("V1 te: " + str(response.json()[vuelta].get("v1")))
                    print("V2 te: " + str(response.json()[vuelta].get("v2")))
                    print("V3 te: " + str(response.json()[vuelta].get("v3")))
                    print("V4 te: " + str(response.json()[vuelta].get("v4")))

                else:
                    resposta_error = "Has introduit un valor no valid"
                    enviar_mensaje(idchat,resposta_error)

            #enviar_mensaje(idchat, vuelta)
            if (vuelta + 1) != 5:
                enviar_mensaje(idchat, bloc_pregunta)

            vuelta = vuelta + 1
            if id_update > (ultima_id - 1):
                ultima_id = id_update + 1
        respondre_test = respondre_test + 1

    """"
    prueba = "Has entrado en la funcion test "
    vueltas = 1
    ult_id = 0
    #enviar_mensaje(idchat, prueba)

    #i = i + 1
    fin_test = 0
    while (fin_test != 1):
        dic = update(ult_id)

        for k in dic["result"]:

            print(k)

            id, nom, sol, id_upd = leer_mensaje(k)
            mensaje = "Dentro del bucle, vuelta nº " + str(vueltas) + " Has escrito " + sol
            vueltas = vueltas + 1
            enviar_mensaje(id, mensaje)

            if id_upd > (ult_id - 1):
                ult_id = id_upd + 1

            if vueltas == 5:
                fin_test = 1
    """

def escollir_test():
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

                            """"
                            #PUT
                            id = response.json()[i].get('_id')
                            url = "https://tfgbd-7eb0.restdb.io/rest/test/"+id
                            e = test.json()[i].get('enunciat')
                            resp1 = test.json()[i].get('r1')
                            resp2 = test.json()[i].get('r2')
                            resp3 = test.json()[i].get('r3')
                            resp4 = test.json()[i].get('r4')
                            val1 = test.json()[i].get('v1')
                            val2 = test.json()[i].get('v2')
                            val3 = test.json()[i].get('v3')
                            val4 = test.json()[i].get('v4')

                            en1 = "{\"enunciat\":\""
                            en2 = str(e)
                            en3 = "\"}"
                            payload_enunciat = en1 + en2 + en3

                            re1_1 = "{\"r1\":\""
                            re1_2 = str(resp1)
                            re1_3 = "\"}"
                            payload_resposta1 = re1_1 + re1_2 + re1_3

                            re2_1 = "{\"r2\":\""
                            re2_2 = str(resp2)
                            re2_3 = "\"}"
                            payload_resposta2 = re2_1 + re2_2 + re2_3

                            re3_1 = "{\"r3\":\""
                            re3_2 = str(resp3)
                            re3_3 = "\"}"
                            payload_resposta3 = re3_1 + re3_2 + re3_3

                            re4_1 = "{\"r4\":\""
                            re4_2 = str(resp4)
                            re4_3 = "\"}"
                            payload_resposta4 = re4_1 + re4_2 + re4_3

                            va1_1 = "{\"v1\":\""
                            va1_2 = str(val1)
                            va1_3 = "\"}"
                            payload_valor1 = va1_1 + va1_2 + va1_3

                            va2_1 = "{\"v2\":\""
                            va2_2 = str(val2)
                            va2_3 = "\"}"
                            payload_valor2 = va2_1 + va2_2 + va2_3

                            va3_1 = "{\"v3\":\""
                            va3_2 = str(val3)
                            va3_3 = "\"}"
                            payload_valor3 = va3_1 + va3_2 + va3_3

                            va4_1 = "{\"v4\":\""
                            va4_2 = str(val4)
                            va4_3 = "\"}"
                            payload_valor4 = va4_1 + va4_2 + va4_3


                            headers = {
                                'content-type': "application/json",
                                'x-apikey': "a797522efb0f9291cdf8f52c3ba6e3e79b047",
                                'cache-control': "no-cache"
                            }

                            tst = requests.request("PUT", url, data=payload_enunciat, headers=headers)
                            tst = requests.request("PUT", url, data=payload_resposta1, headers=headers)
                            tst = requests.request("PUT", url, data=payload_resposta2, headers=headers)
                            tst = requests.request("PUT", url, data=payload_resposta3, headers=headers)
                            tst = requests.request("PUT", url, data=payload_resposta4, headers=headers)
                            tst = requests.request("PUT", url, data=payload_valor1, headers=headers)
                            tst = requests.request("PUT", url, data=payload_valor2, headers=headers)
                            tst = requests.request("PUT", url, data=payload_valor3, headers=headers)
                            tst = requests.request("PUT", url, data=payload_valor4, headers=headers)

                            print(tst.text)
                            i = i+1 """
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

def contrasenya_escollir_test():
    ultima_id = 0
    obviar = 0
    contrasenya_correcta = False
    missatge_resposta = "Escriu la contrasenya de professor per a poder accedir a aquesta opció"
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
                    escollir_test()

        obviar = obviar + 1
        if id_update > (ultima_id - 1):
            ultima_id = id_update + 1

def triar_opcio(solucio, usuari):
    eleccio = "La teva opcio ha sigut " + solucio
    enviar_mensaje(idchat,eleccio)
    if solucio == "T":
        test(usuari)
    if solucio == "E":
        contrasenya_escollir_test()



def menu_principal():
    menu_principal = "Benvingut al menu principal: \n" \
                     "Opcions: \n" \
                     "T -> Realitzar test \n"  \
                    "E -> Escollir test \n"
    enviar_mensaje(idchat, menu_principal)

def introduir_niu():
    ultima_id = 0
    obviar = 0
    intro_niu = "Introdueix el teu NIU \n"

    url = "https://tfgbd-7eb0.restdb.io/rest/estadistiques"
    headers = {
        'content-type': "application/json",
        'x-apikey': "a797522efb0f9291cdf8f52c3ba6e3e79b047",
        'cache-control': "no-cache"
    }
    usuaris_registrats = requests.request("GET", url, headers=headers)

    filas = len(usuaris_registrats.json())
    niu_existent = False
    niu = ""
    while (niu_existent == False):
        mensajes_diccionario = update(ultima_id)

        for i in mensajes_diccionario["result"]:


            # Llamar a la funcion "leer_mensaje()"
            id, nombre, solucio, id_update = leer_mensaje(i)


            if obviar == 0:
                print("obviar")
            else:
                enviar_mensaje(idchat, intro_niu)
                count = 0
                while count < filas:
                    if solucio == str(usuaris_registrats.json()[count].get('niu')):
                        niu_existent = True
                        trobat = "S'ha trobat el NIU: " + solucio
                        niu = str(usuaris_registrats.json()[count].get('_id'))
                        enviar_mensaje(idchat,trobat)
                    count = count + 1
        obviar = obviar + 1
        if id_update > (ultima_id - 1):
            ultima_id = id_update + 1
    return niu

# Variable para almacenar la ID del ultimo mensaje procesado
ultima_id = 0
index = 0

usuari = ""
while (True):

    mensajes_diccionario = update(ultima_id)

    for i in mensajes_diccionario["result"]:

        # Llamar a la funcion "leer_mensaje()"
        idchat, nombre, solucio, id_update = leer_mensaje(i)


        if ultima_id == 0:
            usuari = introduir_niu()
        else:
            menu_principal()
            triar_opcio(solucio, usuari)




        if id_update > (ultima_id - 1):
            ultima_id = id_update + 1











        #variable_a_modificar = "Introdueix variable a modificar:\n"
        #age = "Introdueix valor:\n"

        # edat = modificar_edat2()
        # modificar_edat()
        # modificar_edat2()
        # resposta = mostrar_coleccion()
        # print(resposta.json())
        # añadir_fila()
        # print(resposta)
        # print(resposta.text)
        # modificar_edat2()
        # Si la ID del mensaje es mayor que el ultimo, se guarda la ID + 1









        """
        url = "https://tfgbd-7eb0.restdb.io/rest/prova"
        url_tema1 = "https://tfgbd-7eb0.restdb.io/rest/tema1"
        url_estadistiques = "https://tfgbd-7eb0.restdb.io/rest/estadistiques"
        headers = {
            'content-type': "application/json",
            'x-apikey': "a797522efb0f9291cdf8f52c3ba6e3e79b047",
            'cache-control': "no-cache"
        }
        index_prova = 0
        index_est = 0
        response = requests.request("GET", url_estadistiques, headers=headers)
        id_est = response.json()[index_est].get('_id')
        print(id_est)
        response = requests.request("GET", url, headers=headers)
        id = response.json()[index_prova].get('_id')
        print(id)
        response = requests.request("GET", url_tema1, headers=headers)
        id_t1 = response.json()[index].get('_id')
        print(id_t1)

        url_est = "https://tfgbd-7eb0.restdb.io/rest/estadistiques" + id_est
        url1 = "https://tfgbd-7eb0.restdb.io/rest/prova/" + id
        url_t1 = "https://tfgbd-7eb0.restdb.io/rest/tema1/" + id_t1

        print(url_est)
        print(url1)
        print(url_t1)

        pregunta = response.json()[index].get('enunciat')
        resposta1 = response.json()[index].get('r1')
        resposta2 = response.json()[index].get('r2')
        resposta3 = response.json()[index].get('r3')
        resposta4 = response.json()[index].get('r4')

        if len(id_t1):
            bloc_pregunta = pregunta + "\n\n" + "1. " + resposta1 + "\n\n" + "2. " + resposta2 + "\n\n" + "3. " + resposta3 + "\n\n" + "4. " + resposta4
            instruccions = "Introdueix un número entre el 1 i el 4 per indicar la teva resposta."
            variable1 = response.json()[index].get('v1')
            variable2 = response.json()[index].get('v2')
            variable3 = response.json()[index].get('v3')
            variable4 = response.json()[index].get('v4')
            index = index + 1
            print(index)
            # Generar una respuesta a partir de la informacion del mensaje
            #if "1" or "2" or "3" or "4" in solucio:
            # Enviar la respuesta
            print(f'You entered {solucio}')
            print(f'v1 {variable1}')
            print(f'v2 {variable2}')
            print(f'v3 {variable3}')
            print(f'v4 {variable4}')

            if "1" in solucio:
                part1 = "{\"edat"
                part2 = "\":\""
                part3 = str(variable1)
                part4 = "\"}"
                # part1 = "{\"edat"
                # part2 = variable_a_modificar
                # part3 = "\":\""
                # part4 = solucio
                # part5 = "\"}"
            if "2" in solucio:
                part1 = "{\"edat"
                part2 = "\":\""
                part3 = str(variable2)
                part4 = "\"}"
            if "3" in solucio:
                part1 = "{\"edat"
                part2 = "\":\""
                part3 = str(variable3)
                part4 = "\"}"
            if "4" in solucio:
                part1 = "{\"edat"
                part2 = "\":\""
                part3 = str(variable4)
                part4 = "\"}"

            punts = (part1, part2, part3, part4)
            payload = "".join(punts)
            print(f'{payload}')
            response = requests.request("PUT", url1, data=payload, headers=headers)


            elif "Hola" in solucio:
                bloc_pregunta = "Hola, " + nombre + "!"
            elif "Adios" in solucio:
                bloc_pregunta = "Hasta pronto!
        else:
            bloc_pregunta =  "Has finalitzat el test"
            instruccions = "Estadístiques:"

        """


    # Vaciar el diccionario
    mensajes_diccionario = []