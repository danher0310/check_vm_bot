from telegram.ext import Application, CommandHandler, JobQueue
from datetime import time
import pytz
import os 
import logging
from dotenv import load_dotenv
import utils
load_dotenv()


token = os.getenv('tlgtoken')
# chat_ids = list(os.getenv('chats').split(','))
# for chatId in  chat_ids:
#   print(chatId)

def truncated_msg(text):
    if len(text) >= 4000:
        result = f"{text[:4000]}...\n \n"
        result += f"MESSAGE TRUNCATED DUE TO TELEGRAM MAX MESSAGE LENGTH"
        return result
    else:
        return text


async def start(update,context):
    """Gives a hearty salutation"""
    user = update.effective_user
    await update.message.reply_text(f"Greetings {user.username} !")
    
    
async def chatId(update,context):
    """Returns the chat id where the bot responds to"""
    chatId = update.message.chat.id
    await update.message.reply_text(chatId)
    
async def checking_vm(context):
  vm = utils.check_vm()
  if vm != None:
    chat_ids = list(os.getenv('chats').split(','))
    for chatId in  chat_ids:      
      await context.bot.send_message(       
        chat_id = chatId,
        text = vm
      )
    

def main():
    """Start the bot"""
    application = Application.builder().token(token).build()
    logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    application.add_handler(CommandHandler('chat_id', chatId))
    application.add_handler(CommandHandler('start', start))
    application.job_queue.run_repeating(checking_vm, interval=900, first = time(hour=6, minute=50, second=0, tzinfo=pytz.timezone('US/Eastern')), last= time(hour=17, minute=00, second=0, tzinfo=pytz.timezone('US/Eastern')))
    print('Bot started')
    application.run_polling()
    
if __name__ == "__main__":
  main()
