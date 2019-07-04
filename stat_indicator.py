
from logger import Logger

class StatIndicator:

    def __init__(self,arg_scenario_runner,arg_scenario_generator):
        '''
        to get a the status in a pretty organisation :
        make sure :
        for unitary and functional tests :
            the out directories to generate the json result files are equivalent to the out directories where to generates the result files (for example : ../pano/result.json) and ../pano)
        for robustness tests :
            the 'in' path is the path where scenario generator genrates the input json file for scenario runner
            so make sure tey have same parent path to get them at the same path level
            NB : automatically the output files (serials, photos and videos) are generated in the parent path of the input scenario file (generated by scenario generator ))
        :param arg_scenario_runner:
        :param arg_scenario_generator:
        '''
        self.scene_stat     = 'Not controlled'
        self.skakyness_stat =  'None'
        self.out_dir        =  '~/Desktop/status'
        self.max_duration   = 4  #s
        self.min_duration   = 2  #s
        self.sd_card_size   = 32 #GB
        self.sc_runner      = arg_scenario_runner
        self.sc_generator   = arg_scenario_generator
        self.logger         = Logger()
        self.result         = []
        self.functional     = \
                          [
                            {   'in': './scenarios/still_pano.json' ,                  'out': '~/Desktop/status/functional/still_pano/func_still_pano.json'    },
                            {   'in': './scenarios/S0.json',                           'out': '~/Desktop/status/functional/S0/func_still_S0.json'              },
                            # {   'in': './scenarios/C0.json',                           'out': '~/Desktop/status/functional/C0/func_still_C0.json'              },
                            # {   'in': './scenarios/func_spheric_video_30_fps.json',    'out': '~/Desktop/status/functional/v30/func_spheric_video_30_fps.json' },
                            # {   'in': './scenarios/func_spheric_video_25_fps.json',    'out':'~/Desktop/status/functional/v25/func_spheric_video_25_fps.json'  },
                            # {   'in': './scenarios/func_spheric_video_24_fps.json',    'out': '~/Desktop/status/functional/v24/func_spheric_video_24_fps.json' },
                            # {   'in': './scenarios/func_spheric_video_15_fps.json',    'out': '~/Desktop/status/functional/v15/func_spheric_video_15_fps.json' }
                          ] # list of dictionnaire with (in_json,ou_json)


        self.unitary    = [
                            {'in': './scenarios/unitary_spheric_video_30_fps_1min.json',  'out': '~/Desktop/status/unitary/v30/1_min/unitary_spheric_video_30_fps_1min.json' },
                            {'in': './scenarios/unitary_spheric_video_30_fps_10min.json', 'out': '~/Desktop/status/unitary/v30/10_min/unitary_spheric_video_30_fps_1min.json'},
                            # {'in': './scenarios/unitary_spheric_video_30_fps_30min.json','out': '~/Desktop/status/unitary/v30/30_min/unitary_spheric_video_30_fps_1min.json'},
                          ]


        self.robustess  = [
                            {'in': '~/Desktop/status/robustness/robus1/robustness1.json','out': '~/Desktop/status/robustness/robus1/result_robustness1.json','sc':'pano'},
                            # {'in': '~/Desktop/status/robustness/robus2/robustness2.json','out': '~/Desktop/status/robustness/robus2/result_robustness2.json','sc':'v25'}
                          ]


    def run(self,arg_list_test):
        for test in arg_list_test :
            self.sc_runner.run_test(test['in'],test['out'])
            if self.sc_runner.test_result == True :
                result = 'OK'
            else :
                result = 'KO'
            self.result.append([self.sc_runner.test_name, result, self.sc_runner.test_duration])




    def gen_robus_sce(self):
        '''
        here we pass the same path as sc_runner input path , be cause scenario_generator generates a scenario in the 'in' path of self.robustness
        :return: generates a json in self.robustness[index]['in']
        '''
        for test in self.robustess :
            self.sc_generator.generate_sceanrio(test['sc'],test['in'],self.min_duration,self.max_duration,self.sd_card_size)


    def pretty_formatting(self):
        s = [[str(e) for e in row] for row in self.result]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        self.result = [fmt.format(*row) for row in s]


    def run_status(self):
        self.result.append(['|====================================','====================================','===================================|'])
        self.result.append(['| functional tests','','                                   |'])
        self.result.append(['|===================================', '====================================','===================================|'])
        self.run(self.functional)
        self.result.append(['|===================================', '====================================','===================================|'])
        self.result.append(['| unitary tests', '', '                                   |'])
        self.result.append(['|===================================', '====================================','===================================|'])
        self.run(self.unitary)
        self.gen_robus_sce()
        self.result.append(['|===================================', '====================================','===================================|'])
        self.result.append(['| robustness tests','', '                                   |'])
        self.result.append(['|===================================', '====================================','===================================|'])
        self.run(self.robustess)
        self.result.append(['------------------------------------', '------------------------------------','------------------------------------'])
        self.result.insert(0, ['| shakyness', self.skakyness_stat, 'Duration(sec)'])
        self.result.insert(0, ['| Scene',  self.scene_stat, ''])
        self.result.insert(0, ['| Serial Number', self.sc_runner.cam_sn, ''])
        self.result.insert(0, ['| SHA1',self.sc_runner.sh1, ''])
        self.result.insert(0, ['| Date',self.sc_runner.date,''])
        self.result.insert(0, ['------------------------------------', '---------firmware status------------', '------------------------------------'])


        self.logger.write_2d_list(self.out_dir,'status.txt',self.result)







