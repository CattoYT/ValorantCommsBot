import threading
import sounddevice as sd
import soundfile as sf
import numpy as np
import speaker
#unused, can remove

def play_audio(file_path, volume):
    # Read the audio file
    data, samplerate = sf.read(file_path)

    # Convert audio data to the expected data type
    data = data.astype(np.float32)

    data *= volume



    # Create a new Stream object
    stream = sd.OutputStream(device=None, channels=1, callback=None, samplerate=samplerate)

    # Start the stream
    stream.start()

    # Write the audio data to the stream
    stream.write(data)

    # Stop and close the stream
    stream.stop()
    stream.close()

def play_audio_in_thread(file_path):
    # Create a new thread to play the audio
    audio_thread = threading.Thread(target=play_audio, args=(file_path, 0.5))
    audio_thread.start()

# Provide the path to your MP3 file
mp3_file_path = 'voices/Keqing-low-hp.wav'
sd.query_devices()
# Call the function to play the audio into the microphone in a separate thread
play_audio_in_thread(mp3_file_path)