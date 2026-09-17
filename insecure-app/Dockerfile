# Start from Ubuntu
FROM ubuntu:20.04

# Avoid interactive dialog during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install Python and pip only (Docker CLI removed as it's not needed for legitimate app functionality)
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create a non-root user to run the application
RUN useradd -m -u 1000 -s /bin/bash appuser

# Create /app directory and set as working directory
RUN mkdir /app && chown appuser:appuser /app
WORKDIR /app
ADD app.py /app/
RUN chown appuser:appuser /app/app.py

# Create an uploads directory with appropriate ownership
RUN mkdir /uploads && chown appuser:appuser /uploads

# Install Flask
RUN pip3 install Flask

# Switch to non-root user before running the application
USER appuser

CMD ["python3", "/app/app.py"]
