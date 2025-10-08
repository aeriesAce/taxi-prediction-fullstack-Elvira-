from fastapi import FastAPI, APIRouter, HTTPException
from taxipred.backend.data_processing import TaxiData, PredictionOutput, UserPriceInput, PriceInputTest, StatsUserInput, ConditionsAddonPrice
import pandas as pd
import joblib
from taxipred.utils.constants import MODEL_PATH

app = FastAPI(description = "A ml-model predicting taxi prices")
taxi_data = TaxiData()
router = APIRouter(prefix = "/api/taxi")

# get all data
@router.get("")
async def read_data():
    try:
        return taxi_data.to_json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while fetching the data: {str(e)}")
    
# for company statistics
@router.get("/company/statistics")
async def average_stats():
    try:
        data = taxi_data.get_stats()
        return {"stats": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    
# to show the user dufferent statistics based on time of day
@router.get("/user/popular")
async def taxi_stats():
    try:
        data = taxi_data.popular_time()
        return {"popular_times": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")

# fetching the model to make statistic visualisations for the company
@router.get("/model/statistics")
async def model_stats():
    try:
        stats = taxi_data.get_model_stats()
        return {"stats": stats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching model stats: {e}")
    
# showing model predictions with residuals
@router.get("/model/residuals")
async def model_residuals(top_n: int = 5):
    try:
        data = taxi_data.residual_analysis(top_n=top_n)
        return {"residuals": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching residuals: {e}")
    
# a made up price calculater for traffic and weather conditions
# more realistic for the user
@router.post("/conditions")
async def condition_add_ons(payload: ConditionsAddonPrice):
    try:
        price = taxi_data.condtion_price_addon(
            base_fare=payload.Base_Fare,
            weather=payload.Weather,
            traffic=payload.Traffic_Conditions,
            time_of_day=payload.Time_of_Day
        )
        return {"price": price}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    
# to see if the data and model loads correctly
@router.post("/predict", response_model=PredictionOutput)
async def predict_price(payload: PriceInputTest):
    try:
        data_to_predict = pd.DataFrame([payload.model_dump()])
        clf = joblib.load(MODEL_PATH)
        prediction = clf.predict(data_to_predict)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    return {"predicted_price": prediction[0]}


# for user prediction in the streamlit dashboad
@router.post("/predict/user", response_model=PredictionOutput)
async def predict_price_user(payload: UserPriceInput):
    try:
        return taxi_data.predict_price(
            payload.Trip_Distance_km,
            payload.Passenger_Count,
            payload.Time_of_Day,
            payload.Day_of_Week,
            payload.Traffic_Conditions,
            payload.Weather,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

app.include_router(router=router)