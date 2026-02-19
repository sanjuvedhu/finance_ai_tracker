import numpy as np
from sklearn.linear_model import LinearRegression

def predict_next_month(monthly_totals: list) -> float:
    if len(monthly_totals) < 2:
        return monthly_totals[0] if monthly_totals else 0.0
    
    X = np.arange(len(monthly_totals)).reshape(-1, 1)
    y = np.array(monthly_totals)
    model = LinearRegression().fit(X, y)
    next_month = np.array([[len(monthly_totals)]])
    return round(float(model.predict(next_month)[0]), 2)