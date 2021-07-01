from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import NetMikoAuthenticationException
from paramiko.ssh_exception import SSHException
import time
import datetime
import schedule
import os
def job():
    TNOW = datetime.datetime.now().replace(microsecond=0)
    IP_LIST = {'juniper_junos':'10.81.1.11','juniper_junos':'10.81.1.40'}
    # DEVICE_LIST =['CSW_cll','CSW_18']
    i = 0
    for DEVICE,IP in IP_LIST.items():
        print ('\n  '+DEVICE.strip()+'-'+IP.strip() + '  \n' )
        RTR = {
        'ip':   IP,
        'port': 60022,
        'username': 'serverprueba',
        'password': 'JWwFiUtHtA*U',
        'device_type': DEVICE,
        }

        try:
            net_connect = ConnectHandler(**RTR, global_delay_factor=2)
        except NetMikoTimeoutException:
            print ('Device not reachable.')
            continue
        except AuthenticationException:
            print ('Authentication Failure.') 
            continue
        except SSHException:
            print ('Make sure SSH is enabled in device.')
            continue

        if not os.path.exists("/home/dedicados/Desktop/backup_configurations"):
            os.makedirs("/home/dedicados/Desktop/backup_configurations")
        if not os.path.exists("/home/dedicados/Desktop/backup_configurations/"+DEVICE):
            os.makedirs("/home/dedicados/Desktop/backup_configurations/"+DEVICE)
        output = net_connect.send_command('show configuration')
        
        SAVE_FILE = open("/home/dedicados/Desktop/backup_configurations/"+DEVICE+'/'+DEVICE+'_'+IP +'_'+ str(TNOW), 'w')
        SAVE_FILE.write(output)
        SAVE_FILE.close
        print ('Finished config backup')
        i+=1
schedule.every().minute.at(":00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
