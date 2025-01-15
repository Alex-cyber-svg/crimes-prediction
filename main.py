from fastapi import FastAPI
import pickle
import numpy as np
from pydantic import BaseModel
import lightgbm

app = FastAPI()

class InputData(BaseModel):
    Month: int
    Latitude: float
    Longitude: float
    Status_category: int

with open('lightgbm_model_latlon.pkl', 'rb') as f:
    model = pickle.load(f)

with open('encoder.pkl', 'rb') as f:
    encoder = pickle.load(f)

@app.post('/predict')
async def predict(input_data: InputData):
    x_new = np.array([[
        input_data.Month,
        input_data.Latitude,
        input_data.Longitude,
        input_data.Status_category
    ]])

    prediction = model.predict(x_new)

    prediction_transformed = encoder.inverse_transform(prediction)

    return {"prediction":str(prediction_transformed)}