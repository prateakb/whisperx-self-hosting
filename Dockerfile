# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV CUDA_VISIBLE_DEVICES=""
ENV NVIDIA_VISIBLE_DEVICES=""
ENV HUGGING_FACE_TOKEN="<YOUR-TOKEN>"
# Set the working directory
WORKDIR /app

# Install required packages in one go and cleanup afterwards
RUN apt-get update -y && \
    apt-get install -y git ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Install python dependencies
RUN pip3 install --no-cache-dir "git+https://github.com/m-bain/whisperx.git" flask

# Expose the necessary port(s) if required
EXPOSE 5000

# Copy the application into the Docker image
COPY app.py /app/app.py

# Run the Python script
CMD ["python", "app.py"]
