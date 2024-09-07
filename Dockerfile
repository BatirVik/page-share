FROM python:3.12

RUN pip install poetry

WORKDIR /app

COPY . .

RUN poetry install --only main

ENV ENV=production

CMD ["poetry", "run", "uvicorn", "--host=0.0.0.0", "--port=8000", "app.main:app"]
