
from check.checker import Checker

import os

# ----------------------------------------------FileStat checker ------------------------------------------

class FileStat(Checker):

    def __init__(self):
        super().__init__()


    def extract_properties(self,arg_file_path,arg_file):
        file_path   = arg_file_path + '/' + arg_file
        file        = arg_file.split('.')
        name        = file[0]
        type        = file[1]
        ret         = os.stat(file_path)
        size        = str(ret.st_size/1000) + 'KB'
        return {'name' : name, 'type':type ,'size':size}


    def check(self,*args ):
        files_properties = []
        result           = False
        path             = args[0]
        assert (path is not None), " No directory for check passed "
        files            = os.listdir(path)
        files_number     = len(files)
        if files  != [] :
            for file in files:
                file_prop = self.extract_properties(path,file)
                files_properties.append(file_prop)
                if file_prop['size'] !=  '0.0KB':
                    result  = True
                else:
                    print('file "{}" is  null'.format(file))
                    pass
        else :
            result = False

        return {'result':result,'number of files':files_number,'files' : files_properties}

