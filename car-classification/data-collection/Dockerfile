FROM python:3.11

WORKDIR /app

COPY requirements.in .
RUN pip install --no-cache-dir -r requirements.in

COPY src .

CMD [ "python", "main.py" ]