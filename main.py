from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from FeatureDto import FeatureRequest
from joblib import load

# load all the models
knn_model = load('./models/knn_model.joblib')
lgm_model = load('./models/lgm_classifier.joblib')
mlp_model = load('./models/mlp_model.joblib')
rf_model = load('./models/mlp_model.joblib')
xgb_model = load('./models/xgb_classifier.joblib')
le = load('./models/label_encoder.joblib')

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/model/{model_name}")
async def predict_crop(model_name: str, data: FeatureRequest):
    feature_set = [[data.N, data.P, data.K, data.temperature, data.humidity, data.ph, data.rainfall]]
    crop = None
    if model_name == 'xgb':
        prediction = xgb_model.predict(feature_set)
        crop = le.inverse_transform(prediction)[0]
    elif model_name == 'lightgbm':
        prediction = lgm_model.predict(feature_set)
        crop = le.inverse_transform(prediction)[0]
    elif model_name == 'knn':
        prediction = knn_model.predict(feature_set)
        crop = le.inverse_transform(prediction)[0]
    elif model_name == 'mlp':
        prediction = mlp_model.predict(feature_set)
        crop = le.inverse_transform(prediction)[0]
    elif model_name == 'random_forest':
        prediction = rf_model.predict(feature_set)
        crop = le.inverse_transform(prediction)[0]
    return {"crop": crop}
