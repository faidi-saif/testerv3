from network.arduinoSerializer import ArduinoSerializer
from network.virtualArduinoSerializer import VirtualArduinoSerializer
from network.sshAgent import SshAgent
#import sshAgent.SshAgent as SshAgent
from network.serializerWithReader import SerializerWithReader
from network.webServerAgent import WebServerAgent
from network.interfaceExplorer import InterfaceExplorer
import os
import time
import shutil

class NetworkManager :

    def __init__(self,username,host,ssh_passwd,arduino_port,linux_port,rtos_port,control_mode):
        self.arduino_port       = arduino_port
        self.linux_port         = linux_port
        self.rtos_port          = rtos_port
        self.ssh_agent          = SshAgent(arg_username = username,arg_host = host,arg_passwd = ssh_passwd)
        self.wb_server          = WebServerAgent()
        self.interface_explorer = InterfaceExplorer()
        self.rtos_ser           = SerializerWithReader(rtos_port,115200,"RTOS")
        self.linux_ser          = SerializerWithReader(linux_port, 115200,"LINUX")
        if control_mode == 'complete':
            self.arduino_ser = ArduinoSerializer(arduino_port, 9600)
        else :
            self.arduino_ser =VirtualArduinoSerializer(arduino_port, 9600)

        time.sleep(1)  # time to initialize the serial instance

    # ---------------------------------------------- refresh------------------------------------------
    def refresh(self):
        '''
        refresh all serial instances
        :return: None
        '''
        self.arduino_ser = ArduinoSerializer(self.arduino_port , 9600)
        self.rtos_ser    = SerializerWithReader(self.linux_port , 115200, "RTOS")
        self.linux_ser   = SerializerWithReader(self.linux_port, 115200, "LINUX")

    # ---------------------------------------------- destructor ------------------------------------------
    def __del__(self):
        self.arduino_ser.__del__()
        self.rtos_ser.__del__()
        self.linux_ser.__del__()

    # ----------------------------------------------fix_web_path ------------------------------------------
    def fix_web_path(self,arg_path):
        '''
        note that webserver scope is : /DCIM/..
        when user pass a complete path like : '/tmp/fuse_d/DCIM/100GOPRO , this function removes '/tmp/fuse_d/'
        :param arg_path: input path example : /tmp/fuse_d/DCIM/100GOPRO
        :return                             : /DCIM/100GOPRO
        '''
        path = arg_path
        if (arg_path.find('/tmp/fuse_d') != -1):
            path = arg_path.replace('/tmp/fuse_d','')
        return path

    # --------------------------------------------------- list_remote_files--------------------------------------------------------
    def list_remote_files(self,arg_path):
        '''
        :param arg_path : remote path
        :return         : complete path for all files in the remote directory
         example         : in DCIM/100GOPRO/ we have file_x and file_y, the return is :
        /DCIM/100GOPRO/file_x
        /DCIM/100GOPRO/file_y
        '''
        path = self.fix_web_path(arg_path)
        return  self.wb_server.list_content(path)

    # --------------------------------------------------- download_file--------------------------------------------------------
    def download_file(self,remote_path,local_dir):
        '''
        download a file 'remote_path' in the directory 'local_dir'
        :param remote_path  : file path
        :param local_dir    : target directory
        :return: None
        '''
        path = self.fix_web_path(remote_path)
        self.wb_server.download(path,local_dir)


    # --------------------------------------------------- download_all-----------------------------------------------
    def download_all(self,arg_remote_path,arg_dir,arg_files):
        '''
        download all the files in a given path  'arg_remote_path' to the 'arg_dir'
        :param arg_remote_path: source directory
        :param arg_dir        : target directory
        :arg_files            : the specific list of files to be downloaded
        :return: None
        '''
        path    = self.fix_web_path(arg_remote_path)
        if arg_dir != '':
            if not os.path.isdir(arg_dir) :
                os.makedirs(arg_dir )
            else :
                # clean the directory content before saving new files
                self.clean_dir(arg_dir)
        files  = [arg_remote_path + '/' + file_name for file_name  in arg_files] # create a list of file paths for the list of the files 'arg_files'
        for file in files :

            self.download_file(file,arg_dir)


    # ---------------------------------------- clean_dir -----------------------------------------------

    def clean_dir(self,arg_path):
        '''
        remove all files in a given path
        :param arg_path: target path
        :return:
        '''
        for the_file in os.listdir(arg_path):
            file_path = os.path.join(arg_path, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)




# netwk = NetworkManager(username = 'root',host = '192.168.0.202',ssh_passwd='')
# netwk.download_all('192.168.0.202:8042/DCIM/100GOPRO/','/home/saif/Desktop')

