import requests
from keys import token, yandex, key, menu
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

# Функция обработчик команд
def command(bot, update):
	bot.send_message(
		chat_id = update.message.chat_id,
		text = 'Бот активирован 🤖\n Будут вопросы жми 🆘🤯⁉️',
		reply_markup = keyboard_help()
		)

def help_command(bot, update):
	bot.send_message(
		chat_id = update.message.chat_id,
		text = menu
		)

# Функция обработчки текста
def txt(bot, update):
	text = update.message.text
	bot.send_message(
		chat_id = update.message.chat_id,
		text = text,
		reply_markup = lang()
		)

# Кнопка помощи, которая будет активна постоянная и находиться под полем ввода текста
def keyboard_help():
	keyboard = [[KeyboardButton('/🆘🤯⁉️')]]
	return ReplyKeyboardMarkup(
		keyboard = keyboard,
		resize_keyboard = True
		)

# Инлайн кнопки, кнопки работающие с текстом, принимающие запрос от пользователя на перевод
# первый ряд
def lang():
	keyboard = [[InlineKeyboardButton('🏴󠁧󠁢󠁥󠁮󠁧󠁿', callback_data = 'ru-en'),
				InlineKeyboardButton('🇩🇪', callback_data = 'ru-de'),
				InlineKeyboardButton('🇮🇹', callback_data = 'ru-it')],

				[InlineKeyboardButton('🇪🇸', callback_data = 'ru-es'),
				InlineKeyboardButton('🇫🇷', callback_data = 'ru-fr'),
				InlineKeyboardButton('🇵🇱', callback_data = 'ru-pl')],

				[InlineKeyboardButton('➕', callback_data = 'next')]
	]
	return InlineKeyboardMarkup(keyboard)

# Второй ряд
def lang_two():
	keyboard = [[InlineKeyboardButton('🇵🇹', callback_data = 'ru-pt'),
				InlineKeyboardButton('🇷🇸', callback_data = 'ru-sr'),
				InlineKeyboardButton('🇨🇿', callback_data = 'ru-cs')],

				[InlineKeyboardButton('🇨🇳', callback_data = 'ru-zh'),
				InlineKeyboardButton('🇺🇦', callback_data = 'ru-uk'),
				InlineKeyboardButton('🇦🇪', callback_data = 'ru-ar')],

				[InlineKeyboardButton('➖', callback_data = 'back')]
	]
	return InlineKeyboardMarkup(keyboard)

# Фукция обработчик команд от кнопок
def lang_callback(bot, update):
	query = update.callback_query
	data = query.data
	chat_id = update.effective_message.chat_id
	current_text = update.effective_message.text

	lange = 'lang={}&'.format(data)

	if data == lange[5:10]:
		url = yandex + lange + key + '&text={}'.format(current_text)
		r = requests.get(url).json()
		ans = r['text']
		for i in ans:
			print(i)
		query.edit_message_text(
			text = i,
			parse_mode = ParseMode.MARKDOWN
			)
		bot.send_message(
			chat_id = chat_id,
			)

	elif data == 'next':
		query.edit_message_text(
			text = current_text,
			reply_markup = lang_two(),
			)

	elif data == 'back':
		query.edit_message_text(
			text = current_text,
			reply_markup = lang(),
			)

# Функция вывода, результат работы остальных функций
def main():
	bot = Bot(token = token)
	updater = Updater(bot = bot)
	update = Update

	# Встроенные обработчки запросов от телеграмм
	command_handler = CommandHandler('start', command)
	help_command_handler = CommandHandler('🆘🤯⁉️', help_command)
	txt_handler = MessageHandler(Filters.text, txt)
	buttons_handler = CallbackQueryHandler(callback = lang_callback)

	# Менеджеры по выводу встроенных функций от телеграмм
	updater.dispatcher.add_handler(command_handler)
	updater.dispatcher.add_handler(txt_handler)
	updater.dispatcher.add_handler(buttons_handler)
	updater.dispatcher.add_handler(help_command_handler)

	# Команда запуска скрпта и обработки его до конца всего цикла
	updater.start_polling()
	updater.idle()


if __name__ == '__main__':
	main()



