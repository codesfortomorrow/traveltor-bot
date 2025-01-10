# base image
FROM python:3.10

WORKDIR /traveltor-bot

RUN python -m venv .venv
RUN . .venv/bin/activate
RUN python -m pip install --upgrade pip setuptools wheel

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
