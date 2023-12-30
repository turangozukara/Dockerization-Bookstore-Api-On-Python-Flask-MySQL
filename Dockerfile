FROM python:alpine
RUN apk update
RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev && \
    pip install --upgrade pip && \
    pip install cryptography
WORKDIR Dockerization-Bookstore-Api-On-Python-Flask-MySQL
COPY bookstore-api.py .
COPY requirements.txt .
RUN pip3 install -r requirements.txt
EXPOSE 80
CMD python3 bookstore-api.py