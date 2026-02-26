import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import warnings

# Suppress harmless statistical warnings for clean terminal output
warnings.filterwarnings("ignore")

def predict_future_demand(days_to_predict: int = 7) -> dict:
    """
    Trains an ARIMA model on historical ticket volume data to predict future demand.
    """
    
    # 1. Mock Archival Data (Demand)
    # In a production system, this would be: 
    # SELECT DATE(created_at), COUNT(id) FROM tickets GROUP BY DATE(created_at)
    historical_data = {
        'date': pd.date_range(start='2026-01-01', periods=30, freq='D'),
        'ticket_count': [5, 7, 6, 12, 14, 4, 3, 6, 8, 7, 15, 16, 5, 4, 7, 9, 8, 14, 18, 6, 5, 8, 10, 9, 17, 19, 7, 6, 9, 11]
    }
    
    # 2. Convert to a Pandas DataFrame
    df = pd.DataFrame(historical_data)
    df.set_index('date', inplace=True)
    
    # 3. Define the ARIMA Model Parameters (p, d, q)
    # p = 5: Look at the last 5 days (AutoRegressive)
    # d = 1: Difference the data once to make it stationary (Integrated)
    # q = 0: No moving average window (Moving Average)
    model = ARIMA(df['ticket_count'], order=(5, 1, 0))
    
    # 4. Train the Model
    fitted_model = model.fit()
    
    # 5. Forecast the Next 'N' Days
    forecast = fitted_model.forecast(steps=days_to_predict)
    
    # 6. Format the output for our API
    forecast_results = {
        "historical_average": float(df['ticket_count'].mean()),
        "forecast": forecast.round(0).astype(int).tolist() # Round to whole numbers
    }
    
    return forecast_results

# --- TEST THE ALGORITHM ---
if __name__ == "__main__":
    print("Forecasting Next 7 Days of CCS Tickets...")
    results = predict_future_demand()
    print(results)