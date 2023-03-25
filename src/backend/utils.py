from sklearn.preprocessing import LabelEncoder


def data_in_int(data):
    le = LabelEncoder().fit(data)
    return le.transform(data)


def get_days_by_type_predict(type_predict: str):
    if type_predict.startswith('долго'):
        days_predict = 365
    elif type_predict.startswith('средне'):
        days_predict = 150
    elif type_predict.startswith('кратко'):
        days_predict = 30
    else:
        return None
    return days_predict
