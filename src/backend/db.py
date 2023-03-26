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
    coll = _connect_mongo('markinghack')[f'transactions_{id_market}']
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
        # data['dates'] = list(utils.data_in_int(data['dates']))
        return data
    except Exception as e:
        print(e)
    return {
        'dates': [],
        'demands': []
    }


def get_product_categories():
    coll = _connect_mongo('markinghack')[f'transactions_6B8E111AB5B5C556C0AEA292ACA4D88B']
    prods = coll.distinct(key='id_product')
    return ['18AA2603B271C19A581133BD34319311'] + prods[:50]


def get_last_price(id_pr):
    try:
        coll = _connect_mongo('markinghack')[f'transactions_6B8E111AB5B5C556C0AEA292ACA4D88B']
        a = list(coll.find({'id_product': id_pr}).sort(key_or_list='dt', direction=pymongo.DESCENDING).limit(1))[0]
        return a['price'] // 100
    except:
        return 0


if __name__ == "__main__":
    from pprint import pprint

    pprint(get_history_demand('18AA2603B271C19A581133BD34319311',
                             '6B8E111AB5B5C556C0AEA292ACA4D88B',
                             dt.timedelta(days=150)))
    # pprint(get_last_price('18AA2603B271C19A581133BD34319311'))
