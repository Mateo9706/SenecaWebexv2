import json
import re

#import netifaces
import requests
from flask import request
from speedtest import Speedtest
#from app import *
from Red.ConvertDbm import *

filename = './Archivos/datos.txt'
listaretorn = []
dict1 = {}
protoc = ["802.11a","802.11b","802.11g","802.11n","802.11ac","802.11ax"]
bandWidth = ["5GHz","2.4GHz","2.4GHz","2.4GHz-5GHz","5GHz", "5GHz"]
channels = [1,2,3,4,5,6,7,8,9,10,11]

# creating dictionary
def dictionay():

    with open(filename) as fh:
        lis = []
        for line in fh:
            wh= line.strip().split('\r\n')

            d = {}
            for line in wh:
                if ': ' in line:
                    vals = line.split(': ')
                    #print(vals)
                    if vals[0].strip() != '' and vals[1].strip() != '':
                        d[vals[0].strip()] = vals[1].strip()


            for key in d.keys():
                #print(key)

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
                    bandFreqG = returnBandWidth(listaretorn[2],canal)
                    listaretorn.append(canal)
                    listaretorn.append(bandFreqG)
                if key == "Direcci¢n f¡sica":
                    mac = d[key].replace(": ","")
                    print(mac)
                    listaretorn.append(mac)
                if key == "Se¤al":
                    signal = d[key]
                    print(d[key])
                    listaretorn.append(signal)
                    dbm = convert(signal)
                    listaretorn.append(dbm)
                    #listaretorn.append("null") # ip

                if key == "Direcci¢n IP":
                    ip = d[key]
                    print(ip)
                    listaretorn.append(ip)
                    listaretorn.append("Wi-Fi")

                print(listaretorn)
    return listaretorn

def returnBandWidth(proto, channel):

    band = ""

    if proto == protoc[0]:
        return bandWidth[0]
    elif proto == protoc[1]:
        return bandWidth[1]
    elif proto == protoc[2]:
        return bandWidth[2]
    elif proto == protoc[3]:
        for x in channels:
            if int(channel) == x:
                return "2.4GHz"
            elif int(channel) > 11:
                return "5GHz"
        #return bandWidth[3]
    elif proto == protoc[4]:
        return bandWidth[4]
    elif proto == protoc[5]:
        return bandWidth[5]
    else:
        print("no encontro")

    return band

def SpeedTest():
    #espera()
    source = "191.102.192.0"
    #s = speedtest.Speedtest(source_address=source)
    s = Speedtest()
    #s.get_best_server(s.set_mini_server("https://www.speedtest.net/es"))

    #s.get_servers()

    #s.get_best_server()
    #print(s.get_servers())
    s.download()
    s.upload()
    res = s.results.dict()
    print(res["download"], res["upload"], res["ping"])
    return res["download"], res["upload"], res["ping"]

def returnSpeed():
    sef = ""
    d, u, p = SpeedTest()

    #print('Test #{}\n'.format(i+1))
    download = round(d/(10**8),2)
    upload = round(u/(10**8),2)
    down = "<strong>Download(Mbps):</strong> " + str(download)
    up = "<strong>Upload(Mbps):</strong> " + str(upload)

    #print('Download: \n', download)
    #print('Upload: \n', upload)
    #print('Ping: {}\n'.format(p))
    sef += "Tu conexion es la siguiente: " + "\n\n" + down + "\n\n" + up + "\n\n" + str(p)
    print(sef)
    return str(download), str(upload), str(p)

#dictionay()
