import torch
import soundfile as sf  # pip install soundfile
import tempfile
import os

# Audio params
SAMPLE_RATE = 16000

# Load Silero STT model from torch.hub
device = torch.device('cpu')
stt_model, stt_decoder, stt_utils = torch.hub.load(
    repo_or_dir='snakers4/silero-models',
    model='silero_stt',
    language='en',
    device=device
)
(read_batch, split_into_batches, read_audio, prepare_model_input) = stt_utils

# Load Silero TE (Text Enhancer) - i.e., punctuation and capitalization model
# No autocorrect unfortunately
te_model, example_texts, languages, punct, apply_te = torch.hub.load(
    repo_or_dir='snakers4/silero-models',
    model='silero_te'
)

def silero_stt(audio_np) -> str:
    # Save numpy audio to temp WAV file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_wav:
        sf.write(tmp_wav.name, audio_np, SAMPLE_RATE)
        tmp_filename = tmp_wav.name

    try:
        batches = split_into_batches([tmp_filename], batch_size=1)
        input_tensor = prepare_model_input(read_batch(batches[0]), device=device)

        output = stt_model(input_tensor)
        transcripts = [stt_decoder(out.cpu()) for out in output]
        transcript = " ".join(transcripts)
        # print("[INFO] Raw: " + transcript)

        # Apply Text Enhancement
        # transcript = apply_te(transcript, lan='en')
        # print("[INFO] Enchanced: " + transcript)

    finally:
        os.remove(tmp_filename)
        return transcript
