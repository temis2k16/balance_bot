FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN chmod 400 .env

RUN pip install -r requirements.txt

CMD [ "python", "hostvds_bot.py" ]