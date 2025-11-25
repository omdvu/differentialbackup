FROM python:3.11-slim
WORKDIR /app
COPY differential.py /app/differential.py
COPY comparedict.py /app/comparedict.py
COPY mirrorbackup.py /app/mirrorbackup.py
COPY requirements.txt /app/
RUN pip3 install -r requirements.txt
ENTRYPOINT [ "python3", "/app/differential.py" ]