FROM alpine:3.20.3
WORKDIR /usr/local/app

RUN apk add --no-cache python3 py3-pip
RUN python -m venv /opt/venv

COPY requirements.txt ./
RUN . /opt/venv/bin/activate && pip install --no-cache-dir -r requirements.txt

COPY src ./src

RUN addgroup -S app && adduser -S app -G app

RUN mkdir /usr/local/app/uploads
RUN mkdir /usr/local/app/logs
RUN chown app:app /usr/local/app/uploads
RUN chown app:app /usr/local/app/logs

USER app

EXPOSE 5000
CMD . /opt/venv/bin/activate && flask --app /usr/local/app/src/app.py run -p 5000 -h 0.0.0.0
