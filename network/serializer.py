from serial import *
import time
class Serializer:

    # ---------------------------------------------------constructor --------------------------------------------------------
    def __init__(self,arg_port,arg_baude_rate = 9600,arg_parity = None,arg_stopbits = None):
        # ------------------------------------- configure serial port --------------------------------------------------------
        self.mstopbits   = arg_stopbits
        self.mparity     = arg_parity
        self.mport       = arg_port
        self.mbaudrate   = arg_baude_rate
        self.ser         = Serial(port = self.mport,baudrate = self.mbaudrate,parity = self.mparity,stopbits = self.mstopbits,timeout = None)
        print( "connect to -------------->  ",self.ser.portstr)

        # ----------------------------------------check which port is really used -----------------------------------
        if self.ser.portstr == self.mport:
            pass
        else:
            raise Exception("Wrong port or device ! check your usb port")

    # ---------------------------------------- encode_data -----------------------------------------
    def encode_data(self,arg_data):
        '''
        :param arg_data:string to send
        :return: encoded data
        '''
        return str.encode(arg_data)
    # ---------------------------------------- sed data via serial port -----------------------------------------

    def send_data(self,arg_data):
        '''
        1-a short sleep to prevent multiple access on serial port
        2-carriage return to data
        3- wait for input/output buffers to be clean before sending data
        4- write in the buffer of the serial instance
        :param arg_data: data to be sent
        :return: None
        '''
        time.sleep(0.2)
        l_data = self.encode_data(arg_data + '\r\n')
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write(l_data)


    # ---------------------------------------- destructor , close serial port -----------------------------------------
    def __del__(self):
        self.ser.close()
