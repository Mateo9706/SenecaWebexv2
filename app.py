from pprint import pprint
import requests
import json
import sys
import os

import http.client, urllib.parse, time

from werkzeug.utils import secure_filename

# from Red.Network import *
#from Red.speedTest import *
#from Menu.Menu import *
from BD.SaveDataNetworkClient import *
from Red.DataNetworkNew import *
from Red.ExtractDataNetwork import returnBandWidth

listaCaras = ["", "", ""]
list = []

try:
    from flask import Flask, send_file, jsonify, url_for, redirect
    from flask import request
except ImportError as e:
    print(e)
    print("Looks like 'flask' library is missing.\n"
          "Type 'pip3 install flask' command to install the missing library.")
    sys.exit()

bearer = os.environ.get("TEAMS_ACCESS_TOKEN")  # BOT'S ACCESS TOKEN NDE4NGM3ZDItYjNlMS00MjllLThjZjEtZjMzOWJhN2U5NmIwZGM1MzAyZGUtNzNj_PF84_b4e50a79-b7de-4ee2-940a-a983d1e5c35b
# Njg2MmZmMzYtZGU5Yi00ZWY4LThmZTYtMTZhZGYwMzFiMTIyYjNiNzJlMjMtZTlj_PF84_b4e50a79-b7de-4ee2-940a-a983d1e5c35b
bearer_direct = "OTY3YmFiY2MtMTI1Zi00NDJlLWFmOWItYTY2MWIwZTFlZDdkMGY2ZGQ3ZmQtMDAz_PF84_b4e50a79-b7de-4ee2-940a-a983d1e5c35b"  # NmU1Yjc2NWYtMWQwMC00Y2RjLWIxMTYtODIzY2ZiYzEzMmJkMTNjNzc0NDctYWRk_PF84_5276e22e-48ea-45a6-9334-eeda411c1e2e
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json; charset=utf-8",
    "Authorization": "Bearer " + bearer_direct
}

headers2 = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + bearer_direct
}

headers3 = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + bearer_direct
}

headers4 = {
    'Content-Type': "application/json",
    'Authorization': "Bearer "+ bearer_direct,
    'Host': "webexapis.com"
}

global in_message


def send_get(url, payload=None, js=True):
    if payload == None:
        request = requests.get(url, headers=headers)
    else:
        request = requests.get(url, headers=headers, params=payload)
    if js == True:
        request = request.json()
    return request


def send_post(url, data):
    #resolt = requests.post(url, json.dumps(data), headers=headers)
    #print(json.dumps(data))
    request = requests.post(url, json.dumps(data), headers=headers).json()
    #print(request)
    #print(resolt)
    return request

def send_post2(url, data):
    #resolt = requests.post(url, json.dumps(data), headers=headers)
    print(json.dumps(data))
    request = requests.post(url, json.dumps(data), headers=headers2).json()
    print(request)
    #print(resolt)
    return request

def send_post3(url, data):
    # resolt = requests.post(url, json.dumps(data), headers=headers)
    #print(json.dumps(data))
    request = requests.post(url, json.dumps(data), headers=headers2).json()
    #print(request)
    # print(resolt)
    return request


def greetings():
    return "Hola soy %s.<br/>" \
           "¿En que te puedo ayudar?.<br/>" % bot_name


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './Images'


@app.route('/download/<filename>')
def download(filename):
    print("archivo llegado", filename)
    direc = "/home/site/wwwroot/Archivos/" + filename  # /home/site/wwwroot/Archivos/
    return send_file(direc, mimetype='application/x-bat')


@app.route("/data", methods=['POST'])
def receiveDataCMD():
    print("entra datas")
    data = request.get_json()
    print(data['userId'], data['mac'], data['ssid'], data['radio'], data['canal'], data['senal'], data['ip'])
    receiveData(data['userId'], data['mac'], data['ssid'], data['radio'], data['canal'], data['senal'], data['ip'])
    return jsonify({'Mensaje': 'Datos Recibidos y Guardados'})


@app.route('/', methods=['GET', 'POST'])
def teams_webhook():
    global in_message
    global valor
    # botter = bot()
    if request.method == 'POST':
        webhook = request.get_json(silent=True)
        # pprint(webhook)
        msg = None
        result = send_get(
            'https://api.ciscospark.com/v1/messages/{0}'.format(webhook['data']['id']))
        in_message = result.get('text', '').lower()
        if in_message.startswith('hola'):
            # pprint(webhook)
            print(webhook['data']['roomId'])
            # SendCardPrincipal()
            SendCardPrincipalMod()
        elif in_message == 'opciones':
            SendCardPrincipalMod()
        resultado = send_get(
            'https://api.ciscospark.com/v1/attachment/actions/{0}'.format(webhook['data']['id']))
        try:
            valorLlegada = resultado['inputs']['action']
            print(valorLlegada)

            if (valorLlegada == '2'):
                print("entra 2")
                # pprint(webhook['data']['personId'])
                verif = validar(webhook['data']['personId'])
                if verif == True:
                    print("VERIFICADO. NO DESCARGA")
                    msgs = selects(webhook['data']['personId'])
                    # print(msgs[1],msgs[2],msgs[3],msgs[4],msgs[5],msgs[6],msgs[7])

                    bandFreqG = returnBandWidth(msgs[3], msgs[4])
                    dbm = convert(msgs[6])

                    ip = msgs[7]
                    mac = msgs[5]
                    proto = msgs[3]
                    conexionss = "WI-FI"
                    ssid = msgs[2]
                    señal = msgs[6] + "%"
                    dbms = dbm
                    band = bandFreqG
                    print(ip, mac, proto, conexionss, ssid, señal, dbms, band)

                    if float(dbms) >= -50:
                        print("entra excellent")
                        SendCardExcellent(ip=ip, mac=mac, proto=proto, conexion=conexionss, ssid=ssid,
                                          signal=señal, dbm=dbms, band=band)
                    elif float(dbms) <= -51 and float(dbms) >= -65:
                        print("entra good")
                        SendCardGood(ip=ip, mac=mac, proto=proto, conexion=conexionss, ssid=ssid,
                                     signal=señal, dbm=dbms, band=band)
                    elif float(dbms) <= -66 and float(dbms) >= -72:
                        print("entra regular")
                        SendCardRegular(ip=ip, mac=mac, proto=proto, conexion=conexionss, ssid=ssid,
                                        signal=señal, dbm=dbms, band=band)
                    elif float(dbms) <= -73:
                        print("entra malo")
                        SendCardBad(ip=ip, mac=mac, proto=proto, conexion=conexionss, ssid=ssid,
                                    signal=señal, dbm=dbms, band=band)

                elif verif == False:
                    print("NO VERIFICADOS")
                    urlsend = "https://botseneca.azurewebsites.net/data"
                    nameBat = "Data_" + webhook['data']['personId']
                    createBat(webhook['data']['personId'])
                    try:

                        #send_post("https://api.ciscospark.com/v1/messages",
                        #          {
                        #              "roomId": webhook['data']['roomId'],
                        #              "markdown": "Probando"
                        #          }
                        #          )

                        #send_post2("https://api.ciscospark.com/v1/messages",
                        #                          {
                        #                              "roomId": webhook['data']['roomId'],
                        #                              "text": "Como es la primera vez que usas esta herramienta, por favor descarga mis dos complementos. "+"\n" +"Solo debes ejecutar el instalador. Ejecutalo como administrador.",
                        #                              # Como es la primera vez que usas esta herramienta, por favor descarga mis dos complementos. "+"\n" +"Solo debes ejecutar el instalador. Ejecutalo como administrador
                        #                              "files": "https://botseneca.azurewebsites.net/download/Install_" + webhook['data']['personId'] + ".bat"
                        #                          })

                        #send_post3("https://webexapis.com/v1/messages",
                        #          {
                        #              "roomId": webhook['data']['roomId'],
                        #              "text": "Cuando se haya ejecutado el instalador. Escribeme opciones",
                        #              "files": "https://botseneca.azurewebsites.net/download/Data_" + webhook['data']['personId'] + ".bat"
                                      # https://senecaandes.azurewebsites.net/download/ExtensionSeneca.bat
                        #          }
                        #          )

                        url = "https://webexapis.com/v1/messages"

                        payload = "{\r\n  \"roomId\" : \"Y2lzY29zcGFyazovL3VzL1JPT00vMWU0NzUwZTUtMDk2My0zZTM2LWIxNjEtY2JhZTcxODgyMmFh\",\r\n  \"text\" : \"Learn Webex API with DevNet\",\r\n  \"files\" : \"https://botseneca.azurewebsites.net/download/Install_Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mYWM0MTY2OC1jYTUwLTRhMDUtYjMzOS1hNTliMzZiYjQ0OGM.bat\"\r\n}"
                        headers = {
                            'Authorization': 'Bearer OTY3YmFiY2MtMTI1Zi00NDJlLWFmOWItYTY2MWIwZTFlZDdkMGY2ZGQ3ZmQtMDAz_PF84_b4e50a79-b7de-4ee2-940a-a983d1e5c35b',
                            'Content-Type': 'application/json'
                        }

                        response = requests.request("POST", url, headers=headers, data=payload)
                        print(response.text)

                    except Exception as e:
                        print(e)


            elif (valorLlegada == '3'):
                print("entra 3")
                SendFirstQuestioncard()
            # elif (valorLlegada == '4'):
            #    print("entra 4")
            elif (valorLlegada == 'Mas info'):
                print("Mas Info")
                # msg = get_windows()
                # msg = dictionay()
                msgs = selects(webhook['data']['personId'])
                # print(msgs[1],msgs[2],msgs[3],msgs[4],msgs[5],msgs[6],msgs[7])

                bandFreqG = returnBandWidth(msgs[3], msgs[4])
                dbm = convert(msgs[6])

                ip = msgs[7]
                mac = msgs[5]
                proto = msgs[3]
                conexionss = "WI-FI"
                ssid = msgs[2]
                señal = msgs[6] + "%"
                dbms = dbm
                band = bandFreqG
                print(ip, mac, proto, conexionss, ssid, señal, dbms, band)
                SendCardSecondary(ip=ip, mac=mac, proto=proto, conexion=conexionss, ssid=ssid, band=band)
                # SendCardSecondary(ip=msg[0],mac=msg[1],proto=msg[2],conexion=msg[3],ssid=msg[4],band=msg[7])
            elif (valorLlegada == 'Q1'):
                print("entra q1")
                valor = 2
                list.append(valor)
                SendSecondQuestioncard()
            elif (valorLlegada == 'Q2' or valorLlegada == 'Q6'):
                valor = 5
                list.append(valor)
                if (valorLlegada == 'Q6'):
                    SendThirdQuestioncard()
                elif (valorLlegada == 'Q2'):
                    SendSecondQuestioncard()
            elif (valorLlegada == 'Q3' or valorLlegada == 'Q7'):
                valor = 10
                list.append(valor)
                if (valorLlegada == 'Q7'):
                    SendThirdQuestioncard()
                elif (valorLlegada == 'Q3'):
                    SendSecondQuestioncard()
            elif (valorLlegada == 'Q4' or valorLlegada == 'Q8'):
                valor = 30
                list.append(valor)
                if (valorLlegada == 'Q8'):
                    SendThirdQuestioncard()
                elif (valorLlegada == 'Q4'):
                    SendSecondQuestioncard()
            elif (valorLlegada == 'Q5'):
                valor = 3
                list.append(valor)
                SendThirdQuestioncard()
            elif (
                    valorLlegada == 'Q9' or valorLlegada == 'Q13' or valorLlegada == 'Q17' or valorLlegada == 'Q21' or valorLlegada == 'Q25' or valorLlegada == 'Q29'):
                valor = 0
                list.append(valor)
                if (valorLlegada == 'Q9'):
                    SendFourthQuestioncard()
                elif (valorLlegada == 'Q13'):
                    SendFifthQuestioncard()
                elif (valorLlegada == 'Q17'):
                    SendSixthQuestioncard()
                elif (valorLlegada == 'Q21'):
                    SendSeventhQuestioncard()
                elif (valorLlegada == 'Q25'):
                    SendOctQuestioncard()
                elif (valorLlegada == 'Q29'):
                    print("salida result")
                    suma = resultEncuesta(list)
                    SendFinishEncuesta(suma)
                    list.clear()
                    # SendOctQuestioncard()
            elif (
                    valorLlegada == 'Q10' or valorLlegada == 'Q14' or valorLlegada == 'Q18' or valorLlegada == 'Q22' or valorLlegada == 'Q26' or valorLlegada == 'Q30'):
                valor = 2
                list.append(valor)
                if (valorLlegada == 'Q10'):
                    SendFourthQuestioncard()
                elif (valorLlegada == 'Q14'):
                    SendFifthQuestioncard()
                elif (valorLlegada == 'Q18'):
                    SendSixthQuestioncard()
                elif (valorLlegada == 'Q22'):
                    SendSeventhQuestioncard()
                elif (valorLlegada == 'Q26'):
                    SendOctQuestioncard()
                elif (valorLlegada == 'Q30'):
                    print("salida result")
                    suma = resultEncuesta(list)
                    SendFinishEncuesta(suma)
                    list.clear()
                    # SendOctQuestioncard()
            elif (
                    valorLlegada == 'Q11' or valorLlegada == 'Q15' or valorLlegada == 'Q19' or valorLlegada == 'Q23' or valorLlegada == 'Q27' or valorLlegada == 'Q31'):
                valor = 5
                list.append(valor)
                if (valorLlegada == 'Q11'):
                    SendFourthQuestioncard()
                elif (valorLlegada == 'Q15'):
                    SendFifthQuestioncard()
                elif (valorLlegada == 'Q19'):
                    SendSixthQuestioncard()
                elif (valorLlegada == 'Q23'):
                    SendSeventhQuestioncard()
                elif (valorLlegada == 'Q27'):
                    SendOctQuestioncard()
                elif (valorLlegada == 'Q31'):
                    print("salida result")
                    suma = resultEncuesta(list)
                    SendFinishEncuesta(suma)
                    list.clear()
                    # SendOctQuestioncard()
            elif (
                    valorLlegada == 'Q12' or valorLlegada == 'Q16' or valorLlegada == 'Q20' or valorLlegada == 'Q24' or valorLlegada == 'Q28' or valorLlegada == 'Q32'):
                valor = 10
                list.append(valor)
                if (valorLlegada == 'Q12'):
                    SendFourthQuestioncard()
                elif (valorLlegada == 'Q16'):
                    SendFifthQuestioncard()
                elif (valorLlegada == 'Q20'):
                    SendSixthQuestioncard()
                elif (valorLlegada == 'Q24'):
                    SendSeventhQuestioncard()
                elif (valorLlegada == 'Q28'):
                    SendOctQuestioncard()
                elif (valorLlegada == 'Q32'):
                    print("salida result")
                    suma = resultEncuesta(list)
                    SendFinishEncuesta(suma)
                    list.clear()
                    # SendOctQuestioncard()
            print(list)

            # selector(resultado)
        except Exception as e:
            print("pasa")
            print(e)
        resultado = send_get(
            'https://api.ciscospark.com/v1/attachment/actions/{0}'.format(webhook['data']['id']))
        # pprint(resultado)

        return "true"
    elif request.method == 'GET':
        message = "<center><img src=\"https://cdn-images-1.medium.com/max/800/1*wrYQF1qZ3GePyrVn-Sp0UQ.png\" alt=\"Webex Teams Bot\" style=\"width:256; height:256;\"</center>" \
                  "<center><h2><b>Congratulations! Your <i style=\"color:#ff8000;\">%s</i> bot is up and running.</b></h2></center>" \
                  "<center><b><i>Don't forget to create Webhooks to start receiving events from Webex Teams!</i></b></center>" % bot_name
        return message


def espera():
    global valor

    webhook = request.get_json(silent=True)
    send_post("https://api.ciscospark.com/v1/messages",
              {
                  "roomId": webhook['data']['roomId'],
                  "markdown": "Por favor espera un momento mientras cargo la información..."
              }
              )
    # if(requestss.status_code == 200):
    #    return True

def SendCardPrincipalMod():
    global valor

    webhook = request.get_json(silent=True)
    print("entra sendcard")

    send_post("https://api.ciscospark.com/v1/messages",
              {
                  "roomId": webhook['data']['roomId'],
                  "markdown": "[Learn more](https://adaptivecards.io) about Adaptive Cards.",
                  "attachments": [
                      {
                          "contentType": "application/vnd.microsoft.card.adaptive",
                          "content": {
                              "type": "AdaptiveCard",
                              "version": "1.0",
                              "body": [
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "TextBlock",
                                                      "text": "Hola!! Soy el Agente Séneca y me gustaría brindarte mi ayuda ",
                                                      "wrap": True,
                                                      "weight": "Bolder",
                                                      "size": "Large",
                                                      "horizontalAlignment": "Center"
                                                  }
                                              ]
                                          }
                                      ]
                                  },
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "width": "auto",
                                              "items": [
                                                  {
                                                      "type": "Image",
                                                      "altText": "",
                                                      "url": "https://samibotapp8040.blob.core.windows.net/images/cabra_completa-01.png",
                                                      "horizontalAlignment": "Center",
                                                      "height": "300px"
                                                  }
                                              ],
                                              "spacing": "Small",
                                              "horizontalAlignment": "Center",
                                              "verticalContentAlignment": "Center"
                                          },
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "TextBlock",
                                                      "text": "Tengo mucha información para ti que podría ser de gran utilidad.",
                                                      "wrap": True,
                                                      "horizontalAlignment": "Center",
                                                      "weight": "Bolder",
                                                      "size": "Medium"
                                                  },
                                                  {
                                                      "type": "ActionSet",
                                                      "actions": [
                                                          {
                                                              "type": "Action.OpenUrl",
                                                              "title": "Conoce tu velocidad de tu Internet",
                                                              "url": "https://uniandes.speedtestcustom.com/"
                                                          }
                                                      ],
                                                      "horizontalAlignment": "Center"
                                                  },
                                                  {
                                                      "type": "ActionSet",
                                                      "actions": [
                                                          {
                                                              "type": "Action.Submit",
                                                              "title": "Detalles de tu conexión a la red",
                                                              "data": {
                                                                  "action": "2"
                                                              }
                                                          }
                                                      ],
                                                      "horizontalAlignment": "Center"
                                                  },
                                                  {
                                                      "type": "ActionSet",
                                                      "actions": [
                                                          {
                                                              "type": "Action.Submit",
                                                              "title": "Encuesta de conectividad",
                                                              "data": {
                                                                  "action": "3"
                                                              }
                                                          }
                                                      ],
                                                      "horizontalAlignment": "Center"
                                                  },
                                                  {
                                                      "type": "ActionSet",
                                                      "actions": [
                                                          {
                                                              "type": "Action.OpenUrl",
                                                              "title": "TIPS de conectividad en casa",
                                                              "url": "https://d2yn4wy9xj5giu.cloudfront.net/wp-content/uploads/2020/08/Tips_WiFi_en_casa.pdf"
                                                          }
                                                      ],
                                                      "horizontalAlignment": "Center"
                                                  }
                                              ]
                                          }
                                      ]
                                  }
                              ]
                          }
                      }
                  ]})

    # print("enviado o", respuesta)


def pruebacard():
    global valor

    webhook = request.get_json(silent=True)
    print("entra sendcard")

    respuesta = send_post("https://api.ciscospark.com/v1/messages",
                          {
                              "roomId": webhook['data']['roomId'],
                              "markdown": "[Learn more](https://adaptivecards.io) about Adaptive Cards.",
                              "attachments": [
                                  {
                                      "contentType": "application/vnd.microsoft.card.adaptive",
                                      "content": {
                                          "type": "AdaptiveCard",
                                          "version": "1.2",
                                          "body": [
                                              {
                                                  "type": "TextBlock",
                                                  "text": "Hola!! Soy el Agente Séneca y me gustaría brindarte mi ayuda",
                                                  "size": "Large",
                                                  "horizontalAlignment": "Center",
                                                  "weight": "Bolder"
                                              },
                                              {
                                                  "type": "ColumnSet",
                                                  "columns": [
                                                      {
                                                          "type": "Column",
                                                          "width": "stretch",
                                                          "items": [
                                                              {
                                                                  "type": "Image",
                                                                  "url": "https://samibotapp8040.blob.core.windows.net/images/cabra_completa-01.png"
                                                              }
                                                          ]
                                                      },
                                                      {
                                                          "type": "Column",
                                                          "width": "stretch",
                                                          "items": [
                                                              {
                                                                  "type": "TextBlock",
                                                                  "text": "Tengo mucha información para ti que podría ser de gran utilidad.",
                                                                  "wrap": True,
                                                                  "horizontalAlignment": "Center",
                                                                  "weight": "Bolder"
                                                              }
                                                          ]
                                                      }
                                                  ]
                                              }
                                          ],
                                          "$schema": "http://adaptivecards.io/schemas/adaptive-card.json"
                                      }
                                  }
                              ]})

    print("enviado o", respuesta)


def SendCardSecondary(ip, mac, proto, conexion, ssid, band):
    global valor
    webhook = request.get_json(silent=True)

    send_post("https://api.ciscospark.com/v1/messages",
              {
                  "roomId": webhook['data']['roomId'],
                  "markdown": "[Learn more](https://adaptivecards.io) about Adaptive Cards.",
                  "attachments": [
                      {
                          "contentType": "application/vnd.microsoft.card.adaptive",
                          "content": {
                              "type": "AdaptiveCard",
                              "version": "1.2",
                              "body": [
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "items": [
                                                  {
                                                      "type": "TextBlock",
                                                      "weight": "Bolder",
                                                      "text": "Detalles de tu conexión a la red",
                                                      "horizontalAlignment": "Left",
                                                      "wrap": True,
                                                      "color": "Light",
                                                      "spacing": "Small",
                                                      "size": "Medium"
                                                  },
                                                  {
                                                      "type": "ColumnSet",
                                                      "columns": [
                                                          {
                                                              "type": "Column",
                                                              "width": 35,
                                                              "items": [
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": "IP:",
                                                                      "size": "Small",
                                                                      "weight": "Bolder"
                                                                  },
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": "MAC:",
                                                                      "weight": "Bolder",
                                                                      "color": "Light",
                                                                      "spacing": "Small",
                                                                      "size": "Small"
                                                                  },
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": "Protocolo:",
                                                                      "weight": "Bolder",
                                                                      "color": "Light",
                                                                      "spacing": "Small",
                                                                      "size": "Small"
                                                                  },
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": "Conexión:",
                                                                      "size": "Small",
                                                                      "color": "Light",
                                                                      "spacing": "Small",
                                                                      "weight": "Bolder"
                                                                  },
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": "Red:",
                                                                      "size": "Small",
                                                                      "color": "Light",
                                                                      "spacing": "Small",
                                                                      "weight": "Bolder"
                                                                  }
                                                              ]
                                                          },
                                                          {
                                                              "type": "Column",
                                                              "width": 65,
                                                              "items": [
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": ip,
                                                                      "color": "Light",
                                                                      "size": "Small"
                                                                  },
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": mac,
                                                                      "color": "Light",
                                                                      "weight": "Lighter",
                                                                      "spacing": "Small",
                                                                      "size": "Small"
                                                                  },
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": proto,
                                                                      "weight": "Lighter",
                                                                      "color": "Light",
                                                                      "spacing": "Small",
                                                                      "size": "Small"
                                                                  },
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": conexion,
                                                                      "size": "Small",
                                                                      "weight": "Lighter",
                                                                      "color": "Light",
                                                                      "spacing": "Small"
                                                                  },
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": ssid,
                                                                      "size": "Small",
                                                                      "color": "Light",
                                                                      "spacing": "Small"
                                                                  }
                                                              ]
                                                          }
                                                      ],
                                                      "spacing": "Padding",
                                                      "horizontalAlignment": "Center"
                                                  }
                                              ],
                                              "width": "auto"
                                          },
                                          {
                                              "type": "Column",
                                              "items": [
                                                  {
                                                      "type": "Image",
                                                      "style": "Person",
                                                      "url": "https://samibotapp8040.blob.core.windows.net/images/cabra_cabeza-01.png",
                                                      "size": "Medium",
                                                      "horizontalAlignment": "Center",
                                                      "height": "160px"
                                                  }
                                              ],
                                              "width": "stretch"
                                          }
                                      ]
                                  },
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "width": "auto",
                                              "items": [
                                                  {
                                                      "type": "ColumnSet",
                                                      "columns": [
                                                          {
                                                              "type": "Column",
                                                              "width": "stretch",
                                                              "items": [
                                                                  {
                                                                      "type": "Image",
                                                                      "altText": "",
                                                                      "url": "https://samibotapp8040.blob.core.windows.net/images/barraGen.png"
                                                                  }
                                                              ]
                                                          }
                                                      ]
                                                  },
                                                  {
                                                      "type": "TextBlock",
                                                      "text": "Nota: Tu conexión actualmente está usando la banda de Frecuencia de " + band + ".\n",
                                                      "wrap": True
                                                  }
                                              ],
                                              "verticalContentAlignment": "Center",
                                              "horizontalAlignment": "Left",
                                              "spacing": "Small"
                                          }
                                      ]
                                  }
                              ]
                          }
                      }
                  ]})


def SendCardThird():
    global valor
    webhook = request.get_json(silent=True)

    send_post("https://api.ciscospark.com/v1/messages",
              {
                  "roomId": webhook['data']['roomId'],
                  "markdown": "[Learn more](https://adaptivecards.io) about Adaptive Cards.",
                  "attachments": [
                      {
                          "contentType": "application/vnd.microsoft.card.adaptive",
                          "content": {
                              "type": "AdaptiveCard",
                              "version": "1.2",
                              "body": [
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "items": [
                                                  {
                                                      "type": "TextBlock",
                                                      "weight": "Bolder",
                                                      "text": "Tu velocidad de Internet es:\n",
                                                      "horizontalAlignment": "Left",
                                                      "wrap": True,
                                                      "color": "Light",
                                                      "size": "Large",
                                                      "spacing": "Small"
                                                  },
                                                  {
                                                      "type": "ColumnSet",
                                                      "columns": [
                                                          {
                                                              "type": "Column",
                                                              "width": 65,
                                                              "items": [
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": "Download",
                                                                      "color": "Light",
                                                                      "horizontalAlignment": "Center",
                                                                      "weight": "Bolder",
                                                                      "size": "Small"
                                                                  },
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": "96.92 Mb/s",
                                                                      "size": "Large",
                                                                      "horizontalAlignment": "Center",
                                                                      "spacing": "Small"
                                                                  }
                                                              ]
                                                          },
                                                          {
                                                              "type": "Column",
                                                              "width": 65,
                                                              "items": [
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": "Upload",
                                                                      "color": "Light",
                                                                      "horizontalAlignment": "Center",
                                                                      "weight": "Bolder",
                                                                      "size": "Small"
                                                                  },
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": "96.92 Mb/s",
                                                                      "horizontalAlignment": "Center",
                                                                      "size": "Large",
                                                                      "spacing": "Small"
                                                                  }
                                                              ]
                                                          }
                                                      ],
                                                      "spacing": "Padding",
                                                      "horizontalAlignment": "Center"
                                                  }
                                              ],
                                              "width": "auto"
                                          }
                                      ],
                                      "horizontalAlignment": "Center",
                                      "style": "emphasis"
                                  },
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "TextBlock",
                                                      "text": "Sitios Web (www): 5/5\n",
                                                      "horizontalAlignment": "Center",
                                                      "weight": "Bolder"
                                                  },
                                                  {
                                                      "type": "ColumnSet",
                                                      "columns": [
                                                          {
                                                              "type": "Column",
                                                              "width": "stretch",
                                                              "items": [
                                                                  {
                                                                      "type": "Image",
                                                                      "altText": "",
                                                                      "url": "https://samibotapp8040.blob.core.windows.net/images/cara_verde.png"
                                                                  }
                                                              ]
                                                          },
                                                          {
                                                              "type": "Column",
                                                              "width": "stretch",
                                                              "items": [
                                                                  {
                                                                      "type": "Image",
                                                                      "altText": "",
                                                                      "url": "https://samibotapp8040.blob.core.windows.net/images/cara_verde.png"
                                                                  }
                                                              ]
                                                          },
                                                          {
                                                              "type": "Column",
                                                              "width": "stretch",
                                                              "items": [
                                                                  {
                                                                      "type": "Image",
                                                                      "altText": "",
                                                                      "url": "https://samibotapp8040.blob.core.windows.net/images/cara_verde.png"
                                                                  }
                                                              ]
                                                          },
                                                          {
                                                              "type": "Column",
                                                              "width": "stretch",
                                                              "items": [
                                                                  {
                                                                      "type": "Image",
                                                                      "altText": "",
                                                                      "url": "https://samibotapp8040.blob.core.windows.net/images/cara_verde.png"
                                                                  }
                                                              ]
                                                          },
                                                          {
                                                              "type": "Column",
                                                              "width": "stretch",
                                                              "items": [
                                                                  {
                                                                      "type": "Image",
                                                                      "altText": "",
                                                                      "url": "https://samibotapp8040.blob.core.windows.net/images/cara_verde.png"
                                                                  }
                                                              ]
                                                          }
                                                      ]
                                                  }
                                              ]
                                          }
                                      ]
                                  },
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "TextBlock",
                                                      "text": "Video HD: 5/5\n",
                                                      "weight": "Bolder",
                                                      "horizontalAlignment": "Center"
                                                  }
                                              ]
                                          }
                                      ]
                                  },
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "Image",
                                                      "altText": "",
                                                      "url": "https://samibotapp8040.blob.core.windows.net/images/cara_verde.png"
                                                  }
                                              ]
                                          },
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "Image",
                                                      "altText": "",
                                                      "url": "https://samibotapp8040.blob.core.windows.net/images/cara_verde.png"
                                                  }
                                              ]
                                          },
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "Image",
                                                      "altText": "",
                                                      "url": "https://samibotapp8040.blob.core.windows.net/images/cara_verde.png"
                                                  }
                                              ]
                                          },
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "Image",
                                                      "altText": "",
                                                      "url": "https://samibotapp8040.blob.core.windows.net/images/cara_verde.png"
                                                  }
                                              ]
                                          },
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "Image",
                                                      "altText": "",
                                                      "url": "https://samibotapp8040.blob.core.windows.net/images/cara_verde.png"
                                                  }
                                              ]
                                          }
                                      ]
                                  },
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "TextBlock",
                                                      "text": "Video-Conferencia: 4/5\n",
                                                      "weight": "Bolder",
                                                      "horizontalAlignment": "Center"
                                                  }
                                              ]
                                          }
                                      ]
                                  },
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "Image",
                                                      "altText": "",
                                                      "url": "https://samibotapp8040.blob.core.windows.net/images/cara_azul.png"
                                                  }
                                              ]
                                          },
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "Image",
                                                      "altText": "",
                                                      "url": "https://samibotapp8040.blob.core.windows.net/images/cara_azul.png"
                                                  }
                                              ]
                                          },
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "Image",
                                                      "altText": "",
                                                      "url": "https://samibotapp8040.blob.core.windows.net/images/cara_azul.png"
                                                  }
                                              ]
                                          },
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "Image",
                                                      "altText": "",
                                                      "url": "https://samibotapp8040.blob.core.windows.net/images/cara_azul.png"
                                                  }
                                              ]
                                          },
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "Image",
                                                      "altText": "",
                                                      "url": "https://samibotapp8040.blob.core.windows.net/images/cara_gris.png"
                                                  }
                                              ]
                                          }
                                      ]
                                  },
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "TextBlock",
                                                      "text": "Juegos en línea: 3/5\n",
                                                      "weight": "Bolder",
                                                      "horizontalAlignment": "Center"
                                                  },
                                                  {
                                                      "type": "ColumnSet",
                                                      "columns": [
                                                          {
                                                              "type": "Column",
                                                              "width": "stretch",
                                                              "items": [
                                                                  {
                                                                      "type": "Image",
                                                                      "altText": "",
                                                                      "url": "https://samibotapp8040.blob.core.windows.net/images/cara_amarillo.png"
                                                                  }
                                                              ]
                                                          },
                                                          {
                                                              "type": "Column",
                                                              "width": "stretch",
                                                              "items": [
                                                                  {
                                                                      "type": "Image",
                                                                      "altText": "",
                                                                      "url": "https://samibotapp8040.blob.core.windows.net/images/cara_amarillo.png"
                                                                  }
                                                              ]
                                                          },
                                                          {
                                                              "type": "Column",
                                                              "width": "stretch",
                                                              "items": [
                                                                  {
                                                                      "type": "Image",
                                                                      "altText": "",
                                                                      "url": "https://samibotapp8040.blob.core.windows.net/images/cara_amarillo.png"
                                                                  }
                                                              ]
                                                          },
                                                          {
                                                              "type": "Column",
                                                              "width": "stretch",
                                                              "items": [
                                                                  {
                                                                      "type": "Image",
                                                                      "altText": "",
                                                                      "url": "https://samibotapp8040.blob.core.windows.net/images/cara_gris.png"
                                                                  }
                                                              ]
                                                          },
                                                          {
                                                              "type": "Column",
                                                              "width": "stretch",
                                                              "items": [
                                                                  {
                                                                      "type": "Image",
                                                                      "altText": "",
                                                                      "url": "https://samibotapp8040.blob.core.windows.net/images/cara_gris.png"
                                                                  }
                                                              ]
                                                          }
                                                      ]
                                                  }
                                              ]
                                          }
                                      ]
                                  }
                              ]
                          }
                      }
                  ]})


def SendCardExcellent(ip, mac, proto, conexion, ssid, signal, dbm, band):
    global valor
    webhook = request.get_json(silent=True)

    send_post("https://api.ciscospark.com/v1/messages",
              {
                  "roomId": webhook['data']['roomId'],
                  "markdown": "[Learn more](https://adaptivecards.io) about Adaptive Cards.",
                  "attachments": [
                      {
                          "contentType": "application/vnd.microsoft.card.adaptive",
                          "content": {
                              "type": "AdaptiveCard",
                              "version": "1.2",
                              "body": [
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "items": [
                                                  {
                                                      "type": "TextBlock",
                                                      "weight": "Bolder",
                                                      "text": "Detalles de tu conexión a la red",
                                                      "horizontalAlignment": "Left",
                                                      "wrap": True,
                                                      "color": "Light",
                                                      "spacing": "Small",
                                                      "size": "Medium"
                                                  },
                                                  {
                                                      "type": "ColumnSet",
                                                      "columns": [
                                                          {
                                                              "type": "Column",
                                                              "width": 35,
                                                              "items": [
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": "IP:",
                                                                      "weight": "Bolder",
                                                                      "color": "Light",
                                                                      "size": "Small"
                                                                  },
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": "MAC:",
                                                                      "weight": "Bolder",
                                                                      "color": "Light",
                                                                      "spacing": "Small",
                                                                      "size": "Small"
                                                                  },
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": "Protocolo:",
                                                                      "weight": "Bolder",
                                                                      "color": "Light",
                                                                      "spacing": "Small",
                                                                      "size": "Small"
                                                                  },
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": "Conexión:",
                                                                      "spacing": "Small",
                                                                      "weight": "Bolder",
                                                                      "size": "Small"
                                                                  },
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": "Red:",
                                                                      "weight": "Bolder",
                                                                      "spacing": "Small",
                                                                      "color": "Light",
                                                                      "size": "Small"
                                                                  }
                                                              ]
                                                          },
                                                          {
                                                              "type": "Column",
                                                              "width": 65,
                                                              "items": [
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": ip,
                                                                      "color": "Light",
                                                                      "size": "Small"
                                                                  },
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": mac,
                                                                      "color": "Light",
                                                                      "weight": "Lighter",
                                                                      "spacing": "Small",
                                                                      "size": "Small"
                                                                  },
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": proto,
                                                                      "weight": "Lighter",
                                                                      "color": "Light",
                                                                      "spacing": "Small",
                                                                      "size": "Small"
                                                                  },
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": conexion,
                                                                      "spacing": "Small",
                                                                      "color": "Light",
                                                                      "size": "Small"
                                                                  },
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": ssid,
                                                                      "spacing": "Small",
                                                                      "color": "Light",
                                                                      "size": "Small"
                                                                  }
                                                              ]
                                                          }
                                                      ],
                                                      "spacing": "Padding",
                                                      "horizontalAlignment": "Center"
                                                  }
                                              ],
                                              "width": "auto",
                                              "style": "emphasis",
                                              "verticalContentAlignment": "Center"
                                          },
                                          {
                                              "type": "Column",
                                              "items": [
                                                  {
                                                      "type": "Image",
                                                      "style": "Person",
                                                      "url": "https://samibotapp8040.blob.core.windows.net/images/cabra_cabeza-01.png",
                                                      "size": "Medium",
                                                      "height": "210px"  # 160
                                                  }
                                              ],
                                              "width": "stretch"
                                          }
                                      ]
                                  },
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "width": "auto",
                                              "items": [
                                                  {
                                                      "type": "TextBlock",
                                                      "text": "Intensidad de Señal " + signal + " RSSI (" + dbm + ")\n",
                                                      "spacing": "Small",
                                                      "horizontalAlignment": "Left",
                                                      "wrap": True,
                                                      "size": "Medium",
                                                      "weight": "Bolder",
                                                      "color": "Light"
                                                  }
                                              ],
                                              "style": "emphasis"
                                          }
                                      ]
                                  },
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "Image",
                                                      "altText": "",
                                                      "url": "https://samibotapp8040.blob.core.windows.net/images/excellent.png",
                                                      "spacing": "Small",
                                                      "width": "80px",
                                                      "horizontalAlignment": "Center"
                                                  }
                                              ]
                                          },
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "Image",
                                                      "altText": "",
                                                      "url": "https://samibotapp8040.blob.core.windows.net/images/excellent_stars.PNG",
                                                      "horizontalAlignment": "Center",
                                                      "size": "Large",
                                                      "width": "205px",
                                                      "height": "80px"
                                                  }
                                              ]
                                          }
                                      ]
                                  },
                                  {
                                      "type": "TextBlock",
                                      "text": "Resultado: El nivel de señal es excelente, lo que significa que estas muy cerca a tu modem o punto de acceso de Internet. La conexión es idónea para el uso de tus aplicaciones.",
                                      "wrap": True
                                  },
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "ActionSet",
                                                      "actions": [
                                                          {
                                                              "type": "Action.Submit",
                                                              "title": "Mas Información",
                                                              "data": {
                                                                  "action": "Mas info"
                                                              }
                                                          }
                                                      ],
                                                      "horizontalAlignment": "Right"
                                                  }
                                              ]
                                          }
                                      ]
                                  }
                              ]
                          }
                      }
                  ]})


def SendCardGood(ip, mac, proto, conexion, ssid, signal, dbm, band):
    global valor
    webhook = request.get_json(silent=True)

    send_post("https://api.ciscospark.com/v1/messages",
              {
                  "roomId": webhook['data']['roomId'],
                  "markdown": "[Learn more](https://adaptivecards.io) about Adaptive Cards.",
                  "attachments": [
                      {
                          "contentType": "application/vnd.microsoft.card.adaptive",
                          "content": {
                              "type": "AdaptiveCard",
                              "version": "1.2",
                              "body": [
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "items": [
                                                  {
                                                      "type": "TextBlock",
                                                      "weight": "Bolder",
                                                      "text": "Detalles de tu conexión a la red",
                                                      "horizontalAlignment": "Left",
                                                      "wrap": True,
                                                      "color": "Light",
                                                      "spacing": "Small",
                                                      "size": "Medium"
                                                  },
                                                  {
                                                      "type": "ColumnSet",
                                                      "columns": [
                                                          {
                                                              "type": "Column",
                                                              "width": 35,
                                                              "items": [
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": "IP:",
                                                                      "weight": "Bolder",
                                                                      "color": "Light",
                                                                      "size": "Small"
                                                                  },
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": "MAC:",
                                                                      "weight": "Bolder",
                                                                      "color": "Light",
                                                                      "spacing": "Small",
                                                                      "size": "Small"
                                                                  },
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": "Protocolo:",
                                                                      "weight": "Bolder",
                                                                      "color": "Light",
                                                                      "spacing": "Small",
                                                                      "size": "Small"
                                                                  },
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": "Conexión:",
                                                                      "weight": "Bolder",
                                                                      "spacing": "Small",
                                                                      "color": "Light",
                                                                      "size": "Small"
                                                                  },
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": "Red:",
                                                                      "weight": "Bolder",
                                                                      "spacing": "Small",
                                                                      "color": "Light",
                                                                      "size": "Small"
                                                                  }
                                                              ]
                                                          },
                                                          {
                                                              "type": "Column",
                                                              "width": 65,
                                                              "items": [
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": ip,
                                                                      "color": "Light",
                                                                      "size": "Small"
                                                                  },
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": mac,
                                                                      "color": "Light",
                                                                      "weight": "Lighter",
                                                                      "spacing": "Small",
                                                                      "size": "Small"
                                                                  },
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": proto,
                                                                      "weight": "Lighter",
                                                                      "color": "Light",
                                                                      "spacing": "Small",
                                                                      "size": "Small"
                                                                  },
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": conexion,
                                                                      "spacing": "Small",
                                                                      "color": "Light",
                                                                      "size": "Small"
                                                                  },
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": ssid,
                                                                      "spacing": "Small",
                                                                      "color": "Light",
                                                                      "size": "Small"
                                                                  }
                                                              ]
                                                          }
                                                      ],
                                                      "spacing": "Padding",
                                                      "horizontalAlignment": "Center"
                                                  }
                                              ],
                                              "width": "auto",
                                              "style": "emphasis",
                                              "verticalContentAlignment": "Center"
                                          },
                                          {
                                              "type": "Column",
                                              "items": [
                                                  {
                                                      "type": "Image",
                                                      "style": "Person",
                                                      "url": "https://samibotapp8040.blob.core.windows.net/images/cabra_cabeza-01.png",
                                                      "size": "Medium",
                                                      "height": "160px"
                                                  }
                                              ],
                                              "width": "stretch"
                                          }
                                      ]
                                  },
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "width": "auto",
                                              "items": [
                                                  {
                                                      "type": "TextBlock",
                                                      "text": "Intensidad de Señal " + signal + " RSSI (" + dbm + ")\n",
                                                      "spacing": "Small",
                                                      "horizontalAlignment": "Left",
                                                      "wrap": True,
                                                      "size": "Medium",
                                                      "weight": "Bolder",
                                                      "color": "Light"
                                                  }
                                              ],
                                              "style": "emphasis"
                                          }
                                      ]
                                  },
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "Image",
                                                      "altText": "",
                                                      "url": "https://samibotapp8040.blob.core.windows.net/images/good.png",
                                                      "spacing": "Small",
                                                      "width": "80px",
                                                      "horizontalAlignment": "Center"
                                                  }
                                              ]
                                          },
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "Image",
                                                      "altText": "",
                                                      "url": "https://samibotapp8040.blob.core.windows.net/images/good_stars.PNG",
                                                      "horizontalAlignment": "Center",
                                                      "size": "Large",
                                                      "width": "205px",
                                                      "height": "80px"
                                                  }
                                              ]
                                          }
                                      ]
                                  },
                                  {
                                      "type": "TextBlock",
                                      "text": "Resultado: El nivel de señal es bueno, lo que significa que posiblemente estas alejado unos metros de tu modem o hay algún obstáculo entre tu dispositivo y el punto de acceso a internet. La conexión es adecuada para el uso de tus aplicaciones.\n",
                                      "wrap": True
                                  },
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "ActionSet",
                                                      "actions": [
                                                          {
                                                              "type": "Action.Submit",
                                                              "title": "Mas Información",
                                                              "data": {
                                                                  "action": "Mas info"
                                                              }
                                                          }
                                                      ],
                                                      "horizontalAlignment": "Right"
                                                  }
                                              ]
                                          }
                                      ]
                                  }
                              ]
                          }
                      }
                  ]})


def SendCardRegular(ip, mac, proto, conexion, ssid, signal, dbm, band):
    global valor
    webhook = request.get_json(silent=True)

    send_post("https://api.ciscospark.com/v1/messages",
              {
                  "roomId": webhook['data']['roomId'],
                  "markdown": "[Learn more](https://adaptivecards.io) about Adaptive Cards.",
                  "attachments": [
                      {
                          "contentType": "application/vnd.microsoft.card.adaptive",
                          "content": {
                              "type": "AdaptiveCard",
                              "version": "1.2",
                              "body": [
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "items": [
                                                  {
                                                      "type": "TextBlock",
                                                      "weight": "Bolder",
                                                      "text": "Detalles de tu conexión a la red",
                                                      "horizontalAlignment": "Left",
                                                      "wrap": True,
                                                      "color": "Light",
                                                      "spacing": "Small",
                                                      "size": "Medium"
                                                  },
                                                  {
                                                      "type": "ColumnSet",
                                                      "columns": [
                                                          {
                                                              "type": "Column",
                                                              "width": 35,
                                                              "items": [
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": "IP:",
                                                                      "weight": "Bolder",
                                                                      "color": "Light",
                                                                      "size": "Small"
                                                                  },
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": "MAC:",
                                                                      "weight": "Bolder",
                                                                      "color": "Light",
                                                                      "spacing": "Small",
                                                                      "size": "Small"
                                                                  },
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": "Protocolo:",
                                                                      "weight": "Bolder",
                                                                      "color": "Light",
                                                                      "spacing": "Small",
                                                                      "size": "Small"
                                                                  },
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": "Conexión:",
                                                                      "weight": "Bolder",
                                                                      "spacing": "Small",
                                                                      "color": "Light",
                                                                      "size": "Small"
                                                                  },
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": "Red:",
                                                                      "weight": "Bolder",
                                                                      "spacing": "Small",
                                                                      "color": "Light",
                                                                      "size": "Small"
                                                                  }
                                                              ]
                                                          },
                                                          {
                                                              "type": "Column",
                                                              "width": 65,
                                                              "items": [
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": ip,
                                                                      "color": "Light",
                                                                      "size": "Small"
                                                                  },
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": mac,
                                                                      "color": "Light",
                                                                      "weight": "Lighter",
                                                                      "spacing": "Small",
                                                                      "size": "Small"
                                                                  },
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": proto,
                                                                      "weight": "Lighter",
                                                                      "color": "Light",
                                                                      "spacing": "Small",
                                                                      "size": "Small"
                                                                  },
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": conexion,
                                                                      "spacing": "Small",
                                                                      "color": "Light",
                                                                      "size": "Small"
                                                                  },
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": ssid,
                                                                      "spacing": "Small",
                                                                      "color": "Light",
                                                                      "size": "Small"
                                                                  }
                                                              ]
                                                          }
                                                      ],
                                                      "spacing": "Padding",
                                                      "horizontalAlignment": "Center"
                                                  }
                                              ],
                                              "width": "auto",
                                              "style": "emphasis",
                                              "verticalContentAlignment": "Center"
                                          },
                                          {
                                              "type": "Column",
                                              "items": [
                                                  {
                                                      "type": "Image",
                                                      "style": "Person",
                                                      "url": "https://samibotapp8040.blob.core.windows.net/images/cabra_cabeza-01.png",
                                                      "size": "Medium",
                                                      "isVisible": True,
                                                      "height": "160px"
                                                  }
                                              ],
                                              "width": "stretch"
                                          }
                                      ]
                                  },
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "width": "auto",
                                              "items": [
                                                  {
                                                      "type": "TextBlock",
                                                      "text": "Intensidad de Señal " + signal + " RSSI (" + dbm + ")\n",
                                                      "spacing": "Small",
                                                      "horizontalAlignment": "Left",
                                                      "wrap": True,
                                                      "size": "Medium",
                                                      "weight": "Bolder",
                                                      "color": "Light"
                                                  }
                                              ],
                                              "style": "emphasis"
                                          }
                                      ]
                                  },
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "Image",
                                                      "altText": "",
                                                      "url": "https://samibotapp8040.blob.core.windows.net/images/regular.png",
                                                      "spacing": "Small",
                                                      "width": "80px",
                                                      "horizontalAlignment": "Center"
                                                  }
                                              ]
                                          },
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "Image",
                                                      "altText": "",
                                                      "url": "https://samibotapp8040.blob.core.windows.net/images/regular_stars.PNG",
                                                      "horizontalAlignment": "Center",
                                                      "size": "Large",
                                                      "width": "205px",
                                                      "height": "80px"
                                                  }
                                              ]
                                          }
                                      ]
                                  },
                                  {
                                      "type": "TextBlock",
                                      "text": "El nivel de señal es Regular, lo que significa que posiblemente estas alejado varios metros de tu modem o hay muchos obstáculos entre tu dispositivo y el punto de acceso a internet. La conexión podría empezar a fallar y por ende afectar el rendimiento de tus aplicaciones.\n",
                                      "wrap": True
                                  },
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "ActionSet",
                                                      "actions": [
                                                          {
                                                              "type": "Action.Submit",
                                                              "title": "Mas Información",
                                                              "data": {
                                                                  "action": "Mas info"
                                                              }
                                                          }
                                                      ],
                                                      "horizontalAlignment": "Right"
                                                  }
                                              ]
                                          }
                                      ]
                                  }
                              ]
                          }
                      }
                  ]})


def SendCardBad(ip, mac, proto, conexion, ssid, signal, dbm, band):
    global valor
    webhook = request.get_json(silent=True)

    send_post("https://api.ciscospark.com/v1/messages",
              {
                  "roomId": webhook['data']['roomId'],
                  "markdown": "[Learn more](https://adaptivecards.io) about Adaptive Cards.",
                  "attachments": [
                      {
                          "contentType": "application/vnd.microsoft.card.adaptive",
                          "content": {
                              "type": "AdaptiveCard",
                              "version": "1.2",
                              "body": [
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "items": [
                                                  {
                                                      "type": "TextBlock",
                                                      "weight": "Bolder",
                                                      "text": "Detalles de tu conexión a la red",
                                                      "horizontalAlignment": "Left",
                                                      "wrap": True,
                                                      "color": "Light",
                                                      "spacing": "Small",
                                                      "size": "Medium"
                                                  },
                                                  {
                                                      "type": "ColumnSet",
                                                      "columns": [
                                                          {
                                                              "type": "Column",
                                                              "width": 35,
                                                              "items": [
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": "IP:",
                                                                      "weight": "Bolder",
                                                                      "color": "Light",
                                                                      "size": "Small"
                                                                  },
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": "MAC:",
                                                                      "weight": "Bolder",
                                                                      "color": "Light",
                                                                      "spacing": "Small",
                                                                      "size": "Small"
                                                                  },
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": "Protocolo:",
                                                                      "weight": "Bolder",
                                                                      "color": "Light",
                                                                      "spacing": "Small",
                                                                      "size": "Small"
                                                                  },
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": "Conexión:",
                                                                      "weight": "Bolder",
                                                                      "spacing": "Small",
                                                                      "color": "Light",
                                                                      "size": "Small"
                                                                  },
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": "Red:",
                                                                      "weight": "Bolder",
                                                                      "spacing": "Small",
                                                                      "color": "Light",
                                                                      "size": "Small"
                                                                  }
                                                              ]
                                                          },
                                                          {
                                                              "type": "Column",
                                                              "width": 65,
                                                              "items": [
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": ip,
                                                                      "color": "Light",
                                                                      "size": "Small"
                                                                  },
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": mac,
                                                                      "color": "Light",
                                                                      "weight": "Lighter",
                                                                      "spacing": "Small",
                                                                      "size": "Small"
                                                                  },
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": proto,
                                                                      "weight": "Lighter",
                                                                      "color": "Light",
                                                                      "spacing": "Small",
                                                                      "size": "Small"
                                                                  },
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": conexion,
                                                                      "spacing": "Small",
                                                                      "color": "Light",
                                                                      "size": "Small"
                                                                  },
                                                                  {
                                                                      "type": "TextBlock",
                                                                      "text": ssid,
                                                                      "spacing": "Small",
                                                                      "color": "Light",
                                                                      "size": "Small"
                                                                  }
                                                              ]
                                                          }
                                                      ],
                                                      "spacing": "Padding",
                                                      "horizontalAlignment": "Center"
                                                  }
                                              ],
                                              "width": "auto",
                                              "style": "emphasis",
                                              "verticalContentAlignment": "Center"
                                          },
                                          {
                                              "type": "Column",
                                              "items": [
                                                  {
                                                      "type": "Image",
                                                      "style": "Person",
                                                      "url": "https://samibotapp8040.blob.core.windows.net/images/cabra_cabeza-01.png",
                                                      "size": "Medium",
                                                      "isVisible": True,
                                                      "height": "160px"
                                                  }
                                              ],
                                              "width": "stretch"
                                          }
                                      ]
                                  },
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "width": "auto",
                                              "items": [
                                                  {
                                                      "type": "TextBlock",
                                                      "text": "Intensidad de Señal " + signal + " RSSI (" + dbm + ")\n",
                                                      "spacing": "Small",
                                                      "horizontalAlignment": "Left",
                                                      "wrap": True,
                                                      "size": "Medium",
                                                      "weight": "Bolder",
                                                      "color": "Light"
                                                  }
                                              ],
                                              "style": "emphasis"
                                          }
                                      ]
                                  },
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "Image",
                                                      "altText": "",
                                                      "url": "https://samibotapp8040.blob.core.windows.net/images/mala.png",
                                                      "spacing": "Small",
                                                      "width": "80px",
                                                      "horizontalAlignment": "Center"
                                                  }
                                              ]
                                          },
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "Image",
                                                      "altText": "",
                                                      "url": "https://samibotapp8040.blob.core.windows.net/images/malo_stars.PNG",
                                                      "horizontalAlignment": "Center",
                                                      "size": "Large",
                                                      "width": "205px",
                                                      "height": "80px"
                                                  }
                                              ]
                                          }
                                      ]
                                  },
                                  {
                                      "type": "TextBlock",
                                      "text": "Resultado: El nivel de señal es Mala, lo que significa que tu dispositivo esta demasiado lejos del modem punto de acceso a internet. La conexión no podrá ser establecida de forma estable el rendimiento de las aplicaciones se verá afectado en gran medida.\n",
                                      "wrap": True
                                  },
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "ActionSet",
                                                      "actions": [
                                                          {
                                                              "type": "Action.Submit",
                                                              "title": "Mas Información",
                                                              "data": {
                                                                  "action": "Mas info"
                                                              }
                                                          }
                                                      ],
                                                      "horizontalAlignment": "Right"
                                                  }
                                              ]
                                          }
                                      ]
                                  }
                              ]
                          }
                      }
                  ]})


def SendFirstQuestioncard():
    global valor
    webhook = request.get_json(silent=True)

    req = send_post("https://api.ciscospark.com/v1/messages",
                    {
                        "roomId": webhook['data']['roomId'],
                        "markdown": "[Learn more](https://adaptivecards.io) about Adaptive Cards.",
                        "attachments": [
                            {
                                "contentType": "application/vnd.microsoft.card.adaptive",
                                "content": {
                                    "type": "AdaptiveCard",
                                    "version": "1.2",
                                    "body": [
                                        {
                                            "type": "ColumnSet",
                                            "columns": [
                                                {
                                                    "type": "Column",
                                                    "items": [
                                                        {
                                                            "type": "Image",
                                                            "style": "Person",
                                                            "url": "https://samibotapp8040.blob.core.windows.net/images/Cabra_transparente.png",
                                                            "size": "Medium",
                                                            "horizontalAlignment": "Center",
                                                            "height": "100px"
                                                        }
                                                    ],
                                                    "width": "auto",
                                                    "horizontalAlignment": "Center"
                                                },
                                                {
                                                    "type": "Column",
                                                    "items": [
                                                        {
                                                            "type": "TextBlock",
                                                            "weight": "Bolder",
                                                            "text": "¿Sabes si el Ancho de banda de tu Internet Hogar es suficiente?\n",
                                                            "horizontalAlignment": "Center",
                                                            "wrap": True,
                                                            "color": "Light",
                                                            "size": "ExtraLarge",
                                                            "spacing": "Small"
                                                        }
                                                    ],
                                                    "width": "stretch"
                                                }
                                            ]
                                        },
                                        {
                                            "type": "TextBlock",
                                            "text": "¿Cuántas personas hacen uso del internet en tu casa? \n",
                                            "horizontalAlignment": "Center",
                                            "weight": "Bolder"
                                        },
                                        {
                                            "type": "ColumnSet",
                                            "columns": [
                                                {
                                                    "type": "Column",
                                                    "width": "stretch",
                                                    "items": [
                                                        {
                                                            "type": "ActionSet",
                                                            "actions": [
                                                                {
                                                                    "type": "Action.Submit",
                                                                    "title": "1-2",
                                                                    "data": {
                                                                        "action": "Q1"
                                                                    }
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                },
                                                {
                                                    "type": "Column",
                                                    "width": "stretch",
                                                    "items": [
                                                        {
                                                            "type": "ActionSet",
                                                            "actions": [
                                                                {
                                                                    "type": "Action.Submit",
                                                                    "title": "3-4",
                                                                    "data": {
                                                                        "action": "Q2"
                                                                    }
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                },
                                                {
                                                    "type": "Column",
                                                    "width": "stretch",
                                                    "items": [
                                                        {
                                                            "type": "ActionSet",
                                                            "actions": [
                                                                {
                                                                    "type": "Action.Submit",
                                                                    "title": "5-6",
                                                                    "data": {
                                                                        "action": "Q3"
                                                                    }
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                },
                                                {
                                                    "type": "Column",
                                                    "width": "stretch",
                                                    "items": [
                                                        {
                                                            "type": "ActionSet",
                                                            "actions": [
                                                                {
                                                                    "type": "Action.Submit",
                                                                    "title": "7 o mas",
                                                                    "data": {
                                                                        "action": "Q4"
                                                                    }
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                }
                            }
                        ]})
    print("mirar aqui", req)


def SendSecondQuestioncard():
    global valor
    webhook = request.get_json(silent=True)

    send_post("https://api.ciscospark.com/v1/messages",
              {
                  "roomId": webhook['data']['roomId'],
                  "markdown": "[Learn more](https://adaptivecards.io) about Adaptive Cards.",
                  "attachments": [
                      {
                          "contentType": "application/vnd.microsoft.card.adaptive",
                          "content": {
                              "type": "AdaptiveCard",
                              "version": "1.2",
                              "body": [
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "items": [
                                                  {
                                                      "type": "Image",
                                                      "style": "Person",
                                                      "url": "https://samibotapp8040.blob.core.windows.net/images/Cabra_transparente.png",
                                                      "size": "Medium",
                                                      "horizontalAlignment": "Center",
                                                      "height": "100px"
                                                  }
                                              ],
                                              "width": "auto",
                                              "horizontalAlignment": "Center"
                                          },
                                          {
                                              "type": "Column",
                                              "items": [
                                                  {
                                                      "type": "TextBlock",
                                                      "weight": "Bolder",
                                                      "text": "¿Sabes si el Ancho de banda de tu Internet Hogar es suficiente?\n",
                                                      "horizontalAlignment": "Center",
                                                      "wrap": True,
                                                      "color": "Light",
                                                      "size": "ExtraLarge",
                                                      "spacing": "Small"
                                                  }
                                              ],
                                              "width": "stretch"
                                          }
                                      ]
                                  },
                                  {
                                      "type": "TextBlock",
                                      "text": "¿Cuántos dispositivos conectas de forma simultánea? \n",
                                      "horizontalAlignment": "Center",
                                      "weight": "Bolder"
                                  },
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "ActionSet",
                                                      "actions": [
                                                          {
                                                              "type": "Action.Submit",
                                                              "title": "1-3",
                                                              "data": {
                                                                  "action": "Q5"
                                                              }
                                                          }
                                                      ]
                                                  }
                                              ]
                                          },
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "ActionSet",
                                                      "actions": [
                                                          {
                                                              "type": "Action.Submit",
                                                              "title": "4-7",
                                                              "data": {
                                                                  "action": "Q6"
                                                              }
                                                          }
                                                      ]
                                                  }
                                              ]
                                          },
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "ActionSet",
                                                      "actions": [
                                                          {
                                                              "type": "Action.Submit",
                                                              "title": "8-10",
                                                              "data": {
                                                                  "action": "Q7"
                                                              }
                                                          }
                                                      ]
                                                  }
                                              ]
                                          },
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "ActionSet",
                                                      "actions": [
                                                          {
                                                              "type": "Action.Submit",
                                                              "title": "10 +",
                                                              "data": {
                                                                  "action": "Q8"
                                                              }
                                                          }
                                                      ]
                                                  }
                                              ]
                                          }
                                      ]
                                  }
                              ]
                          }
                      }
                  ]})


def SendThirdQuestioncard():
    global valor
    webhook = request.get_json(silent=True)

    send_post("https://api.ciscospark.com/v1/messages",
              {
                  "roomId": webhook['data']['roomId'],
                  "markdown": "[Learn more](https://adaptivecards.io) about Adaptive Cards.",
                  "attachments": [
                      {
                          "contentType": "application/vnd.microsoft.card.adaptive",
                          "content": {
                              "type": "AdaptiveCard",
                              "version": "1.2",
                              "body": [
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "items": [
                                                  {
                                                      "type": "Image",
                                                      "style": "Person",
                                                      "url": "https://samibotapp8040.blob.core.windows.net/images/Cabra_transparente.png",
                                                      "size": "Medium",
                                                      "horizontalAlignment": "Center",
                                                      "height": "100px"
                                                  }
                                              ],
                                              "width": "auto",
                                              "horizontalAlignment": "Center"
                                          },
                                          {
                                              "type": "Column",
                                              "items": [
                                                  {
                                                      "type": "TextBlock",
                                                      "weight": "Bolder",
                                                      "text": "¿Sabes si el Ancho de banda de tu Internet Hogar es suficiente?\n",
                                                      "horizontalAlignment": "Center",
                                                      "wrap": True,
                                                      "color": "Light",
                                                      "size": "ExtraLarge",
                                                      "spacing": "Small"
                                                  }
                                              ],
                                              "width": "stretch"
                                          }
                                      ]
                                  },
                                  {
                                      "type": "TextBlock",
                                      "text": "¿Qué tan frecuente usas video chat o llamadas? \n",
                                      "horizontalAlignment": "Center",
                                      "weight": "Bolder"
                                  },
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "TextBlock",
                                                      "text": "(Skype, FaceTime, WhatsApp, Messenger, etc) \n",
                                                      "horizontalAlignment": "Center",
                                                      "size": "Small"
                                                  }
                                              ]
                                          }
                                      ]
                                  },
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "ActionSet",
                                                      "actions": [
                                                          {
                                                              "type": "Action.Submit",
                                                              "title": "Nunca",
                                                              "data": {
                                                                  "action": "Q9"
                                                              }
                                                          }
                                                      ]
                                                  }
                                              ]
                                          },
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "ActionSet",
                                                      "actions": [
                                                          {
                                                              "type": "Action.Submit",
                                                              "title": "Rara Vez",
                                                              "data": {
                                                                  "action": "Q10"
                                                              }
                                                          }
                                                      ]
                                                  }
                                              ]
                                          },
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "ActionSet",
                                                      "actions": [
                                                          {
                                                              "type": "Action.Submit",
                                                              "title": "Semanalmente",
                                                              "data": {
                                                                  "action": "Q11"
                                                              }
                                                          }
                                                      ]
                                                  }
                                              ]
                                          },
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "ActionSet",
                                                      "actions": [
                                                          {
                                                              "type": "Action.Submit",
                                                              "title": "Todos los dias",
                                                              "data": {
                                                                  "action": "Q12"
                                                              }
                                                          }
                                                      ]
                                                  }
                                              ]
                                          }
                                      ]
                                  }
                              ]
                          }
                      }
                  ]})


def SendFourthQuestioncard():
    global valor
    webhook = request.get_json(silent=True)

    send_post("https://api.ciscospark.com/v1/messages",
              {
                  "roomId": webhook['data']['roomId'],
                  "markdown": "[Learn more](https://adaptivecards.io) about Adaptive Cards.",
                  "attachments": [
                      {
                          "contentType": "application/vnd.microsoft.card.adaptive",
                          "content": {
                              "type": "AdaptiveCard",
                              "version": "1.2",
                              "body": [
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "items": [
                                                  {
                                                      "type": "Image",
                                                      "style": "Person",
                                                      "url": "https://samibotapp8040.blob.core.windows.net/images/Cabra_transparente.png",
                                                      "size": "Medium",
                                                      "horizontalAlignment": "Center",
                                                      "height": "100px"
                                                  }
                                              ],
                                              "width": "auto",
                                              "horizontalAlignment": "Center"
                                          },
                                          {
                                              "type": "Column",
                                              "items": [
                                                  {
                                                      "type": "TextBlock",
                                                      "weight": "Bolder",
                                                      "text": "¿Sabes si el Ancho de banda de tu Internet Hogar es suficiente?\n",
                                                      "horizontalAlignment": "Center",
                                                      "wrap": True,
                                                      "color": "Light",
                                                      "size": "ExtraLarge",
                                                      "spacing": "Small"
                                                  }
                                              ],
                                              "width": "stretch"
                                          }
                                      ]
                                  },
                                  {
                                      "type": "TextBlock",
                                      "text": "¿Qué tan frecuente usas aplicaciones de audio por streaming? \n",
                                      "horizontalAlignment": "Center",
                                      "weight": "Bolder"
                                  },
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "TextBlock",
                                                      "text": "(Spotify, Apple Music, Deezer, Youtube Music, etc) \n\n",
                                                      "horizontalAlignment": "Center",
                                                      "size": "Small"
                                                  }
                                              ]
                                          }
                                      ]
                                  },
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "ActionSet",
                                                      "actions": [
                                                          {
                                                              "type": "Action.Submit",
                                                              "title": "Nunca",
                                                              "data": {
                                                                  "action": "Q13"
                                                              }
                                                          }
                                                      ]
                                                  }
                                              ]
                                          },
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "ActionSet",
                                                      "actions": [
                                                          {
                                                              "type": "Action.Submit",
                                                              "title": "Rara Vez",
                                                              "data": {
                                                                  "action": "Q14"
                                                              }
                                                          }
                                                      ]
                                                  }
                                              ]
                                          },
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "ActionSet",
                                                      "actions": [
                                                          {
                                                              "type": "Action.Submit",
                                                              "title": "Semanalmente",
                                                              "data": {
                                                                  "action": "Q15"
                                                              }
                                                          }
                                                      ]
                                                  }
                                              ]
                                          },
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "ActionSet",
                                                      "actions": [
                                                          {
                                                              "type": "Action.Submit",
                                                              "title": "Todos los dias",
                                                              "data": {
                                                                  "action": "Q16"
                                                              }
                                                          }
                                                      ]
                                                  }
                                              ]
                                          }
                                      ]
                                  }
                              ]
                          }
                      }
                  ]})


def SendFifthQuestioncard():
    global valor
    webhook = request.get_json(silent=True)

    send_post("https://api.ciscospark.com/v1/messages",
              {
                  "roomId": webhook['data']['roomId'],
                  "markdown": "[Learn more](https://adaptivecards.io) about Adaptive Cards.",
                  "attachments": [
                      {
                          "contentType": "application/vnd.microsoft.card.adaptive",
                          "content": {
                              "type": "AdaptiveCard",
                              "version": "1.2",
                              "body": [
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "items": [
                                                  {
                                                      "type": "Image",
                                                      "style": "Person",
                                                      "url": "https://samibotapp8040.blob.core.windows.net/images/Cabra_transparente.png",
                                                      "size": "Medium",
                                                      "horizontalAlignment": "Center",
                                                      "height": "100px"
                                                  }
                                              ],
                                              "width": "auto",
                                              "horizontalAlignment": "Center"
                                          },
                                          {
                                              "type": "Column",
                                              "items": [
                                                  {
                                                      "type": "TextBlock",
                                                      "weight": "Bolder",
                                                      "text": "¿Sabes si el Ancho de banda de tu Internet Hogar es suficiente?\n",
                                                      "horizontalAlignment": "Center",
                                                      "wrap": True,
                                                      "color": "Light",
                                                      "size": "ExtraLarge",
                                                      "spacing": "Small"
                                                  }
                                              ],
                                              "width": "stretch"
                                          }
                                      ]
                                  },
                                  {
                                      "type": "TextBlock",
                                      "text": "¿Qué tan frecuente juegas en línea desde casa?\n",
                                      "horizontalAlignment": "Center",
                                      "weight": "Bolder"
                                  },
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "TextBlock",
                                                      "text": "(Call of Duty, Battlefield, World of Warcraft, League of Legends, etc) \n\n",
                                                      "horizontalAlignment": "Center",
                                                      "size": "Small"
                                                  }
                                              ]
                                          }
                                      ]
                                  },
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "ActionSet",
                                                      "actions": [
                                                          {
                                                              "type": "Action.Submit",
                                                              "title": "Nunca",
                                                              "data": {
                                                                  "action": "Q17"
                                                              }
                                                          }
                                                      ]
                                                  }
                                              ]
                                          },
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "ActionSet",
                                                      "actions": [
                                                          {
                                                              "type": "Action.Submit",
                                                              "title": "Rara Vez",
                                                              "data": {
                                                                  "action": "Q18"
                                                              }
                                                          }
                                                      ]
                                                  }
                                              ]
                                          },
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "ActionSet",
                                                      "actions": [
                                                          {
                                                              "type": "Action.Submit",
                                                              "title": "Semanalmente",
                                                              "data": {
                                                                  "action": "Q19"
                                                              }
                                                          }
                                                      ]
                                                  }
                                              ]
                                          },
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "ActionSet",
                                                      "actions": [
                                                          {
                                                              "type": "Action.Submit",
                                                              "title": "Todos los dias",
                                                              "data": {
                                                                  "action": "Q20"
                                                              }
                                                          }
                                                      ]
                                                  }
                                              ]
                                          }
                                      ]
                                  }
                              ]
                          }
                      }
                  ]})


def SendSixthQuestioncard():
    global valor
    webhook = request.get_json(silent=True)

    send_post("https://api.ciscospark.com/v1/messages",
              {
                  "roomId": webhook['data']['roomId'],
                  "markdown": "[Learn more](https://adaptivecards.io) about Adaptive Cards.",
                  "attachments": [
                      {
                          "contentType": "application/vnd.microsoft.card.adaptive",
                          "content": {
                              "type": "AdaptiveCard",
                              "version": "1.2",
                              "body": [
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "items": [
                                                  {
                                                      "type": "Image",
                                                      "style": "Person",
                                                      "url": "https://samibotapp8040.blob.core.windows.net/images/Cabra_transparente.png",
                                                      "size": "Medium",
                                                      "horizontalAlignment": "Center",
                                                      "height": "100px"
                                                  }
                                              ],
                                              "width": "auto",
                                              "horizontalAlignment": "Center"
                                          },
                                          {
                                              "type": "Column",
                                              "items": [
                                                  {
                                                      "type": "TextBlock",
                                                      "weight": "Bolder",
                                                      "text": "¿Sabes si el Ancho de banda de tu Internet Hogar es suficiente?\n",
                                                      "horizontalAlignment": "Center",
                                                      "wrap": True,
                                                      "color": "Light",
                                                      "size": "ExtraLarge",
                                                      "spacing": "Small"
                                                  }
                                              ],
                                              "width": "stretch"
                                          }
                                      ]
                                  },
                                  {
                                      "type": "TextBlock",
                                      "text": "¿Qué tan frecuente ves televisión o películas en línea?\n",
                                      "horizontalAlignment": "Center",
                                      "weight": "Bolder"
                                  },
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "TextBlock",
                                                      "text": "(Netflix, Amazon Prime, Disney +, HBO GO etc) \n\n",
                                                      "horizontalAlignment": "Center",
                                                      "size": "Small"
                                                  }
                                              ]
                                          }
                                      ]
                                  },
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "ActionSet",
                                                      "actions": [
                                                          {
                                                              "type": "Action.Submit",
                                                              "title": "Nunca",
                                                              "data": {
                                                                  "action": "Q21"
                                                              }
                                                          }
                                                      ]
                                                  }
                                              ]
                                          },
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "ActionSet",
                                                      "actions": [
                                                          {
                                                              "type": "Action.Submit",
                                                              "title": "Rara Vez",
                                                              "data": {
                                                                  "action": "Q22"
                                                              }
                                                          }
                                                      ]
                                                  }
                                              ]
                                          },
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "ActionSet",
                                                      "actions": [
                                                          {
                                                              "type": "Action.Submit",
                                                              "title": "Semanalmente",
                                                              "data": {
                                                                  "action": "Q23"
                                                              }
                                                          }
                                                      ]
                                                  }
                                              ]
                                          },
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "ActionSet",
                                                      "actions": [
                                                          {
                                                              "type": "Action.Submit",
                                                              "title": "Todos los dias",
                                                              "data": {
                                                                  "action": "Q24"
                                                              }
                                                          }
                                                      ]
                                                  }
                                              ]
                                          }
                                      ]
                                  }
                              ]
                          }
                      }
                  ]})


def SendSeventhQuestioncard():
    global valor
    webhook = request.get_json(silent=True)

    send_post("https://api.ciscospark.com/v1/messages",
              {
                  "roomId": webhook['data']['roomId'],
                  "markdown": "[Learn more](https://adaptivecards.io) about Adaptive Cards.",
                  "attachments": [
                      {
                          "contentType": "application/vnd.microsoft.card.adaptive",
                          "content": {
                              "type": "AdaptiveCard",
                              "version": "1.2",
                              "body": [
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "items": [
                                                  {
                                                      "type": "Image",
                                                      "style": "Person",
                                                      "url": "https://samibotapp8040.blob.core.windows.net/images/Cabra_transparente.png",
                                                      "size": "Medium",
                                                      "horizontalAlignment": "Center",
                                                      "height": "100px"
                                                  }
                                              ],
                                              "width": "auto",
                                              "horizontalAlignment": "Center"
                                          },
                                          {
                                              "type": "Column",
                                              "items": [
                                                  {
                                                      "type": "TextBlock",
                                                      "weight": "Bolder",
                                                      "text": "¿Sabes si el Ancho de banda de tu Internet Hogar es suficiente?\n",
                                                      "horizontalAlignment": "Center",
                                                      "wrap": True,
                                                      "color": "Light",
                                                      "size": "ExtraLarge",
                                                      "spacing": "Small"
                                                  }
                                              ],
                                              "width": "stretch"
                                          }
                                      ]
                                  },
                                  {
                                      "type": "TextBlock",
                                      "text": "¿Qué tan frecuente realizas carga o descarga de archivos?\n",
                                      "horizontalAlignment": "Center",
                                      "weight": "Bolder"
                                  },
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "TextBlock",
                                                      "text": "(Torrents,  Drive, Dropbox, icloud, etc) \n\n",
                                                      "horizontalAlignment": "Center",
                                                      "size": "Small"
                                                  }
                                              ]
                                          }
                                      ]
                                  },
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "ActionSet",
                                                      "actions": [
                                                          {
                                                              "type": "Action.Submit",
                                                              "title": "Nunca",
                                                              "data": {
                                                                  "action": "Q25"
                                                              }
                                                          }
                                                      ]
                                                  }
                                              ]
                                          },
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "ActionSet",
                                                      "actions": [
                                                          {
                                                              "type": "Action.Submit",
                                                              "title": "Rara Vez",
                                                              "data": {
                                                                  "action": "Q26"
                                                              }
                                                          }
                                                      ]
                                                  }
                                              ]
                                          },
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "ActionSet",
                                                      "actions": [
                                                          {
                                                              "type": "Action.Submit",
                                                              "title": "Semanalmente",
                                                              "data": {
                                                                  "action": "Q27"
                                                              }
                                                          }
                                                      ]
                                                  }
                                              ]
                                          },
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "ActionSet",
                                                      "actions": [
                                                          {
                                                              "type": "Action.Submit",
                                                              "title": "Todos los dias",
                                                              "data": {
                                                                  "action": "Q28"
                                                              }
                                                          }
                                                      ]
                                                  }
                                              ]
                                          }
                                      ]
                                  }
                              ]
                          }
                      }
                  ]})


def SendOctQuestioncard():
    global valor
    webhook = request.get_json(silent=True)

    send_post("https://api.ciscospark.com/v1/messages",
              {
                  "roomId": webhook['data']['roomId'],
                  "markdown": "[Learn more](https://adaptivecards.io) about Adaptive Cards.",
                  "attachments": [
                      {
                          "contentType": "application/vnd.microsoft.card.adaptive",
                          "content": {
                              "type": "AdaptiveCard",
                              "version": "1.2",
                              "body": [
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "items": [
                                                  {
                                                      "type": "Image",
                                                      "style": "Person",
                                                      "url": "https://samibotapp8040.blob.core.windows.net/images/Cabra_transparente.png",
                                                      "size": "Medium",
                                                      "horizontalAlignment": "Center",
                                                      "height": "100px"
                                                  }
                                              ],
                                              "width": "auto",
                                              "horizontalAlignment": "Center"
                                          },
                                          {
                                              "type": "Column",
                                              "items": [
                                                  {
                                                      "type": "TextBlock",
                                                      "weight": "Bolder",
                                                      "text": "¿Sabes si el Ancho de banda de tu Internet Hogar es suficiente?\n",
                                                      "horizontalAlignment": "Center",
                                                      "wrap": True,
                                                      "color": "Light",
                                                      "size": "ExtraLarge",
                                                      "spacing": "Small"
                                                  }
                                              ],
                                              "width": "stretch"
                                          }
                                      ]
                                  },
                                  {
                                      "type": "TextBlock",
                                      "text": "¿Qué tan frecuente usas aplicaciones para videoconferencia? \n",
                                      "horizontalAlignment": "Center",
                                      "weight": "Bolder"
                                  },
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "TextBlock",
                                                      "text": "(Webex Teams, Microsoft Teams, Zoom, Google Meet, etc)  \n\n",
                                                      "horizontalAlignment": "Center",
                                                      "size": "Small"
                                                  }
                                              ]
                                          }
                                      ]
                                  },
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "ActionSet",
                                                      "actions": [
                                                          {
                                                              "type": "Action.Submit",
                                                              "title": "Nunca",
                                                              "data": {
                                                                  "action": "Q29"
                                                              }
                                                          }
                                                      ]
                                                  }
                                              ]
                                          },
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "ActionSet",
                                                      "actions": [
                                                          {
                                                              "type": "Action.Submit",
                                                              "title": "Rara Vez",
                                                              "data": {
                                                                  "action": "Q30"
                                                              }
                                                          }
                                                      ]
                                                  }
                                              ]
                                          },
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "ActionSet",
                                                      "actions": [
                                                          {
                                                              "type": "Action.Submit",
                                                              "title": "Semanalmente",
                                                              "data": {
                                                                  "action": "Q31"
                                                              }
                                                          }
                                                      ]
                                                  }
                                              ]
                                          },
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "ActionSet",
                                                      "actions": [
                                                          {
                                                              "type": "Action.Submit",
                                                              "title": "Todos los dias",
                                                              "data": {
                                                                  "action": "Q32"
                                                              }
                                                          }
                                                      ]
                                                  }
                                              ]
                                          }
                                      ]
                                  }
                              ]
                          }
                      }
                  ]})


def SendFinishEncuesta(number):
    global valor
    webhook = request.get_json(silent=True)

    send_post("https://api.ciscospark.com/v1/messages",
              {
                  "roomId": webhook['data']['roomId'],
                  "markdown": "[Learn more](https://adaptivecards.io) about Adaptive Cards.",
                  "attachments": [
                      {
                          "contentType": "application/vnd.microsoft.card.adaptive",
                          "content": {
                              "type": "AdaptiveCard",
                              "version": "1.2",
                              "body": [
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "items": [
                                                  {
                                                      "type": "Image",
                                                      "style": "Person",
                                                      "url": "https://samibotapp8040.blob.core.windows.net/images/Cabra_transparente.png",
                                                      "size": "Medium",
                                                      "height": "100px"
                                                  }
                                              ],
                                              "width": "auto"
                                          },
                                          {
                                              "type": "Column",
                                              "items": [
                                                  {
                                                      "type": "TextBlock",
                                                      "weight": "Bolder",
                                                      "text": "¿Sabes si el Ancho de banda de tu Internet Hogar es suficiente?\n",
                                                      "horizontalAlignment": "Left",
                                                      "wrap": True,
                                                      "color": "Light",
                                                      "size": "ExtraLarge"
                                                  }
                                              ],
                                              "width": "stretch"
                                          }
                                      ]
                                  },
                                  {
                                      "type": "TextBlock",
                                      "text": "El mínimo ancho de banda requerido para el uso de tus aplicaciones en casa es:\n",
                                      "wrap": True,
                                      "horizontalAlignment": "Center",
                                      "weight": "Bolder"
                                  },
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "horizontalAlignment": "Center",
                                              "items": [
                                                  {
                                                      "type": "TextBlock",
                                                      "text": str(number),
                                                      "horizontalAlignment": "Right",
                                                      "color": "Warning",
                                                      "size": "ExtraLarge",
                                                      "weight": "Bolder"
                                                  }
                                              ]
                                          },
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "TextBlock",
                                                      "text": "Mbps",
                                                      "horizontalAlignment": "Left",
                                                      "size": "ExtraLarge",
                                                      "weight": "Bolder"
                                                  }
                                              ]
                                          }
                                      ],
                                      "horizontalAlignment": "Center",
                                      "minHeight": "10px"
                                  },
                                  {
                                      "type": "ColumnSet",
                                      "columns": [
                                          {
                                              "type": "Column",
                                              "width": "stretch",
                                              "items": [
                                                  {
                                                      "type": "TextBlock",
                                                      "text": "Revisa con tu operador si cumples, o elije la opción de ",
                                                      "size": "Small",
                                                      "horizontalAlignment": "Center"
                                                  },
                                                  {
                                                      "type": "TextBlock",
                                                      "text": "“Conoce la velocidad de tu Internet” ",
                                                      "horizontalAlignment": "Center",
                                                      "size": "Small",
                                                      "weight": "Bolder"
                                                  }
                                              ]
                                          }
                                      ],
                                      "horizontalAlignment": "Center"
                                  }
                              ]
                          }
                      }
                  ]})


def speedtest(down, up, ping):
    global valor
    webhook = request.get_json(silent=True)

    reque = send_post("https://api.ciscospark.com/v1/messages",
                      {
                          "roomId": webhook['data']['roomId'],
                          "markdown": "[Learn more](https://adaptivecards.io) about Adaptive Cards.",
                          "attachments": [
                              {
                                  "contentType": "application/vnd.microsoft.card.adaptive",
                                  "content": {
                                      "type": "AdaptiveCard",
                                      "version": "1.2",
                                      "body": [
                                          {
                                              "type": "ColumnSet",
                                              "columns": [
                                                  {
                                                      "type": "Column",
                                                      "items": [
                                                          {
                                                              "type": "TextBlock",
                                                              "weight": "Bolder",
                                                              "text": "Tu velocidad de Internet es",
                                                              "horizontalAlignment": "Center",
                                                              "wrap": True,
                                                              "size": "Large",
                                                              "spacing": "Small"
                                                          }
                                                      ],
                                                      "width": "stretch"
                                                  }
                                              ]
                                          },
                                          {
                                              "type": "ColumnSet",
                                              "columns": [
                                                  {
                                                      "type": "Column",
                                                      "width": "stretch",
                                                      "items": [
                                                          {
                                                              "type": "TextBlock",
                                                              "text": "Descarga",
                                                              "horizontalAlignment": "Center",
                                                              "weight": "Bolder",
                                                              "size": "Medium"
                                                          },
                                                          {
                                                              "type": "TextBlock",
                                                              "text": down + " Mb/s",
                                                              "horizontalAlignment": "Center",
                                                              "size": "Large"
                                                          }
                                                      ]
                                                  },
                                                  {
                                                      "type": "Column",
                                                      "width": "stretch",
                                                      "items": [
                                                          {
                                                              "type": "TextBlock",
                                                              "text": "Carga",
                                                              "horizontalAlignment": "Center",
                                                              "weight": "Bolder",
                                                              "size": "Medium"
                                                          },
                                                          {
                                                              "type": "TextBlock",
                                                              "text": up + " Mb/s",
                                                              "horizontalAlignment": "Center",
                                                              "size": "Large"
                                                          }
                                                      ]
                                                  }
                                              ]
                                          },
                                          {
                                              "type": "ColumnSet",
                                              "columns": [
                                                  {
                                                      "type": "Column",
                                                      "width": "stretch",
                                                      "items": [
                                                          {
                                                              "type": "ColumnSet",
                                                              "columns": [
                                                                  {
                                                                      "type": "Column",
                                                                      "width": "stretch",
                                                                      "items": [
                                                                          {
                                                                              "type": "TextBlock",
                                                                              "text": "Ping",
                                                                              "horizontalAlignment": "Center",
                                                                              "weight": "Bolder",
                                                                              "size": "Medium"
                                                                          }
                                                                      ]
                                                                  }
                                                              ]
                                                          },
                                                          {
                                                              "type": "TextBlock",
                                                              "text": ping + " ms",
                                                              "horizontalAlignment": "Center",
                                                              "size": "Large"
                                                          },
                                                          {
                                                              "type": "ColumnSet"
                                                          },
                                                          {
                                                              "type": "TextBlock",
                                                              "text": "Si quieres una segunda opinión, ",
                                                              "horizontalAlignment": "Center"
                                                          },
                                                          {
                                                              "type": "TextBlock",
                                                              "text": "puedes consultar la siguientes opciones",
                                                              "horizontalAlignment": "Center"
                                                          },
                                                          {
                                                              "type": "ActionSet",
                                                              "horizontalAlignment": "Center",
                                                              "actions": [
                                                                  {
                                                                      "type": "Action.OpenUrl",
                                                                      "title": "SpeedTest Secundario",
                                                                      "url": "https://www.speedtest.net/es"
                                                                  }
                                                              ]
                                                          },
                                                          {
                                                              "type": "ActionSet",
                                                              "horizontalAlignment": "Center",
                                                              "actions": [
                                                                  {
                                                                      "type": "Action.OpenUrl",
                                                                      "title": "MediaTest",
                                                                      "url": "https://mediatest.ciscospark.com/#/main"
                                                                  }
                                                              ]
                                                          }
                                                      ]
                                                  }
                                              ]
                                          }
                                      ]
                                  }
                              }
                          ]})

    print("mirar:", reque)


def enviar(msg):
    print("entrar333")
    global valor
    if request.method == 'POST':
        webhook = request.get_json(silent=True)
        # if webhook['data']['personEmail']!= bot_email:
        # pprint(webhook)
        # if webhook['data']['personEmail']== bot_email:
        #    send_post("https://api.ciscospark.com/v1/messages",
        #              {
        #                  "roomId": webhook['data']['roomId'],
        #                  "markdown": (greetings() +
        #                               "**Nota: Por favor has una breve descripción de tu problema y déjanos saber cómo prefieres que te contactemos**")
        #              }
        #              )

        if webhook['resource'] == "memberships" and webhook['data']['personEmail'] == bot_email:
            print("bot")
            # if webhook['data'][
            #    'roomId'] == "Y2lzY29zcGFyazovL3VzL1JPT00vODAxZDZkMDAtODU4OC0xMWVhLTgwMjMtZGQ3MmQ1YjIxNzc0":
            #    print("entras")
            #    prim = second_msg()
            #    send_post("https://api.ciscospark.com/v1/messages",
            #              {
            #                  "roomId": webhook['data']['roomId'],
            #                  "markdown": ("Hola soy %s.<br/>" % bot_name + "Este es el asunto: " + valor)
            #              }
            #              )

            # pprint(webhook['data'])
            send_post("https://api.ciscospark.com/v1/messages",
                      {
                          "roomId": webhook['data']['roomId'],
                          "markdown": (greetings() +
                                       "**Nota: Por favor has una breve descripción de tu problema y déjanos saber cómo prefieres que te contactemos**")
                      }
                      )

def resultEncuesta(list):
    sum = 0
    for x in list:
        sum+=x
    print(sum)
    return sum

def createBat(userId):
    urlsend = "https://botseneca.azurewebsites.net/data"
    print("llega a crear")
    try:
        file = open("/home/site/wwwroot/Archivos/Data_" + userId + ".bat", "w")
        print(file)
        file.write("@echo on" + "\n")
        file.write("set UserId=" + userId + "\n")
        print("escribiendo...")
        file.write("netsh wlan show interface > temp1" + "\n" + "netsh interface ipv4 show address Wi-Fi > temp2" + "\n" +
            "more +3 temp2 > temp" + "\n" + "type temp1 temp > datos.txt" + "\n" + "del /f/q temp1" + "\n" + "del /f/q temp2" + "\n" + "del /f/q temp" + "\n" +
            "echo %~p0" + "\n" + "echo %~dp0" + "\n" + "set var=%~p0" + "\n" + "set var=%var:\=/%" + "\n" + "echo %var%" + "\n" +
            "For /F "'"UseBackQ Tokens=* Delims=."'" %%a In (""datos.txt"") Do (" + "\n" + "       Set /A ""Count+=1" + "\n" + """       Call Set "Var%%Count%%=%%~a""" + "\n" + ")""" + "\n" +
            "set var1=%Var5: =%" + "\n" + "set var2=%Var7: =%" + "\n" + "set var3=%Var10: =%" + "\n" + "set var4=%Var14: =%" + "\n" + "set var5=%Var17: =%" + "\n" +
            "set var6=%Var20: =%" + "\n" + "setlocal EnableDelayedExpansion" + "\n" + "set line2=%var1:*ca:=%" + "\n" + "set line3=%var2:*:=%" + "\n" + "set line4=%var3:*:=%" + "\n" + "set line5=%var4:*:=%" + "\n" +
            "set line6=%var5:*:=%" + "\n" + "set line7=%var6:*:=%" + "\n" + "set line1=!var1:/%line2%=!" + "\n" + "setlocal DisableDelayedExpansion" + "\n" +
            "curl -X POST ^ -H "'"content-type: application/json"'" ^ -d "'"{\\"userId\\":\\"%UserId%\\",\\"mac\\":\\"%line2%\\",\\"ssid\\":\\"%line3%\\",\\"radio\\":\\"%line4%\\",\\"canal\\":\\"%line5%\\",\\"senal\\":\\"%line6%\\",\\"ip\\":\\"%line7%\\"}"'" \ " + urlsend + "\n" +
            "del /f/q datos.txt")
        print("archivo data generado")
        file.close()

        file2 = open("/home/site/wwwroot/Archivos/Install_" + userId + ".bat", "w")
        file2.write("@echo on" + "\n")
        file2.write("echo %~p0" + "\n" + "echo %~dp0" + "\n" + "echo %~1" + "\n" + "set var=%~p0" + "\n" + "set var =%var:\=/%" + "\n" +
            "echo %var%" + "\n" + "MOVE C:%var%Data_" + userId + ".bat /Users/%username%/" + "\n" +
            "schtasks.exe /create /sc MINUTE /mo 2 /tn SenecaTareas /tr /Users/%username%/Data_" + userId + ".bat /st 06:00 /ru SYSTEM" + "\n" +
            "schtasks /run /tn SenecaTareas")

        print("archivo install generado")
        file2.close()
    except Exception as e:
        print(e)
        print("ocurrio algo")

def main():
    global bot_email, bot_name
    if len(bearer_direct) != 0:
        test_auth = send_get("https://api.ciscospark.com/v1/people/me", js=False)
        if test_auth.status_code == 401:
            print("Revisar si el access token es correcto.\n"
                  "Por favor revise la cuenta del bot.\n"
                  "No te preocupes, si perdiste el access token. "
                  "Puedes ingresar a https://developer.webex.com/my-apps "
                  "y generar un nuevo access token.")
            sys.exit()
        if test_auth.status_code == 200:
            test_auth = test_auth.json()
            # bot()
            bot_name = test_auth.get("displayName", "")
            bot_email = test_auth.get("emails", "")[0]
    else:
        print("'bearer' variable esta vacia! \n")
        sys.exit()

    if "@webex.bot" not in bot_email:
        print("No esta relacionado con una cuenta del Bot.\n")
        sys.exit()
    #else:
    #    app.run(host='0.0.0.0', port=8091, threaded=True)


#if __name__ == "__main__":
main()
