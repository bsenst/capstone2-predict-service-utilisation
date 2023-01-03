import pickle
from math import sqrt
import pandas as pd
import numpy as np
import bentoml
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model

print("Loading dataset ...")
hours = pd.read_excel("https://files.digital.nhs.uk/5C/702A3E/AE2021_National_Data_Tables.xlsx", sheet_name=13, skiprows=6, nrows=24)

poly_feat = PolynomialFeatures(3)

X_trian, X_test, y_train, y_test = train_test_split(np.array(range(24)).reshape(-1, 1),
                                                    (hours["Number of A&E attendances that arrived by ambulance"])*100/sum(hours["Number of A&E attendances that arrived by ambulance"]),
                                                    test_size=0.3, random_state=42)

X_train = poly_feat.fit_transform(X_trian)
X_test = poly_feat.fit_transform(X_test)

lr_model= linear_model.LinearRegression()

lr_model.fit(X_train, y_train)

y_pred = lr_model.predict(X_test)
rmse = sqrt(mean_squared_error(y_test, y_pred))

#root mean squared error
print("Root Mean squared error with PolynomialFeatures set to 2 degrees: %.2f" 
        % sqrt(mean_squared_error(y_test, y_pred)))

# save the model to disk
filename = 'finalized_model.pkl'
pickle.dump(lr_model, open(filename, 'wb'))
print("Model saved to", filename)

# Save model to the BentoML local model store
saved_model = bentoml.sklearn.save_model("ed_volume_model", lr_model)
print(f"Model saved with BentoML: {saved_model}")