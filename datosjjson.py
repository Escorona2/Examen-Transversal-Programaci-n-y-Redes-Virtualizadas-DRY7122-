from ncclient import manager

# Datos de conexión al router CSR1000V
host = '192.168.56.103'  # Remplaza con la IP del router CSR1000V
port = 830  # Puerto SSH
username = 'prueba3'  # Remplaza con tu nombre de usuario
password = 'cisco123'  # Remplaza con tu contraseña

# XML para crear la interfaz loopback  con la dirección IPv4 22.22.22.22/32
loopback_config = """
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
            <Loopback>
                <name>22</name>
                <ip>
                    <address>
                        <primary>
                            <address>22.22.22.22</address>
                            <mask>255.255.255.255</mask>
                        </primary>
                    </address>
                </ip>
            </Loopback>
        </interface>
    </native>
</config>
"""

# Conexión al router CSR1000v
with manager.connect(
    host=host,
    port=port,
    username=username,
    password=password,
    hostkey_verify=False,  # Desactivar la verificación del hostkey SSH
    device_params={'name': 'csr'}
) as m:
    # Enviar configuración XML para crear la interfaz loopback
    netconf_reply = m.edit_config(target='running', config=loopback_config)
    print("Interfaz loopback 22 creada exitosamente.")