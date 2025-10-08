import joblib
import numpy as np
import pandas as pd
from taxipred.utils.constants import MODEL_PATH, TRAINING_DATA_PATH
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

df = pd.read_csv(TRAINING_DATA_PATH)
X, y = df.drop("Trip_Price", axis = 1), df["Trip_Price"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

def build_train_model(X_train, y_train, X_test, y_test):
    model = RandomForestRegressor(n_estimators=200, random_state=42)
    #model = HistGradientBoostingRegressor(random_state=42, max_iter=200)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    mae  = mean_absolute_error(y_test, pred)
    rmse = np.sqrt(mean_squared_error(y_test, pred))
    r2   = r2_score(y_test, pred)
    r_rmse = rmse / np.abs(y_test.mean())

    print(f"MAE: {mae:.2f}  RMSE: {rmse:.2f}  R²: {r2:.3f}  Relative RMSE: {r_rmse:.3f}")
    return model

def save_model(X, y):
    final_model =  RandomForestRegressor(n_estimators=200, random_state=42)
    #final_model = HistGradientBoostingRegressor(random_state=42, max_iter=200)
    final_model.fit(X,y)
    joblib.dump(final_model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

    return MODEL_PATH

def load_and_evaluate(model_path, X, y):
    clf = joblib.load(model_path)
    pred = clf.predict(X)

    mae  = mean_absolute_error(y, pred)
    rmse = float(np.sqrt(mean_squared_error(y, pred)))
    r2   = r2_score(y, pred)
    r_rmse = rmse/np.abs(y.mean())

    print(f"MAE: {mae:.2f}  RMSE: {rmse:.2f}  R²: {r2:.3f} Relative RMSE: {r_rmse:.2f}")
    print(rmse/np.abs(y.mean()))

    return mae, rmse, r2,  r_rmse

model = build_train_model(X_train, y_train, X_test, y_test)
model_path = save_model(X, y)
load_model = load_and_evaluate(model_path, X, y)
