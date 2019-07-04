from network.serializer import *
from network.arduinoOptions import *
import os

device_serial = 'YKa1184'

class ArduinoSerializer(Serializer):

    # ---------------------------------------------- constructor------------------------------------------
    def __init__(self,arg_port,arg_baude_rate=9600):
        self.mparity = PARITY_NONE
        self.mstopbits = STOPBITS_ONE
        super().__init__(arg_port=arg_port,arg_baude_rate=arg_baude_rate,arg_parity=self.mparity,arg_stopbits=self.mstopbits)
        time.sleep(1)

    # ---------------------------------------------- destructor------------------------------------------
    def __del__(self):
        super().__del__()

    # ---------------------------------------------- power_on------------------------------------------
    def power_on(self):  # tested ok
        os.system('sudo ykushcmd ykushxs -s {} -d'.format(device_serial))
        time.sleep(0.5)
        os.system('sudo ykushcmd ykushxs -s {} -u'.format(device_serial))
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write(PRESS_POW)
        time.sleep(2)
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write(RELEASE_POW)
        time.sleep(2)

    # ---------------------------------------------- power_off------------------------------------------
    def power_off(self): # not tested yet
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write(PRESS_POW)
        time.sleep(8)
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write(RELEASE_POW)
        time.sleep(2)

    # ---------------------------------------------- reinit------------------------------------------
    def reinit(self):  # tested Ok
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write(RE_INIT)
        time.sleep(3)

    # ---------------------------------------------- reset------------------------------------------
    def reset(self):
        time.sleep(3)
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write(PRESS_EP_RST)
        time.sleep(0.5)
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write(RELEASE_EP_RST)
        time.sleep(0.5)

    # ---------------------------------------------- fw_flash------------------------------------------
    def fw_flash(self):
        os.system('sudo ykushcmd ykushxs -s {} -d'.format(device_serial))
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write(PRESS_POW)  # press power
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write(PRESS_SHUTT)  # press shutter
        time.sleep(0.5)
        os.system('sudo ykushcmd ykushxs -s {} -u'.format(device_serial))
        time.sleep(14)
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write(RELEASE_POW)
        time.sleep(2)
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write(RELEASE_SHUTT)
        time.sleep(8)
        self.reset()

    # ---------------------------------------------- press------------------------------------------
    def press(self,arg_button):
        '''

        :param arg_button: pressed button
        :return:
        '''
        assert (arg_button == 'mode' or arg_button == 'shutter') ,"Invalid button , use : 'mode or 'shutter "
        if arg_button == 'shutter' :
            press   = PRESS_SHUTT
            release = RELEASE_SHUTT
        else :
            press   = PRESS_POW
            release = RELEASE_POW
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write(press)
        time.sleep(1)
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write(release)

    # ---------------------------------------------- reboot------------------------------------------
    def reboot(self):
        os.system('sudo ykushcmd ykushxs -s {} -d'.format(device_serial))
        time.sleep(0.5)
        os.system('sudo ykushcmd ykushxs -s {} -u'.format(device_serial))
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write(PRESS_POW)
        time.sleep(2)
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write(RELEASE_POW)
        time.sleep(2)







# m_serialzer = ArduinoSerializer('/dev/ARDUINO',9600)
# m_serialzer.fw_flash()
# os.system('ssh root@192.168.0.202 "/usr/local/gopro/bin/gpdevSendCmd RB &"')
# m_serialzer.fw_flash()
# ArduinoSerializer.reinitialise()

