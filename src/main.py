# from http.client import HTTPException
from queue import Empty
from sqlite3 import DatabaseError
from sre_constants import SUCCESS
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
import uuid
from auth import AuthHandler
from models import AuthDetails, User
# import psycopg2
# from config import config
from db import Database

app = FastAPI()
auth_handler = AuthHandler()
users = []

# def connect():
#   connection = None
#   try:
#     params = config()
#     print('Connecting to postgreSQL database ...')
#     connection = psycopg2.connect(**params)

#     crsr = connection.cursor()
#     print('PostgreSQL database version: ')
#     crsr.execute('SELECT version()')
#     db_version = crsr.fetchone()
#     print(db_version)
#     crsr.close()
#   except(Exception, psycopg2.DatabaseError) as err:
#     print(err)
#   finally:
#     if connection is not None:
#       connection.close()
#       print('Database connection terminated')

@app.post("/api/v1/register", status_code=201)
async def register(user_details: User):
  # print(Database.query('SELECT * from "FaceRecog".users'))
  regist_users = []
  regist_users = Database.query(
      f"SELECT * from \"FaceRecog\".users where users.username='{user_details.username}'")
  # print(regist_users)
  if len(regist_users) == 0:
    hashed_password = auth_handler.get_password_hash(user_details.password)
    Database.query(
        f"""INSERT INTO \"FaceRecog\".users 
        (id, first_name, last_name, username, \"password\")
         VALUES('{uuid.uuid4()}','{user_details.first_name}', '{user_details.last_name}', '{user_details.username}', '{hashed_password}')"""
    )
    return {"msg": 'User created'}
  else:
    raise HTTPException(status_code=401, detail=f"Username '{regist_users[0][3]}' is already taken")
    
  # if any(x['username'] == auth_details.username for x in users):
  #   raise HTTPException(status_code=400, detail='Username is already taken')
  
  # users.append({
  #   'username': auth_details.username,
  #   'password': hashed_password
  # })
  return

@app.post("/api/v1/login")
async def login(auth_details: AuthDetails):
  user = None
  user = Database.query(
      f"SELECT * from \"FaceRecog\".users where users.username='{auth_details.username}'")
  print(user[0][4])
  if (len(user) > 0):
    print("first if")
    user = user[0]
    if auth_handler.verify_password(auth_details.password, user[4]):
      print("second if")
      token = auth_handler.encode_token(user[0])
      return {'token': token}
      
    else:
      raise HTTPException(
      status_code=401, detail='Invalid username and/or password')
  

@app.get("/")
async def root():
  return ({"message": "Welcome on the Python server"})

@app.post("/api/v1/users/images/check")
async def check_image(file: UploadFile = File(...)):
  #img.filename = "check.jpg"
  #contents = await file.read()
  return {"filename": file}

@app.post("/api/v1/users/images/upload")
# async def upload_image(file: bytes = File(...), username = Depends(auth_handler.auth_wrapper)):
#   myuuid = uuid.uuid4()
#   file.filename = "check.jpg"
#   # contents = await file.read()
#   with open('../assets/'+str(myuuid)+'.jpg',"wb") as image:
#   image.write(file)
#   image.close()
#   return {"msg": "SUCCESS"}
async def upload_image(file: bytes = File(...), username=Depends(auth_handler.auth_wrapper)):
  myuuid = uuid.uuid4()
  #img.filename = "check.jpg"
  #contents = await file.read()
  with open('../assets/'+str(myuuid)+'.jpg', "wb") as image:
    image.write(file)
    image.close()
  return {"msg": "SUCCESS"}

# async def upload_image(file: bytes = File(...)):
#   myuuid = uuid.uuid4()
#   #img.filename = "check.jpg"
#   #contents = await file.read()
#   with open('../assets/'+str(myuuid)+'.jpg',"wb") as image:
#     image.write(file)
#     image.close()
#   return {"msg": "SUCCESS"}