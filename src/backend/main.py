import datetime as dt
from random import randint

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging

import models
import db
import utils

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


@app_api.post('/predict/demand')
def predict_demand(body: models.PredictRequest) -> models.PredictDemandResponse:
    # TODO implement function
    days_ago = 7  # days ago from now
    days_predict = utils.get_days_by_type_predict(body.type_predict)
    now = dt.date.today()

    resp = models.PredictDemandResponse(
        dates=[(now + dt.timedelta(days=ds)).strftime('%d-%m-%Y') for ds in range(-days_ago, days_predict + 1)],
        demands=[randint(0, 1000) for _ in range(-days_ago, days_predict + 1)]
    )

    return resp


@app_api.post('/predict/price')
def predict_price(body: models.PredictRequest) -> models.PredictPriceResponse:
    pass
