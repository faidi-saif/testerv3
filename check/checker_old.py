
import os
import subprocess
import re
from check.parserForChecker import  ParserForChecker
#from parserForChecker import ParserForChecker
from abc import ABC, abstractmethod
import copy

# ------------------------------------------------------Checker---------------------------------------------------------#
#                                                                                                                       #
#                                                                                                                       #
# ------------------------------------------------------Checker --------------------------------------------------------#
class Checker (ABC):

    def __init__(self):
        self._result = False
        super().__init__()



    @ property
    def result(self):
        return self._result


    @abstractmethod
    def check(self,*args ):
        pass
 # ----------------------------------------------FileNotNull checker ------------------------------------------
class FileNotNull(Checker):


    def check(self, *args):
        resul = True
        path  = args[0]
        assert (path is not None) , " No directory for check passed "
        files = os.listdir(path)
        if files != []:
            for file in files :
                file_path = path + '/' + file
                r = os.stat(file_path)
                if r.st_size == 0:
                    res = False
                    print('file "{}" is  null'.format(file))
                else:
                    res = True
                resul = resul and res
        else :
            resul = False
        return {'result' : resul}







# ------------------------------------------------------FrwVersion------------------------------------------------------#
#                                                                                                                       #
#                                                                                                                       #
# ------------------------------------------------------FrwVersion -----------------------------------------------------#
class FrwVersion(Checker):

    def check(self,*args ):
        cam = args[0]
        version = None
        if cam.is_ready('serial','ssh', arg_timeout=40) :
            version = cam.get_frw_version()
            if version != '':
                ret =  True
            else:
                ret =  False
        else :
            ret =  False
        return {'result' : ret ,'firmware version' : version}













# ------------------------------------------------------FileStat -------------------------------------------------------#
#                                                                                                                       #
#                                                                                                                       #
# ------------------------------------------------------FileStat -------------------------------------------------------#

class FileStat(Checker):

    def __init__(self):
        super().__init__()
        self.parser = ParserForChecker()

    #---------------------------------------------- find_step_index ------------------------------------------
    def find_step_index(self,steps, case):
        '''
        :param steps:
        :param case:
        :return:
        call this function to find index of the
        '''
        index = 0
        for el in steps:
            if el['case'] == case:
                return index
            index += 1

    # ----------------------------------------------extract_out_properties  ------------------------------------------
    def extract_out_properties(self,arg_file_path,arg_file):
        # result = subprocess.Popen(["ffprobe", arg_file_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # file_info = result.stdout.read().decode()
        file_path = arg_file_path + '/' + arg_file
        f = arg_file.split('.')
        name        = f[0]
        type        = f[1]
        size        = str(os.stat(file_path).st_size/1048576.0)
        return {'name' : name, 'type':type ,'size MB':size}

    # ---------------------------------------------- check ------------------------------------------
    def check(self,*args ):
        files_properties    = []
        result              = False
        files_path          = args[0]
        preview_state       = args[1]
        non_preview_state   = args[2]

        files            = os.listdir(files_path)
        files_number     = len(files)
        if files  != [] :
            for file in files:
                file_out_properties = self.extract_out_properties(files_path,file)

                files_properties.append(file_out_properties)
                if file_out_properties['size MB'] !=  0:
                    result  = True
                else:
                    #print('file "{}" is  null'.format(file))
                    pass
        else :
            result = False

        return {'result':result,'number of files':files_number,'files' : files_properties}



    # ---------------------------------------------- compare ------------------------------------------
    def compare(self,arg_in_properties,arg_out_properties):
        '''
        :param arg_in_properties:
        :param arg_out_properties:
        :return:
        '''





# ------------------------------------------------------FileStat checker -----------------------------------------------#
#                                                                                                                       #
#                                                                                                                       #
# ------------------------------------------------------FileStat checker -----------------------------------------------#
class VideoStat(FileStat):

    def __init__(self):
        self.bit_rate = 60000.0 #60kb kilo bit
        super().__init__()



    # def get_info(self,file_path,arg_info):
    #     '''
    #
    #     :param filename: the video in question
    #     :param arg_info: the information to search for for the video , example : duration, frame rate ...
    #     :return: the info if it's found else None
    #     '''
    #     result = subprocess.Popen(["ffprobe", file_path],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #     for el in result.stdout.readlines():
    #         info = self.parser.search_pattern(el.decode(),arg_info)
    #         if info is not None :
    #             return info


    # -------------------------------------------------------get_in_resolution ----------------------------------------------
    def get_in_resolution(self,arg_resolution,arg_stitch_mode):
        '''
        :param arg_resolution:  5K , 4K ..
        :param arg_stitch_mode: EAC , ERP ..
        :return: dictionary {'video_type' : 'LRV and MP4' ,'resolution' : 'XxY'}
        '''
        if arg_stitch_mode == 'EAC':
            if arg_resolution == '5K':
                resolution = {'MP4':'4032x2688','LRV':'1408x704'}
            elif arg_resolution =='4K':
                resolution = {'MP4':'3840x2160','LRV':'1408x704'}
            else:
                raise Exception('this resolution {} is not handled in the checker'.format(arg_resolution))
        else :
            raise Exception('this stitch mode {} is not handled in the checker'.format(arg_stitch_mode))
        return resolution



    # -------------------------------------------------------get_in_color_format ----------------------------------------------
    def get_in_color_format(self):
        return {'MP4':'yuvj420p' ,'LRV' : 'yuvj420p'}


    # -------------------------------------------------------get_in_encode_format ----------------------------------------------
    def get_in_encode_format(self,arg_resolution,arg_stitch_mode):
        if arg_stitch_mode == 'EAC':
            if arg_resolution == '5K':
                encode_format = {'MP4':'hevc','LRV':'h264'}
            elif arg_resolution =='4K':
                encode_format = {'MP4':'h264','LRV':'hevc'}
            else:
                raise Exception('this resolution {} is not handled in the checker'.format(arg_resolution))
        else :
            raise Exception('this stitch mode {} is not handled in the checker'.format(arg_stitch_mode))
        return encode_format





    # -------------------------------------------------------estimate_size ----------------------------------------------
    def estimate_size(self,arg_resolution,arg_stitch_mode,arg_bit_rate,arg_duration):
        '''
        :param arg_resolution: 5K , 4K .. (string)
        :param arg_stitch_mode: 'EAC' , 'ERP'
        :param arg_bit_rate: ex: {'MP4': '58246', 'LRV': '2547'}
        :param arg_duration: '4' ,'60' .. (string)
        :return: {'MP4':MP4_size ,'LRV' : LRV_size}
        '''
        if arg_stitch_mode == 'EAC':
            if arg_resolution == '5K':
                MP4_size = (int(arg_bit_rate['MP4']) * int(arg_duration))/8192.0  #(8*1204.0) kbit/s *  (s)  /8*1024 => Mega bytes
                LRV_size = (int(arg_bit_rate['LRV']) * int(arg_duration))/8192.0
                return {'MP4':MP4_size ,'LRV' : LRV_size}
            else:
                raise Exception('this resolution {} is not handled in the checker'.format(arg_resolution))
        else :
            raise Exception('this stitch mode {} is not handled in the checker'.format(arg_stitch_mode))



    # -------------------------------------------------------VideoStat checker ----------------------------------------------
    def extract_in_properties(self,arg_preview,arg_non_preview):
        '''

        :param arg_preview:
        :param arg_non_preview:
        :return: {'fps':fps,'duration':duration,'resolution':{'MP4':'3840x2160','LRV':'1408x704'},'color_format':{'MP4':'yuvj420p' ,'LRV' : 'yuvj420p'},'encode_format':{'MP4':'h264','LRV':'hevc'},'bit_rate':''588246,'size':{'MP4':MP4_size ,'LRV' : LRV_size}}
         extract the properties from the input preview and video scenario descriptor dictionary
         '''
        in_resolution    = arg_preview['params']['params_mode']['resolution']
        in_stitch_mode   = arg_preview['params']['params_mode']['stitch_mode']
        fps              = arg_preview['params']['params_mode']['fps']
        duration         = arg_non_preview['params']['options_mode']['run_time']
        resolution       = self.get_in_resolution(in_resolution, in_stitch_mode)
        color_format     = self.get_in_color_format()
        encode_format    = self.get_in_encode_format(in_resolution, in_stitch_mode)
        bit_rate         =  self.get_bit_rate(self.bit_rate)
        size             = self.estimate_size(in_resolution, in_stitch_mode,bit_rate,duration)
        return {'fps':fps,'duration':duration,'resolution':resolution,'color_format':color_format,'encode_format':encode_format,'bit_rate kb/s':bit_rate,'size MB':size}

    # ------------------------------------------------------- get_bit_rate ----------------------------------------------
    def get_bit_rate(self,arg_bit_rate):

        return {'MP4':arg_bit_rate,'LRV' : arg_bit_rate/22.2}

    # -------------------------------------------------------extract_out_properties ----------------------------------------------
    def extract_out_properties(self,arg_files_path,arg_files):
        '''
        :param arg_file_path:
        :param arg_file: a  list fo files ahving the same extension (MP4 , LRV ...)
        :return: extract the properties from the result file
        '''

        result_dict = {} # this dictionary resume all the files properties having the same extension
        for file in arg_files :
            file_path = arg_files_path + '/' + file
            f = file.split('.')
            result = subprocess.Popen(["ffprobe", file_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            video_properties = result.stdout.read().decode()
            #print(video_properties)
            name                        = f[0]
            type                        = f[1]
            ret                         = os.stat(file_path)
            size                        = ret.st_size/1048576.0 # 1024*1204 # en ( bytes --> Mega bytes)
            if type == 'THM':
                thm=  {'name' : name, 'type':type ,'size MB':size}
                if not result_dict  : # means it's empty
                    result_dict = thm
                else:
                    result_dict.update({'size MB' : result_dict['size MB'] + thm['size MB']})
            else: # mp4 or lrv
                if size != 0.0:
                    duration                    = self.get_duration_sec(self.parser.search_pattern(video_properties,'video_duration'))
                    frame_rate                  = self.parser.search_pattern(video_properties,'frame_rate')
                    bit_rate                    = self.parser.search_pattern(video_properties,'bit_rate')
                    resolution                  = self.parser.search_pattern(video_properties,'resolution')
                    encode_format_string        = self.parser.search_pattern(video_properties,'video_pattern')
                    color_code_string           = encode_format_string.split(',')[1] # yuvj420p(pc, bt709)
                    encode_format               = self.parser.search_pattern(encode_format_string,'encode_format')
                    color_format                = self.parser.search_pattern(color_code_string,'color_format')
                    mp4_lrv = {'name': name, 'type': type, 'size MB': size, 'fps': frame_rate, 'duration': duration,
                               'bit_rate kb/s': bit_rate, 'resolution': resolution, 'encode_format': encode_format,
                               'color_format': color_format}
                else :
                    mp4_lrv = {'name' : name, 'type':type ,'size MB':size, 'fps' : 0, 'duration': 0, 'bit_rate kb/s' : 0,'resolution' : '', 'encode_format' : '', 'color_format' : ''}
                #print('--------->',mp4_lrv)
                if not result_dict  : # means it's empty
                    result_dict = mp4_lrv
                else:
                    result_dict.update({'size MB' : result_dict['size MB']  + mp4_lrv['size MB']})
                    result_dict.update({'duration': result_dict['duration'] + mp4_lrv['duration']})
        return result_dict

    # ----------------------------------------------------------compare ------------------------------------------------
    def compare(self,arg_in_properties,arg_out_properties):
        '''
        :param arg_in_properties: {'fps':fps,'duration':duration,'resolution':{'MP4':'3840x2160','LRV':'1408x704'},'color_format':{'MP4':'yuvj420p' ,'LRV' : 'yuvj420p'},'encode_format':{'MP4':'h264','LRV':'hevc'},'bit_rate':''588246,'size':{'MP4':MP4_size ,'LRV' : LRV_size}}
        :param arg_out_properties:{'name' : name, 'type':type ,'size':size, 'frame_rate' : frame_rate, 'duration': duration, 'bit_rate' : bit_rate,'resolution' : resolution, 'encode_format' : encode_format, 'color_format' : color_format}
        :return: boolean
        '''
        # print('in : ')
        # print(arg_in_properties)

        out_properties = copy.deepcopy(arg_out_properties)
        file_result = {'result' : True}
        if arg_out_properties['type'] == 'THM':
            if arg_out_properties['size MB'] != 0 :
                pass
            else :
                file_result = {'result': True}
        else :
            type = arg_out_properties['type']
            if arg_out_properties['resolution'] == arg_in_properties['resolution'][type]:
                pass
            else :
                file_result = {'result' : False}
                del out_properties['resolution']
                out_properties.update({'resolution*':{'resolution' : arg_out_properties['resolution'],
                                                      'expected' : arg_in_properties['resolution'][type]}
                                                     }
                                      )
            if arg_out_properties['color_format'] == arg_in_properties['color_format'][type]:
                pass
            else :
                file_result = {'result' : False}
                del out_properties['color_format']
                out_properties.update({'color_format*':{'color_format' : arg_out_properties['color_format'],
                                                      'expected' : arg_in_properties['color_format'][type]}
                                                     }
                                      )
            if arg_out_properties['encode_format'] == arg_in_properties['encode_format'][type]:
                pass
            else :
                file_result = {'result' : False}
                del out_properties['encode_format']
                out_properties.update({'encode_format*':{'encode_format' : arg_out_properties['encode_format'],
                                                      'expected' : arg_in_properties['encode_format'][type]}
                                                     }
                                      )
            if  int(arg_out_properties['bit_rate kb/s']) >= arg_in_properties['bit_rate kb/s'][type]-10000 and int(arg_out_properties['bit_rate kb/s']) <= arg_in_properties['bit_rate kb/s'][type]+10000:
                pass
            else:
                pass
                file_result = {'result' : False}
                del out_properties['bit_rate kb/s']
                out_properties.update({'bit_rate kb/s*': {'bit_rate kb/s': arg_out_properties['bit_rate kb/s'],
                                                          'expected ~ ': arg_in_properties['bit_rate kb/s'][type]}
                                       }
                                      )
            if arg_out_properties['size MB'] < arg_in_properties['size MB'][type] + 200 and arg_out_properties['size MB'] > arg_in_properties['size MB'][type] - 200 and arg_out_properties['size MB'] !=0 : # marge de 200 MB chane it when u r sure
                pass
            else:
                pass
                file_result = {'result' : False}
                del out_properties['size MB']
                out_properties.update({'size MB*': {'size': arg_out_properties['size MB'],
                                                          'expected ~ ': arg_in_properties['size MB'][type]}
                                       }
                                      )
            if arg_out_properties['duration'] <= (int(arg_in_properties['duration']) + 4 ) and arg_out_properties['duration'] >= ( int(arg_in_properties['duration']) - 4):
                pass
            else:
                pass
                file_result = {'result' : False}
                del out_properties['duration']
                out_properties.update({'duration*': {'duration': arg_out_properties['duration'],
                                                          'expected ~ ': arg_in_properties['duration']}
                                       }
                                      )
            if float(arg_out_properties['fps'])  >= int(arg_in_properties['fps']) - 0.04 and float(arg_out_properties['fps'])  <= int(arg_in_properties['fps']) + 0.04: # 23.98 and 29.97  -0.02 or -0.03 ? --> use margin
                pass
            else:
                file_result = {'result' : False}
                del out_properties['fps']
                out_properties.update({'fps*': {'fps': arg_out_properties['fps'],
                                                          'expected': arg_out_properties['fps']}
                                       }
                                      )

        out_properties.update(file_result) # add result flag for each file to improve errors localisation

        # print('out : ')
        # print(out_properties,'\n')

        return out_properties


    # ---------------------------------------------- check ------------------------------------------
    def get_duration_sec(self,time_str):
        h, m, s = time_str.split(':')
        return int(h) * 3600 + int(m) * 60 + int(float(s))



    # ---------------------------------------------- regroup_based_on_type ------------------------------------------
    def regroup_based_on_type(self,file_list):
        '''

        :param file_list: [f1.mp4 ,f2.lrv ,f3.thm, f11.mp4, f22.lrv, f33.thm]
        :return: [[f1.mp4,f11.mp4] ,[f2.lrv, f22.lrv] ,[f3.thm,, f33.thm]]
        '''
        regrouped_files = []
        lrv_files = []
        mp4_files = []
        thm_files = []
        for file in file_list :
            type= file.split('.')[1]
            if type == 'MP4':
                mp4_files.append(file)
            elif type =='THM':
                thm_files.append(file)
            else: # lrv
                lrv_files.append(file)
        regrouped_files.append(mp4_files)
        regrouped_files.append(thm_files)
        regrouped_files.append(lrv_files)
        return regrouped_files





    # ---------------------------------------------- check ------------------------------------------
    def check(self, *args):
        files_properties = []
        result_flag = True
        files_path = args[0]
        preview_state = args[1]
        non_preview_state = args[2]

        files = os.listdir(files_path)
        files_number = len(files)
        regrouped_files = self.regroup_based_on_type(files)
        if files != []:
            files_in_properties = self.extract_in_properties(preview_state,non_preview_state)
            for file_group in regrouped_files:
                if len(file_group) !=0:
                    file_out_properties = self.extract_out_properties(files_path, file_group)
                    file_result = self.compare(files_in_properties,file_out_properties)
                    result_flag = result_flag and file_result['result']
                    files_properties.append(file_result)
                else:
                    raise Exception("checker for video can't find all the  required files in : {}".format(files_path))
        else:
            result_flag = False

        return {'result': result_flag, 'number of files': files_number, 'files': files_properties}






# ------------------------------------------------------FileStat checker -----------------------------------------------#
#                                                                                                                       #
#                                                                                                                       #
# ------------------------------------------------------FileStat checker -----------------------------------------------#
class PhotoStat(FileStat):

    def extract_in_properties(self,arg_non_preview):
        submode = None
        in_resolution = arg_non_preview['params']['params_mode']['resolution']
        if 'submode' in arg_non_preview['params']['params_mode']:
            submode = arg_non_preview['params']['params_mode']['submode']
        stitch_mode = arg_non_preview['params']['params_mode']['stitch_mode']
        resolution = self.get_resolution(in_resolution,stitch_mode,submode)
        return {'resolution' : resolution}

    # ---------------------------------------------- get_resolution ------------------------------------------
    def get_resolution(self,arg_resolution,arg_stitch_mode,arg_submode):
        if arg_submode == 'PANO':
            return '4320x1440'
        elif arg_submode =='CAL':
            return '4056x3040'
        elif arg_resolution == '6K' and arg_stitch_mode == 'ERP':
            return '5760x2880'
        else :
            raise Exception('can\'t extract resolution for in_resolution = {} , submode = {} and stitch_mode ={}'.format(arg_resolution,arg_submode,arg_stitch_mode))

    # ---------------------------------------------- compare ------------------------------------------
    def compare(self,arg_in_properties,arg_out_properties):
        out_properties = copy.deepcopy(arg_out_properties)
        file_result = {'result' : True}
        if arg_out_properties['resolution'] == arg_in_properties['resolution']:
            pass
        else :
            file_result = {'result' : False}
            del out_properties['resolution']
            out_properties.update({'resolution*':{'resolution' : arg_out_properties['resolution'],
                                                  'expected' : arg_in_properties['resolution']}
                                                     })
        out_properties.update(file_result)
        #print(out_properties)
        return out_properties



    # ---------------------------------------------- extract_out_properties ------------------------------------------
    def extract_out_properties(self,arg_file_path,arg_file):
        file_path = arg_file_path + '/' + arg_file
        result = subprocess.Popen(["ffprobe", file_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        photo_properties = result.stdout.read().decode()
        f = arg_file.split('.')
        name        = f[0]
        type        = f[1]
        size        = str(os.stat(file_path).st_size/1048576.0)
        if size != 0.0:
            resolution   = self.parser.search_pattern(photo_properties,'resolution')
        else :
            resolution  = ''
        return {'name' : name, 'type':type ,'size MB':size ,'resolution' : resolution}


    # ---------------------------------------------- extract_out_properties ------------------------------------------
    def check(self,*args ):
        files_properties = []
        result_flag = True
        files_path = args[0]
        non_preview_state = args[2]
        files = os.listdir(files_path)
        files_number = len(files)
        if files != []:
            files_in_properties = self.extract_in_properties(non_preview_state)
            for file in files:
                file_out_properties = self.extract_out_properties(files_path, file)
                file_result = self.compare(files_in_properties,file_out_properties)
                result_flag = result_flag and file_result['result']
                files_properties.append(file_result)
        else:
            result_flag = False

        return {'result': result_flag, 'number of files': files_number, 'files': files_properties}








# preview = {
#         "case": "preview",
#         "params":
#           {
#           "shooting_mode" : "lcd",
#           "params_mode":
#           {
#             "fps"         : "30",
#             "stitch_mode" : "EAC",
#             "resolution"  : "5K"
#           },
#           "options_mode":
#           {
#             "eac_split"   : "disable",
#             "lrv"         : "enable",
#             "bypass"      : "enable",
#             "rear"        : "disable"
#           }
#         }
#       }
# non_preview = {
#         "case": "video",
#         "params":
#         {
#           "shooting_mode"         : "spherical",
#           "options_mode" :
#           {
#             "flare"               : "0",
#             "flare_art"           : "identity",
#             "flare_fake"          : "disable",
#             "flare_fake_time"     : "2",
#             "flare_art_front_corr": "60",
#             "bypass"              : "enable",
#             "run_time"            : "600",
#             "debug_dump"          : "disable",
#             "debug_dump_opt"      : "yuv,data",
#             "ring_high_res"       : "enable",
#             "stab"                : "disable",
#             "spher_eis"           : "0",
#             "stab_degree"         : "0.7",
#             "exposure"            : "enable"
#           }
#         },
#         "logs" : "~/Desktop/test_logs/V0/30/serials"
#       }
# #
# #
# #
# c = VideoStat()
# print(c.check('/home/saif/Desktop/test_null',preview,non_preview))

#
# non_preview = {
#         "case": "still",
#         "params":
#         {
#           "shooting_mode"  : "spherical",
#           "params_mode"    :
#            {
#              "fps"            : "30",
#              "submode"        : "PANO",
#              "stitch_mode"    : "ERP",
#              "resolution"     : "6K"
#            },
#           "options_mode" :
#           {
#             "flare"         : "0",
#             "flare_art"     : "",
#             "bypass"        : "disable",
#             "ring_low_res"  : "disable",
#             "dump_raw"      : "disable",
#             "raw_nbits"     : "16",
#             "bayer_width"   : "4056",
#             "mpx"           : "6MP",
#             "debug_dump"    : "disable",
#             "rear"          : "disable"
#
#           }
#         }
# }


# c = PhotoStat()
# print(c.check('/home/saif/Desktop/test_null',preview,non_preview))

# # print(c.check('/home/saif/Desktop/test_logs/C0/photos'))

# [{
#     "description": "S0 : 6K ERP 30fps ",
#     "steps":
#     [
#       {
#         "case": "still",
#         "params":
#         {
#           "shooting_mode"  : "spherical",
#           "params_mode"    :
#            {
#              "fps"            : "30",
#              "stitch_mode"    : "ERP",
#              "resolution"     : "6K"
#            },
#           "options_mode" :
#           {
#             "flare"         : "0",
#             "flare_art"     : "",
#             "bypass"        : "disable",
#             "ring_low_res"  : "disable",
#             "dump_raw"      : "disable",
#             "raw_nbits"     : "16",
#             "bayer_width"   : "3008",
#             "debug_dump"    : "disable",
#             "debug_dump_opt": "",
#             "mpx"           : "18MP"
#
#           }
#         },
#         "logs" : "~/Desktop/test_logs/S0/serials"
#       },
#
#       {
#         "case": "reset",
#         "params":
#           {
#             "option": "soft"
#           }
#       },
#       {
#         "case": "checker",
#         "params":
#         {
#           "out_directory"  : "~/Desktop/test_logs/S0/photos",
#           "TypeChecker"    : "PhotoStat"
#         }
#       }
#
#
#     ]
# }
# ]
# result = subprocess.Popen(["ffprobe", '/home/saif/Desktop/test_logs/V0/24/videos/GS010269.MP4'],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
# file_info = result.stdout.read().decode()