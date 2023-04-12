FROM tensorflow/tensorflow:latest

WORKDIR /app

COPY requirements.in .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.in

COPY src .

CMD [ "python", "main.py" ]