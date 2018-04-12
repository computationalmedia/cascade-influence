from functools import reduce
import pandas as pd
import numpy as np

def casIn(cascade_path, time_decay):
    """
    compute influence in one cascade
    """

    cascade = pd.read_csv(cascade_path) # Read one cascade from local file
    p_ij = P(cascade, r=time_decay) # compute p_ij in given cascade
    inf, m_ij = influence(p_ij) # compute user influence
    cascade["influence"] = pd.Series(inf)
    return cascade


def P(cascade,r = -0.000068):
    """ 
    this function compute the maritx P of a cascade
    """

    n = len(cascade)
    t = np.zeros(n,dtype = np.float64)
    f = np.zeros(n,dtype = np.float64)
    p = np.zeros((n,n),dtype = np.float64)
    norm = np.zeros(n,dtype = np.float64)
    for k, row in cascade.iterrows():
        if k == 0:
            p[0][0] = 1
            t[0] = row['time']
            f[0] = 1 if row['magnitude'] == 0 else row['magnitude']
            continue

        t[k] = row['time']
        f[k] = 1 if row['magnitude'] == 0 else row['magnitude']
        p[:k, k] = ((r * (t[k] - t[0:k])) + np.log(f[0:k])) # store the P_ji in log space
        norm[k] = reduce(np.logaddexp, p[:k, k])
        p[:k, k] = np.exp(p[:k, k] - norm[k])# recover the P_ji from log space
      
    return p


def influence(p):

    """Estimate user influence
    This function compute the user influence and store 
    it in matirx m_ij
    """
    n = len(p)
    m = np.zeros((n, n))
    m[0, 0] = 1
    for i in range(0, n-1):
        vec = p[:i+1, i+1]
        m[:i+1, i+1] = m[:i+1, :i+1]@vec
        m[i+1, i+1] = 1
    influence = np.sum(m, axis = 1)

    return influence, m

