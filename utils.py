import paramiko
import os 
from dotenv import load_dotenv
import mysql.connector
from pathlib import Path

load_dotenv()



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



def check_vm():
  vmlist = searchs_vm()
  print(vmlist)
  vmlist = list(filter(is_audio,vmlist))
  
  if len(vmlist) > 0:  
    msj = check_database(len(vmlist))    
    return msj if msj!= None else None
  
  else: 
    refreshDb()

 


def connectDb():
  try:
    mydb = mysql.connector.connect(
      host = os.getenv('dbhost'),
      user = os.getenv('userdb'),
      password ='',
      database = os.getenv('dbname'),
      auth_plugin = "mysql_native_password"
    )
    return mydb
  except OSError:
    return OSError


    
def refreshDb():
  mydb = connectDb()
  myCursor = mydb.cursor()
  myCursor.execute("TRUNCATE voice_mail;")
  mydb.close()
  
   
 


def not_in_the_list(x,list):
  return x not in list

def check_database(lenvm):
  mydb = connectDb()  
  myCursor = mydb.cursor()
  myCursor.execute("SELECT TIMESTAMPDIFF(hour, dateregister, current_timestamp())  as timediff from voice_mail where numberVm = %s  and (TIMESTAMPDIFF(hour, dateregister, current_timestamp()) >= 1 or  TIMESTAMPDIFF(hour, dateregister, current_timestamp()) <= 1) and TIMESTAMPDIFF(day, dateregister, current_timestamp()) <1   order by timediff ASC ;",(lenvm,))
  result = myCursor.fetchone()    
  if result == None:
      scriptSQL = ("INSERT INTO voice_mail (numberVm) VALUES (%s) ")
      value = lenvm
      myCursor.execute(scriptSQL, (value,))
      mydb.commit()
      return f"URGENT: Hi team we have {lenvm} new message(s).\nPlease review them as soon as possible."   
  else:
    for x in result:
      if str(x) != '0':
        return f"URGENT: Hi team we have {lenvm} new message(s), it has {x} hour in the voicemail.\nPlease review them as soon as possible."
      else:
        return None
  mydb.close()
    
   
  
    
  
      
    

    
  
  
  
  
