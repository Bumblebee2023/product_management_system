import datetime as dt
from random import randint

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
import bestconfig

import models
import db
import utils
from ml import BaseModel, TimeSeria

app_api = FastAPI()
logger = logging.getLogger(__name__)
config = bestconfig.Config()

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
    days_predict = utils.get_days_by_type_predict(body.type_predict)

    history = db.get_history_demand(body.name_product,
                                    body.id_market,
                                    dt.timedelta(days=int(config.int('time-window-years')) * 365))
    try:
        ts = TimeSeria()
        for i in range(len(history['dates'])):
            ts.add_value(history['dates'][i], history['demands'][i])

        predict = list(map(int, BaseModel().predict(ts, days_predict)))
        now = dt.date.today()
        resp = models.PredictDemandResponse(
            dates=[(now + dt.timedelta(days=d + 1)).strftime('%Y-%m-%d') for d in range(len(predict))],
            demands=predict
        )

        return resp
    except Exception as e:
        print(e)
    return models.PredictDemandResponse(
            dates=[],
            demands=[]
        )


@app_api.post('/predict/price')
def predict_price(body: models.PredictRequest) -> models.PredictPriceResponse:
    # TODO implement function
    raise HTTPException(status_code=401)
