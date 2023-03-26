import datetime as dt
from random import randint

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import logging
import bestconfig
from starlette.middleware import Middleware
from starlette.status import HTTP_204_NO_CONTENT

import models
import db
import utils
from ml import BaseModel, TimeSeria

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
]
app_api = FastAPI(middleware=middleware)
logger = logging.getLogger(__name__)
config = bestconfig.Config()

origins = ["*"]

# app_api.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["POST", "GET"],
#     allow_headers=["*"],
# )

@app_api.options("/{path:path}")
def options_path(response: Response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.status_code = HTTP_204_NO_CONTENT
    return response


@app_api.middleware("http")
async def cors_handler(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    return response


# @app_api.options("/{path:path}")
# async def options_handler(request: Request, path: str):
#     return Response(headers={
#         "Access-Control-Allow-Origin": request.headers.get("Origin", "*"),
#         "Access-Control-Allow-Methods": ",".join(app_api.routes.get(path, [])[0].methods),
#         "Access-Control-Allow-Headers": "*",
#     })


@app_api.get('/')
def home():
    return {'Hello': 'world'}
    # return JSONResponse(content={'Hello': 'world'}, headers=headers, status_code=200)


@app_api.post('/predict/demand')
def predict_demand(body: models.PredictRequest) -> models.PredictDemandResponse:
    # TODO implement function
    try:
        days_ago, days_predict = utils.get_days_by_type_predict(body.type_predict)

        history = db.get_history_demand(body.name_product,
                                        body.id_market,
                                        dt.timedelta(days=int(config.int('time-window-years')) * 365))
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


@app_api.get('/categories')
def categories() -> models.Categories:
    return models.Categories(categories=db.get_product_categories())


@app_api.post('/predict/price')
def predict_price(body: models.PredictRequest) -> models.PredictPriceResponse:
    # TODO implement function
    raise HTTPException(status_code=401)
