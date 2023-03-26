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
from ml import BaseModel, TimeSeria, LstmFacade

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
        data = []
        for i in range(len(history['dates'])):
            data.append((history['dates'][i], history['demands'][i]))
        data.sort(reverse=True)
        data = data[:days_ago]
        print(data)
        m = LstmFacade()
        pr_day = (dt.datetime.strptime(data[0][0], '%Y-%m-%d') + dt.timedelta(days=1))
        strweek = ["Понедельник",
                   "Вторник",
                   "Среда",
                   "Четверг",
                   "Пятница",
                   "Суббота",
                   "Воскресенье"]
        answ = []
        if days_predict == 1:
            answ = [m.predict(
                [d[1] for d in data],
                db.get_last_price(body.name_product),
                body.name_product,
                float("nan"),
                strweek[pr_day.weekday()],
                pr_day.strftime('%m-%d')
            )]
            resp = models.PredictDemandResponse(
                dates=[d[0] for d in data] + [(pr_day + dt.timedelta(days=i)).strftime('%Y-%m-%d') for i in
                                              range(days_predict)],
                demands=[d[1] for d in data] + answ
            )
        elif days_predict == 7:
            answ = m.predict_medium(
                [d[1] for d in data],
                db.get_last_price(body.name_product),
                body.name_product,
                float("nan"),
                strweek[pr_day.weekday()],
                pr_day.strftime('%m-%d')
            )
            resp = models.PredictDemandResponse(
                dates=[d[0] for d in data] + [(pr_day + dt.timedelta(days=i)).strftime('%Y-%m-%d') for i in
                                              range(days_predict)],
                demands=[d[1] for d in data] + [answ[k] for k in sorted(answ.keys())]
            )
        # if days_predict == 7
        # ts = TimeSeria()
        # for i in range(len(history['dates'])):
        #     ts.add_value(history['dates'][i], history['demands'][i])
        #
        # predict = list(map(int, BaseModel().predict(ts, days_predict)))
        now = dt.date.today()


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
    return models.PredictPriceResponse(
        demand=models._Demand(
            prices=[257, 154, 148, 220],
            demands=[24, 55, 76, 14]
        ),
        profit=models._Profit(
            prices=[257, 154, 148, 220],
            profits=[24 * 257, 55 * 154, 76 * 148, 14 * 220]
        ),
        best_price=148
    )
    # raise HTTPException(status_code=401)
