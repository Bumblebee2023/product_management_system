import torch
import torch.nn as nn


class Model(nn.Module):
    def __init__(self, hidden_size=128, num_layers=12):
        super().__init__()
        self.num_layers = num_layers
        self.lstm = nn.LSTM(1, hidden_size, num_layers=num_layers, batch_first=True)
        self.linear = nn.Linear(hidden_size, 32)
        self.gtin_embeddings = nn.Embedding(9269, 32)
        self.group_embeddings = nn.Embedding(130, 32)
        self.day_embedding = nn.Embedding(7, 4)
        self.date_embedding = nn.Embedding(365, 4)
        self.dropout = nn.Dropout(0.2)
        self.decoder = nn.Sequential(nn.Linear(105, 512), nn.ReLU(), nn.Linear(512, 1))

    def forward(self, prev_values, price, gtin, item_group, day_of_the_week, date):
        gtin = self.gtin_embeddings(gtin)
        item_group = self.group_embeddings(item_group)
        date = self.date_embedding(date)
        day_of_the_week = self.day_embedding(day_of_the_week)
        prev_values = self.lstm(prev_values)[1][0][self.num_layers - 1]
        prev_values = self.linear(prev_values)
        x = torch.cat([prev_values, day_of_the_week, date, item_group, gtin, price], dim=1)
        x = self.dropout(x)
        return self.decoder(x)

