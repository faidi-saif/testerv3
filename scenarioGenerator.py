import random
import json
import re
import copy
from random import randint
from logger import Logger
class ScenarioGenerator :
    '''
    take a list of elementary scenarios and generates from it a random scenario
    subscenario is the elementary action to perform for example :  v25 ( take video with 25 fps )
    for other options we can use this format  : scenario_name*occurence*flare-option*split-option example :
    for split and flare enabled and occurence =  2 : v15*2*flare*split
    for flare and split disabled and occurence = 1 : v15
    scenarios :  s0  , pano are by default 30fps

    '''


    def __init__(self):

        self.max_retries = 100 # max retries to generate the scenario
        self.test_id     =  0
        self.preview = {
                         "description": "preview 5.6K 100 fps ",
                         "steps":
                         [
                           {
                             "case": "preview",
                             "params":
                               {
                               "shooting_mode" : "lcd",
                               "params_mode":
                               {
                                 "fps"         : "24",
                                 "stitch_mode" : "EAC",
                                 "resolution"  : "5K"
                               },
                               "options_mode":
                               {
                                 "eac_split"   : "disable",
                                 "lrv"         : "enable",
                                 "bypass"      : "enable",
                                 "rear"        : "disable"
                               }
                             }
                           }
                         ]
                        }
        self.video = {
                        "description": "record video with 5.6K 30 fps ",
                        "steps":
                        [
                          {
                            "case": "video",
                            "params":
                            {
                              "shooting_mode"         : "spherical",
                              "options_mode" :
                              {
                                "flare"               : "0",
                                "flare_art"           : "identity",
                                "flare_fake"          : "disable",
                                "flare_fake_time"     : "2",
                                "flare_art_front_corr": "60",
                                "bypass"              : "enable",
                                "run_time"            : "60",
                                "debug_dump"          : "disable",
                                "debug_dump_opt"      : "yuv,data",
                                "ring_high_res"       : "enable",
                                "stab"                : "disable",
                                "spher_eis"           : "0",
                                "stab_degree"         : "0.7",
                                "exposure"            : "enable"
                              }
                            },
                            "logs" : ""
                            },
                            {
                                "case": "checker",
                                "params":
                                {
                                  "out_directory"  : "",
                                  "TypeChecker"    : "VideoStat"
                                }
                            }
                          ]
                    }


        self.s0 = {
                    "description": "S0 : 6K ERP ",
                    "steps":
                    [
                      {
                        "case": "still",
                        "params":
                        {
                          "shooting_mode"  : "spherical",
                          "params_mode"    :
                               {
                                 "fps"            : "30",
                                 "stitch_mode"    : "ERP",
                                 "resolution"     : "6K"
                               },
                          "options_mode" :
                              {
                                "flare"         : "0",
                                "flare_art"     : "",
                                "bypass"        : "disable",
                                "ring_low_res"  : "disable",
                                "dump_raw"      : "disable",
                                "raw_nbits"     : "16",
                                "bayer_width"   : "3008",
                                "debug_dump"    : "disable",
                                "debug_dump_opt": "",
                                "mpx"           : "18MP"
                              }
                        },
                         "logs" : ""
                      },
                      {
                        "case": "checker",
                        "params":
                            {
                              "out_directory"  : "",
                              "TypeChecker"    : "PhotoStat"
                            }
                      }
                    ]
                }

        self.pano = {
                    "description": "still pano",
                    "steps":
                    [
                      {
                        "case"  : "still",
                        "params":
                        {
                          "shooting_mode"     : "spherical",
                          "params_mode"       :
                           {
                             "fps"            : "30",
                             "submode"        : "PANO",
                             "stitch_mode"    : "ERP",
                             "resolution"     : "6K"
                           },
                          "options_mode" :
                          {
                            "flare"         : "0",
                            "flare_art"     : "",
                            "bypass"        : "disable",
                            "ring_low_res"  : "disable",
                            "dump_raw"      : "disable",
                            "raw_nbits"     : "16",
                            "bayer_width"   : "4056",
                            "mpx"           : "6MP",
                            "debug_dump"    : "disable",
                            "rear"          : "disable"

                          }
                        },
                        "logs" : ""
                      },
                      {
                        "case": "checker",
                        "params":
                        {
                          "out_directory"  : "",
                          "TypeChecker"    : "PhotoStat"
                        }
                      }
                    ]
                }
        self.logger = Logger()
    # --------------------------------------------------------------------- add_preview_options  ------------------------------------------------------------------------------

    def add_preview_options(self,preview,sub_sceanrio):
        '''
        :param preview: the preview mode added before each non preview mode
        :param sub_sceanrio: the non preview mode
        : add split to preview if the user specifies split option in the non preview mode
        return : return ['p30','split'] is split is specified (example input : ['v30','split']
        '''
        if 'split' in  sub_sceanrio:
            preview.append('split')
        return preview

#--------------------------------------------------------------------- adjust_sceanrio  ------------------------------------------------------------------------------

    def add_preview_mode(self,arg_sequence):
        '''
        :param arg_sequence: a list of test scenarios each one is a list of [name,occurrence,split,flare] = [['v15'], ['p24'], ['pano'], ['p30'], ['p15', '2', 'split', 'flare'], ['v25'], ['s0'], ['p25']]
        :return: adjusted list , so add a preview mode before each non preview scenario
        '''
        adjusted_scenario = []
        for sub_scenario in arg_sequence : # subsceanrio is a list :  ['p15', '2', 'split', 'flare']
            #if it's not preview --> if it is not p{number}
            is_preview = re.compile("p\d+").search(sub_scenario[0])
            if is_preview is  None: # scenario is something else than preview
                is_video = re.compile("v(\d{2})").search(sub_scenario[0])
                if is_video is not None :
                    preview_mode  = ['p{}'.format(is_video.group(1))] # get the fps
                else:
                    preview_mode = ['p30'] # adjust with 'p30' for s0 and pano
                preview_mode = self.add_preview_options(preview_mode,sub_scenario) # return ['p30','split'] if the split is passed as option (v25*split)
                adjusted_scenario.append(preview_mode)
            adjusted_scenario.append(sub_scenario)

        return adjusted_scenario

    # --------------------------------------------------------------------- genrate_random_sequence  ------------------------------------------------------------------------------

    def genrate_random_sequence(self,arg_sequence):
        '''

        :param arg_sequence: a lsit of sceanrio [[p30],[v25]] ..
        :return: random order of arg_sequence
        '''
        random_scenario = []
        while arg_sequence :
            sub_scenario = random.choice(arg_sequence)
            random_scenario.append(sub_scenario)
            arg_sequence.remove(sub_scenario)
        return random_scenario
    # --------------------------------------------------------------------- find_scenario_occurence ------------------------------------------------------------------------------


    def find_scenario_occurence(self,sub_sceanrio_list):
        '''
        :param sub_sceanrio_list: example : ['p15', '2', 'split', 'flare']
        :return: boolean(if occurence is specidifed = true ) , the occurrence value
        '''
        result = False ,1
        for item in sub_sceanrio_list :
            if item.isdecimal() :
                result =  True,int(item)
        return result


    # --------------------------------------------------------------------- genrate_scenario_list ------------------------------------------------------------------------------
    def genrate_scenario_list(self,arg_sub_scenarios):
        '''
        :param arg_sub_scenarios: input string having all the features to be tested : 'p15*2*split,v25*3*flare*split'
        :return:[['p15', 'split'], ['p25', 'split'], ['v25', 'flare', 'split'], ['p25', 'split'], ['v25', 'flare', 'split'], ['p15', 'split'], ['p25', 'split'], ['v25', 'flare', 'split']]
        '''
        input_sceanrio = arg_sub_scenarios.split(',')  #'p15*2*split*flare','p24','p25','p30'','v15','v25','s0','pano'
        scenario = []
        for seq_description in input_sceanrio :
            # duplicate the subs_ceanrio * occurence example :  ['p15', '2', 'split', 'flare'] becomes : ['p15', 'split', 'flare'],['p15', 'split', 'flare']
            sub_sceanrio = seq_description.split('*')
            is_occ_specified,occ = self.find_scenario_occurence(sub_sceanrio)
            if is_occ_specified :
                sub_sceanrio.remove(str(occ))
                for occu_iterator in range(occ):
                    scenario.append(sub_sceanrio)
            else:
                scenario.append(sub_sceanrio)
        scenario = self.genrate_random_sequence(scenario)
        scenario = self.add_preview_mode(scenario) # added preview before each non preview sequence
        return scenario
    # --------------------------------------------------------------------- edit_description ------------------------------------------------------------------------------

    def edit_description(self,description,arg_fps):
        if arg_fps :
            match = re.compile('([0-9]*|[0-9]) fps').search(description)
            if match is not None :
                description = description.replace(match.group(1),arg_fps)
        return description

    # --------------------------------------------------------------------- find_item_position ------------------------------------------------------------------------------
    def find_item_position(self,arg_attribute,arg_steps):
        position = 0
        for step in arg_steps :
            if (arg_attribute == 'logs' and 'logs' in step ) or (arg_attribute =='checker' and step['case'] == 'checker'):
                return position
            position += 1


    # --------------------------------------------------------------------- generate_preview ------------------------------------------------------------------------------

    def generate_dict(self,arg_mode,arg_fps = None ,arg_split = None,arg_flare = None , arg_run_time = None ,arg_path =  None ):
        '''
        :param arg_mode:
        :param arg_fps:
        :param arg_split:
        :param arg_flare: if flare is specified (enable) --> updated with '1'
        :param arg_run_time:
        :return:
        '''
        def find_step_index(steps,case):
            '''
            :param steps:
            :param case:
            :return:
            call this function to find index of the
            '''
            index = 0
            for el in steps :
                if el['case'] == case :
                    return index
                index += 1




        self.test_id += 1
        updated_sub_scenario = {'id':str(self.test_id)}
        if arg_mode == 'preview':

            updated_sub_scenario.update(copy.deepcopy(self.preview))                        # update the description field
            preview_case_index = find_step_index(updated_sub_scenario['steps'],'preview')  # find the position of the case 'preview in the list of steps
            #print('self.preview---->',self.preview)
            updated_sub_scenario['steps'][preview_case_index]['params']['params_mode']['fps'] = arg_fps # update the fps field
            if arg_split :
                updated_sub_scenario['steps'][preview_case_index]['params']['options_mode']['eac_split'] = 'enable'  # update the split field
            else :
                pass # split is disabled by default
        else :
            if arg_mode == 'video':
                #assert arg_run_time is not None ,'No run_time set for video'
                # edit fps in the description , run_time , and the flare , the flare is automatically set to 1
                updated_sub_scenario.update(copy.deepcopy(self.video))
                video_case_index    = find_step_index(updated_sub_scenario['steps'], 'video')
                updated_sub_scenario['steps'][video_case_index]['params']['options_mode']['run_time'] = arg_run_time
                complementary_path  = 'videos/'+ arg_fps + '_fps/' + updated_sub_scenario['id']
            elif arg_mode == 's0' :
                updated_sub_scenario.update(copy.deepcopy(self.s0))
                complementary_path  = 's0/'+ updated_sub_scenario['id']
            elif arg_mode =='pano':
                updated_sub_scenario.update(copy.deepcopy(self.pano))
                complementary_path  = 'pano/' + updated_sub_scenario['id']
            if arg_flare :
                updated_sub_scenario['steps'][video_case_index]['params']['options_mode']['flare'] = '1'
            logs_position       = self.find_item_position('logs',updated_sub_scenario['steps'])
            checker_position    = self.find_item_position('checker', updated_sub_scenario['steps'])

            updated_sub_scenario['steps'][logs_position]['logs'] = arg_path + '/' + complementary_path + '/serials'
            updated_sub_scenario['steps'][checker_position]['params']['out_directory'] = arg_path + '/' + complementary_path + '/files'
            #
            # print('logs', updated_sub_scenario['steps'][logs_position]['logs'])
            # print('out_directory', updated_sub_scenario['steps'][checker_position]['params']['out_directory'])

        description = self.edit_description(updated_sub_scenario['description'], arg_fps)
        updated_sub_scenario['description'] = description

        return updated_sub_scenario


    # --------------------------------------------------------------------- generate_sub_dictionnary ------------------------------------------------------------------------------

    def generate_sub_dictionnary(self,sub_scenario,arg_path):
        '''
        :arg_path : folder to store the robustness test results
        :param sub_scenario: example : ['p15', 'split']
        :return: dictionary related to sub_scenario
        '''
        sub_dictionary = {} # sub_dictioanary is the dictioanary related to a sub scenario , it can be one of these : preview  , s0 ..
        def get_run_time(arg_video_list):
            pattern = re.compile(r'd(\d+)')
            for item in arg_video_list :
                match = pattern.search(item)
                if match :
                    return match.group(1)

        # case 1- preview
        is_preview = re.compile("p(\d+)").search(sub_scenario[0])
        mode            =  ''
        flare           = None
        fps             = None
        split           = None
        run_time        = None
        result_path     = None
        if is_preview  :
            fps   = is_preview.group(1)
            if 'split' in sub_scenario :
                split = 'enable'
            mode = 'preview'
        #case 2- video  ,s0 , pano
        else :
            if 'flare' in sub_scenario:
                flare = 'enable'
            is_video = re.compile("v(\d+)").search(sub_scenario[0])
            if is_video  :
                run_time = get_run_time(sub_scenario)
                fps = is_video.group(1)
                mode = 'video'
            elif sub_scenario[0] == 's0':
                mode = 's0'
            elif sub_scenario[0] == 'pano':
                mode = 'pano'
            else :
                raise Exception( 'Invalid mode used, Mode is :s0, pano, v15 ,v24 , v25 ,v30 , p15 , p24, p25 ,p30')
            result_path = arg_path
        sub_dictionary = self.generate_dict(arg_mode= mode ,arg_flare=flare,arg_fps=fps,arg_split=split,arg_run_time=run_time,arg_path = result_path)
        return sub_dictionary
        #print(sub_dictionnary)

    # --------------------------------------------------------------------- add_durations ------------------------------------------------------------------------------
    def add_durations(self,arg_sceanrio,min_duration,max_duration,sd_card_size):
        '''
        :param arg_sceanrio: sceanrion 2d list
        :param max_duration: max duration of the video in s
        :param min_duration: min duration of the video in s
        :arg_sd_card_size  : size of the sd card in GB (byte)
        :return:
        '''
        import time
        bitrate = 10 # 10MB Mega byte (80 Mbit)
        valid_estimaed_size = False

        retries = 0
        while valid_estimaed_size == False :
            size = 0  # Mega bits
            retries += 1
            if retries > self.max_retries / 1.6 or retries > self.max_retries / 1.4 or retries > self.max_retries /1.2:
                max_duration = int(max_duration * 0.8 )
                min_duration = int(min_duration * 0.8)
            if retries == self.max_retries :
                raise Exception('sd card size exceeded with this sceanrio , think to decrease max and min duration or the occurence of your sub-scenarios')


            new_sceanrio = []
            for sub_sc in arg_sceanrio :
                if re.compile("v\d+").search(sub_sc[0]): # it's a video
                    duration = randint(min_duration,max_duration)
                    size     = size + duration*bitrate
                    sub_sceanrio = list(sub_sc)
                    sub_sceanrio.append('d{}'.format(duration))
                elif sub_sc[0] == 's0':
                    size = size + 7
                    sub_sceanrio = sub_sc
                else  : # sub_sc == pano
                    size = size + 6
                    sub_sceanrio = sub_sc
                new_sceanrio.append(sub_sceanrio)
            # print(float(size / (1024)))
            # time.sleep(1)
            if  float (size/(1024)) < sd_card_size:
                valid_estimaed_size = True
        return new_sceanrio

    # --------------------------------------------------------------------- generate_sceanrio ------------------------------------------------------------------------------
    def generate_sceanrio(self,arg_sceanrio,arg_result_path,min_duration=10,max_duration=14,sd_card_size = 32):
        '''

        :param arg_sceanrio:
        :param arg_result_path: path where to generate the scenario as a json file
        :param min_duration:
        :param max_duration:
        :param sd_card_size:
        :return:
        NOTE : in the json generated the files path in "logs" and "out_directory" of the steps is in the parent directory of the "arg_result_path"
        '''
        self.test_id    = 0
        final_scenario  = []
        arg_path        = self.logger.get_parent_path(arg_result_path)
        sceanrio_list   = self.genrate_scenario_list(arg_sceanrio)
        sceanrio_list   = self.add_durations(sceanrio_list,min_duration,max_duration,sd_card_size)
        #print(' random scenario generated : ',sceanrio_list)
        for sc in sceanrio_list :
            final_scenario.append(self.generate_sub_dictionnary(sc,arg_path))
        # for sc in final_scenario:
        #     print(sc)
        #     print()
        self.logger.write_json(arg_result_path,final_scenario)











#
# sc_gen =  ScenarioGenerator()
# adjusted = sc_gen.add_preview_mode([['v15'], ['p24'], ['pano'], ['p30'], ['p15', '2', 'split', 'flare'], ['v25'], ['s0'], ['v25']])
# print(adjusted)

#random_seq = sc_gen.genrate_scenario_list('p15*2*split,v25*3*flare*split')
#['p15', 'flare','split'],['v30','flare'],[
# sc_gen.generate_sub_dictionnary(['pano','flare','split'])

# spec,occ = sc_gen.find_scenario_occurence(['p15', '2', 'split', 'flare'])
# print(spec,occ)
# seq =  [['v15'], ['p24'], ['pano'], ['p30'], ['p15', '2', 'split', 'flare'], ['v25'], ['s0'], ['p25']]
#
# for el in seq:
#     print(el)
# l= [['p15', 'split'], ['p25'], ['v25', 'flare'], ['p15', 'split']]
# print(sc_gen.generate_sub_dictionnary(l[0]))
# print(sc_gen.generate_sub_dictionnary(l[1]))
# sc_gen.generate_sceanrio('p15*2*split,v25*1*flare,pano*2,s0','~/Desktop/status/robustness/generated_sceanrios/robustness1.json')

#print(sc_gen.add_duration([['v15'], ['pano'],  ['v25'], ['s0'], ['v25']],2,6,arg_sd_card_size=4))

#print(randint(10, 20))