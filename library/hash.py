import numpy as np

def hash(mes):
    print(mes)
    hash = 0
    for i in range(len(mes)):
        data =  ord(mes[i])
        hash += np.floor(np.log2(data)/np.log2(2)) + 1
    return(int (hash))

