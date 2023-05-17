import pyvisa
import numpy as np


class Pna:
    def __init__(self,
                 visa_manager: pyvisa.ResourceManager,
                 addr_pna: str = 'TCPIP0::169.254.25.7::inst0::INSTR'):
        self.rm = visa_manager
        self.pna = visa_manager.open_resource(addr_pna)  # The name of the PNA in the experiment
        self.pna.write("SYStem:PRESet")
        self.pna.write("FORM REAL, 64")
        self.pna.write("FORMat:DATA ascii")
        print(self.pna.query("*IDN?"))

    def bandwidth_Setup(self, freq_start, freq_stop, num_of_points):

        """
        This function sets up the frequency parameters of the PNA
        :param freq_start: the lowest frequency
        :param freq_stop: the highest frequency
        :param num_of_points: number of frequency points
        :return: NaN
        """

        self.pna.write("SENS:SWE:TYPE LIN")
        self.pna.write(f"SENS:FREQ:START {freq_start}")
        self.pna.write(f"SENS:FREQ:STOP {freq_stop}")
        self.pna.write(f"SENS:SWE:POINts {num_of_points}")

    def attenuating_Setup(self, output_attenuation_power_level):

        """
        This function sets up the output attenuating power level to the second port
        :param output_attenuation_power_level: level of attenuation, dB
        :return: NaN
        """

        if (output_attenuation_power_level % 5) or (output_attenuation_power_level > 35):
            print('Такое ослабление использовать нельзя')
        else:
            self.pna.query(f"SENS:ATT BREC, {output_attenuation_power_level}")

    def power_Settings_Setup(self, output_power):

        """
        This function sets up the output power
        :param output_power: output power
        :return: NaN
        """

        if output_power > 20:
            print('Такую мощность подавать нельзя')
        else:
            self.pna.query(f"SOUR:POW:CORR:LEV {output_power}")

    def get_trace(self, input_trace_numbers) -> np.array:
        """
        This function is getting up array of data of different traces
        :param input_trace_numbers:
        :return:
        """

        array_of_trace_data = []
        number_of_trace = 1
        i = 0
        length_of_str = len(input_trace_numbers)
        array_of_trace_data = np.arange(0, length_of_str / 2, 1)
        temp = np.array([])
        while i < length_of_str:
            if length_of_str % 2:
                print('Проверка на дурака не пройдена')
            else:
                temp = [input_trace_numbers[i], input_trace_numbers[i+1]]
                print(temp)
                self.pna.write(f'CALC:PAR:DEF MyMeasurment, S{temp[0]}{temp[1]}')
                self.pna.write('CALC:PAR:SEL MyMeasurment')
                data = self.pna.query(f':CALCulate1:DATA:SNP? {number_of_trace}')
                i += 2
                data = [float(x) for x in data]
                array_of_trace_data[number_of_trace - 1] = data
                number_of_trace += 1
        return array_of_trace_data

    @staticmethod
    def get_freq(freq_start, freq_stop, num_of_points):

        """
        This function forms array of frequencies
        :param freq_start: the lowest possible frequency
        :param freq_stop: the highest possible frequency
        :param num_of_points: amount of data points
        :return: array with frequency points
        """

        return np.linspace(freq_start, freq_stop, num_of_points)

    pass
