echo FROM python:3.9-slim > Dockerfile
echo WORKDIR /app >> Dockerfile
echo COPY requirements.txt . >> Dockerfile
echo RUN pip install --no-cache-dir -r requirements.txt >> Dockerfile
echo COPY . . >> Dockerfile
echo ENV PORT=8080 >> Dockerfile
echo CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"] >> Dockerfile