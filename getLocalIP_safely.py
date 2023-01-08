#import socket

#X = socket.gethostname()

#Y = socket.gethostbyname(socket.gethostname())

#socket.gethostbyname(socket.gethostname())

def get_interfaces_with_mac_addresses(interface_name_substring=''):
    import subprocess
    import xml.etree.ElementTree

    cmd = 'wmic.exe nic'
    if interface_name_substring:
        cmd += ' where "name like \'%%%s%%\'" ' % interface_name_substring
    cmd += ' get /format:rawxml'

    DETACHED_PROCESS = 8
    xml_text = subprocess.check_output(cmd, creationflags=DETACHED_PROCESS)

    # convert xml text to xml structure
    xml_root = xml.etree.ElementTree.fromstring(xml_text)

    xml_types = dict(
        datetime=str,
        boolean=lambda x: x[0].upper() == 'T',
        uint16=int,
        uint32=int,
        uint64=int,
        string=str,
    )

    def xml_to_dict(xml_node):
        """ Convert the xml returned from wmic to a dict """
        dict_ = {}
        for child in xml_node:
            name = child.attrib['NAME']
            xml_type = xml_types[child.attrib['TYPE']]

            if child.tag == 'PROPERTY':
                if len(child):
                    for value in child:
                        dict_[name] = xml_type(value.text)
            elif child.tag == 'PROPERTY.ARRAY':
                if len(child):
                    assert False, "This case is not dealt with"
            else:
                assert False, "This case is not dealt with"

        return dict_

    # convert the xml into a list of dict for each interface
    interfaces = [xml_to_dict(x)
                  for x in xml_root.findall("./RESULTS/CIM/INSTANCE")]

    # get only the interfaces which have a mac address
    interfaces_with_mac = [
        intf for intf in interfaces if intf.get('MACAddress')]

    for item in interfaces_with_mac:
        print ('CreationClassName:' + item['CreationClassName'] )
        print ('AdapterType:' + item['AdapterType'] )
        print ('DeviceID:' + item['DeviceID'] )

        print('--------------')
    return interfaces_with_mac


#{'AdapterType': 'Ethernet 802.3', 'AdapterTypeId': 0, 'Availability': 3,
# 'Caption': '[00000016] VMware Virtual Ethernet Adapter for VMnet8', 
# 'ConfigManagerErrorCode': 0, 'ConfigManagerUserConfig': False, 'CreationClassName':
#  'Win32_NetworkAdapter', 'Description': 'VMware Virtual Ethernet Adapter for VMnet8', 'DeviceID': '16', 'GUID': '{35C07FCF-3862-43EB-86DC-BC1ACDD1BB3C}', 'Index': 16, 'Installed': True, 
#'InterfaceIndex': 6, 'MACAddress': '00:50:56:C0:00:08', ...}

get_interfaces_with_mac_addresses('')

