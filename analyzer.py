import pyvisa
import numpy as np


class Pna:
    def __init__(self,
                 visa_manager: pyvisa.ResourceManager,
                 addr_pna: str = 'TCPIP0::169.254.25.7::inst0::INSTR'):
        self.rm = visa_manager
        self.pna = visa_manager.open_resource(addr_pna)  # The name of the PNA in the experiment
        # self.pna.write("SYStem:PRESet")     # Sets up default parameters of the PNA
        self.pna.write("FORM REAL, 64")     # Defines type of output data and precision
        self.pna.write("FORMat:DATA ascii")
        print(self.pna.query("*IDN?"))      # Test of IDN function,  prints name of the device

    def bandwidth_Setup(self, freq_start, freq_stop, num_of_points):

        """
        This function sets up the frequency parameters of the PNA
        :param freq_start: the lowest frequency
        :param freq_stop: the highest frequency
        :param num_of_points: number of frequency points
        :return: NaN
        """

        self.pna.write("SENS:SWE:TYPE LIN")                         # Sets up linear scale of freq
        self.pna.write(f"SENS:FREQ:START {freq_start}")
        self.pna.write(f"SENS:FREQ:STOP {freq_stop}")
        self.pna.write(f"SENS:SWE:POINts {num_of_points}")

    def Reset(self):
        self.pna.write("*RST")

    def attenuating_Setup(self, output_attenuation_power_level):

        """
        This function sets up the output attenuating power level to the second port
        :param output_attenuation_power_level: level of attenuation, dB
        :return: NaN
        """

        if (output_attenuation_power_level % 5) or (output_attenuation_power_level > 35):   # Проверка на дурака
            print('Такое ослабление использовать нельзя')
        else:
            self.pna.query(f"SENS:ATT BREC, {output_attenuation_power_level}")

    def power_Settings_Setup(self, output_power):

        """
        This function sets up the output power
        :param output_power: output power
        :return: NaN
        """

        if output_power > 20:   # Проверка на дурака
            print('Такую мощность подавать нельзя')
        else:
            self.pna.query(f"SOUR:POW:CORR:LEV {output_power}")

    def get_trace(self, input_trace_numbers) -> np.array:
        """
        This function is getting up array of data of different traces
        :param input_trace_numbers:
        :return:
        """

        number_of_trace = 0
        i = 1
        # Count of symbols in inputted string
        length_of_str = int(len(input_trace_numbers))
        # Fetching count of points from PNA-X
        count_of_points =int(self.pna.query(f"SENS1:SWE:POINts?"))

        data=[]

        temp = np.array([])

        while length_of_str % 2:
            print('Введите чётное количество цифр.')
            input_trace_numbers = input()
            length_of_str = len(input_trace_numbers)

        while i < length_of_str:
            temp = [input_trace_numbers[i-1], input_trace_numbers[i]]
            print(temp)
            self.pna.write(f'CALC:PAR:DEF Measurment{number_of_trace+1}, S{temp[0]}{temp[1]}')
            self.pna.write(f'CALC:PAR:SEL Measurment{number_of_trace+1}')
            data_vector_of_trace = self.pna.query(f':CALCulate1:DATA:SNP? {number_of_trace+1}')
            data_vector_of_trace = data_vector_of_trace.split(',')
            data_vector_of_trace = [float(x) for x in data_vector_of_trace]
            i += 2
            data.append(data_vector_of_trace)
            # array_of_trace_data[number_of_trace - 1] = data
            number_of_trace += 1
        return data

    def set_new_trace(self, input_trace_numbers):
        # Initialization
        i = 1
        length_of_str = len(input_trace_numbers)
        number_of_trace = 1
        temp = np.array([])
        # Checking for valid input
        while length_of_str % 2:
            print('Введите чётное количество цифр.')
            input_trace_numbers = input()
            length_of_str = len(input_trace_numbers)
        #
        while i < length_of_str:
            temp = [input_trace_numbers[i - 1], input_trace_numbers[i]]
            print(temp)
            self.pna.write(f'CALC:CUST:DEF {number_of_trace}, "Standard"')
            self.pna.write(f'CALC:PAR:SEL "Standard"')
            self.pna.write(f'CALC:CUST:MOD "S{temp[0]}{temp[1]}"')

            number_of_trace += 1
            i += 2
        return None
    pass


