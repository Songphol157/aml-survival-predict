FROM python:3.11-slim
 
# scikit-survival needs a compiler for some versions; drop these two lines if
# the build succeeds without them.
RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*
 
WORKDIR /app
 
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
 
COPY . .
 
# app.py loads the model via a path relative to itself, so it must run from
# the webpage/ directory.
WORKDIR "/app/master project/webpage"
 
EXPOSE 8080
 
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--timeout", "120", "app:app"]
 
