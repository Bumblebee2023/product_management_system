from typing import List, Optional, Dict, Iterable, Tuple


class TimeSeria(object):
    def __init__(self):
        self.__day_number: List[int] = []
        self.__value: Dict[int, float] = {}

    def add_value(self, day_number: int, value: Optional):
        if day_number in self.__value.keys():
            raise Exception("Repeatable day number!")
        self.__day_number.append(day_number)
        self.__value[day_number] = float(value)

    @property
    def value(self) -> Iterable[Tuple[int, float]]:
        self.__day_number.sort()
        left, right = self.__day_number[0], self.__day_number[-1]
        day_number_i = -1
        for i in range(left, right + 1):
            if i in self.__value.keys():
                day_number_i += 1
                yield i, self.__value[i]
            else:
                a, b = self.__day_number[day_number_i], self.__day_number[day_number_i + 1]
                diff = self.__value[b] - self.__value[a]
                yield i, self.__value[a] + diff * (i - a) / (b - a)


class Item(object):
    def __init__(self):
        pass


if __name__ == "__main__":
    ts = TimeSeria()
    ts.add_value(0, 0)
    ts.add_value(2, 4)
    ts.add_value(5, 25)
    print(list(ts.value))