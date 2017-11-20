
import sys
import wave
import numpy as np
from gcc_phat import gcc_phat
from removeNoice import removeNoice

def tdoa(point1,point2) :
    # if len(sys.argv) != 3:
    #     print('Usage: {} near.wav far.wav'.format(sys.argv[0]))
    #     sys.exit(1)
    #we can improve the code by avoiding redoing same process by checking wheather _clear is available already ....
    print("Localization in progress...")
    firstPoint = point1
    secondPoint = point2
    # removeNoice(sys.argv[1])
    # removeNoice(sys.argv[2])
    removeNoice(firstPoint)
    removeNoice(secondPoint)
    #################
    # near= wave.open(sys.argv[1]+"_clear.wav", 'rb')
    # far = wave.open(sys.argv[2]+"_clear.wav", 'rb')

    near = wave.open(firstPoint + "_clear.wav", 'rb')
    far = wave.open(secondPoint+"_clear.wav", 'rb')
    rate = near.getframerate()
    timelist = []
    N = rate

    window = np.hanning(N)

    while True:
            sig = near.readframes(N)
            if len(sig) != 2 * N:
                break

            ref = far.readframes(N)
            sig_buf = np.fromstring(sig, dtype='int16')
            ref_buf = np.fromstring(ref, dtype='int16')
            tau, _ = gcc_phat(sig_buf * window, ref_buf * window, fs=rate, max_tau=1)
            timelist.append(( tau *1000)/0.0226)
            # print ((tau*1000))
    # print(timelist[4])
    return (timelist[4])
        #tau, _ = gcc_phat(sig_buf, ref_buf, fs=rate, max_tau=1)
        #print(( tau *1000 )/0.0226)
