from sklearn.preprocessing import LabelEncoder


def data_in_int(data):
    le = LabelEncoder().fit(data)
    return le.transform(data)


def get_days_by_type_predict(type_predict: str):
    type_predict = type_predict.lower().strip()
    if type_predict.startswith('долго'):
        days_predict = (150, 30)
    elif type_predict.startswith('средне'):
        days_predict = (30, 7)
    elif type_predict.startswith('кратко'):
        days_predict = (7, 1)
    else:
        return None
    return days_predict
