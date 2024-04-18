from sllurp.reader import R420
from sllurp import llrp
import time
import re
from datetime import datetime, timezone, timedelta
import pandas as pd


# La funcion parse_string recibe los datos crudos del Impinj, los limpea, los formatea, y lo divide por categorias
def parse_string(data):
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
    return extracted_data

reader = R420('192.168.0.20') #Conecta el Impinj R420 a su direccion IP


freqs = reader.freq_table #Establece la frecuencia del R420
powers = reader.power_table #Establece la frecuencia del R420
columnas_df = ['RFID','Registro de Tiempo (UNIX)','Registro de Tiempo (UTC-05)','PhaseAngle','RSSI'] # Nombre de las columnas para el Dataframe
df = pd.DataFrame(columns=columnas_df) # Inicia un DataFrame vacio
while True: # Loop infinito
    tags = reader.detectTags(powerDBm=powers[-1], freqMHz=freqs[0], #Lee las etiquetas alrededor usando LLRP
        mode=1002, session=2, population=1, duration=0.5, searchmode=2)
    for tag in tags: # Para cada etiqueta que se leyo
        tagstr = str(tag) #Conviete el output a un String
        datos = parse_string(tagstr) #Aplica la funcion para formatear los datos
        df.loc[len(df)] = datos #Inserta los datos al dataframe
        print(df) # Imprime los datos hacia la consola
    time.sleep(3) #Espera 3 segundos para repetir
