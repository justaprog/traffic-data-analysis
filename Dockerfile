FROM python:3

WORKDIR /usr/youroctopus

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV FLASK_APP=src.webapplication
ENV FLASK_ENV=production

CMD ["flask", "run", "--host=0.0.0.0"]
