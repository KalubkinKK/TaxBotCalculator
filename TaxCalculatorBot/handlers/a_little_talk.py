from loguru import logger
from telebot.types import Message

from keyboards.inline.inline_keyboard import *
from loader import bot
from states.user_states import UserStates
from utils.tax_fuction import *
from loguru import logger


@bot.message_handler(commands=["counter"])
def legal_form_choise_run(message: Message) -> None:
    text = "Выберите правовую форму"
    bot.send_message(message.from_user.id, text, reply_markup=legal_form_choise())
    bot.set_state(message.from_user.id, UserStates.legal_form_choise_state)
    logger.debug(f'message_handler')


@bot.message_handler(state="*", commands=["cancel"])
def cancel_command(message: Message) -> None:
    text = "Чем я еще могу помочь?"
    bot.send_message(message.from_user.id, text, reply_markup=default_keyboard())
    bot.delete_state(message.from_user.id)


@bot.callback_query_handler(func=lambda call_back: True, state=UserStates.legal_form_choise_state)
def tax_type(call_back) -> None:
    bot.delete_message(call_back.from_user.id, call_back.message.id)
    with bot.retrieve_data(call_back.from_user.id) as data:
        data["CEO_or_LTD_choice"] = call_back.data
    text = "Выберите систему налогообложения"
    bot.send_message(call_back.from_user.id, text, reply_markup=tax_type_keyboard())
    bot.set_state(call_back.from_user.id, UserStates.tax_type_choise_state)


@bot.callback_query_handler(func=lambda call_back: True, state=UserStates.tax_type_choise_state)
def value_added_menu_run(call_back) -> None:
    bot.delete_message(call_back.from_user.id, call_back.message.id)
    with bot.retrieve_data(call_back.from_user.id) as data:
        data["classic_or_simple_tax_choise"] = call_back.data
    text = "Работаете ли вы с НДС?"
    bot.send_message(call_back.from_user.id, text, reply_markup=value_added_menu_keyboard())
    bot.set_state(call_back.from_user.id, UserStates.value_added_menu_state)


@bot.callback_query_handler(func=lambda call_back: True, state=UserStates.value_added_menu_state)
def simple_tax_sys_menu_run(call_back) -> None:
    bot.delete_message(call_back.from_user.id, call_back.message.id)
    with bot.retrieve_data(call_back.from_user.id) as data:
        data["VAT_choise"] = call_back.data
    text = f'Введите размер Вашей выручки за I квартал'
    bot.send_message(call_back.from_user.id, text)
    bot.set_state(call_back.from_user.id, UserStates.revenue_quarter_I)


@bot.message_handler(state=UserStates.revenue_quarter_I, content_types=['text'])
def simple_tax_sys_menu_run(message: Message) -> None:
    if message.text.replace('.', '').isdigit() or message.text.replace(',', '').isdigit():
        with bot.retrieve_data(message.from_user.id) as data:
            data["revenue_quarter_I"] = float(message.text)
        text = f'Введите размер Вашей выручки за II квартал'
        bot.send_message(message.from_user.id, text)
        bot.set_state(message.from_user.id, UserStates.revenue_quarter_II)
    else:
        text = f'Нужно ввести число без лишних символов!'
        bot.send_message(message.from_user.id, text)
        bot.set_state(message.from_user.id, UserStates.revenue_quarter_I)


@bot.message_handler(state=UserStates.revenue_quarter_II, content_types=['text'])
def simple_tax_sys_menu_run(message: Message) -> None:
    if message.text.replace('.', '').isdigit() or message.text.replace(',', '').isdigit():
        with bot.retrieve_data(message.from_user.id) as data:
            data["revenue_quarter_II"] = float(message.text)
        text = f'Введите размер Вашей выручки за III квартал'
        bot.send_message(message.from_user.id, text)
        bot.set_state(message.from_user.id, UserStates.revenue_quarter_III)
    else:
        text = f'Нужно ввести число без лишних символов!'
        bot.send_message(message.from_user.id, text)
        bot.set_state(message.from_user.id, UserStates.revenue_quarter_II)


@bot.message_handler(state=UserStates.revenue_quarter_III, content_types=['text'])
def simple_tax_sys_menu_run(message: Message) -> None:
    if message.text.replace('.', '').isdigit() or message.text.replace(',', '').isdigit():
        with bot.retrieve_data(message.from_user.id) as data:
            data["revenue_quarter_III"] = float(message.text)
            text = f'Введите размер Вашей выручки за IV квартал'
            bot.send_message(message.from_user.id, text)
            bot.set_state(message.from_user.id, UserStates.revenue_quarter_IV)
    else:
        text = f'Нужно ввести число без лишних символов!'
        bot.send_message(message.from_user.id, text)
        bot.set_state(message.from_user.id, UserStates.revenue_quarter_III)



@bot.message_handler(state=UserStates.revenue_quarter_IV, content_types=['text'])
def simple_tax_sys_menu_run(message: Message) -> None:
    if message.text.replace('.', '').isdigit() or message.text.replace(',', '').isdigit():
        with bot.retrieve_data(message.from_user.id) as data:
            data["revenue_quarter_IV"] = float(message.text)
            data["total_revenue"] = revenue(
                revenue_1=data["revenue_quarter_I"], revenue_2=data["revenue_quarter_II"],
                revenue_3=data["revenue_quarter_III"], revenue_4=data["revenue_quarter_IV"]
            )
            data["VAT"] = value_added_tax(total_revenue=data["total_revenue"])
            logger.debug(f'data["VAT"] - {data["VAT"]}')
            logger.debug(f'data["classic_or_simple_tax_choise"] - {data["classic_or_simple_tax_choise"]}')
            if data["classic_or_simple_tax_choise"] == "2":
                result_of_tax = simple_revenue_tax(
                    total_revenue=data["total_revenue"], value_added_tax_choice=data["VAT_choise"],
                    value_added_tax_result=data["VAT"], ceo_or_ltd_choice_choice=data["CEO_or_LTD_choice"]
                )
                logger.debug(f"result_of_tax - {result_of_tax}")
                logger.debug(f'data["total_revenue"] - {data["total_revenue"]} and type - {type(data["total_revenue"])}')
                text = f'Сумма налога к уплате составляет: {result_of_tax} рублей.'
                bot.send_message(message.from_user.id, text)
            else:
                text = f'Введите размер Ваших расходов за I квартал'
                bot.send_message(message.from_user.id, text)
                bot.set_state(message.from_user.id, UserStates.costs_quarter_I)
    else:
        text = f'Нужно ввести число без лишних символов!'
        bot.send_message(message.from_user.id, text)
        bot.set_state(message.from_user.id, UserStates.revenue_quarter_IV)


@bot.message_handler(state=UserStates.costs_quarter_I, content_types=['text'])
def simple_tax_sys_menu_run(message: Message) -> None:
    if message.text.replace('.', '').isdigit() or message.text.replace(',', '').isdigit():
        with bot.retrieve_data(message.from_user.id) as data:
            data["costs_quarter_I"] = float(message.text)
        text = f'Введите размер Ваших расходов за II квартал'
        bot.send_message(message.from_user.id, text)
        bot.set_state(message.from_user.id, UserStates.costs_quarter_II)
    else:
        text = f'Нужно ввести число без лишних символов!'
        bot.send_message(message.from_user.id, text)
        bot.set_state(message.from_user.id, UserStates.costs_quarter_I)


@bot.message_handler(state=UserStates.costs_quarter_II, content_types=['text'])
def simple_tax_sys_menu_run(message: Message) -> None:
    if message.text.replace('.', '').isdigit() or message.text.replace(',', '').isdigit():
        with bot.retrieve_data(message.from_user.id) as data:
            data["costs_quarter_II"] = float(message.text)
        text = f'Введите размер Ваших расходов за III квартал'
        bot.send_message(message.from_user.id, text)
        bot.set_state(message.from_user.id, UserStates.costs_quarter_III)
    else:
        text = f'Нужно ввести число без лишних символов!'
        bot.send_message(message.from_user.id, text)
        bot.set_state(message.from_user.id, UserStates.costs_quarter_II)


@bot.message_handler(state=UserStates.costs_quarter_III, content_types=['text'])
def simple_tax_sys_menu_run(message: Message) -> None:
    if message.text.replace('.', '').isdigit() or message.text.replace(',', '').isdigit():
        with bot.retrieve_data(message.from_user.id) as data:
            data["costs_quarter_III"] = float(message.text)
        text = f'Введите размер Ваших расходов за IV квартал'
        bot.send_message(message.from_user.id, text)
        bot.set_state(message.from_user.id, UserStates.costs_quarter_IV)
    else:
        text = f'Нужно ввести число без лишних символов!'
        bot.send_message(message.from_user.id, text)
        bot.set_state(message.from_user.id, UserStates.costs_quarter_III)


@bot.message_handler(state=UserStates.costs_quarter_IV, content_types=['text'])
def simple_tax_sys_menu_run(message: Message) -> None:
    if message.text.replace('.', '').isdigit() or message.text.replace(',', '').isdigit():
        with bot.retrieve_data(message.from_user.id) as data:
            logger.debug(f'message - {message.text}')
            data["costs_quarter_IV"] = float(message.text)

            data["total_costs"] = costs(
                costs_1=data["costs_quarter_I"], costs_2=data["costs_quarter_II"],
                costs_3=data["costs_quarter_III"], costs_4=data["costs_quarter_IV"]
            )
            if data["VAT_choise"] == '1':
                text = f'Сумма НДС к уплате: {data["VAT"]}, рублей.'
                bot.send_message(message.from_user.id, text)

            logger.info(f'\ndata["classic_or_simple_tax_choise"] - {data["classic_or_simple_tax_choise"]}')

            if data["classic_or_simple_tax_choise"] == '1':  # classic
                tax_result = profit_tax(
                    total_revenue=data["total_revenue"], total_costs=data["total_costs"],
                    value_added_tax_choice=data["VAT_choise"], value_added_tax_result=data["VAT"]
                )
                text = f'Сумма налога к уплате: {tax_result} рублей.'
                bot.send_message(message.from_user.id, text)
            elif data["classic_or_simple_tax_choise"] == '3':  # 15%
                logger.debug(f'Вошли в сценарий 15%')
                tax_result = simple_profit_tax(
                    total_revenue=data["total_revenue"], total_costs=data["total_costs"],
                    value_added_tax_choice=data["VAT_choise"], value_added_tax_result=data["VAT"]
                )
                logger.info(f'tax_result - {tax_result}')
                text = f'Сумма налога к уплате: {tax_result} рублей.'
                bot.send_message(message.from_user.id, text)
    else:
        text = f'Нужно ввести число без лишних символов!'
        bot.send_message(message.from_user.id, text)
        bot.set_state(message.from_user.id, UserStates.costs_quarter_IV)
