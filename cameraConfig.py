import os

class CameraConfig:

    def __init__(self):
        '''
        for each environment variable added :
        1- add it in the dictionary env ( self.env )
        2- add a getter and a setter
        3- add it in the setter of self.env
        '''
    # ----------------------------------------------- default config  -----------------------------------------


        self.mode                  = ''
        self._download_target_dir  = os.environ['HOME'] + '/Desktop/test_capt'
        self.encoder               = 'HEVC'
        self.sensor                = 'IMX577'
        fps                        = ''
        stitch_mode                = '' # EAC, ERP
        submode                    = '' # streamed , encoded , mixed for preview / pano , burst , normal for Non spherical  ...
        resolution                 = '' # deduite pour video
        eac_split                  = '' # Use SPLIT mode for EAC projection
        bypass                     = ''
        lrv                        = ''
        stab                       = 'disable'
        stab_degree                = '0.5'
        ring_high_res              = 'disable'
        exposure                   = ''
        debug_dump                 = ''
        debug_dump_opt             = ''# Pass comma-separated list of the type of data to dump, among 'yuv', 'data', 'raw'. Ex: yuv,data"
        raw_nbits                  = ''
        bayer_width                = ''
        dump_raw                   = ''
        mpx                        = ''
        run_time                   = ''
        flare_fake_time            = '0' # if flare is on --> use default configuration
        flare_art_front_corr       = '50'
        flare_fake                 = 'enable'
        flare                      = ''
        flare_art                  = ''  # Enable artificial <pattern> for flare correction and correct <fnt>% of tiles on front (rest on back)"
        rear                       = ''  # choose front when disabled , back when enabled
        spher_eis                  = '0' # Value for spherical EIS degree of stabilization (float)




        self.shooting_mode              = ''
        self.params_mode                = {
                                          'fps'                 :    fps,
                                          'stitch_mode'         :    stitch_mode,
                                          'resolution'          :    resolution,
                                          'submode'             :    submode
                                          }

        self.options_mode               = {
                                         'eac_split'            :   eac_split,
                                         'flare'                :   flare,
                                         'flare_art'            :   flare_art,
                                         'flare_fake_time'      :   flare_fake_time,
                                         'flare_art_front_corr' :   flare_art_front_corr,
                                         'flare_fake'           :   flare_fake,
                                         'bypass'               :   bypass,
                                         'lrv'                  :   lrv,
                                         'stab'                 :   stab,
                                         'stab_degree'          :   stab_degree,
                                         'ring_high_res'        :   ring_high_res,
                                         'exposure'             :   exposure,
                                         'debug_dump'           :   debug_dump,
                                         'debug_dump_opt'       :   debug_dump_opt,
                                         'raw_nbits'            :   raw_nbits,
                                         'bayer_width'          :   bayer_width,
                                         'dump_raw'             :   dump_raw,
                                         'mpx'                  :   mpx,
                                         'run_time'             :   run_time,
                                         'rear'                 :   rear,
                                         'spher_eis'            :   spher_eis

                                         }
    #----------------------------------------------- getters -------------------------------------------------

    # @property
    # def options_mode(self):
    #     return self._options_mode
    #
    # @property
    # def params_mode(self):
    #     return self._params_mode

    @property
    def env(self):
        self.environment = \
             {
                 'shooting_mode': self.shooting_mode,
                 'params_mode'  : self.params_mode,
                 'options_mode' : self.options_mode
             }
        return  self.environment




    # ----------------------------------------------- env test getter  -----------------------------------------------------
    def get_environment(self):
        return self.env

    # ----------------------------------------------- reset all test variables -----------------------------------------------------
    def reset_test_env(self):
        self.__init__()

    # ----------------------------------------------- shooting_mode setter -----------------------------------------------------
    def set_shooting_mode(self,arg_shut_mode):
        assert(arg_shut_mode == 'spherical' or arg_shut_mode == 'non_spherical' or arg_shut_mode =='dual'or  arg_shut_mode == 'lcd' or arg_shut_mode =='wifi'),'invalid shooting mode'
        self.shooting_mode = arg_shut_mode

    # ----------------------------------------------- params_mode_setter -----------------------------------------------------
    def set_params_mode(self,arg_params_mode):
        '''
        set the parameters of the  camera mode
        :param arg_params_mode:
        :return: None
        '''
        for key, value in arg_params_mode.items():
            key = key.strip()
            if key in self.params_mode.keys():
                if key                             == 'fps':
                    assert (value == '24' or value =='25' or value =='30' or value =='60' or value =='50' or value =='15')
                    self.params_mode['fps']        = arg_params_mode['fps']
                elif key                           == 'stitch_mode':
                    self.params_mode['stitch_mode']    = arg_params_mode['stitch_mode']
                elif key                           == 'submode':
                    self.params_mode['submode']    = arg_params_mode['submode']
                elif key                           == 'resolution':
                    self.params_mode['resolution'] = arg_params_mode['resolution']
                else :
                    raise Exception ('this mode "{}" is not known so it will not be handled in this test'.format(key))


    def set_options_mode(self,arg_options_mode):
        '''
        set all the options camera config
        :param arg_options_mode: class attribute having all the options
        :return: None
        '''
        for key, value in arg_options_mode.items():
            key = key.strip()
            if key in self.options_mode.keys():
                if key                                                == 'eac_split':
                    self.options_mode['eac_split']                    = arg_options_mode['eac_split']
                elif key                                              == 'flare':
                    self.options_mode['flare']                        = arg_options_mode['flare']
                elif key                                              == 'flare_art':
                    self.options_mode['flare_art']                    = arg_options_mode['flare_art']
                elif key                                              == 'flare_fake_time':
                    self.options_mode['flare_fake_time']              = arg_options_mode['flare_fake_time']
                elif key                                              == 'flare_art_front_corr':
                    self.options_mode['flare_art_front_corr']         = arg_options_mode['flare_art_front_corr']
                elif key                                              == 'flare_fake':
                    self.options_mode['flare_fake']                   = arg_options_mode['flare_fake']
                elif key                                              == 'bypass':
                    self.options_mode['bypass']                       = arg_options_mode['bypass']
                elif key                                              == 'lrv':
                    self.options_mode['lrv']                          = arg_options_mode['lrv']
                elif key                                              == 'stab':
                    self.options_mode['stab']                         = arg_options_mode['stab']
                elif key                                              == 'stab_degree':
                    self.options_mode['stab_degree']                  = arg_options_mode['stab_degree']
                elif key                                              == 'ring_high_res':
                    self.options_mode['ring_high_res']                 = arg_options_mode['ring_high_res']
                elif key                                              == 'exposure':
                    self.options_mode['exposure']                     = arg_options_mode['exposure']
                elif key                                              == 'debug_dump':
                    self.options_mode['debug_dump']                   = arg_options_mode['debug_dump']
                elif key                                              == 'debug_dump_opt':
                    self.options_mode['debug_dump_opt']               = arg_options_mode['debug_dump_opt']
                elif key                                              == 'raw_nbits':
                    self.options_mode['raw_nbits']                    = arg_options_mode['raw_nbits']
                elif key                                              == 'bayer_width':
                    self.options_mode['bayer_width']                  = arg_options_mode['bayer_width']
                elif key                                              == 'dump_raw':
                    self.options_mode['dump_raw']                     = arg_options_mode['dump_raw']
                elif key                                              == 'mpx':
                    self.options_mode['mpx']                          = arg_options_mode['mpx']
                elif key                                              == 'run_time':
                    self.options_mode['run_time']                     = arg_options_mode['run_time']
                elif key                                              == 'rear':
                    self.options_mode['rear']                         = arg_options_mode['rear']
                elif key                                              == 'spher_eis':
                    self.options_mode['spher_eis']                    = arg_options_mode['spher_eis']


                else :
                    raise Exception ('this mode {} is not known so it will not be handled in this test'.format(key))

    def set_environment(self,arg_dict):
        pass













#
# test_env =  TestEnvironment()
# test_env.download_target_dir = 'hell'