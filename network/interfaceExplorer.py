import netifaces

# ------------------------------------------------ class to discover exixting network inerfaces  --------------------------------------------------------
class InterfaceExplorer:
    def __init__(self):
        pass

    # ------------------------------------------------ exploring all network interfaces --------------------------------------------------------

    def explore(self,arg_type = 'all' ):
        '''
        :param arg_type: 'all' for all the information and 'filtered' only for needed information
        :return: network_table providing all the information about the network interfaces
        '''
        network_table = []
        interfaces = (netifaces.interfaces())
        for inter in interfaces :
            try:
                interface =netifaces.ifaddresses( inter )
            except ValueError as e :
                print('interface name: {} and error : {}'.format(inter,e))
            if arg_type == 'filtered':
                if 2 in interface.keys():
                    # the second field of the dictionnary contains the ip adress and the netmask
                    interface_info = interface[2][0]
                    # add the name of the interface
                    interface_info.update({'name':inter})
                    # create a table f network interfaces
                    network_table.append(interface_info)
            elif arg_type == 'all':# all interfaces
                interface.update({'name':inter})
                network_table.append(interface)
        return network_table



    # ------------------------------------------------ display the table of the network interfaces --------------------------------------------------------
    def display(self,arg_table):
        '''
        :param arg_table: display the network table
        :return: None
        '''
        for el in arg_table:
            print (el)

    # ------------------------------------------------ check if an interface exist based on it's ip adress --------------------------------------------------------
    def find_by_ip(self,arg_ip):
        '''
        :param arg_ip: ip adress to look for
        :return:
        '''
        wireless_interfaces = self.explore('filtered')
        exist = False
        for field in wireless_interfaces:
            if field ['addr'] == arg_ip:
                exist = True
                return exist
        if exist == False:
            return exist






#m_networkexp = InterfaceExplorer()
#table = m_networkexp.explore('all')
# interface  = m_networkexp.find_by_ip('192.168.0.1')
# print(interface)
#m_networkexp.display(table)
# ------------------------------------------------  --------------------------------------------------------