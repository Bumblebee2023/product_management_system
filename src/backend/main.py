from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging

import models
import db

app_api = FastAPI()
logger = logging.getLogger(__name__)

origins = ["*"]

app_api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app_api.get('/')
def home():
    return {'Hello': 'world'}
    # return JSONResponse(content={'Hello': 'world'}, headers=headers, status_code=200)


@app_api.post('/user/create/tg')
def new_user_tg(body: models.NewUserTg):
    try:
        # db.Users.update(user_tg_id=body.tgUserID).where(username_tg=body.username)
        user = db.Users.get(db.Users.username_tg == body.username.lower())
        user.user_tg_id = body.user_tg_id
        resp = {'first_name': user.first_name, 'second_name': user.second_name}
        user.save()
        return resp
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
