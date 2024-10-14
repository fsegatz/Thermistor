import streamlit as st
import math

K_to_C = lambda t:                  t - 273.15
C_to_K = lambda t:                  t + 273.15
K_from_R = lambda r, r0, b0, t0:    b0 * t0 / (b0 - 2 * math.log( r0 / r ) )
R_from_K = lambda t, r0, b0, t0:    r0 * math.exp( b0 / 2 * (t0 / t - 1) )

class Sidebar:
    _bValueNtc = 0
    _rValueNtc = 0
    _tValueCNtc = 0
    _bValueSoftware = 0
    _rValueSoftware = 0
    _tValueCSoftware = 0
    _tMinC = 0
    _tMaxC = 0
    def __init__(self):
        st.sidebar.header('Thermistor')
        self._bValueNtc = st.sidebar.number_input(  'B Value', 0, 10000, 4063)
        self._rValueNtc = st.sidebar.number_input(  'R Value', 0, 100000, 10000)
        self._tValueCNtc = st.sidebar.number_input( 'T Value (C)', -50, 50, 25)
        st.sidebar.header('Software')
        self._bValueSoftware = st.sidebar.number_input('B SW Value', 0, 10000, 4100)
        self._rValueSoftware = st.sidebar.number_input('R SW Value', 0, 100000, 10000)
        self._tValueCSoftware = st.sidebar.number_input('T SW Value (C)', -50, 50, 25)
        st.sidebar.header('Temperature range')
        self._tMinC = st.sidebar.number_input('T min (C)', -1000, 0, -40)
        self._tMaxC = st.sidebar.number_input('T max (C)', 0, 1000, 180)

class App:
    def __init__(self):
        st.title('Thermistor Calculator')
        st.write('This app calculates the temperature measurement error when using a thermistor with different properties than specified in the software.')
        self.sidebar = Sidebar()
    
    def run(self):
        ## Create array of resistor values for the 
        tValuesCNtc = [i for i in range(self.sidebar._tMinC, self.sidebar._tMaxC + 1)]

        rValuesNTC = [R_from_K(C_to_K(tC), self.sidebar._rValueNtc, self.sidebar._bValueNtc, C_to_K(self.sidebar._tValueCNtc)) for tC in tValuesCNtc]
        # Create the temperatures calculated by software
        tValuesCSoftware = [K_to_C(K_from_R(r, self.sidebar._rValueSoftware, self.sidebar._bValueSoftware, C_to_K(self.sidebar._tValueCSoftware))) for r in rValuesNTC]
        
        # Calculate the error between the two
        error = [tNtc - tSoftware for tNtc, tSoftware in zip(tValuesCNtc, tValuesCSoftware)]

        # Create a dictionary with the values
        data = {
            'Temperature (C)': tValuesCNtc,
            'Resistor NTC': rValuesNTC,
            'Temperature Software (C)': tValuesCSoftware,
            'Error (C)': error
        }

        # Create a scatter plot
        st.line_chart(
            data,
            x='Temperature (C)',
            y=['Error (C)']
        )
        



if __name__ == '__main__':
    app = App()
    app.run()