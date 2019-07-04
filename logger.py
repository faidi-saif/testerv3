import os
import shutil
import json

class Logger:

    def __init__(self):
        pass

    #---------------------------------------------- ------------------------------------------
    def open(self,arg_file):
        file = open(arg_file,"w+")
        return file

    # ---------------------------------------------- ------------------------------------------
    def write(self,arg_file,arg_data):
        file = self.open(arg_file)
        file.write(arg_data)
        self.close(file)

    # ---------------------------------------------- ------------------------------------------
    def close(self,arg_file):
       arg_file.close()

    # ---------------------------------------------- ------------------------------------------
    def __del__(self):
        pass

    # ---------------------------------------- remove all files in a given path -----------------------------------------------

    def clean_dir(self,arg_path):
        for the_file in os.listdir(arg_path):
            file_path = os.path.join(arg_path, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)

    # ----------------------------------- check if a given directory exists else create it ------------------------------------

    def create_dir(self,arg_path):
        _path = self.check_format(arg_path) # get the equivalent to ~/ in path
        if os.path.isdir(_path):
            pass
        else:
            os.makedirs(_path)
        return _path

    # -------------------------------------------copy files in a given path (clean before ) -----------------------
    def copy_files(self,from_path, to_path):
        if os.path.exists(to_path):
            shutil.rmtree(to_path)
        shutil.copytree(from_path, to_path)

    # ---------------------------------------------- load_json ------------------------------------------
    def load_json(self , arg_file):
        '''
        :param arg_file: json input file
        :return:  dictionary from json file
        '''
        path = self.check_format(arg_file)
        with open(path ,'r') as f :
            sceanrio = json.load(f)
            return sceanrio

    # ---------------------------------------------- write_json ------------------------------------------
    def write_json(self,arg_path,arg_data):
        '''

        :param arg_path: ~/Desktop/results/scenario1.json
        :param arg_data:  dictionary to write in the scenario1.json file
        :return: None
        '''
        file_name  = self.get_file_name_from_path(arg_path) #scenario1.json
        path_name  = self.get_parent_path(arg_path) #~/Desktop/results
        path       = self.create_dir(path_name) #creates the directory if it dosen't exist
        result_path = path + '/' + file_name # recreate the path : /home/saif/Desktop/results/scenario1.json
        # print('result_path : ',result_path)
        # print('path  : ' ,path)
        with open(result_path, 'w') as outfile:
            json.dump(arg_data, outfile,indent=4)


    # ---------------------------------------------- check_format ------------------------------------------
    def check_format(self,arg_path):
        '''
        convert ~ into home directory and remove white spaces
        :param arg_path:
        :return:
        '''
        path = arg_path.strip()
        if arg_path[0] == '~':
            path = os.environ['HOME'] + arg_path[1:]
        return path


    # ---------------------------------------------- get_parent_path ------------------------------------------
    def get_parent_path(self,arg_path):
        arg_path = '/'.join(arg_path.split('/')[:-1])
        return arg_path

    # ---------------------------------------------- get_file_name_from_path ------------------------------------------
    def get_file_name_from_path(self,arg_path):
        if '.' in arg_path :# then it's a file
            return os.path.basename(arg_path)

    # ---------------------------------------------------write_2d_list ------------------------------------------------
    def write_2d_list(self,arg_path,file_name,arg_list):
        path = self.create_dir(arg_path)
        path = path + '/' + file_name
        s = [[str(e) for e in row] for row in arg_list]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        #print('\n'.join(table))
        with open(path, 'w') as f:
            for item in table:
                f.write("%s\n" % '')
                for el in item:
                    f.write("%s" % el)

# l.clean_dir('/home/saif/Desktop/test_logs/S0')

# import os
# path_str = "/var/www/index.html"
# path = os.path.join('/saif/faidi',path_str)
# print(path)
# print(os.path.abspath(os.path.join(path_str, os.pardir)))
# print(os.path.basename(path_str))