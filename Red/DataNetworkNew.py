import json
import re

#import netifaces
import requests
from flask import request
from speedtest import Speedtest
from app import *
from Red.ConvertDbm import *
from BD.SaveDataNetworkClient import *


listaretorn = []
dict1 = {}
protoc = ["802.11a","802.11b","802.11g","802.11n","802.11ac","802.11ax"]
bandWidth = ["5GHz","2.4GHz","2.4GHz","2.4GHz-5GHz","5GHz", "5GHz"]
channels = [1,2,3,4,5,6,7,8,9,10,11]
"""
def dictionay(userId):
    val,iduser, nameFile = validarArchivoUser()
    filename = 'C:/Users/cmb585103/Desktop/SenecaWebex/Archivos/'+nameFile+'.txt'
    #print(iduser)
    if iduser == userId:
        print("son iguales")
        with open(filename) as fh:
            lis = []
            for line in fh:
                wh = line.strip().split('\r\n')

                d = {}
                for line in wh:
                    if ': ' in line:
                        vals = line.split(': ')
                        #print(vals)
                        if vals[0].strip() != '' and vals[1].strip() != '':
                            d[vals[0].strip()] = vals[1].strip()

                for key in d.keys():

                    if key == "SSID":
                        ssid = d[key]
                        print(ssid)
                        listaretorn.append(ssid)
                    if key == "Tipo de radio":
                        bandFreq = d[key]
                        print(bandFreq)
                        listaretorn.append(bandFreq)
                    if key == "Canal":
                        canal = d[key]
                        print(canal)
                        # bandFreqG = returnBandWidth(listaretorn[2],canal)
                        listaretorn.append(canal)
                        # listaretorn.append(bandFreqG)
                    if key == "Direcci¢n f¡sica":
                        mac = d[key].replace(": ", "")
                        print(mac)
                        listaretorn.append(mac)
                    if key == "Se¤al":
                        signal = d[key]
                        print(d[key])
                        listaretorn.append(signal)
                        # dbm = convert(signal)
                        # listaretorn.append(dbm)
                        # listaretorn.append("null") # ip

                    if key == "Direcci¢n IP":
                        ip = d[key]
                        print(ip)
                        listaretorn.append(ip)
                        #listaretorn.append("Wi-Fi")
                    #print(listaretorn)
    confirmacion = selects(userId)
    #if confirmacion == True:
    #    print("validado en bd, no guarda")
    #else:
    #    print("Ya esta guardado")

    #receiveData(userId,listaretorn[0], listaretorn[1], listaretorn[2], listaretorn[3], listaretorn[4], listaretorn[5])



    #return listaretorn
"""
def validarArchivoUser(user):
    print("entra")
    try:
        validat = selects(user)
        if validat[1] == user:
            return True
        else:
            return False

        """
        path = "C:/Users/cmb585103/Desktop/SenecaWebex/Archivos"
        lstDir = os.walk(path)
        # conversion()
        for root, dirs, files in lstDir:
            for fichero in files:
                (nombreFichero, extension) = os.path.splitext(fichero)
                #print(nombreFichero)
                userId = nombreFichero.split("_")
                #print(userId[1])

                if (extension == ".txt" and nombreFichero == "datos_"+userId):
                    status = True
                    print("Estado txt",status)
                    return status, userId[1], nombreFichero
                else:
                    status = False
                    #SendFile()
                    print("Estado txt",status)
                    return status
            """
    except:
        print("error")
        #SendFile()
        #print("No esta datos.txt", status)


def validar(ids):
    try:
        validat = selects(ids)
        print(validat)
        if validat[1] == ids:
            return True
        #elif validat == None:
        #    return False
        else:
            return False
        """
        path = "C:/Users/cmb585103/Desktop/SenecaWebex/Archivos"
        lstDir = os.walk(path)
        # conversion()
        for root, dirs, files in lstDir:
            for fichero in files:
                (nombreFichero, extension) = os.path.splitext(fichero)
                # print(nombreFichero)
                userId = nombreFichero.split("_")
                #print(userId[1])
                if userId[1] == ids:
                    print("NO SE REQUIERE DESCARGAR ARCHIVO")
                    return True
                else:
                    print("SE REQUIERE DESCARGAR")
                    return False
                    #SendFile()
                """

    except:
        print("error")
        return False

#validar("Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mYWM0MTY2OC1jYTUwLTRhMDUtYjMzOS1hNTliMzZiYjQ0OGM")
#validarArchivoUser()
#dictionay("Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mYWM0MTY2OC1jYTUwLTRhMDUtYjMzOS1hNTliMzZiYjQ0OGM")