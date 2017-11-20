from pydub import AudioSegment
import wave
import matplotlib.pyplot as plt
import numpy as np

def removeNoice(signal):
    refSignal =  AudioSegment.from_wav(signal+".wav")
    loudness = refSignal.max_dBFS
    length = refSignal.sample_width
    frameRate = refSignal.frame_rate
    frameCount = refSignal.frame_count()
    print ("Loudness    :"+str(loudness))
    print("NumberOfFrames   :"+str(frameCount))
    print ("FrameRate   :"+str(frameRate))
    print ("SampleWidth :"+str(length))
    new = refSignal.high_pass_filter(1000)
    name = signal + "_clear.wav"
    new.export(name, format="wav")
