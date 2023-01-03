FROM python:3.9-slim-buster

WORKDIR .

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "scripts/train_test.py"]

CMD ["streamlit", "run", "app/app.py"]

# CMD ["bentoml", "serve", "scripts/service.py"]
