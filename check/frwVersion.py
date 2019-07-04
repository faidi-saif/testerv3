

from check.checker import Checker


 # ----------------------------------------------FrwVersion checker ------------------------------------------
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

