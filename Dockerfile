FROM python:3

WORKDIR /usr/youroctopus

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV FLASK_APP=src.app
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "src.wsgi:app"]

