import paramiko
import os 
from dotenv import load_dotenv

load_dotenv()

host = os.getenv('host')
port = os.getenv('port')
user = os.getenv('usernameh')
password = os.getenv('password')


transport = paramiko.Transport((os.getenv('host'),int(os.getenv('port'))))


transport.connect(username=os.getenv('usernameh'), password=os.getenv('password'))
sftp = paramiko.SFTPClient.from_transport(transport)

test = sftp.listdir('/var/spool/asterisk/voicemail/default/7599/INBOX')

sftp.close()
transport.close()

print(test)