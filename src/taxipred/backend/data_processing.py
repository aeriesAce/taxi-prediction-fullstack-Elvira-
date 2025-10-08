from taxipred.utils.constants import TRAINING_DATA_PATH, DATA_USER_PATH, MODEL_PATH
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from pydantic import BaseModel, Field
from typing import Optional
import numpy as np
import pandas as pd
import joblib
import json

class TaxiData:
    def __init__(self):
        self.df = pd.read_csv(DATA_USER_PATH)
        self.df_training = pd.read_csv(TRAINING_DATA_PATH)
        self.model = None
        self.prepare_data()
        self.load_model()

    def to_json(self):
        return json.loads(self.df.to_json(orient="records"))
    
    def to_json(self):
        return json.loads(self.df.training.to_json(orient="records"))
    
    def load_model(self):
        try: 
            self.model = joblib.load(MODEL_PATH)
            print("The model loaded succesfully.")
        except Exception as e:
            raise RuntimeError(f"Error loading model: {e}")
        
    def prepare_data(self):
        features = ["Trip_Distance_km", "Base_Fare", "Per_Km_Rate", "Per_Minute_Rate",
                    "Trip_Duration_Minutes", "Time_of_Day_Afternoon", "Time_of_Day_Evening",
                    "Time_of_Day_Morning", "Time_of_Day_Night",
                    "Day_of_Week_Weekday", "Day_of_Week_Weekend",
                    "Traffic_Conditions_High", "Traffic_Conditions_Low", "Traffic_Conditions_Medium",
                    "Weather_Clear", "Weather_Rain", "Weather_Snow"]

        X = self.df_training[features]
        y = self.df_training["Trip_Price"]

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    def residual_analysis(self, top_n, int = 5):
        y_pred = self.model.predict(self.X_test)
        residuals = self.y_test - y_pred

        df_res = pd.DataFrame({
            "Residual": residuals,
            "Predicted": y_pred,
            "Actual": self.y_test
        }, index=self.X_test.index)

        df_res = df_res.join(self.X_test)

        neg_res = df_res.nsmallest(top_n, "Residual")

        pos_res = df_res.nlargest(top_n, "Residual")

        return {
            "negative_residuals": neg_res.to_dict(orient="records"),
            "positive_residuals": pos_res.to_dict(orient="records")
        }

    def dummy_categories(self, Weather: str = "Clear", Traffic_Conditions: str = "Low", Time_of_Day: str = "Morning", Day_of_Week: str = "Weekday"):
        df_dummy = pd.DataFrame([{
            "Weather": Weather,
            "Traffic_Conditions": Traffic_Conditions,
            "Time_of_Day": Time_of_Day,
            "Day_of_Week": Day_of_Week
        }])

        df_encode = pd.get_dummies(df_dummy, columns=["Weather", "Traffic_Conditions", "Time_of_Day", "Day_of_Week"])

        return df_encode.iloc[0].to_dict()
    
    def predict_price(self, trip_distance_km: float, passenger_count: int, weather: str, time_of_day: str, day_of_week: str, traffic_conditions: str):
        features = self.dummy_categories(weather, traffic_conditions, time_of_day, day_of_week)
        numeric = {
            "Trip_Distance_km": trip_distance_km,
            "Base_Fare": 1.0,
            "Per_Km_Rate": 1.0,
            "Per_Minute_Rate": 1.0,
            "Trip_Duration_Minutes": float(trip_distance_km)
        }

        cat_num = {**features, **numeric}
        model_columns = list(self.model.feature_names_in_)
        feature_values =  {col: float(cat_num.get(col, 0.0)) for col in model_columns}
        df_row = pd.DataFrame([feature_values], columns=model_columns)
        
        price_predict = float(self.model.predict(df_row)[0])
        
        return PredictionOutput(
            predicted_price = price_predict,
        )
    
    # since these doesnt affect the price that much, but affects 
    # trip_distance_km a little, I decided to add a small amount that will affect the price
    def condtion_price_addon(self, base_fare: float, weather: str, traffic: str, time_of_day: str) -> float:
        WEATHER = {"Klart": 0.0, "Regn": 0.1, "Snö": 0.2}
        TRAFFIC  = {"Låg": 0.0, "Medium": 0.1, "Hög": 0.2}
        TIME = {"Morgon": 0.0, "Eftermiddag": 0.2, "Kväll": 0.1, "Natt": 0.0}

        total_factor = WEATHER.get(weather, 0.0) + \
                       TRAFFIC.get(traffic, 0.0) + \
                       TIME.get(time_of_day, 0.0)
        price = base_fare * (1 + total_factor)
        return price

    # function to see the average stats, for company
    def get_stats(self):
        df_filtered = self.df
        return {
            "median_price": df_filtered["Trip_Price"].median(),
            "avg_price": df_filtered["Trip_Price"].mean(),
            "avg_price_per_km": (df_filtered["Trip_Price"] / df_filtered["Trip_Distance_km"]).mean(),
            "median_trip_distance_km": df_filtered["Trip_Distance_km"].median(), 
            "top_times_of_day": df_filtered["Time_of_Day"].value_counts().to_dict(),
            "top_days_of_week": df_filtered["Day_of_Week"].value_counts().to_dict(),
        }
    
    # function to predict most popular time to travel, for user
    def popular_time(self):
        df_grouped = self.df.groupby(["Day_of_Week", "Time_of_Day"]).size().reset_index(name="count")
        return df_grouped.to_dict(orient="records")
    
    # function to get model standards and statistics
    def get_model_stats(self):
        y_pred = self.model.predict(self.X_test)
        mae = mean_absolute_error(self.y_test, y_pred)
        mse = mean_squared_error(self.y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(self.y_test, y_pred)

        return {
            "mae": mae,
            "rmse": rmse,
            "r2": r2,
            "predicted_prices": y_pred.tolist(),
            "actual_prices": self.y_test.tolist()
        }

# for testing the model
class PriceInputTest(BaseModel):
    Trip_Distance_km: float = Field(..., gt=0, lt=120)
    Base_Fare: float = Field(..., gt=0, lt=200)
    Per_Km_Rate: float = Field(..., gt=0, lt=800)
    Per_Minute_Rate: float = Field(..., gt=0, lt=800)
    Trip_Duration_Minutes: float = Field(..., gt=0, lt=2000)

    # dummy columns
    Time_of_Day_Afternoon: bool = Field(...)
    Time_of_Day_Evening: bool = Field(...)
    Time_of_Day_Morning: bool = Field(...)
    Time_of_Day_Night: bool = Field(...)

    Day_of_Week_Weekday: bool = Field(...)
    Day_of_Week_Weekend: bool = Field(...)

    Traffic_Conditions_High: bool = Field(...)
    Traffic_Conditions_Low: bool = Field(...)
    Traffic_Conditions_Medium: bool = Field(...)

    Weather_Clear: bool = Field(...)
    Weather_Rain: bool = Field(...)
    Weather_Snow: bool = Field(...)

class UserPriceInput(BaseModel):
    Trip_Distance_km: float = Field(gt=0, lt=10000)
    Passenger_Count: int = Field(gt = 0, lt = 5)
    Time_of_Day: Optional[str] = Field(default=None)
    Day_of_Week: Optional[str] = Field(default=None)
    Traffic_Conditions: Optional[str] = Field(default=None)
    Weather: Optional[str] = Field(default=None)

class PredictionOutput(BaseModel):
    predicted_price: float

class ConditionsAddonPrice(BaseModel):
    Base_Fare: float
    Time_of_Day: Optional[str] = Field(default=None)
    Traffic_Conditions: Optional[str] = Field(default=None)
    Weather: Optional[str] = Field(default=None)
