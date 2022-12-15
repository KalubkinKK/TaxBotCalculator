import emoji
from telebot.types import Message

from config_data.config import DEFAULT_COMMANDS
from loader import bot


@bot.message_handler(commands=['start'])
# @logger.catch
def bot_start(message: Message) -> None:
    """
    Функция приветствия на команду /start
    :param message: Сообщение пользователю
    :return: None
    """

    text = f'Добрый день!{emoji.emojize(":waving_hand:")}\nДобро пожаловать в налоговый калькулятор!\n' \
           f'Мы стараемся быть максимально полезными для вашего ' \
           f'бизнеса{emoji.emojize(":smiling_face_with_open_hands:")}\n\n'
    bot.send_message(message.from_user.id, text)
    text_2 = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS]
    bot.send_message(message.from_user.id, '\n'.join(text_2))


