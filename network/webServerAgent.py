import wget
import requests
from bs4 import BeautifulSoup



class WebServerAgent:

    class fetcher :
        def __init__(self):
            pass

        def list_content(self,url,ext=''):
            '''
            :param url: path to the directory
            :param ext: file esxtension , in this case ='' , means all the files
            :return: names of the files in the input directory
            '''
            page = requests.get(url).text
            soup = BeautifulSoup(page, 'html.parser')
            return [url + '/' + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]





    def __init__(self):
        self.fetcher = self.fetcher()


    def list_content(self,url,ext=''):
         '''
         :param url:  path to the directory
         :param ext: ext :file extension
         :return: the list of files in the "url" directory
         '''
         l_url = self.check_path_format(url)
         list_files =  self.fetcher.list_content(l_url,ext)
         for file in list_files:
             if file.endswith("/../"): # remove the .. directory
                 list_files.remove(file)
         return list_files


    # ------------------------------download(path to the remote file ,target directory)--------------------------------------------------------
    def check_path_format(self,arg_url):
        '''
        :param arg_url: input path , example : 192.168.0.202:8042/DCIM/100GOPRO
        :return: complete path https://192.168.0.202:8042/DCIM/100GOPRO
        '''
        if arg_url.find('http') == -1:
            arg_url = 'http://'+arg_url
        else:
            pass
        return arg_url

    # ------------------------------download(path to the remote file ,target directory)--------------------------------------------------------
    def download(self,arg_url,arg_output_directory):
        '''

        :param arg_url: url of the source directory
        :param arg_output_directory: path to the directory where to save the files
        :return: None
        '''
        url = self.check_path_format(arg_url)
        # no need to check for path existence , already handled by urllib
        file = wget.download(url,out = arg_output_directory)
        print('download file ------>', file) #~/Desktop/test_logs/S0/photos/GS010263.LRV




#wb = WebServerAgent()
# print(wb.list_content('192.168.0.202:8042/DCIM/100GOPRO'))
# wb.download('192.168.0.202:8042/DCIM/100GOPRO/GS010272.LRV','/home/saif/Desktop')
# print(wb.list_content('192.168.0.202:8042/DCIM/100GOPRO'))
# print(wb.list_content('192.168.0.202:8042/DCIM/100GOPRO'))
# print(wb.list_content('192.168.0.202:8042/DCIM/100GOPRO'))

#wb.download('192.168.0.202:8042/DCIM/100GOPRO/GS__0269.JPG','/home/saif/Desktop/')
