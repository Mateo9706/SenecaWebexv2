import os
import pyodbc
import datetime

direccion_servidor = 'dbcol.database.windows.net'
nombre_bd = 'SAMICHATDB_PROD'
nombre_usuario = 'azuredbadmin'
password = '4zur3DB@dm1n'

def conexions():
    try:
        conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+direccion_servidor + ';DATABASE=' + nombre_bd + ';UID=' + nombre_usuario + ';PWD=' + password)

        print("entro")

    except Exception as e:
        print("Ocurrió un error al conectar a SQL Server: ", e)

    return conexion


def receiveData(userId, mac, ssid, tiporadio,canal,señal,ip):
    print(userId, mac, ssid, tiporadio,canal,señal,ip)
    try:

        conex = conexions()
        with conex.cursor() as cursor:
            #DT_FECHA = datetime.now()

            consulta = "INSERT INTO dbo.DataNetworkClientSeneca(UserIdTeams,SSID, TypeRadio,Channel,MAC,Signal,IP,Dates) VALUES (?, ?, ?, ?, ?, ?, ?, ?);"
            cursor.execute(consulta, (userId,ssid,tiporadio,canal,mac,señal,ip,datetime.datetime.now()))
            print("guardo")
    except Exception as e:
        print("Ocurrió un error al insertar: ", e)
    finally:
        print("")
        conex.close()
    return

def selects(userid):
    print("")
    try:

        conex = conexions()
        with conex.cursor() as cursor:
            #DT_FECHA = datetime.now()

            consulta = "SELECT * FROM dbo.DataNetworkClientSeneca WHERE UserIdTeams='"+userid+"' AND Dates = (SELECT MAX(Dates) from dbo.DataNetworkClientSeneca)"
            cursor.execute(consulta)
            print("select")
            #print(cursor.fetchall())
            for fl in cursor.fetchall():
                #print(fl[3])
                return fl
                #if fl[1] == userid:
                #    print("son iguales en bd")
                #    return True
                #else:
                #    return False


    except Exception as e:
        print("Ocurrió un error al insertar: ", e)
    finally:
        print("")
        conex.close()
    return

#conexions()

#selects("Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mYWM0MTY2OC1jYTUwLTRhMDUtYjMzOS1hNTliMzZiYjQ0OGM")
