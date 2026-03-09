import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# 1. Create Synthetic Tilapia Data (Step 1 of your Math Model)
data = {
    'pH': [7.2, 8.4, 5.0, 9.5, 7.0],
    'Temp': [28, 29, 20, 35, 27],
    'DO': [6.5, 5.5, 2.1, 1.5, 7.0],
    'Turbidity': [10, 15, 45, 60, 8],
    'Quality': [2, 2, 0, 0, 2] # 2=Good, 0=Bad
}

df = pd.DataFrame(data)

# 2. Initialize the Random Forest
X = df[['pH', 'Temp', 'DO', 'Turbidity']] # Inputs
y = df['Quality'] # Labels

model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

# 3. Save the Brain
joblib.dump(model, 'tilapia_model.pkl')
print("Step 1 Complete: Model 'tilapia_model.pkl' has been created!")