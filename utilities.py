import glob
import io
import os
from scipy.io import wavfile
import numpy as np
import IPython
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image, ImageTk
import librosa


def calc_fft(y,sr, maxFreq=-1):
    """
    Calcul la transformee de fourier de y qui est sample a rate sr
    L analyse est tronquee a maxFreq
    """
    n=len(y)
    freq=np.fft.rfftfreq(n,d=1/sr)
    Y=abs(np.fft.rfft(y)/n)
    if maxFreq==-1:
        return (freq,Y)
    else:
        return (freq[0:maxFreq], Y[0:maxFreq])
    
def extract2s(signal, rate):
    lengh = len(signal)
    if lengh <= 2*rate:
        return signal, rate
    else:
        return signal[int(lengh/2) - rate:int(lengh/2) + rate], rate
    

def load_train(nb_per_class,begin=0,duration=2,maxfreq=5000):
    
    if nb_per_class > 700:
        raise ValueError("too many files")
    df_train = pd.read_csv("./dataset/Metadata_Train.csv")
    guitar = df_train[df_train['Class'] == "Sound_Guitar"]
    drum = df_train[df_train['Class'] == "Sound_Drum"]
    violin = df_train[df_train['Class'] == "Sound_Violin"]
    piano = df_train[df_train['Class'] == "Sound_Piano"]
    df_exp = pd.concat([violin[0:nb_per_class], drum[0:nb_per_class], piano[0:nb_per_class], guitar[0:nb_per_class]])
    
    frequencies = None
    df_prim = pd.DataFrame
    dic = {}
    l = 0
    flag = True
    for file_name in df_exp["FileName"]:
        signal, rate = librosa.load("./dataset/Train_submission/Train_submission/"+file_name,offset=begin,duration=duration)
        #newS, newR = extract2s(signal, rate)
        fft1,fft2 = calc_fft(signal,rate, maxFreq=maxfreq)
        if(flag):
            l = len(fft1)
            flag = False
        #if frequencies == None:
        #    frequencies = fft1
        for i in range(l):
            dic[str(i/2.)] = fft2[i] # a changer si on choisit d autre frequences
    df_prim = pd.DataFrame(dic, index=df_exp.index[0:4*nb_per_class])
    df_exp = pd.concat((df_exp, df_prim), axis=1)
    return df_exp


