# capstone2-predict-service-utilisation
linear regression model to predict service demand based on public NHS emergency department utilisation data from 2019-2021

## problem description
* Ressource allocation is essential for the healthcare system. Emergency services are expected to respond to unforeseeable events. This project creates a polynomial regression model to estimate the number of patient arrivals per hour of the day (output) from daily total visits in the past (input).

## exploratory data analysis
* Explored two datasets (Dataverse and NHS).

## model training
* Multiple polynomial regression models have been evaluated using RMSE and line plots.

## reproducibility
To clone the repository run `git clone https://github.com/bsenst/capstone2-predict-service-utilisation` and move to the folder with `cd capstone2-predit-service-utilisation`.

### dependencies & environments
After cloning the repository create an environment and install the dependencies with the following steps:

`python -m venv venv`

`source venv/bin/activate`

`pip install -r requirements.txt`

or using pipenv with:

`pipenv install`

### train & test scripts for reproducibility, deployment
To run the scripts go to the scripts folder with `cd scripts` and run `python train_test.py` to reproduce the model or `bentoml serve service:svc` to serve the model with bentoml.

![image](https://user-images.githubusercontent.com/8211411/212476549-a5163503-bf55-4643-86bf-86598d19a94c.png)

To run the frontend go to the main folder via `cd ..` and run `streamlit run app/app.py` to display the streamlit frontend and explore the model and the use case.

### container
Build the Docker container with:

`docker build -t ed-volume-prediction .`

Run the Docker container with:

`docker run --rm --name ed-volume-prediction`

## cloud application
The running application can be found here: https://bsenst-capstone2-predict-service-utilisation-appapp-5tnr6y.streamlit.app/

![image](https://user-images.githubusercontent.com/8211411/212476706-a526f917-dd9f-4d38-8179-28db19212108.png)
