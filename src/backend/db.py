from random import randint

import pymongo
import bestconfig
import datetime as dt
from yaml import safe_load


config = bestconfig.Config()


def _connect_mongo(db_name: str):
    config_path = str(config.str('mongodb-config-path'))
    conf = safe_load(open(config_path))
    client = pymongo.MongoClient(host=conf['host'], port=int(conf['port']))
    return client[db_name]


def get_history_demand(name_product: str, id_market: str, time_window: dt.timedelta):
    # TODO mongo
    days_predict = 100
    return {
        'dates': [(dt.date.today() + dt.timedelta(days=ds)).strftime('%d-%m-%Y') for ds in range(1, days_predict + 1)],
        'demands': [randint(0, 1000) for _ in range(1, days_predict + 1)]
    }
