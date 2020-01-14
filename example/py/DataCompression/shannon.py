import random
import numpy as np
from collections import Counter

def generator(prob, N):

    return [0 if random.random() < prob else 1 for i in range(N)]

def entropy_exp(s):  # entropy by experience distribution. ex) s='0101..11'

    prb_0 = list(s).count('0') / len(s)
    prb_1 = 1.0 - prb_0
    if prb_0 == 1.0 or prb_1 == 1.0:
        ent_exp = 0.0
    else:
        ent_exp = - prb_0*np.log2(prb_0)- prb_1*np.log2(prb_1)

    return ent_exp
    
def coder(data, blk, ent, eps, rat):

    # binary data to symbols (= message)
    # ex) [0,1,1,0,1,0,0,1,...] -> ['0110','1001',...] (for blk = 4) 
    message = [''.join(map(str,data[i:i+blk])) for i in range(0,len(data),blk)]

    # histogram
    syms = list(Counter(message).keys())
    frqs = list(Counter(message).values())
    prbs = [frqs[i]/len(message) for i in range(len(frqs))]
    hist = dict(zip(syms, prbs))

    # codebook
    index = 0
    digits = int(rat*blk)  # number of digits for each code
    codebook = {}
    for s,p in hist.items():
        ent_exp = entropy_exp(s)
        if abs(ent_exp - ent) <= eps and index < 2**digits-1:
            codebook[s] = '{:0{digits}b}'.format(index, digits=digits)
            index += 1
    codebook[False] = '{:0{digits}b}'.format(index, digits=digits)

    # coding (message -> codes)
    codes = [codebook[s] if s in codebook else codebook[False]
             for s in message]

    # decodebook
    decodebook = {}
    for k,v in codebook.items():
        decodebook[v] = k
    
    return (codes, decodebook)

def decoder(codes, decodebook, block):

    message = [decodebook[c] for c in codes]
    blocks = [list(s) if s != False else generator(0.5,block) for s in message]
    data_str = sum(blocks, [])

    return [int(d) for d in data_str]

def error_rate(data_in, data_out):

    N = len(data_in)
    count = 0
    for i in range(N):
        if data_in[i] != data_out[i]:
            count += 1
            
    return count / N

if __name__ == "__main__":

    # settings
    BLK = 10          # block size
    NUM = BLK * 1000  # number of binary data sequence
    PRB = 0.8         # probability to generate '0'
    ENT = - PRB * np.log2(PRB) - (1-PRB) * np.log2(1-PRB)  # entropy (= 0.7219..)
    RAT = 0.9         # transmission rate (RAT > ENT)
    EPS = 0.15         # eplsilon for typical sequence
    print("NUM = ", NUM)
    print("BLK = ", BLK)
    print("ENT = ", ENT)
    print("RAT = ", RAT)

    # generate data sequence
    data_in = generator(PRB, NUM)

    # code the data
    (codes, decodebook) = coder(data_in, BLK, ENT, EPS, RAT)

    # decode the data
    data_out = decoder(codes, decodebook, BLK)

    # evaluate error rate
    err_rate = error_rate(data_in, data_out)
    print("error rate = ", err_rate)
