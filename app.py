from flask import Flask, request
import torch
import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""
from werkzeug.utils import secure_filename
import whisperx
import gc
from pyannote.audio import Pipeline
import logging
logging.basicConfig(level=logging.DEBUG) 
app = Flask(__name__)

device = "cpu"
compute_type = "float32"  # change to "int8" if low on GPU mem (may reduce accuracy)
YOUR_HF_TOKEN=os.getenv("HUGGING_FACE_TOKEN", "nothing")
# Load the models and initialize them outside the request handling function
diarize_model = whisperx.DiarizationPipeline(use_auth_token=YOUR_HF_TOKEN, device=device)

model = whisperx.load_model("large-v2", device, compute_type=compute_type)

@app.route("/transcribe", methods=["POST"])
def transcribe():
    # Check if the "audio" field is in the request
    if "audio" not in request.files:
        return "No audio file provided", 400

    # Save the uploaded audio file
    audio_file = request.files["audio"]
    filename = secure_filename(audio_file.filename)
    audio_path = f"uploads/{filename}"
    audio_file.save(audio_path)

    batch_size = 32  # reduce if low on GPU mem

    # 1. Transcribe with original whisper (batched)
    audio = whisperx.load_audio(audio_path)
    result = model.transcribe(audio, batch_size=batch_size)
    transcriptions = result["segments"]  # before alignment

    # 2. Align whisper output
    model_a, metadata = whisperx.load_align_model(language_code="en", device=device)
    result = whisperx.align(transcriptions, model_a, metadata, audio, device, return_char_alignments=False)
    aligned_transcriptions = result["segments"]  # after alignment

    # 3. Assign speaker labels
    diarize_segments = diarize_model(audio_path)
    result = whisperx.assign_word_speakers(diarize_segments, result)
    speaker_segments = result["segments"]  # segments are now assigned speaker IDs

    # Clean up the uploaded audio file
    gc.collect()
    audio_file.close()

    # Return the transcriptions with speaker labels
    return {
        "transcriptions": transcriptions,
        "aligned_transcriptions": aligned_transcriptions,
        "speaker_segments": speaker_segments
    }


if __name__ == "__main__":
    app.run(host = "0.0.0.0")
