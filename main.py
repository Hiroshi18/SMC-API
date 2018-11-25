from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import get_notification
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
list_user_cups = []
notification = get_notification.get_notification()

def start(bot, update, job_queue):
    """Send a message when the command /start is issued."""
    user_cups = {
        "username" : update.message['chat']['username'],
		"chat_id" : update.message.chat_id
	}
    list_user_cups.append(user_cups)
    print(list_user_cups)
    job = job_queue.run_repeating(alarm, 5)
    update.message.reply_text('Hello! Now you will receive updates for your cup.')

def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Make sure that your username is allowed to received messages on the site.')

def alarm(bot, job):
    """Send the alarm message."""
    global notification
    new = get_notification.get_notification()
    if (notification == new):
        pass
    else:
        notification = get_notification.get_notification()
        for user in list_user_cups:
            print(user['username'])
            for aux in notification['objects']:
                if(aux['id'] == user['username']):
                    bot.send_message(user['chat_id'], text=notification)

def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("687648766:AAHyFpxtXdiJQaxYMitS0ekB6lBA-pYZzfI")
    
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start, pass_job_queue=True))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    #dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)
    # Start the Bot
    updater.start_polling()
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()