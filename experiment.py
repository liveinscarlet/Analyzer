import pyvisa
import numpy as np
from analyzer import Pna

if __name__ == "__main__":
    rm = pyvisa.ResourceManager()
    PNA = Pna(rm, 'TCPIP0::169.254.25.7::inst0::INSTR')

    # обозначение переменных
    points = 2001
    freq_start = 5 * 10 ** 6
    freq_stop = 5 * 10 ** 9

    # analyzer.bandwidth_Setup(freq_start, freq_stop, points)
    print('Ready to input traces...')
    # print(PNA.get_trace((input())))
    PNA.set_new_trace((input()))









