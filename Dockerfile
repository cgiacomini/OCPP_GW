# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install PostgreSQL client and development libraries
RUN apt-get update && apt-get install -y \
    libpq-dev \
    postgresql-client \
    gcc \
    && rm -rf /var/lib/apt/lists/*

ENV CONFIG_FILE /app/config.cfg
ENV LOG_FILE /app/logs/csms_server.log
ENV LOG_LEVEL INFO
ENV PYTHONPATH /app
RUN mkdir -p /app/logs
RUN mkdir -p /app/utils

# Copy the current directory contents into the container at /app
#COPY ./sleep.py /app/sleep.py
COPY ./csms_server/csms_server.py /app
COPY ./utils /app/utils
COPY ./sleep.py /app
COPY requirements.txt /app/
COPY config.cfg /app/
RUN pip install --no-cache-dir -r requirements.txt


# Run csms_server.py when the container launches
CMD python csms_server.py --config $CONFIG_FILE --log_file $LOG_FILE --log_level "$LOG_LEVEL"
#CMD ["python", "sleep.py"]
