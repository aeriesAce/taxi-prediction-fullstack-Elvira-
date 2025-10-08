import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from taxipred.utils.constants import TRAINING_DATA_PATH

df = pd.read_csv(TRAINING_DATA_PATH)
X, y = df.drop("Trip_Price", axis = 1), df["Trip_Price"]

def scale_dataset(X_train, X_test):
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return X_train_scaled, X_test_scaled
    
def model_evaluation(X_train, X_test, y_train, y_test):
    # linear regression model
    X_train_scaled, X_test_scaled = scale_dataset(X_train, X_test)
    results = []
    
    lr = LinearRegression()
    lr.fit(X_train_scaled, y_train)
    predict_lr = lr.predict(X_test_scaled)
    results.append({
        "Model": "Linear Regression",
        "MAE": mean_absolute_error(y_test, predict_lr),
        "RMSE":np.sqrt(mean_squared_error(y_test, predict_lr)),
        "R²": r2_score(y_test, predict_lr)
    })

    # randomforest model
    rf = RandomForestRegressor(random_state = 42, n_estimators = 200)
    rf.fit(X_train, y_train)
    predict_rf = rf.predict(X_test)
    results.append({
        "Model": "Random Forest",
        "MAE": mean_absolute_error(y_test, predict_rf),
        "RMSE": np.sqrt(mean_squared_error(y_test, predict_rf)),
        "R²": r2_score(y_test, predict_rf)
    })

#     # gradientboosting model, found it while googling for different models, just wanted to test
      # it got a really good result, talk to kokchun about it
#     hgb = HistGradientBoostingRegressor(random_state=42, max_iter=200)
#     hgb.fit(X_train, y_train)
#     predict_hgb = hgb.predict(X_test)

#     results.append({
#         "Model": "HistGradientBoosting",
#         "MAE":  mean_absolute_error(y_test, predict_hgb),
#         "RMSE": np.sqrt(mean_squared_error(y_test, predict_hgb)),
#         "R²":   r2_score(y_test, predict_hgb)
# })

    return pd.DataFrame(results)


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
res = model_evaluation(X_train, X_test, y_train, y_test)
print(res)
best = res.loc[res["RMSE"].idxmin(), "Model"]
print("\nThe model that scored best:", best)