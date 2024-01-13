FROM python:latest

WORKDIR /
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . ./

CMD ["python3", "ca-on-tor-rescu_update.py"]