from network.networkManager import NetworkManager
import os
import time


class Camera :



    def __init__(self,username,host_ip,ssh_passwd,web_port,arduino_port,linux_port,rtos_port,grid,control_mode):
        '''

        :param username:
        :param host_ip:
        :param ssh_passwd:
        :param web_port:
        :param arduino_port:
        :param linux_port:
        :param rtos_port:
        :param grid: camera has a grid to knw with which host it can communicate
        '''
        self.username           = username
        self.ssh_passwd         = ssh_passwd
        self.arduino_port       = arduino_port
        self.linux_port         = linux_port
        self.rtos_port          = rtos_port
        self.host_ip            = host_ip
        self.web_port           = web_port
        self.grid               = grid
        self.grid.target_ip     = self.host_ip # target ip for the grid is the host ip for the camera
        self.netwk_manager      = NetworkManager(username =self.username ,host = self.host_ip,ssh_passwd = self.ssh_passwd,arduino_port=self.arduino_port,linux_port=self.linux_port,rtos_port=self.rtos_port,control_mode=control_mode)



    # ---------------------------------------------- ------------------------------------------
    def serial_status(self):
        '''
        check if serial port return any information
        :return:
        '''
        self.netwk_manager.rtos_ser.start_acquisition()
        self.tcmd('t dbg on')
        time.sleep(0.2)
        self.netwk_manager.rtos_ser.stop_acquisition()
        data = self.netwk_manager.rtos_ser.get_data()
        # print(data[1])
        if data == '':
            return False
        else:
            return True

    # ---------------------------------------------- ------------------------------------------
    def is_serial_ready(self, arg_timeout):
        '''
        :param self: camera object
        :param arg_timeout: maximum time to wait for serial communication
        :return: True if serial is available before the timeout
                 False if serial is not available after timeout
        '''
        time_elapsed = 0
        reset_flag = False
        serial_flag = self.serial_status()
        while serial_flag == False:
            time_elapsed = time_elapsed + 0.3  # time in the sleep of the serial_status
            #print("still checking for serial port")
            serial_flag = self.serial_status()
            if time_elapsed >= arg_timeout / 2 and reset_flag == False:
                print(" reset camera ---- > look serial ports")
                reset_flag = True
                self.soft_reset()
            if time_elapsed >= arg_timeout:
                #raise Exception(' serial port is not ready , timeout ')
                return False
        #print('serial port is available')
        return True

    def is_ssh_ready(self, arg_timeout):
        '''
        :param self: this class _--> camera
        :param arg_timeout: timemout waiting for network interface between the grid and the camera to
        be established
        :return: True if the camera is ready ( both serial and ssh connection are valid
                False if ssh or serial connection fails
        '''
        time_elapsed = 0
        reset_flag = False
        ip_adress  = self.grid.host_ip
        while self.netwk_manager.interface_explorer.find_by_ip(ip_adress) == False:
            time.sleep(0.1)
            #print('waiting for network connection')
            time_elapsed = time_elapsed + 0.1
            if time_elapsed >= arg_timeout / 2 and reset_flag == False:
                print(" reset camera ---- > look for interfaces again")
                reset_flag = True
                self.soft_reset()
            if time_elapsed >= arg_timeout:
                #raise Exception('ssh is not ready , timeout ')
                return False
        #print('Connection established to ---> {}'.format(self.grid.host_ip),'time elapsed :',time_elapsed)
        return True

    # ---------------------------------------------- ------------------------------------------
    def is_ready(self,*arg_interface,arg_timeout = 30):

        '''
        check for serial port status ( for camera )
        check for ssh connection , is the network interface established ?
        if the 2 flags are ok -----> camera is ready
        *arg_interface : list of the network interfaces to check on
        :return: None
        '''
        is_ready_flag = True
        for el in arg_interface :
            assert (el == 'ssh' or el =='serial') ,' print invalid choice for interface choose "ssh" or "serial"'
            if el =='serial':
                rtos_flag = self.is_serial_ready(arg_timeout ) # blocking function
                is_ready_flag = is_ready_flag and rtos_flag
            if el == 'ssh':
                ssh_flag = self.is_ssh_ready(arg_timeout) # blocking function
                is_ready_flag = is_ready_flag and ssh_flag

        return is_ready_flag

    # ---------------------------------------------- ------------------------------------------
    def get_status(self):
        '''
        get the camera status  , on or off
        :return:
        '''
        if self.serial_status():
            return 'on'
        else :
            return 'off'

    # ----------------------------------------------start acquisition from rtos-linux  ports ------------------------------------------
    def start_acquisition(self):
        '''
        start the acquisition threads ( called when a test is finished )
        :return: None
        '''
        self.netwk_manager.rtos_ser.start_acquisition()
        self.netwk_manager.linux_ser.start_acquisition()

    # ----------------------------------------stop acquisition from rtos-linux  ports-----------------------------------
    def stop_acquisition(self):
        '''
        stop the acquisition threads ( called when a test is finished )
        :return: None
        '''
        self.netwk_manager.rtos_ser.stop_acquisition()
        self.netwk_manager.linux_ser.stop_acquisition()

    # ----------------------------------------getdata from rtos-linux serial readers -------------------------------------
    def get_data(self):
        '''
        get the data acquired from serial ports after stopping the acquisition
        linux_log : gets the linux_serial traces
        rtos_log : gets the rtos_serial traces
        :return: a list of logs
        '''
        linux_log =self.netwk_manager.linux_ser.get_data()
        rtos_log = self.netwk_manager.rtos_ser.get_data()
        m_data=[linux_log,rtos_log]
        return m_data


    def send_serial_command(self,arg_port,arg_command):
        '''

        :param arg_port: name of the port from which data is sent
        :param arg_command: command sent on the serial port
        :return: None
        '''
        assert (arg_port == self.arduino_port or arg_port == self.rtos_port or arg_port == self.linux_port ) ,\
            " not a valid port ,port must be {} , {} or {}".format(self.arduino_port,self.linux_port,self.rtos_port)
        if  arg_port == self.rtos_port:
            self.netwk_manager.rtos_ser.send_data(arg_command)
        elif arg_port == self.linux_port:
            self.netwk_manager.linux_ser.send_data(arg_command)
        else :
            self.netwk_manager.arduino_ser.send_data(arg_command)


    def flash(self,arg_mode,arg_frw_type):
        '''
        :param arg_mode: flashing mode which must be
        :param arg_frw_type: firmware type must be spherical or Jbay , Jbay not implemented yet
        :return:
        '''
        assert((arg_mode == 'arduino' or arg_mode == 'make') and arg_frw_type == 'spherical'), 'invalid flash option , choose "arduino or "make" to set flash option'
        if arg_mode   == "arduino":
            self.netwk_manager.arduino_ser.fw_flash()

        elif arg_mode =="make":
            cam_ip = str(self.host_ip)
            binary_file = '../../../../waf_build/{}/build/eaglepeak/sd_fwupdate/DATA.bin'.format(arg_frw_type)
            os.environ['VARIANT'] = arg_frw_type
            #print('../../../../admin/host_tools/gen/remote_flash.sh {} {}'.format(cam_ip,binary_file))
            os.system('../../../../admin/host_tools/gen/remote_flash.sh {} {}'.format(cam_ip,binary_file))
            #/waf_build/spherical/build/eaglepeak/sd_fwupdate/DATA.bin
            time.sleep(4)
            self.soft_reset()
        else:
            pass




    def refresh(self):
        '''
        this function refresh the instances of the network components of the camera
        after hard_flash (with arduino) camera must refresh it's network instances
        :return: None
        '''
        self.netwk_manager.refresh()



    # ---------------------------------------------- ------------------------------------------
    def press_button(self,arg_button):
        '''
        :param arg_button: must be 'shutter' or 'mode'
        :return:
        '''
        self.netwk_manager.arduino_ser.press(arg_button)

    # ---------------------------------------------- ------------------------------------------
    def soft_reset(self):
        '''
        soft_reset using arduino
        :return: None
        '''
        self.netwk_manager.arduino_ser.reset()
        if self.is_ready('serial',arg_timeout=90) :
            pass
        else :
            raise Exception ('camera is not ready , timeout')


    # ---------------------------------------------- ------------------------------------------
    def hard_reset(self):
        '''
        this function reset the camera after turnning it on using arduino
        (1- power_cut , 2- get power back 3- power on ) 4- reset
        :return: None
        '''
        self.netwk_manager.arduino_ser.reboot()
        self.soft_reset()
        if self.is_ready('serial', arg_timeout=90):
            pass
        else :
            raise Exception ('camera is not ready , timeout')




    # ---------------------------------------------- ------------------------------------------
    def reinit(self):
        '''
        reinitialise the firmware. All GPIOs reprogrammed to input mode.
        :return: None
        '''
        self.netwk_manager.arduino_ser.reinit()

    # ---------------------------------------------- ------------------------------------------

    def turn_on(self):
        '''
        tur the camera on after cut and getting back the power
        :return: None
        '''
        self.netwk_manager.arduino_ser.power_on()

    # ---------------------------------------------- ------------------------------------------
    def turn_off(self):
        '''
        turn the camera off
        :return: None
        '''
        self.netwk_manager.arduino_ser.power_off()

    # ---------------------------------------------- ------------------------------------------
    def tcmd(self,arg_cmd):
        '''
        :param arg_cmd: tcmd to send on rtos serial port, example : t dbg on , t version
        :return: None
        '''
        self.netwk_manager.rtos_ser.send_data(arg_cmd)




# from grid import  Grid
# grid = Grid(arg_host_ip = "192.168.0.1",arg_host_http_path='/var/www/html')
# cam  = Camera(username = 'root',host_ip = '192.168.0.202',ssh_passwd='',web_port=8042,arduino_port='/dev/ARDUINO',linux_port='/dev/LINUX',rtos_port='/dev/RTOS',grid =grid)
# cam.netwk_manager.arduino_ser.power_on()
# cam.flash('arduino','spherical')
#cam.flash('make','spherical')
# cam.send_serial_command(arg_port=cam.rtos_port,arg_command="t dbg on")
# cam.send_serial_command(arg_port=cam.rtos_port,arg_command="t version")
# cam.send_serial_command(arg_port=cam.rtos_port,arg_command="t dbg off")
#cam.reboot('soft')
#print(cam1.is_ready())
#print(cam.get_status())
#cam.is_ready('ssh','serial',arg_timeout=30)
