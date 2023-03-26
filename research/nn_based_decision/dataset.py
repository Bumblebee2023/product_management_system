import torch
import json
import gc
from tqdm import tqdm
from torch.utils.data import Dataset, DataLoader


class CustomDataset(Dataset):
    def __init__(self, data):
        self.data = data
        date_to_token = json.load(open("../../../pms/src/backend/ml/tokenizers/date_tokenizer.json"))
        item_group_to_token = json.load(open("../../../pms/src/backend/ml/tokenizers/item_group_tokenizer.json"))
        gtin_to_token = json.load(open("../../../pms/src/backend/ml/tokenizers/gtin_tokenizer.json"))
        day_to_token = {
            "Понедельник": 0,
            "Вторник": 1,
            "Среда": 2,
            "Четверг": 3,
            "Пятница": 4,
            "Суббота": 5,
            "Воскресенье": 6
        }
        for i in tqdm(range(len(data))):
            self.data[i]["gtin"] = gtin_to_token[self.data[i]["gtin"]]
            self.data[i]["day_of_week"] = day_to_token[self.data[i]["day_of_week"]]
            self.data[i]["date"] = date_to_token[self.data[i]["date"]]
            if type(self.data[i]["item_group"]) is float:
                self.data[i]["item_group"] = 0
            else:
                self.data[i]["item_group"] = item_group_to_token[self.data[i]["item_group"]]
        gc.collect()

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        x = self.data[index]
        prev_values = torch.Tensor(x["prev_values"])
        prev_values = prev_values.reshape(*prev_values.shape, 1)
        gtin = torch.Tensor([x["gtin"]]).long()
        item_group = torch.Tensor([x["item_group"]]).long()
        day = torch.Tensor([x["day_of_week"]]).long()
        date = torch.Tensor([x["date"]]).long()
        y_true = torch.Tensor([x["y_true"]])
        price = torch.Tensor([x["price"]])
        return {"prev_values": prev_values,
                "price": price,
                "gtin": gtin,
                "item_group": item_group,
                "day_of_week": day,
                "date": date,
                "y_true": y_true}


class CustomDataloader(DataLoader):
    def __init__(self, dataset, batch_size, num_workers):
        super().__init__(dataset, batch_size=batch_size, num_workers=num_workers)
