from cameraMind import CameraMind



class Vcamera :

    def __init__(self,camera,frw_type):
        '''
         mode : can be still or video
        :param Camera: hardware camera , low level access
        '''
        assert (frw_type == 'spherical'),'invalid firmware type for camera'
        self.frw_type           = frw_type
        self.camera             = camera
        self.mind               = CameraMind(self)
        self.mode               = None



    # ---------------------------------------------- ------------------------------------------
    def take_photo(self,arg_mode):
        '''
        :param arg_mode: a dictionary of the different params of the photo
        example :
        params = {'fps': '25', 'res': '5.6K', 'flare': '1000'}
        :return: None
        '''
        #self.mind.conf.mode = 'still'
        self.set_camera_conf(arg_mode)
        self.mind.run('still')

    # ---------------------------------------------- ------------------------------------------
    def record_video(self,arg_mode):
        '''
       :param arg_mode: a dictionary of the different params of the video
        example :
        params = {'fps': '25', 'res': '5.6K', 'flare': '1000'}
        :return: None
        '''
        #self.mind.conf.mode = 'video'
        self.set_camera_conf(arg_mode)
        self.mind.run('video')


    # ---------------------------------------------- ------------------------------------------
    def preview(self,arg_mode):# complete dictionary , shooting_mode , params_mode,options_mode
        #self.mind.conf.mode = 'preview'
        self.set_camera_conf(arg_mode)
        self.mind.run('preview')


    # ----------------------------------------------get_frw_version  ------------------------------------------
    def get_frw_version(self):
        frw_version = self.mind.get_frw_version()
        return frw_version


    # ----------------------------------------------get_info  ------------------------------------------
    def get_info(self):
        return self.mind.get_info()


    # ---------------------------------------------- ------------------------------------------
    def clean_content(self,arg_path):
        '''
        ( remove all files and directories in the arg_path )
        :param arg_path: path to clean
        :return: None
        '''
        self.camera.netwk_manager.ssh_agent.execute_command('rm -rf ' + arg_path)
    # ---------------------------------------------- ------------------------------------------

    def get_files(self,source_path,target_path,files):
        '''
        :param source_path: path from which the fle will be downloaded , example : /DCIM/100GOPRO/
        or '/tmp/fuse_d/DCIM/100GOPRO/'
        :param target_path: path for the downloaded file example : /logs ( for jenkins )
        :return: None
        '''
        complete_path = self.camera.host_ip + ':' + str(self.camera.web_port) + source_path
        #192.168.0.202:8042/tmp/fuse_d/DCIM/100GOPRO/
        self.camera.netwk_manager.download_all(complete_path,target_path,files)




    # ---------------------------------------------- ------------------------------------------
    def ls_files(self,arg_path):
        '''
        :param arg_path: path for files to be listed example : /tmp/fuse_d/DCIM/100GOPRO/
        :return: names of the files in the arg_path
        '''
        files = self.camera.netwk_manager.ssh_agent.execute_command('ls ' + arg_path)
        print('files in {} : '.format(arg_path),files)
        return files


    def get_file_stat(self,arg_path):
        '''
        :param arg_path: path to the searched file   : /tmp/fuse_d/DCIM/100GOPRO/GH010197.MP4
        :return: dictionnary containing, the size , name and permissions of the file
        example : {'file': '/tmp/fuse_d/DCIM/100GOPRO/GH010197.MP4', 'size': '27.8M', 'permission': '-rwxr-xr-x'}
        '''
        status = self.camera.netwk_manager.ssh_agent.execute_command('ls -lh '+ arg_path)
        status = status.split()
        # status = ['-rwxr-xr-x', '1', 'root', 'root', '27.8M', 'Jan', '3', '00:27', '/tmp/fuse_d/DCIM/100GOPRO/GH010197.MP4']
        stat = {'file' : status[8] , 'size' : status[4] ,'permission' :status[0]}
        return stat

     # ---------------------------------------------- ------------------------------------------

    def get_results(self, arg_path,debug_dump = None, dump_raw = None,arg_files = None,debug_dump_files = None, dump_raw_files = None):
         if arg_path != '':
             # affectation de la variable tes_env_target_dir doit etre mise dans set_camera_conf
             self.mind.conf.download_target_dir = arg_path
         else :
             pass
         self.mind.get_results(self.mind.conf.download_target_dir,debug_dump = debug_dump,dump_raw = dump_raw,arg_files = arg_files,dump_raw_files = dump_raw_files,debug_dump_files = debug_dump_files)


    # ---------------------------------------------- ------------------------------------------

    def get_file(self,source_path,target_path):
     '''
     :param source_path: path from which the fle will be downloaded , example : /DCIM/100GOPRO/
     or '/tmp/fuse_d/DCIM/100GOPRO/'
     :param target_path: path for the downloaded file example : /logs ( for jenkins )
     :return: None
     '''
     complete_path = self.camera.host_ip + ':' + str(self.camera.web_port) + source_path
     self.camera.netwk_manager.download_file(complete_path,target_path)

    # ---------------------------------------------- ------------------------------------------
    def get_status(self):
        return self.camera.get_status()

    # ---------------------------------------------- ------------------------------------------
    def get_test_mode(self):
        test_ev = self.mind.conf.get_environment()
        return test_ev

    # ---------------------------------------------- ------------------------------------------
    def set_camera_conf(self,arg_dict_mode): # change name
       '''

       :param arg_dict_mode:
       {
          "shooting_mode" : "dual",
          "params_mode"    :
           {
             "fps"     : "24,25,30,60"
           },
          "options_mode" :
          {
            "flare" : "ON,OFF",
            "flare_art" :"RANDOM,ID,STRONG,LITE",
            "bypass"    : "ON,OFF",
            "ring_low_res" : "ON,OFF",
            "dump_raw"     : "ON,OFF


            "debud_dump" : "ON/OFF"

          }
        }
       :return:
       '''

       #erase_previous_conf
       self.mind.conf.reset_test_env()
       assert ('shooting_mode' in arg_dict_mode.keys()) ,'no shooting_mode selected'
       self.mind.conf.set_shooting_mode(arg_dict_mode['shooting_mode'])
       if 'params_mode' in arg_dict_mode.keys():
            self.mind.conf.set_params_mode(arg_dict_mode['params_mode'])
       if 'options_mode' in arg_dict_mode.keys():
           self.mind.conf.set_options_mode(arg_dict_mode['options_mode'])



    # ---------------------------------------------- ------------------------------------------
    def reboot(self,arg_reboot_option):
        '''
        :param arg_reboot_option: to reboot the camera after a power cut or using gpdevSendCmd RB
        # for hard reboot we use power_on() from arduino class since it's based on  power cut using
        the 'ykushxs' device
        :return: None
        '''
        arg_reboot_option =arg_reboot_option.strip()
        assert(arg_reboot_option == 'hard' or arg_reboot_option =='soft') , ' Invalid reboot option ,  must be "soft " or " hard "'
        if arg_reboot_option == 'hard' :
            self.camera.netwk_manager.arduino_ser.reboot()
        elif arg_reboot_option == 'soft':
            self.camera.netwk_manager.ssh_agent.execute_command(self.mind._soft_reboot)


    # ---------------------------------------------- ------------------------------------------
    def reset(self,arg_mode):
        '''
        :param arg_mode: reset mode can be 'soft' or 'hard'
        :return: None
        '''
        arg_mode = arg_mode.strip()
        assert(arg_mode == 'soft' or arg_mode =='hard') , 'Invalid reset option , must be "soft" or "hard" '
        if arg_mode == 'soft':
            self.camera.soft_reset()
        else :
            self.camera.hard_reset()

    def is_ready(self,*arg_net_interfaces,arg_timeout = 30):
        """

        :param arg_net_interfaces: serial or ssh
        :param arg_timeout: maximum time took to check for the availability of the interfaces
        :return: boolean = True when interface(s) are available
        """
        return self.camera.is_ready(*arg_net_interfaces,arg_timeout=arg_timeout)

    # ---------------------------------------------- ------------------------------------------
    def start_acquisition(self):
        self.camera.start_acquisition()

    # ---------------------------------------------- ------------------------------------------
    def stop_acquisition(self):
        self.camera.stop_acquisition()

    # ---------------------------------------------- ------------------------------------------
    def get_data(self):
        '''
        :return: linux and rtos serial logs
        '''
        return self.camera.get_data()

    # ---------------------------------------------- ------------------------------------------
    def flash(self,arg_mode,arg_frw_type):
        self.camera.flash(arg_mode,arg_frw_type)

    # ---------------------------------------------- ------------------------------------------
    def cleanup(self,):
        self.mind.cleanup()

    # ---------------------------------------------- ------------------------------------------
    def run_scenario(self,arg_list):
        self.mind.run_scenario(arg_list)











#cam.get_files('/DCIM/100GOPRO/','/home/saif/Desktop/')
#cam.get_files('/tmp/fuse_d/DCIM/100GOPRO/','/home/saif/Desktop/') # cammed also this way
#print(cam.get_file_stat('/tmp/fuse_d/DCIM/100GOPRO/GH010197.MP4'))
#cam.clean_content('/tmp/fuse_d/DCIM/100GOPRO/*')
#cam.get_results('/home/saif/Desktop/test_capt')

#print (vcam.get_frw_version())
# f ={'fps': '6', 'res': 'rien', 'flare': '1000'}
# cam.set_camera_conf(f)
# print(cam.get_test_mode())

# ----------------------------------------------  test : take_photo------------------------------------------
# f ={'fps': '25', 'res': '5.6K', 'flare': '1000'}
# vcam.take_photo(f)


# from grid import  Grid
# from camera import Camera
# grid= Grid(arg_host_ip = "192.168.0.1",arg_host_http_path = '/var/www/html')
# hard_cam  = Camera(username = 'root',host_ip = '192.168.0.202',ssh_passwd = '',web_port = 8042,arduino_port = '/dev/ARDUINO',linux_port = '/dev/LINUX',rtos_port = '/dev/RTOS',grid = grid,control_mode='complete')
# vcam = Vcamera(hard_cam,'spherical')

# vcam.get_results('/home/saif/Desktop')
# vcam.get_results('/home/saif/Desktop')
# vcam.get_results('/home/saif/Desktop')
# vcam.get_results('/home/saif/Desktop')
# #
# vcam.ls_files('/tmp/fuse_d/DCIM/100GOPRO/')
# #
# scenario_s0 = [ 't dbg on',
#                 't appc status disable',
#                 'sleep 4',
#                 't frw test disp_id 0',
#                 't frw test open',
#                 't frw test mode 5K_EAC_30_W_HEVC_IMX577_BYPASS',
#                 't frw test graph still_spherical',
#                 't frw test liveview',
#                 'sleep 2',
#                 't frw cal raw 12',
#                 't frw cal bayer_width 3008',
#                 't frw test mode PHOTO_18MP_30_W_IMX577',
#                 't frw test still',
#                 'sleep 5 ',
#                 't frw test stop_still',
#                 # 't frw test mode 5K_EAC_30_W_HEVC_IMX577_BYPASS',
#                 # 't frw test liveview'
#                 ]
# scenario_c0 = [
#                 't appc status disable',
#                 't frw test disp_id 0',
#                 't frw test open',
#                 't frw test mode 5K_EAC_30_W_HEVC_IMX577_BYPASS',
#                 't frw test graph still_spherical',
#                 't frw test liveview',
#                 'sleep 2',
#                 't frw cal raw 16',
#                 't frw cal bayer_width 4056',
#                 't frw test mode PHOTO_12MP_30_W_IMX577_DUAL_CAL',
#                 't frw test still',
#                 'sleep 5',
#                 't frw test stop_still',
#                 't frw test mode 5K_EAC_30_W_HEVC_IMX577_BYPASS',
#                 't frw test liveview',
#              ]
# scebario_test1 = [
#
# ]
# # vcam.reset('soft')
# # time.sleep(6)
#
# vcam.start_acquisition()
# vcam.run_scenario(scenario_s0)
# time.sleep(3)
# vcam.stop_acquisition()
# data = vcam.get_data()
# print(data[1])
# time.sleep(4)
# vcam.run_scenario(scenario_c0)
# vcam.reset('soft')
# time.sleep(4)
# vcam.run_scenario(scenario_s0)
# vcam.reset('soft')

# dictio = {
#     "shooting_mode": "lcd",
#     "params_mode":
#         {
#             "fps": "30",
#             "submode" : "",
#             "stitch_mode":'EAC',
#             "resolution" : "5K"
#         },
#     "options_mode":
#         {
#             'eac_split'      : "ON" ,
#             'flare'          : "ON"  ,
#             'flare_art'      : "RANDOM",
#             'bypass'         : "ON"  ,
#             'lrv'            : "ON" ,
#             'stab'           : "ON",
#             'stab_degree'    : "2",
#             'ring_low_res'   : "ON",
#             'exposure'       : "ON",
#             'debug_dump'     : "ON",
#             'raw_nbits'      : "6",
#             'bayer_width'    : "4056",
#             'dump_raw'       : "ON",
#             'mpx'            : "18MPX",
#             'run_time'       : "6"
#
#         }
# }
#
# #vcam.set_camera_conf(dictio)
# #print(vcam.mind.conf.get_environment())
# vcam.preview(dictio)