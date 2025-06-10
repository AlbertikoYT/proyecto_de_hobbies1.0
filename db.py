from pymongo import MongoClient
from dotenv import load_dotenv
import os
import certifi

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI") 
ca = certifi.where()

def dbConnection():
    try:
        client = MongoClient(MONGO_URI, tlsCAFile=ca)
        db = client["hobbies"]
        return db
    except Exception as e:
        print("Error en la conexión a la base de datos:", e)
        return None

# 🔧 Solución aquí:
db = dbConnection()
if db is not None:
    hobbies_collection = db["hobbies"]
else:
    hobbies_collection = None
