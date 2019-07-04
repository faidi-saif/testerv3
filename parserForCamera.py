from parser import Parser
import re

class ParserForCamera(Parser):

    def __init__(self):
        '''
        each pattern is made of a tuple ( pattern,group) where pattern is the string we look for and the group is the exact return value
        example: pattern : 'Name : Gopro proto 2.0' group = 'Gopro proto 2.0'
        '''
        super().__init__()
        self.sh1_pattern = re.compile(r'git\s+:\s+(.*)'), 1
        self.cam_sn_pattern = re.compile(r'Camera Serial Number\s+:\s+(.*)'), 1
        self.cam_id_pattern = re.compile(r'Id\s+:\s+(.*)'), 1
        self.frw_ver_pattern = re.compile(r'version\s+:\s+(.*)'), 1
        self.cam_name = re.compile(r'Name\s+:\s+(.*)'), 1
        self.compile_date = re.compile(r'Date\s+:\s+(.*)'), 1


    def search_pattern(self,arg_string,arg_info):
        '''
        :param arg_string   :the input string where to search for info
        :param arg_info     :information looking for
        :return: the out str=ing if fund , else None
        '''
        assert (   arg_info == 'sh1'
                or arg_info == 'cam_sn'
                or arg_info == 'cam_id'
                or arg_info == 'cam_name'
                or arg_info == 'compile_date'
                or arg_info == 'frw_version') \
        ,'invalid information to search for , add implementation for : {} in {}'.format(arg_info,__class__.__name__)
        if  arg_info == 'cam_sn':
            pattern, group = self.cam_sn_pattern
        elif arg_info == 'cam_id':
            pattern, group = self.cam_id_pattern
        elif arg_info == 'frw_version':
            pattern, group = self.frw_ver_pattern
        elif arg_info == 'compile_date':
            pattern, group = self.compile_date
        elif arg_info == 'cam_name':
            pattern, group = self.cam_name
        else:  # arg_info == 'sh1':
            pattern, group = self.sh1_pattern
        match_string = self.get_string(arg_string, pattern, group)
        return match_string

