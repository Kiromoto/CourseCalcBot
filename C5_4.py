import telebot

bot = telebot.TeleBot('5443961552:AAGG8XQrZdWXL24QOAeJLX79zLE1tXYUE_w')


@bot.message_handler(commands=['start', 'help'])
def send__start_help(message):
    bot.reply_to(message, f"Welcome, {message.chat.first_name}!")

    # bot.send_message(message.chat.id, f"Welcome, {message.chat.username}")


@bot.message_handler(content_types=['text'])
def repeat_text(message: telebot.types.Message):
    bot.send_message(message.chat.id, message.text)


@bot.message_handler(content_types=['photo'])
def say_lmao(message: telebot.types.Message):
    bot.reply_to(message, 'Nice meme XDD')


bot.polling(none_stop=True)



# @bot.message_handler(content_types=['document', 'audio'])
# def handle_docs_audio(message):
#     pass
#
# @bot.message_handler(ontent_types=['text'])
# def message_for_bot(message):
#     bot.reply_to(message, "This is a message handler")
#     print(message.text)
