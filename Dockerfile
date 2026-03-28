FROM python:3.11-slim

WORKDIR /app/pipeline/

RUN pip install --no-cache-dir \
	pandas numpy matplotlib seaborn scikit-learn scipy requests

COPY . /app/pipeline/

CMD ["bash"]
