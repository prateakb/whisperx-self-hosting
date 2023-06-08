
# Flask Speech-to-Text App with Whisperx

This repository contains a Flask application that uses the Whisperx library to transcribe and align audio data, and then assign speaker labels to the transcriptions.

## Setup

1. **Build Docker Image**

 To build the Docker image, navigate to the directory containing the Dockerfile and run: 
 ```shell
    docker build -t whisperx-app:latest .
``` 
2. **Run Docker Container**

 After building the Docker image, run the container using: 
 ```shell
    docker run -p 5000:5000 -d whisperx-app:latest
``` 
## Usage

To use the app, send a POST request to `http://localhost:5000/transcribe` with an audio file attached with the key `audio`. The application will return the transcriptions with speaker labels.

Example:

```shell
curl -X POST -F 'audio=@your_audio_file.wav' http://localhost:5000/transcribe
``` 

## Requirements

-   Docker
-   Python 3.10
-   Whisperx

## Environment Variables

-   `CUDA_VISIBLE_DEVICES`: This environment variable is used to limit the number of visible CUDA devices. In this application, it's set to an empty string which implies no GPU is used.
-   `NVIDIA_VISIBLE_DEVICES`: Similar to `CUDA_VISIBLE_DEVICES`, this environment variable is used to limit the number of visible Nvidia devices. In this application, it's set to an empty string.
-   `HUGGING_FACE_TOKEN`: The API token for the Hugging Face API. Set this to your Hugging Face API token.
## Hosting on Kubernetes

If you prefer to host the application on a Kubernetes cluster, configuration files are provided in the `k8-manifests` directory.

1.  **Deploy the Application**
    
    To deploy the application, use the `kubectl apply` command:
    
    ```shell
    kubectl apply -f k8-manifests/deployment.yaml
    kubectl apply -f k8-manifests/service.yaml
    kubectl apply -f k8-manifests/hpa.yaml` 
    ```
2.  **Access the Application**
    
    The application will be accessible through the service `whisperx-transcription-service` at port `80`.

## Notes

-   The application runs on the CPU and not the GPU, so it may not be suitable for large-scale production use.
-   Remember to replace `<YOUR-TOKEN>` in the Dockerfile with your actual Hugging Face API token.