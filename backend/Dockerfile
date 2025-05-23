FROM python:3.11-slim

WORKDIR /app

# Copy only the contents of backend/ (adjusted to real host structure)
COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt

ENV PYTHONPATH=/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


