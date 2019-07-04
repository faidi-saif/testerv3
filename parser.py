import re


class Parser(object):

    def __init__(self):
        pass


    def search_pattern(self,arg_string,arg_info):
        pass



    def get_string(self,arg_string,arg_pattern,arg_group):
        match = arg_pattern.search(arg_string)
        if match :
            return match.group(arg_group)
        else :
            return None






# l  = """--------------------
# Camera information :
# --------------------
#   `--> Compilation :
#       `--> Date : Jun 24 2019
#       `--> Time : 18:19:51
#       `--> git  : 0cab4a63c-dirty
#   `--> Firmware :
#       `--> version : HD7.01.01.49.92
#   `--> Board :
#       `--> Id   : 31955
#       `--> Name : Coconut PROTO2.0
#   `--> Device :
#       `--> Camera Serial Number    : C33513PRO21035
#       `--> Camera Part Number      :
#       `--> Camera Part Number Rev. :
#       `--> Board Serial Number     :
#       `--> Board Part Number       :
#       `--> Board Part Number Rev.  :
#       `--> Manufacturing Date      : 00-00-00
#       `--> Manufacturing Line      : 0
#       `--> Lens Lot Number         :
# --------------------"""
# p  = Parser()
# print(p.search_pattern(l,'sh1'))


# string =  ' saif faidi . / *-+ 8.0 fps'
# p = re.compile('(?:[0-9]*.[0-9]*|[0-9]*) (fps)')
# m = p.search(string)
# print(m.group())

#
# s= 'Duration: 00:01:00.31, start: 0.000000, '
# m2 = re.compile("Duration: (\d{2}:\d{2}:\d{2}.\d{2}),").search(s)
# print(m2.group(1))



# print(p.findall(string))