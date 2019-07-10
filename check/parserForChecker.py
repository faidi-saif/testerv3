from parser import Parser
import re

class ParserForChecker(Parser):


    def __init__(self):
        '''
        each pattern is made of a tuple ( pattern,group) where pattern is the string we look for and the group is the exact return value
        example : pattern to find fps is '23.98 fps' the exact value is '23.98'
        '''
        Parser.__init__(self)
        self.duration_pattern   = re.compile("Duration: (\d{2}:\d{2}:\d{2}.\d{2}),"),1
        self.frame_rate_pattern = re.compile('((?:[0-9]*.[0-9]*|[0-9]*)) fps'),1
        self.bit_rate_pattern   = re.compile(r'bitrate:\s+(\d+)\s+kb/s'),1
        self.resol_pattern      = re.compile(r',\s+(\d+x\d+)'),1
        #self.encode_format      = re.compile(r'\s+(.*)\s+\(\w'),1
        self.color_format       = re.compile(r'\s+(.*)\('),1
        self.video_pattern      = re.compile('Video:(.*)\n'),1
        self.errors             = re.compile('Library closed with (\d+)'),1
        self.skipped_frames     = re.compile('errors and (\d+) skipped frames'),1






    def search_pattern(self,arg_string,arg_info):
        '''
        :param arg_string   :the input string where to search for info
        :param arg_info     :information looking for
        :return: the out str=ing if fund , else None
        '''
        assert(   arg_info  == 'video_duration'
               or arg_info == 'frame_rate'
               or arg_info == 'bit_rate'
               or arg_info == 'encode_format'
               or arg_info == 'color_format'
               or arg_info == 'resolution'
               or arg_info == 'skipped_frames'
               or arg_info == 'errors'
               or arg_info == 'video_pattern')\
            ,'invalid information to search for , add implementation for : {} in {}'.format(arg_info,__class__.__name__)
        if arg_info  == 'video_duration':
            pattern,group = self.duration_pattern
        elif arg_info == 'bit_rate':
            pattern,group = self.bit_rate_pattern
        elif arg_info == 'resolution':
            pattern,group = self.resol_pattern
        elif arg_info =='encode_format':
            return arg_string.strip().split(' ')[0]
        elif arg_info == 'color_format':
            pattern,group = self.color_format
        elif arg_info == 'video_pattern':
            pattern,group = self.video_pattern
        elif arg_info =='skipped_frames':
            pattern,group = self.skipped_frames
        elif arg_info == 'errors':
            pattern,group = self.errors
        else : # frame rate (fps)
            pattern, group = self.frame_rate_pattern

        match_string  = self.get_string(arg_string,pattern,group)
        #print(match_string)
        return match_string


# p = ParserForChecker()
# ret = p.search_pattern('*** Library closed with 1 errors and 5 skipped frames *** ','errors')
# print (ret)