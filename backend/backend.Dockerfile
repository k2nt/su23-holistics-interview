FROM python:3.11-alpine
WORKDIR /backend
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt
COPY . .
CMD ["flask", "run"]
