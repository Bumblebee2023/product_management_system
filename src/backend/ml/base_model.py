from sklearn.linear_model import LinearRegression
import numpy as np
from typing import List

from data import TimeSeria


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


if __name__ == "__main__":
    ts = TimeSeria()
    ts.add_value(0, 0)
    ts.add_value(2, 4)
    ts.add_value(5, 25)
    ts.add_value(6, 36)
    m = BaseModel()
    print(m.predict(ts, 10))
