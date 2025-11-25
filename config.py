#!/usr/bin/env python3
import mysql.connector
from mysql.connector import Error

def conectar_banco():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="SellArt"
        )
        return conn
    except Error as erro:
        print("Erro ao conectar ao banco de dados:", erro)









