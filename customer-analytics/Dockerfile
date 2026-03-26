FROM python:3.11-slim

WORKDIR /app/pipeline/

COPY requirements.txt /app/pipeline/
RUN pip install -r requirements.txt

COPY . /app/pipeline/

CMD ["bash"]
COPY preprocess.py /app/pipeline/