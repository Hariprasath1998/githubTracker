import telegram.ext
import json

API_KEY = open('.botToken').readline()


def help(update, context):
    reply = update.message.reply_text
    firstName = update.message.chat.first_name
    reply(f"Hello {firstName} ")
    reply("Send /subscribe to get alerts for repo commits")
    reply("Send /unsubscribe to stop receiving alerts")
    print('Update')
    print(update)


def subscribe(update, context):
    firstName = update.message.chat.first_name
    chat_id = update.message.chat_id
    reply = update.message.reply_text
    subscriberList = open('subscribers.txt').read().strip().split('\n')
    if str(chat_id) not in subscriberList:
        with open('subscribers.txt', 'w+') as file:
            subscriberList.append(chat_id)
            for subscriber in subscriberList:
                file.write(str(subscriber) + '\n')
        print(f'{firstName} with chat ID {chat_id} has subscribed')
        reply('You will be receiving commit alerts from now!')
    else:
            print('You have already Subscribed!')
            reply('You have already Subscribed!')

    
        
    
    # context.bot.sendMessage(chat_id, 'subscribed!')

def unsubscribe(update, context):
    firstName = update.message.chat.first_name
    chat_id = update.message.chat_id
    reply = update.message.reply_text
    subscriberList = open('subscribers.txt').read().strip().split('\n')
    if str(chat_id) in subscriberList:
        with open('subscribers.txt', 'w+') as file:
            subscriberList.remove(str(chat_id))
            for subscriber in subscriberList:
                file.write(str(subscriber) + '\n')
        print(f'{firstName} with chat ID {chat_id} has unsubscribed')
        reply('You will no longer receive commit alerts')
    else:
            print('You have not Subscribed!')
            reply('You have not Subscribed!')


updater = telegram.ext.Updater(API_KEY)
add_handler = updater.dispatcher.add_handler

add_handler(telegram.ext.CommandHandler("start", help))
add_handler(telegram.ext.CommandHandler("help", help))
add_handler(telegram.ext.CommandHandler("subscribe", subscribe))
add_handler(telegram.ext.CommandHandler("unsubscribe", unsubscribe))

sendMessage = updater.bot.send_message

updater.start_polling()