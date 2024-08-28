import os
import firebase_admin
from firebase_admin import credentials, firestore
from utils import to_thread
# from cachetools import cached, TTLCache
from google.cloud.exceptions import NotFound
import logging


# firebase database connection

if os.getenv("FIREBASE_PATH"):
  cred = credentials.Certificate(os.getenv("FIREBASE_PATH"))
  firebase_admin.initialize_app(cred)
  db = firestore.client()
else:
  logging.error("No FIREBASE_PATH in environment variables. Exiting...")
  exit()

# CACHE = TTLCache(maxsize=100, ttl=300)

class Database():
  def __init__(self):
    pass

  def _get(self, collection, doc):
    return db.collection(collection).document(doc).get().to_dict()
  
  def _set(self, collection, doc, data):
    return db.collection(collection).document(doc).set(data)
  
  def _update(self, collection, doc, data):
    try:
      return db.collection(collection).document(doc).update(data)
    except NotFound:
      # create
      logging.error(f"Document {doc} not found in collection {collection}. Creating new...")
      return db.collection(collection).document(doc).set(data)

      
  
  def _delete(self, collection, doc):
    return db.collection(collection).document(doc).delete()
  
  def _getall(self, collection):
    res = db.collection(collection).stream()
    return [{**doc.to_dict(), "id": doc.id} for doc in res]
  
  def _query(self, collection, field, operator, value):
    return db.collection(collection).where(field, operator, value).get()
  
  @to_thread
  def get(self, collection, doc):
    return self._get(collection, doc)
  
  @to_thread
  def set(self, collection, doc, data):
    return self._set(collection, doc, data)
  
  @to_thread
  def update(self, collection, doc, data):
    return self._update(collection, doc, data)
  
  @to_thread
  def delete(self, collection, doc):
    return self._delete(collection, doc)
  
  @to_thread
  def query(self, collection, field, operator, value):
    return self._query(collection, field, operator, value)


    