import pyvisa
import numpy as np


class Pna:
    def __init__(self,
                 visa_manager: pyvisa.ResourceManager,
                 addr_pna: str = 'TCPIP0::169.254.25.7::inst0::INSTR'):
        self.rm = visa_manager
        self.pna = visa_manager.open_resource(addr_pna)  # The name of the PNA in the experiment
        # self.Pna.query("SYStem:PRESet")
        print(self.pna.query("*IDN?"))

    def bandwidth_Setup(self, freq_start, freq_stop, num_of_points):
        """
        This function sets up the frequency parameters of the PNA
        :param freq_start: the lowest frequency
        :param freq_stop: the highest frequency
        :param num_of_points: step
        :return:
        """
        self.pna.write("SENS:SWE:TYPE LIN")
        self.pna.write(f"SENS:FREQ:START {freq_start}")
        self.pna.write(f"SENS:FREQ:STOP {freq_stop}")
        self.pna.write(f"SENS:SWE:POINts {num_of_points}")
        return freq_start, freq_stop, num_of_points

    def attenuating_Setup(self, output_attenuation_power_level):
        """
        This function sets up the output attenuating power level to the second port
        :param output_attenuation_power_level: level of attenuation, dB
        :return: NaN
        """
        self.pna.query(f"SENS:ATT BREC, {output_attenuation_power_level}")

    def power_Settings_Setup(self, output_power):
        """
        This function sets up the output power
        :param output_power: output power
        :return: NaN
        """
        self.pna.query(f"SOUR:POW:CORR:LEV {output_power}")

    def get_trace(self, number_of_trace, num_of_points):
        """
        This function gets up the points of trace in string type
        :param number_of_trace:
        :param num_of_points:
        :return:
        """
        # self.pna.write(f'CALC:DATA RDATA')
        # self.pna.write('INIT:CONT OFF')
        # self.pna.write('INIT:IMM;*wai')
        self.pna.write('CALC:PAR:DEF MyMeasurment, S11')
        self.pna.write('CALC:PAR:SEL MyMeasurment')
        return self.pna.query(f':CALCulate1:DATA:SNP? 1')
        # data = self.pna.read("CALC:DATA? A")
        # for i in num_of_points:
        #     for j in 1:
        #     string_of_points = self.pna.query()
    pass

