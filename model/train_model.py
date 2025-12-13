# model/train_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pickle
import os

os.makedirs("model", exist_ok=True)

df = pd.read_csv("model/dataset.csv")

# dataset columns: fuel,speed,distance,traffic,co2
X = df[["fuel", "speed", "distance", "traffic"]]
y = df["co2"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=150, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

# Save model
with open("model/emission_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained and saved to model/emission_model.pkl")
