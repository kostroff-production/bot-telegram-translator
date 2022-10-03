import requests
import json
from keys import token, yandex, IAM_TOKEN, folder_id, menu
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

# Функция обработчик команд
def command(update, bot):
	update.message.reply_text(
		text='Бот активирован 🤖\n Будут вопросы жми /info',
		reply_markup=keyboard_help()
	)

def help_command(update, bot):
	update.message.reply_text(text=menu)

# Функция обработчки текста
def txt(update, bot):
	text = update.message.text
	update.message.reply_text(
		text=text,
		reply_markup=lang()
	)

# Кнопка помощи, которая будет активна постоянная и находиться под полем ввода текста
def keyboard_help():
	keyboard = [[KeyboardButton('/info')]]
	return ReplyKeyboardMarkup(
		keyboard=keyboard,
		resize_keyboard=True
		)

# Инлайн кнопки, кнопки работающие с текстом, принимающие запрос от пользователя на перевод
# первый ряд
def lang():
	keyboard = [[InlineKeyboardButton('🇬🇧󠁢󠁥󠁮󠁧󠁿', callback_data='en'),
				InlineKeyboardButton('🇩🇪', callback_data='de'),
				InlineKeyboardButton('🇮🇹', callback_data='it')],

				[InlineKeyboardButton('🇪🇸', callback_data='es'),
				InlineKeyboardButton('🇫🇷', callback_data='fr'),
				InlineKeyboardButton('🇵🇱', callback_data='pl')],

				[InlineKeyboardButton('➕', callback_data='next')]
	]
	return InlineKeyboardMarkup(keyboard)

# Второй ряд
def lang_two():
	keyboard = [[InlineKeyboardButton('🇵🇹', callback_data='pt'),
				InlineKeyboardButton('🇷🇸', callback_data='sr'),
				InlineKeyboardButton('🇨🇿', callback_data='cs')],

				[InlineKeyboardButton('🇨🇳', callback_data='zh'),
				InlineKeyboardButton('🇺🇦', callback_data='uk'),
				InlineKeyboardButton('🇦🇪', callback_data='ar')],

				[InlineKeyboardButton('➖', callback_data='back')]
	]
	return InlineKeyboardMarkup(keyboard)

# Фукция обработчик команд от кнопок
def lang_callback(update, bot):
	query = update.callback_query
	target_language = query.data
	texts = [update.effective_message.text]

	if not target_language in ['next', 'back']:
		body = {
			"targetLanguageCode": target_language,
			"texts": texts,
			"folderId": folder_id,
		}

		headers = {
			"Content-Type": "application/json",
			"Authorization": "Bearer {0}".format(IAM_TOKEN)
		}

		response = requests.post(
			yandex,
			json=body,
			headers=headers
		)

		text = json.loads(response.text)['translations'][0]['text']

		query.edit_message_text(
			text=text,
			parse_mode=ParseMode.MARKDOWN
		)

	elif target_language == 'next':
		query.edit_message_text(
			text=texts[0],
			reply_markup=lang_two(),
			)

	elif target_language == 'back':
		query.edit_message_text(
			text=texts[0],
			reply_markup=lang(),
			)

# Функция вывода, результат работы остальных функций
def main():
	bot = Bot(token=token)
	updater = Updater(bot=bot)

	# Встроенные обработчки запросов от телеграмм
	command_handler = CommandHandler('start', command)
	help_command_handler = CommandHandler('info', help_command)
	txt_handler = MessageHandler(Filters.text, txt)
	buttons_handler = CallbackQueryHandler(callback=lang_callback)

	# Менеджеры по выводу встроенных функций от телеграмм
	updater.dispatcher.add_handler(command_handler)
	updater.dispatcher.add_handler(help_command_handler)
	updater.dispatcher.add_handler(txt_handler)
	updater.dispatcher.add_handler(buttons_handler)

	# Команда запуска скрпта и обработки его до конца всего цикла
	updater.start_polling()
	updater.idle()


if __name__ == '__main__':
	main()
