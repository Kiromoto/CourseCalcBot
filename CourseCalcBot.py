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


# @bot.message_handler(content_types=['text'])
# def exchange(message: telebot.types.Message):
#     # r = requests.get('https://belarusbank.by/api/kursExchange')
#     # texts = jsons.loads(r.content)
#     # for tx in texts:
#     #     print(tx)
#
#     r = requests.get('https://www.nbrb.by/api/exrates/rates?periodicity=0')
#     texts = jsons.loads(r.content)
#
#     tx = texts[0]
#     text_answer = f'Актуальные курсы на {tx["Date"]}'
#     text_answer = text_answer[:30] + ':\n'
#
#     for tx in texts:
#         # cur_scale = tx['Cur_Scale'] if tx['Cur_Scale']>0 else cur_scale = ''
#         text_answer += tx['Cur_Abbreviation'] + ' ' + tx['Cur_Name'] + ' ' + str(tx['Cur_OfficialRate']) + '\n'
#         # print(tx['Cur_Abbreviation']+' '+tx['Cur_Name']+' '+str(tx['Cur_OfficialRate']))
#         print(tx['Cur_Abbreviation'] + ' ' + tx['Cur_Name'] + ' ' + str(tx['Cur_OfficialRate']))
#
#     bot.send_message(message.chat.id, text_answer)