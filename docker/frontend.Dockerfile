FROM python:3.9
WORKDIR /app
COPY frontend/ .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
