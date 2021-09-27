FROM tiangolo/uvicorn-gunicorn-fastapi

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY ./app /app