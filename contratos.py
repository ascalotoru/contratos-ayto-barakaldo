from pymongo import MongoClient
from dotenv import load_dotenv
import requests
import os

load_dotenv()

URL = 'https://www.contratacion.euskadi.eus/ac70cPublicidadWar/serviciosWidgetREST/recuperarContratos/?tipoWidget=2&idioma=es&idPoder=171&idEntidad=&estadoContrato=&tipoContrato=&contratosMenores=&R01HNoPortal=true'

client = MongoClient(host="127.0.0.1", port=27017, username=os.getenv('MONGO_USER'), password=os.getenv('MONGO_PASSWORD'))
aytobarakaldo = client.aytobarakaldo
contratos = aytobarakaldo.contratos

j = requests.get(URL).json()
lista_contratos = j['lista']
for c in lista_contratos:
  cod_contrato = c['valores'][0]['valor']
  objecto_contrato = c['valores'][1]['valor']
  importe_con_iva = c['valores'][2]['valor']
  link = c['link']

  if contratos.find_one({"cod_contrato": cod_contrato}):
    print("El contrato ya está en la BBDD. No hacemos nada.")
    continue

  new_con = {
    "cod_contrato": cod_contrato,
    "objeto_contrato": objecto_contrato,
    "importe_con_iva": importe_con_iva,
    "link": link,
  }
  contratos.insert_one(new_con)


