import random
from logger import Logger
from settings import config
from data import *
from telebot import types
from telebot.handler_backends import State, StatesGroup
import telebot


log = Logger(config.BOT_NAME[1:])
bot = telebot.TeleBot(config.BOT_TOKEN, parse_mode="markdown")
log.info(f"Bot <{config.BOT_NAME}> started")

known_users = []
userStep = {}
buttons = []


class MyStates(StatesGroup):
    target_word: State = State()
    translate_word = State()
    another_words = State()


class Command:
    ADD_WORD = 'Добавить слово +'
    DELETE_WORD = 'Удалить слово <-'
    NEXT = 'Дальше ->>'


@bot.message_handler(commands=["start"])
def answer_start(message):
    bot.send_photo(message.chat.id, START_IMAGE_URL, text_commands["start"])
    log.info(f"START user_name=<{message.from_user.username}>, name=<{message.from_user.first_name}>")


# noinspection PyTypeChecker
@bot.message_handler(commands=['cards'])
def create_cards(message):
    cid = message.chat.id
    if cid not in known_users:
        known_users.append(cid)
        userStep[cid] = 0
        bot.send_message(cid, "Hello, stranger, let study English...")
    markup = types.ReplyKeyboardMarkup(row_width=2)

    target_word = 'Peace'
    translate = 'Мир'
    target_word_btn = types.KeyboardButton(target_word)
    buttons.append(target_word_btn)
    others = ['Green', 'White', 'Hello', 'Car']
    other_words_btns = [types.KeyboardButton(word) for word in others]
    buttons.extend(other_words_btns)
    random.shuffle(buttons)
    next_btn = types.KeyboardButton(Command.NEXT)
    add_word_btn = types.KeyboardButton(Command.ADD_WORD)
    delete_word_btn = types.KeyboardButton(Command.DELETE_WORD)
    buttons.extend([next_btn, add_word_btn, delete_word_btn])
    markup.add(*buttons)

    greeting = f"Выбери перевод слова:\n🇷🇺 {translate}"
    bot.send_message(message.chat.id, greeting, reply_markup=markup)
    bot.set_state(message.from_user.id, MyStates.target_word, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['target_word'] = target_word
        data['translate_word'] = translate
        data['other_words'] = others


@bot.message_handler(func=lambda message: message.text == Command.NEXT)
def next_cards(message):
    create_cards(message)


@bot.message_handler(func=lambda message: message.text == Command.DELETE_WORD)
def delete_word(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        print(data['target_word'])


@bot.message_handler(func=lambda message: message.text == Command.ADD_WORD)
def add_word(message):
    cid = message.chat.id
    userStep[cid] = 1


@bot.message_handler(func=lambda message: message.text == Command.NEXT)
def next_cards(message):
    create_cards(message)


@bot.message_handler(func=lambda message: message.text == Command.DELETE_WORD)
def delete_word(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        print(data['target_word'])


@bot.message_handler(func=lambda message: message.text == Command.ADD_WORD)
def add_word(message):
    cid = message.chat.id
    userStep[cid] = 1


@bot.message_handler(commands=["commands"])
def answer_commands(message):
    bot.send_message(message.chat.id, text_commands["commands"])
    log.info(f"COMMANDS user_name=<{message.from_user.username}>, name=<{message.from_user.first_name}>")


@bot.message_handler(commands=["about"])
def answer_about(message):
    bot.send_message(message.chat.id, text_commands["about"])
    log.info(f"ABOUT user_name=<{message.from_user.username}>, name=<{message.from_user.first_name}>")


@bot.message_handler(commands=["englishwords"])
def answer_english_words(message):
    nouns = "\n".join([f"🔻 {noun}" for noun in words["nouns"]])
    verbs = "\n".join([f"🔻 {verb}" for verb in words["verbs"]])

    bot.send_photo(message.chat.id, "https://disk.yandex.ru/i/7WG0dU2SrJkdnA",
                   text_commands["english_words"].format(nouns, verbs))
    log.info(f"ENGLISH WORDS user_name=<{message.from_user.username}>, name=<{message.from_user.first_name}>")


@bot.message_handler(func=lambda x: True)
def answer_to_all_messages(message):
    translated_message = ""
    for part_of_speech in words:
        for word in words[part_of_speech]:
            if message.text.lower() == word:
                translated_message = f"{dictionary[part_of_speech].title()}: {message.text.lower()}\n" \
                                     f"Перевод: {words[part_of_speech][word]}\n\n" \
                                     f"Отправьте /englishwords, чтобы посмотреть список слов"
                bot.send_message(message.chat.id, translated_message)
                log.info(f"TRANSLATED user_name=<{message.from_user.username}>, name=<{message.from_user.first_name}>, "
                         f"text=<{message.text}>")
                break
    if not translated_message:
        bot.send_message(message.chat.id, text_commands["default"].format(message.chat.first_name))
        log.info(f"RECV user_name=<{message.from_user.username}>, name=<{message.from_user.first_name}>, "
                 f"text=<{message.text}>")


if __name__ == "__main__":
    bot.polling(none_stop=True)
    log.warning(f"Bot <{config.BOT_NAME}> finished")
