import sys
import json
import logging

from telegram.ext import Updater, CommandHandler

from octoprint import OctoPrint

sys.path.append('./future-0.15.2/src/')

logging.basicConfig(filename='bot.log', format='%(asctime)s %(message)s',
                    level=logging.DEBUG)


def start(bot, update):
    with open('config.json', 'r') as f:
        printers = json.loads(f.read()).get('printers', [])

    messages = [
        "Hi! I'm the 3D Printer Bot for HackLab Toronto.",
        "I'm aware of {0} printers at the HackLab.".format(len(printers)),
        "Below is their current state:"
    ]

    for printer in printers:
        octo = OctoPrint(printer['api_url'], printer['api_key'])
        state = octo.connection['current']['state']
        messages.append("{0} - {1}".format(printer['name'], state))

    for msg in messages:
        bot.sendMessage(update.message.chat_id, msg)


def main():
    with open('config.json', 'r') as f:
        config = json.loads(f.read())

    updater = Updater(config['telegram_api_key'])

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('hello', start))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
