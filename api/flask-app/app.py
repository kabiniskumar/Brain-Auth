from flask import Flask, jsonify, request
import pyedflib
import numpy as np
from scipy.fftpack import fft
import pickle

app = Flask(__name__)

fft_n = 5

def preprocess_and_predict(file):
    data = pyedflib.EdfReader(file)
    signals = data.signals_in_file
    L = data.getNSamples()[0]

    user_data = None
    init = True
    for i in range(signals):
        channel = data.readSignal(i)
        Y = fft(channel)
        P2 = abs(Y / L) * 2
        P1 = P2[0:int(L / 2) + 1]
        if init:
            user_data = P1[0:fft_n]
            init = False
        else:
            user_data = np.concatenate((user_data, P1[0:fft_n]))
    user_data_final = user_data.reshape(1, fft_n * signals)

    clf = pickle.load(open(
        "C:/Users/palla/OneDrive/Documents/ASU/SemesterIII/MobileComputing/Project/Data/eeg-motor-movementimagery-dataset-1.0.0/files/model_4.sav","rb"))
    predictions = clf.predict(user_data_final)
    print(predictions)
    result = {}
    result[1] = int(predictions[0])
    return result

@app.route('/authenticate', methods=['POST'])
def authenticate():
    request_data = request.get_data()
    break_pt = request_data.find(b"\r\n\r\n")+4
    f = open('temp_file.edf', 'wb')
    f.write(request_data[break_pt:])
    f.close()
    out = preprocess_and_predict('temp_file.edf')
    return jsonify(out)

if __name__ == '__main__':
    app.run()