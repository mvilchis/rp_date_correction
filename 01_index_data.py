#! /usr/bin/env python
# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch
import os
INDEX_SETTINGS = { "settings":{
                        "analysis": {
                            "filter": {
                                "dbl_metaphone"  : {  "type":"phonetic","encoder": "double_metaphone","languageset":"spanish"}
                            },
                            "analyzer": {
                                "dbl_metaphone": { "tokenizer": "standard", "filter":    "dbl_metaphone"}
                            }
                        }
                    }
                }



NUMBERS = {'primero':1, 'segundo':2, 'tercero':3, 'cuarto':4,
           'uno':1, 'dos':2, 'tres':3, 'cuatro':4, 'cinco':5,
           'seis':6, 'siete': 7, 'ocho':8, 'nueve':9, 'diez':10,
           'once':11, 'doce':12, 'trece':13, 'catorce':14, 'quince':15,
           'dieciseis':16, 'diecisiete':17, 'dieciocho':18,
           'diecinueve':19, 'veinte':20, 'ventiuno':21, 'veintidos':22,
           'veintitres':23, 'veinticuatro':24, 'veinticinco':25, 'veintiseis':26,
           'veintisiete':27, 'veintiocho':28, 'veintinueve':29, 'treinta':30, 'treinta y uno':31}

MONTHS  =  {'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5,
            'junio': 6, 'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10,
            'noviembre': 11, 'diciembre': 12}

def main():
    elastic_port = int(os.getenv('ELASTIC_PORT',9200))
    elastic_ip = os.getenv('ELASTIC_IP','localhost')
    elasticsearch_url = "{ip}:{port}"
    es = Elasticsearch([elasticsearch_url.format(ip=elastic_ip, port=elastic_port)])
    es.indices.delete(index='fechas', ignore=[400, 404])
    es.indices.create(index = 'fechas', body = INDEX_SETTINGS)
    for key in NUMBERS.keys():
        es.index(index = 'fechas', doc_type = 'fecha', body = {'name':key, 'number': NUMBERS[key]})
    for key in MONTHS.keys():
        es.index(index = 'fechas', doc_type = 'fecha', body = {'name':key, 'number': MONTHS[key]})

main()
