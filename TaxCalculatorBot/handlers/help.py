import emoji
from telebot.types import Message

from config_data.config import DEFAULT_COMMANDS
from loader import bot


@bot.message_handler(commands=['help'])
def bot_help(message: Message) -> None:
    """
    Функция помощник которая выводит список команд и раскрывает возможности бота /help
    :param message: Сообщение пользователю
    :return: None
    """
    text_1 = f'Здесь перечислены команды, с помощью которых Вы можете управлять ботом!' \
             f'{emoji.emojize(":winking_face:")}\n\n'
    text_2 = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS]

    bot.send_message(message.from_user.id, text_1)
    bot.send_message(message.from_user.id, '\n'.join(text_2))
