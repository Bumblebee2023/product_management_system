from random import randint
from pathlib import Path

import pymongo
import bestconfig
import datetime as dt
from yaml import safe_load

import utils


config = bestconfig.Config()


def _connect_mongo(db_name: str):
    config_path = str(config.str('mongodb-config-path'))
    conf = safe_load(open(str(Path.home()) + config_path))
    client = pymongo.MongoClient(host=conf['host'], port=int(conf['port']))
    return client[db_name]


def get_history_demand(name_product: str, id_market: str, time_window: dt.timedelta):
    # TODO mongo
    coll = _connect_mongo('markinghack')[f'transactions_{id_market}']

    # history = coll.find({
    #     'id_product': name_product,
    #     'dt': {'$gte': (dt.date.today() - time_window).strftime('%Y-%m-%d')}
    # })
    history = coll.aggregate([
        {'$match': {'id_product': name_product, 'dt': {'$gte': (dt.date.today() - time_window).strftime('%Y-%m-%d')}}},
        {'$group': {'_id': '$dt', 'count': {'$sum': 1}}}
    ])
    data = {
        'dates': [],
        'demands': []
    }
    try:
        for line in history:
            data['dates'].append(line['_id'])
            data['demands'].append(line['count'])
        data['dates'] = list(utils.data_in_int(data['dates']))
    except Exception as e:
        print(e)
    return data
    # return {
    #     'dates': [(dt.date.today() + dt.timedelta(days=ds)).strftime('%d-%m-%Y') for ds in range(1, days_predict + 1)],
    #     'demands': [randint(0, 1000) for _ in range(1, days_predict + 1)]
    # }


if __name__ == "__main__":
    from pprint import pprint

    pprint(get_history_demand('18AA2603B271C19A581133BD34319311',
                             '6B8E111AB5B5C556C0AEA292ACA4D88B',
                             dt.timedelta(days=150)))
