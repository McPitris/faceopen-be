import base64
from queue import Empty
from fastapi import FastAPI, File, Depends, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
import uuid
from auth import AuthHandler
from face_recog import FaceRecog
from models import AuthDetails, User
from db import Database
import os
import glob

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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


@app.get("/api/v1/users")
async def get_user(username=Depends(auth_handler.auth_wrapper)):
    users_in_json = []
    # users = Database.query(f"SELECT * from \"FaceRecog\".users'")
    users = Database.query(
        f"SELECT id, first_name, last_name, username, images_count FROM \"dctis7jlv0tai8\".users")
    # print(users)
    for user in users:
        print(user)
        user_json = {
            "id": user[0],
            "first_name": user[1],
            "last_name": user[2],
            "username": user[3],
            "img_count": user[4]
        }
        users_in_json.append(user_json)

    return users_in_json


# @app.get("/api/v1/users/{user_id}/images")
# async def get_user_umages():
#   images = []
#   path = "../assets"
#   valid_images = [".jpg", ".gif", ".png", ".tga"]

#   for f in os.listdir(path):
#     ext = os.path.splitext(f)[1]
#     if ext.lower() not in valid_images:
#         continue
#     images.append(Image.open(os.path.join(path, f)))
#   return images


@app.get("/api/v1/users/{username}/images")
async def get_user_umages(username: str, usrAuth=Depends(auth_handler.auth_wrapper)):
    path = "./</"
    images = []
    images_path = []
    os.chdir(path)
    for file in glob.glob(f'{username}_*'):
        images_path.append(file)

    for image_path in images_path:
        print(image_path)
        with open(image_path, "rb") as b_image:
            stri = base64.b64encode(b_image.read())
            images.append(
                {
                    "name": image_path, "image": stri
                })
    return images

    # with open(path, "rb") as fim:
    #   str = base64.b64encode(fim.read())
    #   images.append(str)
    # return images

# @app.get("/api/v1/users/{user_id}/images")
# async def get_user_umages():
#   test = []
#   path = "../assets/test.jpg"
#   file_path = os.path.join(path)
#   return FileResponse(file_path, media_type="image/jpeg", filename="ttt.jpg")

    # users = Database.query(f"SELECT * from \"FaceRecog\".users'")
    # users = Database.query(
    #     f"SELECT id, first_name, last_name, username, images_count FROM \"FaceRecog\".users")
    # # print(users)
    # for user in users:
    #   print(user)
    #   user_json = {
    #       "id": user[0],
    #       "first_name": user[1],
    #       "last_name": user[2],
    #       "username": user[3],
    #       "img_count": user[4]
    #   }
    #   users_in_json.append(user_json)

    # return users_in_json

    # if (len(users) > 0):
    #   print(users)
    #   return users

    # else:
    #   raise HTTPException(
    #       status_code=401, detail='Not users in database')


@app.post("/api/v1/auth/register", status_code=201)
async def register(user_details: User):
    # print(Database.query('SELECT * from "FaceRecog".users'))
    regist_users = []
    regist_users = Database.query(
        f"SELECT * from \"dctis7jlv0tai8\".users where users.username='{user_details.username}'")
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
        raise HTTPException(
            status_code=401, detail=f"Username '{regist_users[0][3]}' is already taken")


@app.post("/api/v1/auth/login")
async def login(auth_details: AuthDetails):
    user = None
    user = Database.query(
        f"SELECT * from \"dctis7jlv0tai8\".users where users.username='{auth_details.username}'")
    print(user[0][4])
    if (len(user) > 0):
        print("first if")
        user = user[0]
        if auth_handler.verify_password(auth_details.password, user[4]):
            print("second if")
            token = auth_handler.encode_token(user[3])
            return {
                "username": auth_details.username,
                "accessToken": token
            }

        else:
            raise HTTPException(
                status_code=401, detail='Invalid username and/or password')


@app.get("/api/v1/auth/valid-token")
async def get_user(username=Depends(auth_handler.auth_wrapper)):
    if username is not Empty:
        raise HTTPException(status_code=200, detail="User is logged")
    # user = Database.query(
    #     f"SELECT * from \"FaceRecog\".users where users.username='{username}'")


@app.get("/")
async def root():
    return ({"message": "Welcome on the Python server"})


@app.post("/api/v1/users/images/check", status_code=200)
async def check_image(response: Response, file: bytes = File(...)):
    myuuid = uuid.uuid4()
    username = None
    with open('./assets/temp/check.jpg', "wb") as image:
        image.write(file)
        image.close()
    result = FaceRecog.compare_faces('./assets/temp/check.jpg')
    print(result)
    return_result = None
    if result[0] == True:
        username = result[1].split("_")[0]
        return_result = True
    else:
        response.status_code = status.HTTP_403_FORBIDDEN
        return_result = False

    # return {"result": return_result, "username": username}
    # return [return_result, username]
    return "true"


@app.post("/api/v1/users/{username}/images/upload")
# async def upload_image(file: bytes = File(...), username = Depends(auth_handler.auth_wrapper)):
#   myuuid = uuid.uuid4()
#   file.filename = "check.jpg"
#   # contents = await file.read()
#   with open('../assets/'+str(myuuid)+'.jpg',"wb") as image:
#   image.write(file)
#   image.close()
#   return {"msg": "SUCCESS"}
async def upload_image(username: str, file: bytes = File(...), usr=Depends(auth_handler.auth_wrapper)):
    myuuid = uuid.uuid4()
    #img.filename = "check.jpg"
    # contents = await file.read()
    image_count = None
    image_count = Database.query(
        f"SELECT images_count from \"dctis7jlv0tai8\".users where users.username='{username}'")
    print({username})
    print(image_count)

# todo: je potřeba převést image_count[0] tuple na int a v ifu porovnat
    # if ((image_count[0] == None or int(image_count[0]) < 5)):
    with open('./assets/'+username+'_'+str(myuuid)+'.jpg', "wb") as image:
        image.write(file)
        image.close()
        tuple_2_int(image_count)
        #put_query = Database.query(
            #f"UPDATE \"FaceRecog\".users SET images_count={image_count} WHERE users.username='{username}'")
        return {"msg": "SUCCESS"}


@app.delete("/api/v1/users/images/delete/{image_name}")
async def delete_image(image_name: str, usrAuth=Depends(auth_handler.auth_wrapper)):
    file_path = f'./assets/{image_name}'
    os.remove(file_path)
    return {"msg": "Picture was removed"}


# async def upload_image(file: bytes = File(...)):
#   myuuid = uuid.uuid4()
#   #img.filename = "check.jpg"
#   #contents = await file.read()
#   with open('../assets/'+str(myuuid)+'.jpg',"wb") as image:
#     image.write(file)
#     image.close()
#   return {"msg": "SUCCESS"}
def tuple_2_int(tuple):
    print("The original tuple : " + str(tuple))

    # Convert Tuple to integer
    res = ""
    for i in tuple:
        res += str(i)
    res = int(res)

# printing result
    print("Tuple to integer conversion : " + str(res))


@app.get("/api/v1/test")
def test():
    return True
