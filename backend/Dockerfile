FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD sh -c "python ./app/database/wait_for_database.py && python -m app.database.init_db && uvicorn app.main:app --host 0.0.0.0 --port 8000"