import json
import logging
import datetime

import humanize

from telegram import ParseMode, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler

from octoprint import OctoPrint


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
        try:
            octo = OctoPrint(printer['api_url'], printer['api_key'])
            conn = octo.connection()
            messages.append("*{0}* - {1}".format(printer['name'],
                                                 conn['current']['state']))
        except:
            pass

    for msg in messages:
        bot.sendMessage(update.message.chat_id, msg,
                        parse_mode=ParseMode.MARKDOWN)


def about(bot, update):
    messages = [
        "Hi! I'm the HackLab Toronto 3D Printers Bot!",
        "I was created by @MylesB.",
        "You can see my source code on [GitHub]("
        "https://github.com/myles/hacklab-octoprint-telegram-bot)."
    ]

    for msg in messages:
        bot.sendMessage(update.message.chat_id, msg,
                        parse_mode=ParseMode.MARKDOWN)


def status(bot, update):
    request = update.message.text.strip('/status ')

    if request == '':
        return start(bot, update)

    with open('config.json', 'r') as f:
        printers = json.loads(f.read()).get('printers', [])

    printer = next((i for i in printers if i["name"] == request), None)

    if not printer:
        return bot.sendMessage(update.message.chat_id,
                               "That printer doesn't exist.")

    octo = OctoPrint(printer['api_url'], printer['api_key'])
    job = octo.job()

    messages = [
        "The printers current state is *{state}*."
    ]

    if job['state'] == 'Printing':
        messages.append('Currently printing the file *{job[file][name]}*.')

        ext_print_time = job['job']['estimatedPrintTime']
        time_left = humanize.naturaltime(datetime.timedelta(seconds=ext_print_time))
        messages.append('Print will be completed in {0}'.format(time_left))

    for msg in messages:
        bot.sendMessage(update.message.chat_id, msg.format(**job),
                        parse_mode=ParseMode.MARKDOWN)


def main():
    with open('config.json', 'r') as f:
        config = json.loads(f.read())

    updater = Updater(config['telegram_api_key'])

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('about', about))
    updater.dispatcher.add_handler(CommandHandler('status', status))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
