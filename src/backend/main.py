import datetime as dt
from random import randint

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


@app_api.get('/predict/demand')
def predict_demand(body: models.PredictDemandRequest) -> models.PredictDemandResponse:
    # TODO implement function
    days_ago = 7  # days ago from now
    days_predict = None
    now = dt.date.today()

    if body.type_predict.startswith('долго'):
        days_predict = 365
    elif body.type_predict.startswith('средне'):
        days_predict = 150
    elif body.type_predict.startswith('кратко'):
        days_predict = 30
    else:
        logger.error(f'bad request type {body.type_predict}')
        days_predict = 1

    resp = models.PredictDemandResponse()
    resp.dates = [(now + dt.timedelta(days=ds)).strftime('%d-%m-%Y') for ds in range(-days_ago, days_predict + 1)]
    resp.demands = [randint(0, 1000) for d in range(-days_ago, days_predict + 1)]

    return resp
