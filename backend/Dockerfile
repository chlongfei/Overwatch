FROM python:latest

WORKDIR /etc/overwatch/backend
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . ./

CMD [ "flask", "--app", "owbackend", "run", "--host=0.0.0.0" ]