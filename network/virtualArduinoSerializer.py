from network.arduinoSerializer import ArduinoSerializer

class VirtualArduinoSerializer:

    def __init__(self,arg_port,arg_baude_rate):
        print('created a virtual arduino on {} port '.format(arg_port))


#stub all arduino function when running a virtual arduino

    def __del__(self):
        pass

    def power_on(self):
        pass

    def power_off(self):
        pass

    def reinit(self):
        pass

    def reset(self):
        print('virtual reset')
        pass

    def fw_flash(self):
        pass

    def press(self,arg_button):
        pass

    def reboot(self):
        pass