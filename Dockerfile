FROM python:3.11-slim
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    make \
    cmake \
    git 
COPY requirements.txt /requirements.txt
RUN pip3 install --prefer-binary -r requirements.txt
RUN pip3 install dash dash-extensions
RUN apt-get clean
WORKDIR /app
COPY . /app
EXPOSE 8000
CMD gunicorn -b :8000 app:app 
