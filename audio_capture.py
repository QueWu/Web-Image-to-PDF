import scipy.io.wavfile as wav
import wave
import pyaudio
from scipy.fftpack import fft
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as interpol
import time as timer


def initRec(handle):
    FORMAT = pyaudio.paInt16
    #RECORD_SECONDS = 5
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024
    global WAVE_OUTPUT_FILENAME
    global dummyArr
    global currentShape
    #WAVE_OUTPUT_FILENAME = "../file_" + str(wavID(seed)) + ".wav"
    WAVE_OUTPUT_FILENAME = handle

    audio = pyaudio.PyAudio()

    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    frames = []
    start = timer.time()
    while(True):
        print("Recording Status ON for: ["+handle+"]")
        userIn = input("q for Quit")
        if(userIn == "q"):
            stream.stop_stream()
            RECORD_SECONDS = timer.time() - start
            print("Recording Stopped ")
            break
        data = stream.read(CHUNK)
        frames.append(data)
    
    
    '''for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)'''
    
    # stop Recording
    
    stream.close()
    audio.terminate()

    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

def batchRec(batch):
    i = 402
    for x in range(batch):
        if(x%6==0):print(">>> SET READY <<<"); time.sleep(5)
        initRec("train_"+str('%02d' % (i))+".wav")
        i+=1


def read_extract(fileName):
    from python_speech_features import mfcc
    from python_speech_features import delta
    from python_speech_features import logfbank

    print("current read: ", fileName, end='\r', flush=True)
    (rate,sig) = wav.read(fileName)
    print(fileName, " read successful", end='\r', flush=True)

    sig = sig[threshold_cut(sig):]
    sig = sig[:threshold_cut_rear(sig)]
    testArr = np.array(sig).ravel()
    sig = sec_cut(testArr)

    mfcc_feat = mfcc(sig,rate)
    d_mfcc_feat = delta(mfcc_feat, 2)
    #dd_mfcc_feat = delta(d_mfcc_feat, 2)
    fbank_feat = logfbank(sig,rate)
    
    return fbank_feat

def select_plot(fileName):
    print("current read: ", fileName, end='\r', flush=True)
    (rate,sig) = wav.read(fileName)
    print(fileName, " read successful", end='\r', flush=True)
    print(sig)
    #sig = sig[threshold_cut(sig):]
    #sig = sig[:threshold_cut_rear(sig)]
    segs = segmentation(sig)
    plot(sig)
    #plot(sig[segs[0][0]])
    #testArr = np.array(sig).ravel()
    #sig = sec_cut(testArr)
    
    #plot(sig[:500])
    #print(sum(sig[:100])/len(sig[:100]))

def plot(inArr):
    plt.ylabel("Y")
    plt.xlabel("X (Time)")
    plt.plot(inArr)
    plt.show()

def segmentation(inSig):
    slience_threshold = 20000
    segments = []
    post = []
    combo = 0
    ref_point = 0
    
    for i in range(len(inSig)):
        if((inSig[i][0]<0.003 and inSig[i][0]>-0.003)):
            combo+=1
        else:
            combo=0
        if(combo==slience_threshold):
            segments.append(i-slience_threshold+1)
            segments.append(i)
            ref_point = i-slience_threshold+1
            combo = 0
            
    j = 1
    while(j < len(segments)-1):
        if(segments[j+1] - segments[j] != 1):
            post.extend(inSig[segments[j]:segments[j+1]])
            #plot(post)
        j+=2
        #post = []
    
    #plot(post)
    #for xc in segments:
        #plt.axvline(x=xc)
    #plt.plot(inSig)
    return post
            
        

def threshold_cut(inSig):
    keeper = 0
    #print(inSig[1])
    for i in range(len(inSig)):
        if((inSig[i][0] > 0.02) or (inSig[i][0] < -0.02)):
            keeper = i
            break
    #print(keeper)
    return keeper
    #newAudio = newAudio[keeper:]
	
def threshold_cut_rear(inSig):
	keeper = 0
	i = -1
	for x in range(len(inSig)):
		if((inSig[i][0] > 0.02) or (inSig[i][0] < -0.02)):
			keeper = i
			break
		i+=-1
	#print(keeper)
	return keeper

def sec_cut(newAudio):
    if(len(newAudio) != 88200):
        #print("in interpol")
        arrInterpol = interpol.interp1d(np.arange(newAudio.size),newAudio)
        arrOut = arrInterpol(np.linspace(0,newAudio.size-1,88200))
    return arrOut


initRec("long_rec_test.wav")
select_plot("long_rec_test.wav")



