FROM python:3

WORKDIR /Puhmuckl/

COPY ./puhmuckl ./
COPY ./cogs ./

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./puhmuckl/bot.py"]