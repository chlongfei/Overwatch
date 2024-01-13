FROM python:latest

WORKDIR /etc/overwatch/backend
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . ./

CMD [ "python", "owbackend.py" ]