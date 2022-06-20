# Specify our container base image
FROM python:3.9

COPY . /app
WORKDIR /app

# Install dependencies
RUN pip install -r requirements.txt

# Give our container internet access
EXPOSE 5000

ENV MYSQL_USER python
ENV MYSQL_PASS password
ENV MYSQL_HOST mysql
ENV MYSQL_DB gamesys

ENTRYPOINT ["python", "-m", "app"]