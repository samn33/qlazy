import numpy as np

def decimal_to_binlist(decimal, digits): # ex) 6,3 --> [1,1,0]

    bin_str = "{:0{digits}b}".format(decimal, digits=digits)
    return  [int(s) for s in list(bin_str)]
    
def binlist_to_decimal(bin_list): # ex) [0,1,1] --> 3

    return int("".join([str(i) for i in bin_list]), 2)

def make_hamming_matrix(r):

    # parity check matrix (H)
    A = []
    for x in range(1,2**r):
        bin_list = decimal_to_binlist(x, r)
        if sum(bin_list) == 1: continue
        A.append(bin_list)
    A = np.array(A)
    I_H = np.eye(r, dtype=int)
    H = np.concatenate([A, I_H])
    
    # represent integer each row of H matrix (for error correction algorithm)
    H_int = [binlist_to_decimal(row) for row in H]
    
    # generator matrix (G)
    I_G = np.eye(2**r-r-1, dtype=int)
    G = np.concatenate([I_G, A], 1)
    
    return G, H, H_int

def generate_data(k, N):  # random k-bits data

    for _ in range(N):
        yield np.random.randint(2, size=k)

def add_noise(d_in):  # bit flip to one bit (select randomly)

    idx = np.random.randint(len(d_in))
    err = np.array([1 if i == idx else 0 for i in range(len(d_in))])
    d_out = (d_in + err) % 2
    return d_out
    
def correct_error(d_in, H_int):

    d_out = d_in.copy()
    p = (d_out @ H) % 2
    x = binlist_to_decimal(p)
    err_idx = H_int.index(x)
    d_out[err_idx] = (d_out[err_idx] + 1) % 2  # bit flip (recover)
    return d_out
    
if __name__ == '__main__':

    r = 3
    n = 2**r - 1
    k = 2**r - r - 1
    N = 10

    G, H, H_int  = make_hamming_matrix(r)

    print("* input(random) -> encode -> add noise(random 1-bit flip) -> correct -> decode:")
    err_count = 0
    for x in generate_data(k, N):
        y = (x @ G)%2
        y_error = add_noise(y)
        y_correct = correct_error(y_error, H_int)
        x_correct = y_correct[0:k]  # decode (= extract 1st to k-th elements)
        print("{0:} -> {1:} -> {2:} -> {3:} -> {4:}".format(x,y,y_error,y_correct,x_correct))
        
        if sum((x+x_correct)%2) == 1: # if x != x_correct --> 1
            err_count += 1

    err_rate = err_count / N
    print("* error rate = {0:} (count:{1:} / total:{2:})".format(err_rate, err_count, N))
