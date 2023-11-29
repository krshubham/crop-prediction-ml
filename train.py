import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
import xgboost as xgb
from joblib import dump
import lightgbm as lgm


data = pd.read_csv('./Crop_recommendation.csv')

features=data[['N', 'P','K','temperature', 'humidity', 'ph', 'rainfall']]
target=data['label']

le = LabelEncoder()
target_encoded = le.fit_transform(target)

Xtrain, Xtest, Ytrain, Ytest = train_test_split(features, target_encoded, test_size=0.2, random_state=2)
scaler = StandardScaler()


def train_xgb_classifier():
    print("Training XGBoost classifier")
    XB = xgb.XGBClassifier()
    train_x = Xtrain.values
    XB.fit(train_x, Ytrain)
    dump(XB, 'models/xgb_classifier.joblib')
    print("Done Training XGBoost classifier. Saved")



def train_lgm_classifier():
    print("Training LightGBM classifier")
    modellgb = lgm.LGBMClassifier()
    modellgb.fit(Xtrain, Ytrain)
    dump(modellgb, 'models/lgm_classifier.joblib')
    print("Done Training LightGBM classifier. Saved")


def train_rf_model():
    print("Training Random Forest classifier")
    rf_model = RandomForestClassifier(n_estimators=10)
    rf_model.fit(Xtrain, Ytrain)
    dump(rf_model, 'models/random_forest_classifier.joblib')
    print("Done training Random Forest Classifier. Saved")


def train_mlp_model():
    print("Training a Neural Network")
    clf_model = MLPClassifier(solver='lbfgs', alpha=1e-4, hidden_layer_sizes=(1000, 700, 400, 200, 100, 50),
                              random_state=1)
    clf_model.fit(Xtrain, Ytrain)
    dump(clf_model, 'models/mlp_model.joblib')
    print("Done training the neural network, saved")


def train_knn_model():
    print("Training a KNN classifier")
    Xtrain_scaled = scaler.fit_transform(Xtrain)
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(Xtrain_scaled, Ytrain)
    dump(knn, 'models/knn_model.joblib')
    print("Done Training a KNN classifier. Saved")


if __name__ == '__main__':
    train_xgb_classifier()
    train_lgm_classifier()
    train_rf_model()
    train_mlp_model()
    train_knn_model()
    dump(le, './models/label_encoder.joblib')




