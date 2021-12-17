from datetime import datetime
from telegram.ext.filters import Filters
from telegram.ext.messagehandler import MessageHandler
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext import Updater, dispatcher
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.conversationhandler import ConversationHandler
import logging
import requests
from getmac import get_mac_address
import json
import emoji

API_TOKEN="2120040735:AAE0lmvNzEr1MiizjPsdcxwwl7y3K2jc1-E"

def start(update:Update,context:CallbackContext):
    logging.info("Command START")
    context.bot.send_message(chat_id=update.effective_chat.id,text="Welcome To Botto!!!")

#ip 46.105.235.75:3000
#richieste set e get
# {'mac':'', 'red':0, 'green':0, 'blue':0}

def getJson(led, state):
    
    if 'red' in led:
        data={'mac': get_mac_address(), 'red':state}
    if 'green' in led:
        data={'mac': get_mac_address(), 'green':state}
    if 'blue' in led:
        data={"mac": get_mac_address(), 'blue':state}
    if 'all' in led:
        data={"mac": get_mac_address(), 'red':state, 'green':state, 'blue':state}
    
    #data['mac']=get_mac_address()

    return data

def getStatus(update:Update,context:CallbackContext):
    logging.info("Command Get Led State")

    statusLed=requests.get(f"http://46.105.235.75:3000/api/get/{get_mac_address()}")
    json=statusLed.json()
    context.bot.send_message(chat_id=update.effective_chat.id,text=f"{emoji.emojize(':red_circle:', use_aliases=True) if json['red']==True else emoji.emojize(':black_circle:', use_aliases=True)}  RED\n{emoji.emojize(':green_circle:', use_aliases=True) if json['green']==True else emoji.emojize(':black_circle:', use_aliases=True)}  GREEN\n{emoji.emojize(':blue_circle:', use_aliases=True) if json['blue']==True else emoji.emojize(':black_circle:', use_aliases=True)}  BLUE\n\n{emoji.emojize(':computer:', use_aliases=True)}  {json['mac']}")

def led(update:Update,context:CallbackContext):
    logging.info("Command Change Led State")
    
    changeStatus=update.effective_message.text
    if 'on' in changeStatus or 'off' in changeStatus:
        if 'on' in changeStatus: state=True
        elif 'off' in changeStatus: state=False
        else: 
            state=''
        
        if state==True or state==False:
            data=getJson(changeStatus, state)
            #print(data)
            requests.post('http://46.105.235.75:3000/api/set/', json.dumps(data), headers={'content-type':'application/json'})
            
        getStatus(update,context)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,text="Opzioni:\n  /{comando} on\n  /{comando} off")

    


def calcel(update:Update,context:CallbackContext):
    update.message.reply_text("Operation Aborted!")
    return ConversationHandler.END

def unknown(update:Update,context:CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,text="Non ho capito slavo.")

def startBOT():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO,
        handlers=[
            logging.FileHandler('logs/log_{:%Y_%m_%d}.log'.format(datetime.now())),
            logging.StreamHandler()
        ]
    )
    
    logger=logging.getLogger(__name__)
    logging.info("BotServer started!")
    #DEFINE UPDATER
    updater=Updater(token=API_TOKEN)
    #DEFINE DISPATCHER
    dispatcher=updater.dispatcher
    
    #DEFINE HANDLER
    start_handler=CommandHandler('start',start)
    dispatcher.add_handler(start_handler)
    
    led_handler=CommandHandler(['red','green','blue','all'], led)
    dispatcher.add_handler(led_handler)
    
    status_handler=CommandHandler('getStatus',getStatus)
    dispatcher.add_handler(status_handler)


    unknown_handler=MessageHandler(Filters.command,unknown)
    dispatcher.add_handler(unknown_handler)
    
    #POLLING
    updater.start_polling()
    
    #SIGTERM
    updater.idle()
    

if __name__=="__main__":
    startBOT()
    



