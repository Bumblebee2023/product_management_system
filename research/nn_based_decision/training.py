import torch
import json
from torch import nn

from dataset import CustomDataloader, CustomDataset
from model import Model
from sklearn.model_selection import train_test_split
from torch.utils.tensorboard import SummaryWriter

import warnings

warnings.filterwarnings("ignore")

data = json.load(open("datasets/short_term_dataset.json"))
train, test = train_test_split(data, random_state=42, train_size=0.8, shuffle=True)
train_dataset = CustomDataset(train)
test_dataset = CustomDataset(test)
device = torch.device("cuda:0")
train_dl = CustomDataloader(train_dataset, batch_size=512, num_workers=1)
test_dl = CustomDataloader(test_dataset, batch_size=512, num_workers=1)
model = Model()
writer = SummaryWriter("logs")
torch.cuda.empty_cache()

if __name__ == '__main__':
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.L1Loss()
    model.to(device)
    for epoch in range(10):
        l = []
        model.train()
        for i, data in enumerate(train_dl):
            y_pred = model(data["prev_values"].to(device),
                           data["price"].to(device),
                           data["gtin"].to(device).reshape(len(data["gtin"])),
                           data["item_group"].to(device).reshape(len(data["item_group"])),
                           data["day_of_week"].to(device).reshape(len(data["day_of_week"])),
                           data["date"].to(device).reshape(len(data["date"])))
            y_test = data["y_true"].to(device)
            loss = criterion(y_pred, y_test)
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            optimizer.zero_grad()
            l.append(loss)
            if i % 5 == 0:
                print(f"Epoch {epoch}, step {i}/{len(train_dl)} - loss = {sum(l) / len(l)}")
        writer.add_scalar("Train_loss", loss, epoch)
        torch.save(model.state_dict(), f"checkpoints/epoch{epoch}.pt")
        model.eval()
        for data in test_dl:
            test_loss = []
            with torch.no_grad():
                y_pred = model(data["prev_values"].to(device),
                               data["price"].to(device),
                               data["gtin"].to(device).reshape(len(data["gtin"])),
                               data["item_group"].to(device).reshape(len(data["item_group"])),
                               data["day_of_week"].to(device).reshape(len(data["day_of_week"])),
                               data["date"].to(device).reshape(len(data["date"])))
                y_test = data["y_true"].to(device)
                loss = criterion(y_pred, y_test)
                test_loss.append(loss)
        writer.add_scalar("Test_loss", loss, epoch)
