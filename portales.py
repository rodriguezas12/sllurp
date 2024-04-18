from sllurp.reader import R420
from sllurp import llrp
import time
import re
from datetime import datetime, timezone, timedelta
import socket
import pickle


# La funcion parse_string recibe los datos crudos del Impinj, los limpea, los formatea, y lo divide por categorias
def parse_string(data,ant):
    res = re.split(r',', data) # separa el string en una lista basado en las comas
    res = res[1:] # quita la primera entrada (es irrelevante)
    res = [item.replace('{', '').replace('}', '') for item in res] #quita los corchetes
    extracted_data = [item.split(':')[1].strip() for item in res] #solamente entrega los strings despues del :
    timestamp_unix = int(extracted_data[1]) #Convierte el string de tiempo formato epoch a un int
    timestamp_unix_seconds = int(timestamp_unix/1000000) # Convierte el tiempo de microsegundos a segundos
    timestamp_utc = datetime.fromtimestamp(timestamp_unix_seconds, tz=timezone.utc) # Conviete el tiempo de UNIX a UTC
    timestamp_et = timestamp_utc.astimezone(timezone(timedelta(hours=-5)))  # Conviete el tiempo a la hora ET
    formatted_timestamp_et = timestamp_et.strftime('%Y-%m-%d %H:%M:%S %Z') #Formatea el tiempo a una forma legible
    extracted_data.insert(2, formatted_timestamp_et) # inserta el string anterior a la lista
    extracted_data.insert(0,'Portales')
    extracted_data.append(ant)
    return extracted_data

readerEntrada = R420('192.168.0.44') #Conecta el Impinj R420 a su direccion IP
readerSalida = R420('192.168.0.42')

freqsEntrada = readerEntrada.freq_table #Establece la frecuencia del R420
powersEntrada = readerEntrada.power_table #Establece la frecuencia del R420
freqsSalida = readerSalida.freq_table #Establece la frecuencia del R420
powersSalida = readerSalida.power_table #Establece la frecuencia del R420

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receiver_address = ('192.168.0.105', 55550)
s.connect(receiver_address)

try:
    while True: # Loop infinito
        tagsEntrada = readerEntrada.detectTags(powerDBm=powersEntrada[-1], freqMHz=freqsEntrada[0], #Lee las etiquetas alrededor usando LLRP
            mode=1002, session=2, population=1, duration=0.5, searchmode=2)
        tagsSalida = readerSalida.detectTags(powerDBm=powersEntrada[-1], freqMHz=freqsEntrada[0], #Lee las etiquetas alrededor usando LLRP
            mode=1002, session=2, population=1, duration=0.5, searchmode=2)
        for tag in tagsEntrada: # Para cada etiqueta que se leyo
            tagstr = str(tag) #Conviete el output a un String
            datosEntrada = parse_string(tagstr,'Entrada') #Aplica la funcion para formatear los datos
            entradaAlServidor = pickle.dumps(datosEntrada)
            s.send(entradaAlServidor)
        for tag in tagsSalida:
            tagstr = str(tag)
            datosSalida = parse_string(tagstr,'Salida')
            salidaAlServidor = pickle.dumps(datosSalida)
            s.send(salidaAlServidor)
        time.sleep(1) #Espera 3 segundos para repetir

finally:
    s.close()
