from sklearn.linear_model import LinearRegression
import numpy as np
import torch
import json
from typing import List, Union

from data import TimeSeria
from lstm import Model


class BaseModel:
    def __init__(self):
        self.model = LinearRegression()

    @staticmethod
    def __build_polynomial_input(first_value: int, last_value: int, degree: int) -> np.ndarray:
        length = last_value - first_value
        x = np.arange(first_value, last_value).reshape(1, length)
        x = np.concatenate([np.power(x, i) for i in range(1, degree + 1)]).transpose()
        return x

    def predict(self, x: TimeSeria, n_values: int) -> List[float]:
        y = np.array([i[1] for i in x.value])
        x_train = BaseModel.__build_polynomial_input(0, len(y), 3)
        self.model.fit(x_train, y)
        x_pred = self.__build_polynomial_input(len(y), len(y) + n_values, 3)
        return self.model.predict(x_pred)


class LstmFacade:
    def __init__(self):
        self.model = Model()
        self.model.load_state_dict(torch.load("weights/epoch9.pt", map_location=torch.device('cpu')))
        self.model.eval()
        self.date_to_token = json.load(open("tokenizers/date_tokenizer.json"))
        self.item_group_to_token = json.load(open("tokenizers/item_group_tokenizer.json"))
        self.gtin_to_token = json.load(open("tokenizers/gtin_tokenizer.json"))
        self.day_to_token = {
            "Понедельник": 0,
            "Вторник": 1,
            "Среда": 2,
            "Четверг": 3,
            "Пятница": 4,
            "Суббота": 5,
            "Воскресенье": 6
        }

    def predict(self,
                prev_values: List[float],
                price: int,
                gtin: str,
                item_group: Union[str, float],
                day_of_the_week: str,
                date: str):
        gtin = torch.Tensor([self.gtin_to_token[gtin]]).long()
        day_of_the_week = torch.Tensor([self.day_to_token[day_of_the_week]]).long()
        date = torch.Tensor([self.date_to_token[date]]).long()
        if type(item_group) is float:
            item_group = torch.Tensor([0]).long()
        else:
            item_group = torch.Tensor([self.item_group_to_token[item_group]]).long()
        price = torch.Tensor([[price]])
        prev_values = torch.Tensor([prev_values])
        prev_values = prev_values.reshape(*prev_values.shape, 1)
        with torch.no_grad():
            s = self.model(prev_values, price, gtin, item_group, day_of_the_week, date).tolist()
        return s[0][0]

    def increase_date(self, date: str):
        date = self.date_to_token[date]
        date = (date + 1) % 365
        for i in self.date_to_token.keys():
            if self.date_to_token[i] == date:
                return i

    def predict_medium(self,
                       prev_values: List[float],
                       price: int,
                       gtin: str,
                       item_group: Union[str, float],
                       day_of_the_week: str,
                       date: str):
        values = {}
        for i in range(7):
            y_pred = self.predict(prev_values, price, gtin, item_group, day_of_the_week, date)
            values[date] = y_pred
            prev_values.append(y_pred)
            day_of_the_week = (self.day_to_token[day_of_the_week] + 1) % 7
            for day in self.day_to_token.keys():
                if self.day_to_token[day] == day_of_the_week:
                    day_of_the_week = day
                    break
            date = self.increase_date(date)
        return values

    def predict_long(self,
                       prev_values: List[float],
                       price: int,
                       gtin: str,
                       item_group: Union[str, float],
                       day_of_the_week: str,
                       date: str):
        values = {}
        for i in range(30):
            y_pred = self.predict(prev_values, price, gtin, item_group, day_of_the_week, date)
            values[date] = y_pred
            prev_values.append(y_pred)
            day_of_the_week = (self.day_to_token[day_of_the_week] + 1) % 7
            for day in self.day_to_token.keys():
                if self.day_to_token[day] == day_of_the_week:
                    day_of_the_week = day
                    break
            date = self.increase_date(date)
        return values


if __name__ == "__main__":
    m = LstmFacade()
    print(m.predict_long([50, 50, 50, 60, 50, 500, 40],
                           10,
                           "0E6D952FEFCA3542FF2E4EB72E544D6E",
                           float("nan"),
                           "Воскресенье",
                           "03-26"))
