
from check.fileStat import FileStat
import subprocess
import os
# ----------------------------------------------VideoStat checker ------------------------------------------
class VideoStat(FileStat):




    def get_info(self,filename,arg_info):
        '''

        :param filename: the video in question
        :param arg_info: the information to search for for the video , example : duration, frame rate ...
        :return: the info if it's found else None
        '''
        result = subprocess.Popen(["ffprobe", filename],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for el in result.stdout.readlines():
            info = self.parser.search_pattern(el.decode(),arg_info)
            if info is not None :
                return info



    def extract_properties(self,arg_file_path,arg_file):
        file_path = arg_file_path + '/' + arg_file
        f = arg_file.split('.')
        name        = f[0]
        type        = f[1]
        ret         = os.stat(file_path)
        size        = str(ret.st_size/1000) + 'KB'
        duration    = self.get_info(file_path,'video_duration')
        frame_rate  = self.get_info(file_path,'frame_rate')
        if type == 'THM':
            return {'name' : name, 'type':type ,'size':size,}
        else :
            return {'name' : name, 'type':type ,'size':size,'frame_rate' : frame_rate,'duration':duration}

