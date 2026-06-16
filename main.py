import os
import subprocess
import librosa
import soundfile as sf
import noisereduce as nr
from pydub import AudioSegment, silence

INPUT_FOLDER = r"D:\path-to-audio-folder"
OUTPUT_FOLDER = os.path.join(INPUT_FOLDER, "processed")

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# ---------- Convert AMR → WAV ----------
def convert_amr_to_wav(input_path, output_path):
    command = [
        "ffmpeg", "-y",
        "-i", input_path,
        "-ar", "16000",
        "-ac", "1",
        output_path
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# ---------- Remove Noise ----------
def reduce_noise(wav_path):
    audio, sr = librosa.load(wav_path, sr=None)
    reduced = nr.reduce_noise(y=audio, sr=sr)
    return reduced, sr


# ---------- Remove Silence ----------
def remove_silence(audio_array, sr):
    temp_path = "temp_clean.wav"
    sf.write(temp_path, audio_array, sr)

    audio = AudioSegment.from_wav(temp_path)

    chunks = silence.split_on_silence(
        audio,
        min_silence_len=400,
        silence_thresh=audio.dBFS - 14,
        keep_silence=200
    )

    if not chunks:
        return None

    combined = sum(chunks)

    out_path = "temp_silence_removed.wav"
    combined.export(out_path, format="wav")

    cleaned, sr = librosa.load(out_path, sr=None)
    return cleaned


# ---------- Process Files ----------
for file in os.listdir(INPUT_FOLDER):
    if file.lower().endswith(".amr"):
        print(f"Processing: {file}")

        input_file = os.path.join(INPUT_FOLDER, file)
        temp_wav = os.path.join(INPUT_FOLDER, "temp.wav")

        output_file = os.path.join(
            OUTPUT_FOLDER,
            file.replace(".amr", ".wav")
        )

        convert_amr_to_wav(input_file, temp_wav)

        audio, sr = reduce_noise(temp_wav)

        cleaned_audio = remove_silence(audio, sr)

        if cleaned_audio is not None:
            sf.write(output_file, cleaned_audio, sr)
        else:
            print(f"Skipped (no usable audio): {file}")


# Cleanup
for f in ["temp.wav", "temp_clean.wav", "temp_silence_removed.wav"]:
    if os.path.exists(f):
        os.remove(f)

print("\n✅ Done! Check 'processed' folder.")
