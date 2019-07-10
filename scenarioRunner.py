import json
import time
from logger import Logger
import  check.checker as checker
import datetime
import re
from parserForCamera import ParserForCamera
class ScenarioRunner :

    # ---------------------------------------------- constructor ------------------------------------------
    def __init__(self,vcamera):
        self.vcamera                    = vcamera
        self.description                = ''
        self.steps                      = []
        self.step_preview               = 'preview'
        self.step_still                 = 'still'
        self.step_reset                 = 'reset'
        self.step_video                 = 'video'
        self.step_checker               = 'checker'
        self.step_flash                 = 'flash'
        self.step_reboot                = 'reboot'
        self.ref_frw_type               = 'spherical'
        self.results                    = []
        self.checkers                   = [] # keep an history of checkers with their parameters  [{'description : ' 5.6k EAC ','files' :[f1,f2] , 'TypeChecker':'videostat' ,'out_directory':'~/Desktop/test_logs'},...]
        self.cam_files                  = [] # at the beginning no files are stored in /tmp/fuse_d/DCIM/100GOPRO
        self.previous_cam_files         = []
        self.dump_raw_files             = []
        self.previous_dump_raw_files    = []
        self.previous_debug_dump_files  = []
        self.debug_dump_files           = []
        self.preview_state              = {} # used to keep the preview mode for the checker
        self.non_preview_state          = {} # used to keep the (still , video) state for the checker
        self.logger                     = Logger()
        self.parser                     = ParserForCamera()
        self.final_test_table           = [] # only this table is not reset , we need to store a table to get the resulst of all the tests with (name, result, duration)



    # ---------------------------------------------- run_wlog ------------------------------------------
    def run_wlog(self,arg_step,function,*args):
        '''

        :param arg_step: dictionary containing the step to be executed
        :param function: callback function associated to the step
        :param args: arguments passed to the function
        :return: None

        this function check if the user wants to keep the serial ports logs for the associated step or not
        '''
        if  'logs' in arg_step.keys():
            self.vcamera.start_acquisition()
            function(*args)
            self.vcamera.stop_acquisition()
            data = self.vcamera.get_data()
            log_path = str(self.logger.create_dir(arg_step['logs']))
            rtos_path = log_path + '/rtos.txt'
            linux_path = log_path + '/linux.txt'
            self.logger.write(rtos_path, data[1])
            self.logger.write(linux_path, data[0])
        else :
            #print(*args)
            function(*args)


    # ---------------------------------------------- run ------------------------------------------

    def run(self,arg_step):
        '''
        :param arg_step: step of the scenario
        :return: result of the step ( None  True or False )
        '''


        if arg_step ['case']   == self.step_reset:
             if self.vcamera.is_ready('serial',arg_timeout=10):
                soft_hard = arg_step['params']['option']
                self.run_wlog(arg_step,self.vcamera.reset,soft_hard)
             else :
                 raise Exception('cant process step : {} camera is not ready'.format(arg_step ['case']))

        elif arg_step ['case'] ==self.step_still:
            if self.vcamera.is_ready('serial',arg_timeout=10):
                self.non_preview_state  = arg_step
                mode                    = arg_step['params']
                self.run_wlog(arg_step, self.vcamera.take_photo, mode)
            else:
                raise Exception('cant process step : {} camera is not ready'.format(arg_step['case']))


        elif arg_step['case'] == self.step_video:
            if self.vcamera.is_ready('serial',arg_timeout=10):
                self.non_preview_state = arg_step
                mode                   = arg_step['params']
                self.run_wlog(arg_step, self.vcamera.record_video, mode)
            else:
                raise Exception('cant process step : {} camera is not ready'.format(arg_step['case']))

        elif arg_step['case'] == self.step_flash :
            if self.vcamera.is_ready('ssh', arg_timeout=40):
                mode     = arg_step['params']['mode']
                frw_type = arg_step['params']['frw_type']
                self.run_wlog(arg_step, self.vcamera.flash, mode,frw_type)
            else:
                raise Exception('cant process step : {} camera is not ready'.format(arg_step['case']))

        elif arg_step['case'] == self.step_preview :
            if self.vcamera.is_ready('ssh', arg_timeout=40):
                self.preview_state    = arg_step
                mode                  = arg_step['params']
                self.run_wlog(arg_step, self.vcamera.preview, mode)
            else:
                raise Exception('cant process step : {} camera is not ready'.format(arg_step['case']))


        elif arg_step ['case'] == self.step_checker:
            if self.vcamera.is_ready('ssh',arg_timeout=120) :
                debug_dump_files = []
                dump_raw_files   = []
                files            = self.get_last_files('/tmp/fuse_d/DCIM/100GOPRO/','files')
                if self.vcamera.mind.conf.options_mode['debug_dump'] == 'enable':
                    debug_dump_files    = self.get_last_files('/tmp/fuse_d/DUMPSTITCH/','debug_dump_files')
                if self.vcamera.mind.conf.options_mode['dump_raw']  == 'enable':
                    dump_raw_files      = self.get_last_files('/tmp/fuse_d/BAYER/', 'dump_raw_files')

                checker_type        = arg_step['params']['TypeChecker']
                if checker_type == 'FrwVersion':
                    params = self.vcamera # to be able to call get_frw_version from checker
                else :
                    params = self.logger.check_format(arg_step['params']['out_directory']) # where to check for the files
                    loc_checker = {
                                      'description'       : self.description,
                                      'files'             : files,
                                      'TypeChecker'       : checker_type,
                                      'params'            : params, #can be self.vcamera or the out_directory
                                      'dump_raw_option'   : self.vcamera.mind.conf.options_mode['dump_raw'],
                                      'debug_dump_option' : self.vcamera.mind.conf.options_mode['debug_dump'],
                                      'debug_dump_files'  : debug_dump_files,
                                      'dump_raw_files'    : dump_raw_files,
                                      'preview_state'     : self.preview_state,
                                      'non_preview_state' : self.non_preview_state
                                    }
                    self.checkers.append(loc_checker)

            else:
                raise Exception('cant process step : {} camera is not ready'.format(arg_step['case']))



        # test_result.update({'result': result})
        # return test_result
    # ----------------------------------------------get_added_files ------------------------------------------
    def get_last_files(self,arg_path,arg_file_type):
        '''
        each time  new files are added in the arg_path directory, this function returns a list of this files names
        :param arg_path: path where to search for new files
        :return: the new files added in the 'arg_path' path
        '''
        if arg_file_type  == 'files':
            self.previous_cam_files         =  list(self.cam_files)
            self.cam_files                  =  re.findall(r'\S+',self.vcamera.ls_files(arg_path)) #from a string get all the file names
            added_files                     =  list(set(self.previous_cam_files) ^ set(self.cam_files))
        elif arg_file_type == 'debug_dump_files':
            self.previous_debug_dump_files  =  list(self.debug_dump_files)
            self.debug_dump_files           =  re.findall(r'\S+',self.vcamera.ls_files(arg_path)) #from a string get all the file names
            added_files                     =  list(set(self.previous_debug_dump_files) ^ set(self.debug_dump_files))
        else : # dump_raw
            self.previous_dump_raw_files    =  list(self.dump_raw_files)
            self.dump_raw_files             =  re.findall(r'\S+',self.vcamera.ls_files(arg_path)) #from a string get all the file names
            added_files                     =  list(set(self.previous_dump_raw_files) ^ set(self.dump_raw_files))
        print('added files in {} are {}'.format(arg_path,added_files))
        return added_files


    def clean_varaibles(self):
        self.steps.clear()
        self.results.clear()
        self.checkers.clear()
        self.cam_files.clear()
        self.previous_cam_files.clear()
        self.dump_raw_files.clear()
        self.previous_dump_raw_files.clear()
        self.previous_debug_dump_files.clear()
        self.debug_dump_files.clear()
        self.preview_state.clear()
        self.non_preview_state.clear()


        # ----------------------------------------------check ------------------------------------------

    def check(self ,derived_checker,*args):
        '''
        instatiate the checker class based on the user input and run the check fuction
        :param derived_checker: checker
        :param args:  parametres for the checker
        :return: result of the test
        '''
        derived_checker = derived_checker.strip()
        klass           = getattr(checker, derived_checker)
        instance        = klass()
        result          = instance.check(*args)
        return result

    # ---------------------------------------------- run_pre_step ------------------------------------------
    def run_pre_step(self,arg_step):
        '''
        performed before each step
        :param arg_step:
        :return:
        '''
        pass

    # ---------------------------------------------- run_post_step ------------------------------------------
    def run_post_step(self,arg_step):
        '''
        performed after each step
        :param arg_step:
        :return:
        '''
        # if firmware is not valid print results , reflash with valid firmware , exit
        if (( arg_step['case'] == self.step_flash) and (self.vcamera.is_ready('ssh','serial',arg_timeout=90) == False )):
            print('invalid firmware ','{} -------> {}'.format(self.description,False))
            self.vcamera.flash('arduino',self.ref_frw_type)
            if self.vcamera.is_ready('ssh','serial',arg_timeout=120):
                print('a valid firmware is installed on the platform')
                exit(1)
            else :
                raise Exception("FlashError , can't flash the platform with a valid firmware " )
        else:
            pass

    # ---------------------------------------------- before_test------------------------------------------
    def clean_up(self):
        '''
        cleanup the camera before starting the test
        :return:None
        '''
        print('*** cleanup camera ***')
        self.vcamera.cleanup()

    # ----------------------------------------------run_pre_scenario  ------------------------------------------

    def run_pre_scenario(self,arg_sceanrio,with_unique_log_index):
            for step in self.steps :
                if with_unique_log_index == True:
                    now = datetime.datetime.now()
                    index = str(now.isoformat())
                    self.add_log_unique_index(arg_step = step,index = index)
                else :
                    pass
            self.description = arg_sceanrio['description']
            self.steps       = arg_sceanrio['steps']
            if 'id' in arg_sceanrio.keys():
                self.scenario_id = arg_sceanrio['id']
            else :
                self.scenario_id = None




    # ---------------------------------------------- run_post_scenario ------------------------------------------
    def run_post_scenario(self):
        '''
        performed after each scenario
        :return:
        '''
        # reinit virtual camera ( all the
        pass
    # ---------------------------------------------- run_post_scenario ------------------------------------------
    def extract_cam_info(self):
        cam_info                = self.vcamera.get_info()
        self.sh1                = self.parser.search_pattern(cam_info, 'sh1')
        self.cam_sn             = self.parser.search_pattern(cam_info, 'cam_sn')
        self.cam_id             = self.parser.search_pattern(cam_info, 'cam_id')
        self.frw_version        = self.parser.search_pattern(cam_info, 'frw_version')
        self.cam_name           = self.parser.search_pattern(cam_info,'cam_name')
        self.frw_compile_date   = self.parser.search_pattern(cam_info,'compile_date')


    # ---------------------------------------------- get_test_result ------------------------------------------
    def get_test_result(self):
        self.test_result = True
        for res in self.results :
            self.test_result = self.test_result and res['result']
            if self.test_result == False :
                return


    # ---------------------------------------------- add_log_unique_index ------------------------------------------
    def add_log_unique_index(self,arg_step,index):
        if 'logs' in arg_step.keys():
            arg_step['logs'] = arg_step['logs'] + '_' + index
        if  'out_directory' in arg_step['params'].keys():
            arg_step['params']['out_directory'] =  arg_step['params']['out_directory'] + '_' + index

    # ---------------------------------------------- pre_test ------------------------------------------
    def run_pre_test(self,arg_sceanrio_file):
        self.clean_up()
        self.clean_varaibles()
        self.test_name       = self.logger.get_file_name_from_path(arg_sceanrio_file).split('.')[0]
        self.date            = datetime.datetime.today().strftime('%Y-%m-%d %H:%M')
        self.test_start_time = time.time()



    # ---------------------------------------------- post_test ------------------------------------------
    def run_post_test(self,arg_result_path):
        self.test_duration      = int(time.time() - self.test_start_time)
        self.extract_cam_info()
        self.get_test_result()
        self.store_result(arg_result_path)
        self.final_test_table.append([self.test_name,self.test_result,self.test_duration])





    # ---------------------------------------------- run_scenario ------------------------------------------
    def run_test(self,arg_scenario_file,arg_result_path,with_unique_log_index = None):
        '''
        :param arg_scenario_file: input file (scenario to be executed )
        :return: None
        1- load json file
        2- find description and the steps
        3- run pre scenario actions
        4- run the different steps of the scenario
        5- get the result and append it to to the self.results list ( the list containing the results of the different
           test cases
        6- run post scenario actions
        '''



        self.run_pre_test(arg_scenario_file)

        scenarios = self.logger.load_json(arg_scenario_file)

        for scenario in scenarios :


            self.run_pre_scenario(scenario,with_unique_log_index = with_unique_log_index)

            print("[--------------------------------------------- start running sceanrio : {} --------------------------------]".format(self.description))

            for step in self.steps :

                self.run_pre_step(step)

                self.run(step)

                self.run_post_step(step)

            self.run_post_scenario()

        self.run_checkers()

        self.run_post_test(arg_result_path)



    # ---------------------------------------------- run_checkers ------------------------------------------
    def run_checkers(self):
        '''
        '''
        test_result = {}
        #print(self.checkers)
        for check_seq in self.checkers:
            if check_seq['TypeChecker'] == 'FrwVersion':
                pass
            else :
                self.vcamera.get_results (  arg_path           =   check_seq['params'],
                                            debug_dump         =   check_seq['debug_dump_option'],
                                            dump_raw           =   check_seq['dump_raw_option'],
                                            arg_files          =   check_seq['files'],
                                            debug_dump_files   =   check_seq['debug_dump_files'],
                                            dump_raw_files     =   check_seq['dump_raw_files']
                                         )
            ret                     = self.check(check_seq['TypeChecker'], check_seq['params'],check_seq['preview_state'],check_seq['non_preview_state'])
            result                  = ret.pop('result') # get the value of ret['result'] and remove it from ret
            test_result.update(ret)    # copy the other fields in the final dictionary
            test_result.update({'result': result})
            test_result['result']   = test_result['result'] and self.vcamera.camera.is_serial_ready(arg_timeout=10)
            ret_value = {'description': 'result ' + check_seq['description']}
            if self.scenario_id: # some scenarios has id  so if it's the case generate the id in the result file
                ret_value.update({'id': self.scenario_id})
            ret_value.update(test_result)
            self.results.append(ret_value)




    # ---------------------------------------------- run_scenario ------------------------------------------
    def store_result(self,result_path):
        '''
        store test results in a  json file at 'result_path'
        :param result_path: path to store test results
        :return: None
        '''

        final_result  = {
                        'test_info':
                            {
                                'name'         : self.test_name,
                                'duration (/s)': self.test_duration,
                                'date'         : self.date,
                                'result'       : self.test_result,
                                'results'      : self.results
                            },
                         'cam_info':
                            {
                              'serial' : self.cam_sn,
                              'id'     : self.cam_id,
                              'name'  : self.cam_name
                            },
                         'firmware_info':
                             {
                                 'git_sh1'          : self.sh1,
                                 'firmware_version' : self.frw_version,
                                 'compilation_date' : self.frw_compile_date
                             },
                         }

        # for el in self.results  :
        #     print(json.dumps(el,indent = 4))
        json.dumps(final_result,indent = 4)
        self.logger.write_json(result_path,final_result)









# s = ScenarioRunner('camera')
# s.run_scenario('./scenarios/scenario1.json')
##if self.vcamera.camera.is_serial_ready(arg_timeout=30):

