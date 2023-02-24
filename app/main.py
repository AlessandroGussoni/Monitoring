import json
import os
import sys

monitoring = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(monitoring)
sys.path.append(os.path.join(monitoring, 'service'))

import joblib
from fastapi import BackgroundTasks, FastAPI

from service.service.production_model import ProductionModel
from train_model import train

MODEL = joblib.load(os.path.join(os.path.dirname(__file__), "..", "app", "models", "iris_v1.joblib"))
CONFIG = os.path.join(os.path.dirname(__file__), "..", "app", "config.json")
FEATURES = ["sepal length (cm)", "sepal width (cm)", "petal length (cm)", "petal width (cm)"]

with open(CONFIG, 'r') as file:
    config = json.load(file)

production_model = ProductionModel(model=MODEL, config=config)
app = FastAPI()


@app.get("/")
async def root():
    return {"status": "OK"}


@app.get("/train")
async def train():
    await train()
    return {"status": "OK"}


@app.post("/predict")
async def predict(sepal_length: float,
                  sepal_width: float,
                  petal_length: float,
                  petal_width: float,
                  background_tasks: BackgroundTasks) -> int:
    features = {feature_name: feature_value
                for feature_name, feature_value in zip(FEATURES,
                                                       [sepal_length, sepal_width, petal_length, petal_width])}

    y = production_model.predict([[sepal_length, sepal_width, petal_length, petal_width]])

    return y


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8090, reload=False)
