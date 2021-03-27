import databases
import sqlalchemy
from sqlalchemy import create_engine
import urllib.parse
from fastapi.encoders import jsonable_encoder

import uuid
from fastapi.responses import JSONResponse
import datetime
from datetime import timedelta
from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv, find_dotenv
import os
import sqlalchemy.dialects.postgresql



# client = pymongo.MongoClient("mongodb+srv://dbMike:pMQI7fDiPLbTyNVg@cluster0.1il65.mongodb.net/myFirstDatabase?retryWrites=true&w=majority") 
# db = client.SberHackBack
###
load_dotenv(find_dotenv())
#import environ
DATABASE_URL = os.environ.get('DATABASE_URL')
DATABASE_URL = DATABASE_URL.replace("postgres", "postgresql")

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()


training_category = sqlalchemy.Table(
    "training_category",
    metadata,
    sqlalchemy.Column("Id", sqlalchemy.Integer,
                      primary_key=True, index=True, unique=True),
    sqlalchemy.Column("name", sqlalchemy.String)
)
training = sqlalchemy.Table(
    "training",
    metadata,
    sqlalchemy.Column("Id", sqlalchemy.Integer, primary_key=True, unique=True),
    sqlalchemy.Column("category", sqlalchemy.Integer,
                      sqlalchemy.ForeignKey("training_category.Id")),
    sqlalchemy.Column("trainingName", sqlalchemy.String),
    sqlalchemy.Column("discription", sqlalchemy.String(1000)),
    sqlalchemy.Column("discriptionJoy", sqlalchemy.String(1000)),
    sqlalchemy.Column("photo", sqlalchemy.String(150)),
    sqlalchemy.Column("time", sqlalchemy.Integer)
)

training_group = sqlalchemy.Table(
    "training_group",
    metadata,
    sqlalchemy.Column("Id", sqlalchemy.Integer, primary_key=True, unique=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("short_description", sqlalchemy.String(150)),
    sqlalchemy.Column("description", sqlalchemy.String(200)),
    sqlalchemy.Column("image", sqlalchemy.String(200))
)

training_training_group = sqlalchemy.Table(
    "training_training_group",
    metadata,
    sqlalchemy.Column("Id", sqlalchemy.Integer, primary_key=True, unique=True),
    sqlalchemy.Column("training_id", sqlalchemy.Integer,
                      sqlalchemy.ForeignKey("training.Id")),
    sqlalchemy.Column("training_group_Id", sqlalchemy.Integer,
                      sqlalchemy.ForeignKey("training_group.Id"))
)

user = sqlalchemy.Table(
    "user",
    metadata,
    sqlalchemy.Column("user_token", sqlalchemy.String(200),
                      primary_key=True, unique=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("age", sqlalchemy.Integer),
    sqlalchemy.Column("gender", sqlalchemy.String),
)

progress = sqlalchemy.Table(
    "progress",
    metadata,
    sqlalchemy.Column("user_toket", sqlalchemy.String(
        200), sqlalchemy.ForeignKey("user.user_token")),
    sqlalchemy.Column("date", sqlalchemy.DateTime),
    sqlalchemy.Column("completed", sqlalchemy.Boolean)
)


engine = create_engine(
    DATABASE_URL, pool_size=5, max_overflow=0
)
metadata.create_all(engine)

Session = sessionmaker(engine)


class User(BaseModel):
    UserId: str
    Name: str
    Age: int
    Gender: str


class Progres(BaseModel):
    UserId: str
    Date: str
    Completed: bool


class Categoriya(BaseModel):
    Name: str

app = FastAPI()

origins = [
    "https://komtriangle.github.io/Bodroe_ytro_front",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


# @app.exception_handler(500)
# async def custom_http_exception_handler(request, exc):
#     #error = ErrorResponse(error="Something went wrong")
#     error = jsonable_encoder(error.dict())

#     response = JSONResponse(content=error, status_code=500)

#     # Since the CORSMiddleware is not executed when an unhandled server exception
#     # occurs, we need to manually set the CORS headers ourselves if we want the FE
#     # to receive a proper JSON 500, opposed to a CORS error.
#     # Setting CORS headers on server errors is a bit of a philosophical topic of
#     # discussion in many frameworks, and it is currently not handled in FastAPI.
#     # See dotnet core for a recent discussion, where ultimately it was
#     # decided to return CORS headers on server failures:
#     # https://github.com/dotnet/aspnetcore/issues/2378
#     origin = request.headers.get('origin')

#     if origin:
#         # Have the middleware do the heavy lifting for us to parse
#         # all the config, then update our response headers
#         cors = CORSMiddleware(
#             app=app,
#             allow_origins=["*"],
#             allow_credentials=True,
#             allow_methods=["*"],
#             allow_headers=["*"])

#         # Logic directly from Starlette's CORSMiddleware:
#         # https://github.com/encode/starlette/blob/master/starlette/middleware/cors.py#L152

#         response.headers.update(cors.simple_headers)
#         has_cookie = "cookie" in request.headers

#         # If request includes any cookie headers, then we must respond
#         # with the specific origin instead of '*'.
#         if cors.allow_all_origins and has_cookie:
#             response.headers["Access-Control-Allow-Origin"] = origin

#         # If we only allow specific origins, then we have to mirror back
#         # the Origin header in the response.
#         elif not cors.allow_all_origins and cors.is_allowed_origin(origin=origin):
#             response.headers["Access-Control-Allow-Origin"] = origin
#             response.headers.add_vary_header("Origin")

#     return response


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
async def hello():
    # cursor = db.user 
    # for document in cursor.find(): 
    #    try:
    #         query = user.insert().values(
    #         user_token=document["UserId"],
    #         name="string",
    #         age=0,
    #         gender="0"
    #         )
    #         await database.execute(query)
    #    except:
    #        continue
    # cursor = db.progress # choosing the collection you need 
    # for document in cursor.find(): 
    #     try:
    #         query = progress.insert().values(
    #         user_toket=document["UserId"],
    #         date=datetime.datetime.strptime(document["date"], "%Y-%m-%dT%H:%M:%S.%fZ"),
    #         completed=True
    #         )
    #         await database.execute(query)
    #     except:
    #         print('fff')
    #     try:
    #         query = progress.insert().values(
    #         user_toket=document["UserId"],
    #         date=datetime.datetime.strptime(document["date"], "%Y-%m-%d"),
    #         completed=True
    #         )
    #         await database.execute(query)
    #     except:
    #         continue
        
    return "hello"



@app.post("/User/")
async def createUser(user_: User):
    query = user.insert().values(
        user_token=user_.UserId,
        name=user_.Name,
        age=user_.Age,
        gender=user_.Gender
    )
    await database.execute(query)
    return {
        "id": user_.UserId,
        **user_.dict(),
        "status": "1"
    }


@app.post("/ProgressAchieve/")
async def createProgressAchieve(achiv: Progres):
    query = progress.insert().values(
        user_toket=achiv.UserId,
        date=datetime.date.today(),
        completed=True
    )
    await database.execute(query)
    return {
        **achiv.dict(),
        "status": "1"
    }


@app.get("/AllGroupsExercises/")
async def getAllGroupsExercises():
    query = training_group.select()
    return await database.fetch_all(query)


@app.get("/ExircicesfromGroup/")
async def getExircicesfromGroup(group_id: int):
    session = Session()
    query = session.execute(training_training_group.select().where(
        training_training_group.c.training_group_Id == group_id)).fetchall()
    res = []
    for i in query:
        res.append(session.execute(training.select().where(
            training.c.Id == i[1])).fetchone())
    # res = training.select().where(training.c.Id == query[0][1])
    session.close()
    return res


@app.get("/ProgressByUser/")
async def getProgressByUser(user_id: str):
    query = progress.select().where(progress.c.user_toket == user_id)
    return await database.fetch_all(query)


@app.get("/AchiviesFomUser/")
async def getAchiviesForUser(user_id: str):
    session = Session()
    count = 1
    days = 0
    date = datetime.date.today()
    while(count != 0):
        query = session.execute(progress.select().where(
            progress.c.date == date and progress.c.user_toket == user_id))
        print("date", date)
        cnt = len(query.fetchall())
        if(cnt > 0):
            days += 1
        count = cnt
        date -= timedelta(days=1)
    count_train = len(session.execute(progress.select().where(
        progress.c.user_toket == user_id)).fetchall())

    count_days_train = session.query(progress.c.date, sqlalchemy.func.count(
        progress.c.date)).where(progress.c.user_toket == user_id).group_by(progress.c.date).all()

    res = dict()
    res['dict'] = days
    res['count_train'] = count_train
    res['count_days_train'] = len(count_days_train)
    session.close()
    return res
