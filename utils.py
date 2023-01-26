import paramiko
import os 
from dotenv import load_dotenv
import mysql.connector
from pathlib import Path

load_dotenv()

# def connectDb():
#   try:
#     mydb = mysql.connector.connect(
#       host = os.getenv('dbhost'),
#       user = os.getenv('userdb'),
#       password ='',
#       database = os.getenv('dbname'),
#       auth_plugin = "mysql_native_password"
#     )
#     return mydb
#   except OSError:
#     return OSError


def searchs_vm():
  transport = paramiko.Transport((os.getenv('host'),int(os.getenv('port'))))
  transport.connect(username=os.getenv('usernameh'), password=os.getenv('password'))
  sftp = paramiko.SFTPClient.from_transport(transport)
  vmlist = sftp.listdir('/var/spool/asterisk/voicemail/default/7599/INBOX')
  sftp.close()
  transport.close()
  return vmlist



def is_audio(msj):
  return msj if msj.endswith('.wav') else False

# def not_in_the_list(x,list):
#   return x not in list

# def check_database(vmlist):
#   mydb = connectDb()
#   myCursor = mydb.cursor()
#   myCursor.execute("SELECT filename from voice_mail ;")
#   vmsaved = [ x[0] for x in myCursor.fetchall()]
#   vmnews = list(filter(lambda x: not_in_the_list(x,vmsaved), vmlist))
#   for newvm in vmnews:
#     querySQL = "INSERT INTO voice_mail (filename, dateregister) VALUES (%s, current_date());"
#     myCursor.execute(querySQL, (newvm,))
#     mydb.commit()
#   return len(vmnews)
    
     

def check_vm():
  vmlist = searchs_vm()
  print(vmlist)
  vmlist = list(filter(is_audio,vmlist))
  if len(vmlist) != 0:
    msj = f"URGENT: Hi team we have {len(vmlist)} new message(s).\nPlease review them as soon as possible."
    return msj
  else:
    return None
 



