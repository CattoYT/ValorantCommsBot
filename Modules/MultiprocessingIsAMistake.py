from flask import Flask, request, jsonify
import threading
import speaker
app = Flask(__name__)
lock = threading.Lock()

someoneistalking = False

# The explanation of this file is very painful.
# I was playing a valorant match testing this, but i suffer from being too good at valorant,
# where multiple events would trigger the speaker
# The speaker lock doesn't work because its dupilcated across multiprocessing instances
# This means that there is no easy way to prevent multispeaking
# My solution to this problem after hearing "i NeEd SoMe HeAlInG oVeR hErE" 5 tims at the same time was to
# create a flask server that would only allow one person to talk at a time
# When I die, God is going to ask what the fuck happened here
# Im not even religious
# This is a mistake.
import sounddevice as sd
import soundfile as sf
@app.route('/')
def IMFUCKINGTALKING():
    global someoneistalking
    scenario = request.args.get("scenario")

    if someoneistalking:
        # Return immediately if someone is already talking
        return jsonify({'status': 'busy'}), 429


    with lock:

        someoneistalking = True
        data, fs = sf.read(speaker.getRandomFile(str(scenario)), dtype='float32')
        data = data * 0.4
        #keyboard.press('v')
        #sd.play(data, fs, device=find_device_id('CABLE Input (VB-Audio Virtual C'))
        sd.play(data, fs)
        sd.wait()
        someoneistalking = False
        return jsonify({'status': 'success'}), 200



    return jsonify({'status': 'busy'}), 429

def start():
    app.run()