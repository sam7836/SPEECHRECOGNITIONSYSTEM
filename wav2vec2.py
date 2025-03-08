import os
import torch
import torchaudio
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

# ✅ Load the pre-trained Wav2Vec 2.0 model
model_name = "facebook/wav2vec2-large-960h"
processor = Wav2Vec2Processor.from_pretrained(model_name)
model = Wav2Vec2ForCTC.from_pretrained(model_name)

def transcribe_audio(audio_path):
    """Transcribe speech from a WAV file using Wav2Vec 2.0"""

    if not os.path.exists(audio_path):
        print(f"❌ Error: File {audio_path} not found!")
        return

    try:
        # ✅ Load the audio file
        waveform, sample_rate = torchaudio.load(audio_path)
        print(f"✅ Loaded {audio_path} successfully with sample rate {sample_rate}")

        # ✅ Convert audio to correct format (16kHz, single channel)
        if sample_rate != 16000:
            transform = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)
            waveform = transform(waveform)
            sample_rate = 16000

        # ✅ Process the audio and run inference
        input_values = processor(waveform.squeeze().numpy(), sampling_rate=sample_rate, return_tensors="pt").input_values
        with torch.no_grad():
            logits = model(input_values).logits
        
        # ✅ Decode the output text
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = processor.batch_decode(predicted_ids)[0]
        
        print(f"📝 Transcription: {transcription}")

    except Exception as e:
        print(f"❌ Error processing audio: {e}")

# ✅ Use your WAV file
audio_file = "converted.wav"
transcribe_audio(audio_file)
