import numpy as np
from lib import fft_convolve2d


def conway(state, k=None):
    """
    Conway's game of life state transition
    """

    # set up kernel if not given
    if k == None:
        m, n = state.shape
        k = np.zeros((m, n))
        k[m//2-1 : m//2+2, n//2-1 : n//2+2] = np.array([[1,1,1],[1,0,1],[1,1,1]])

    # computes sums around each pixel
    b = fft_convolve2d(state,k).round()
    c = np.zeros(b.shape)

    c[np.where((b == 2) & (state == 1))] = 1
    c[np.where((b == 3) & (state == 1))] = 1

    c[np.where((b == 3) & (state == 0))] = 1

    # return new state
    return c

def replicator(state, k=None):
    """
    'Replicator' cellular automaton state transition
    http://www.conwaylife.com/wiki/Replicator_(CA)
    """
    if k == None:
        m, n = state.shape
        k = np.zeros((m, n))
        k[m//2-1 : m//2+2, n//2-1 : n//2+2] = np.array([[1,1,1],[1,0,1],[1,1,1]])

    b = fft_convolve2d(state,k).round()
    c = np.zeros(b.shape)
    # checks the values, and sets alive vs. dead state
    c[np.where((b + 1) % 2 == 0)] = 1

    # return new state
    return c

def day_and_night(state, k=None):
    """
    'Day & night' automata state transition
    http://www.conwaylife.com/wiki/Day_%26_Night
    """
    # set up kernel if not given
    if k == None:
        m, n = state.shape
        k = np.zeros((m, n))
        k[m//2-1 : m//2+2, n//2-1 : n//2+2] = np.array([[1,1,1],[1,0,1],[1,1,1]])

    # computes sums around each pixel
    b = fft_convolve2d(state,k).round()
    c = np.zeros(b.shape)

    c[np.where((b == 3) & (state == 1))] = 1
    c[np.where((b == 6) & (state == 1))] = 1
    c[np.where((b == 7) & (state == 1))] = 1
    c[np.where((b == 8) & (state == 1))] = 1

    c[np.where((b == 3) & (state == 0))] = 1
    c[np.where((b == 4) & (state == 0))] = 1
    c[np.where((b == 6) & (state == 0))] = 1
    c[np.where((b == 7) & (state == 0))] = 1
    c[np.where((b == 8) & (state == 0))] = 1

    # return new state
    return c

def high_life(state, k=None):
    """
    'HighLife' automata state transition
    http://www.conwaylife.com/wiki/HighLife
    """
    if k == None:
        m, n = state.shape
        k = np.zeros((m, n))
        k[m//2-1 : m//2+2, n//2-1 : n//2+2] = np.array([[1,1,1],[1,0,1],[1,1,1]])

    # computes sums around each pixel
    b = fft_convolve2d(state,k).round()
    c = np.zeros(b.shape)

    c[np.where((b == 2) & (state == 1))] = 1
    c[np.where((b == 3) & (state == 1))] = 1

    c[np.where((b == 3) & (state == 0))] = 1
    c[np.where((b == 6) & (state == 0))] = 1

    # return new state
    return c


if __name__ == "__main__":
    # set up board
    m,n = 10,10
    A = np.random.random(m*n).reshape((m, n)).round()
    