# capstone2-predict-service-utilisation
linear regression model to predict service demand based on public NHS emergency department utilisation data from 2019-2021

## problem description
* Ressource allocation is essential for the healthcare system. Emergency services are expected to respond to unforeseeable events. This project creates a polynomial regression model to estimate the number of patient arrivals per hour of the day (output) from daily total visits in the past (input).

## exploratory data analysis
* Explored two datasets (Dataverse and NHS).
* The data does not contain all feature details (high granularity).

## model training
* Multiple polynomial regression models have been evaluated using RMSE and line plots.

## train & test scripts for reproducibility, deployment
Run `python train_test.py` to reproduce the model.
Run `bentoml serve service:svc` to serve the model with bentoml.
Run `streamlit run app/app.py` to display the streamlit frontend and explore the model and the use case.

## dependencies & environments
`python -m venv venv -r requirements.txt`
or
`pipenv install`

## container
* docker container

## cloud application
The running applicaton can be found here: https://bsenst-capstone2-predict-service-utilisation-appapp-5tnr6y.streamlit.app/
