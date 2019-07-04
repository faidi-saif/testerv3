from network.serializer import *
import threading
import time



class SerializerWithReader(Serializer):

    # --------------------------------------------------- constructor --------------------------------------------------------
    def __init__(self,arg_port,arg_baude_rate,arg_name):

        super().__init__(arg_port,arg_baude_rate,arg_parity=PARITY_NONE,arg_stopbits=STOPBITS_ONE)
        self.mthread_name     = arg_name
        self.mthread_target   = self.read_data
        self.mthread          = threading.Thread(name=self.mthread_name,target=self.mthread_target)
        self.thread_exit_flag = False
        self.m_data           = ""
        self.coded_data       = []
        self.name             = arg_name
        #print("****************************************", self.mthread_name, " serializer Init")

    # ---------------------------------------------------append data from serial port ------------------------------------
    def read_data(self):
        '''
        store the data from serial ports
        :return: None
        '''
        self.clean_data()
        while self.thread_exit_flag == False:
            len_data = self.ser.inWaiting()
            if len_data != 0:
                data = self.ser.read(len_data)
                self.coded_data.append(data)
            time.sleep(0.01)

    # --------------------------------------------------- start_acquisition --------------------------------------------------------

    def start_acquisition(self):
        '''
        start the thread for a new acquisition
        :return: None
        '''
        self.thread_exit_flag = False
        self.mthread = threading.Thread(name = self.mthread_name, target = self.mthread_target)
        self.mthread.start()


    # --------------------------------------------------- getter for data --------------------------------------------------------
    def get_data(self):
        '''
        decode data
        :return: data stored form serial ports
        '''
        self.m_data = ""
        for line in self.coded_data:
            try:
                self.m_data = self.m_data + line.decode('utf-8')
            except UnicodeDecodeError  :
                print("data available but exception detected  : 'utf-8' codec can't decode byte 0xf8 in position 0: invalid start byte")
        return self.m_data

    # --------------------------------------------------- clean buffer --------------------------------------------------------
    def clean_data(self):
        '''
        after reading , clean variables for new reading
        :return: None
        '''
        self.m_data = ""
        self.coded_data.clear()

    # ---------------------------------------------------stop acquisition --------------------------------------------------------
    def stop_acquisition(self):
        '''
        stop the acquisition at the end of reading
        :return:
        '''
        self.thread_exit_flag = True
        self.mthread.join()

    # --------------------------------------------------- destructor --------------------------------------------------------
    def __del__(self):
        super().__del__()

# ser = SerializerWithReader('/dev/RTOS',115200,'rtos')
# ser.start_acquisition()
# ser.send_data('t dbg on')
# time.sleep(0.01)
# ser.stop_acquisition()
# print(ser.get_data())

