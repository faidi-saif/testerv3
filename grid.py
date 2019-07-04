import os

class Grid :


    def __init__(self ,arg_host_http_path,arg_gpdev='1',arg_host_ip='192.168.0.1'):

        self._host_ip                = arg_host_ip
        self._target_ip              = '192.168.0.202' # modified when passed as argument to camera
        self._host_http_path         = arg_host_http_path
        self._gpdev                  = arg_gpdev
        os.environ['GPDEV']          = self._gpdev
        os.environ['TARGET_IP']      = self._target_ip
        os.environ["HOST_IP"]        = self._host_ip
        os.environ['HOST_HTTP_PATH'] = self._host_http_path

    #----------------------------------------------- getters -----------------------------------------



    @property
    def host_ip(self):
        return self._host_ip

    @property
    def target_ip(self):
        return self._target_ip


    @property
    def host_http_path(self):
        return self._host_http_path

    @property
    def gpdev(self):
        return self._gpdev

    #----------------------------------------------- setters -----------------------------------------




    @host_ip.setter
    def host_ip(self,arg_host_ip):
        self._host_ip    = arg_host_ip
        os.environ['HOST_IP'] = self._host_ip


    @target_ip.setter
    def target_ip(self,arg_target_ip):
        self._target_ip = arg_target_ip
        os.environ['TARGET_IP'] = self._target_ip

    @host_http_path.setter
    def host_http_path(self,arg_host_http_path):
        self._host_http_path = arg_host_http_path
        os.environ['HOST_HTTP_PATH'] = self._host_http_path

    @gpdev.setter
    def gpdev(self,arg_gpdev):
        self._gpdev = arg_gpdev
        os.environ['GPDEV'] = self._gpdev








