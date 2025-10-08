from importlib.resources import files

TAXI_CSV_PATH = files("taxipred").joinpath("data/taxi_trip_pricing.csv")
TRAINING_DATA_PATH = files("taxipred").joinpath("data/training_data.csv")
DATA_USER_PATH = files("taxipred").joinpath("data/user_data.csv")
MODEL_PATH = files("taxipred").joinpath("models/final_model.joblib")