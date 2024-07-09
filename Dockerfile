FROM python:3.10.13-slim-bullseye

# RUN apt-get update && apt-get install lzip git make gcc g++ -y && apt clean && rm -rf /var/lib/apt/lists/*

# setting working directory
WORKDIR /app

COPY ./requirements.txt ./requirements.txt

# install dependencies
RUN pip install -r requirements.txt --no-cache-dir

# copy this project to the working directory
COPY . /app

# RUN cp example.env .env

# setting timezone for log
ENV TZ="Asia/Taipei"

# run the app by using uvicorn command
CMD ["python", "main.py"]