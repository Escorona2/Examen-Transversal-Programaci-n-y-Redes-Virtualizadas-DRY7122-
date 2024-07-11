from ncclient import manager
import xmltodict
import json

# Datos de conexión al router CSR1000V
host = '192.168.56.103'  # Reemplaza con la IP del router CSR1000V
port = 830  # Puerto NETCONF
username = 'prueba3'  # Reemplaza con tu nombre de usuario
password = 'cisco123'  # Reemplaza con tu contraseña

# Conexión al router CSR1000V
with manager.connect(
    host=host,
    port=port,
    username=username,
    password=password,
    hostkey_verify=False,  # Desactivar la verificación del hostkey SSH
    device_params={'name': 'csr'}
) as m:
    # Obtener la configuración de las interfaces
    netconf_reply = m.get_config(source='running', filter=('subtree', '<interfaces xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native"/>')).data_xml
    
    # Convertir XML a dict
    interfaces_dict = xmltodict.parse(netconf_reply)
    
    # Convertir dict a JSON
    interfaces_json = json.dumps(interfaces_dict, indent=4)
    
    # Imprimir el JSON
    print(interfaces_json)