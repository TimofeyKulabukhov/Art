FROM python:3.12-alpine
RUN pip install flask-login
RUN pip install flask-SQLAlchemy
COPY . /opt/app
WORKDIR /opt/app
CMD [ "python", "app.py" ]