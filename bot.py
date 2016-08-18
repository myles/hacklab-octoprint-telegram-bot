import json
import logging
import datetime

import humanize

from telegram import ParseMode, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler

from octoprint import OctoPrint


logging.basicConfig(filename='bot.log', format='%(asctime)s %(message)s',
                    level=logging.DEBUG)


class HackLabTOPrintersBot(object):

    def __init__(self):
        with open('config.json', 'r') as config_file:
            config = json.loads(config_file.read())

        self.telegram_api_key = config['telegram_api_key']
        self.printers = config['printers']
        
        kb_status = []

        for printer in self.printers:
            kb_status.append(KeyboardButton('/status {name}'.format(**printer)))

        self.keyboard = [kb_status, [KeyboardButton('/status'),
                                     KeyboardButton('/about')]]

    def get_printer(name):
        return next((i for i in self.printers if i["name"] == name), None)

    def start(self, bot, update):
        len_printers = len(self.printers)
        
        messages = [
            "Hi! I'm the 3D Printer Bot for HackLab Toronto.",
            "I'm aware of {0} printers at the HackLab.".format(len_printers),
            "Below is their current state:"
        ]

        for printer in self.printers:
            try:
                octo = OctoPrint(printer['api_url'], printer['api_key'])
                conn = octo.connection()
                messages.append("*{0}* - {1}".format(printer['name'],
                                                     conn['current']['state']))
            except:
                messages.append("*{0}* - Offline".format(printer['name']))

        for msg in messages:
            bot.sendMessage(update.message.chat_id, msg,
                            parse_mode=ParseMode.MARKDOWN,
                            reply_markup=self.keyboard)

    def about(self, bot, update):
        messages = [
            "Hi! I'm the HackLab Toronto 3D Printers Bot!",
            "I was created by @MylesB.",
            "You can see my source code on [GitHub]("
            "https://github.com/myles/hacklab-octoprint-telegram-bot)."
        ]

        for msg in messages:
            bot.sendMessage(update.message.chat_id, msg,
                            parse_mode=ParseMode.MARKDOWN,
                            reply_markup=self.keyboard)

    def status(self, bot, update):
        request = update.message.text.strip('/status ')

        if request == '':
            return start(bot, update)

        printer = get_printer(request)

        if not printer:
            return bot.sendMessage(update.message.chat_id,
                                   "That printer doesn't exist.",
                                   reply_markup=self.keyboard)

        octo = OctoPrint(printer['api_url'], printer['api_key'])
        job = octo.job()

        messages = [
            "The printers current state is *{state}*."
        ]

        if job['state'] == 'Printing':
            messages.append('Currently printing the file *{job[file][name]}*.')
            messages.append("Print will be completed in "
                            "{job[estimatedPrintTime]} seconds.")

        for msg in messages:
            bot.sendMessage(update.message.chat_id, msg.format(**job),
                            parse_mode=ParseMode.MARKDOWN,
                            reply_markup=self.keyboard)

    def main(self):
        updater = Updater(self.telegram_api_key)

        updater.dispatcher.add_handler(CommandHandler('start', self.start))
        updater.dispatcher.add_handler(CommandHandler('about', self.about))
        updater.dispatcher.add_handler(CommandHandler('status', self.status))

        updater.start_polling()
        updater.idle()


if __name__ == "__main__":
    bot = HackLabTOPrintersBot()
    bot.main()
