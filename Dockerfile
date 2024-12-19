FROM python:3.11
WORKDIR /autoCRM-backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
COPY docker-entrypoint.sh /docker-entrypoint.sh

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
EXPOSE 8000
ENTRYPOINT ["sh", "/docker-entrypoint.sh"]

