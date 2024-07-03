FROM python:3.11-slim

LABEL authors="joelshapiro"

WORKDIR /app

# NOTE TO SELF: to build and deploy to GCP, use this "docker buildx build --platform linux/amd64 -t gcr.io/waste-not-leftovers/waste-not:[v0.1] ."

# Install necessary packages and clean up
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# copy the contents of the current directory into the app
COPY . /app


RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8080

# Define environment variable
#ENV PORT=8501

# Define the health check
#HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
#  CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# run the app/main.py when the container launches
ENTRYPOINT ["streamlit", "run", "app/main.py", "--server.port=8080", "--server.address=0.0.0.0"]