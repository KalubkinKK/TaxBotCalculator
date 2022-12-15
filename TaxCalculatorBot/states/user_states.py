from telebot.handler_backends import State, StatesGroup


class UserStates(StatesGroup):
    legal_form_choise_state = State()
    tax_type_choise_state = State()
    value_added_menu_state = State()

    revenue_quarter_I = State()
    revenue_quarter_II = State()
    revenue_quarter_III = State()
    revenue_quarter_IV = State()

    costs_quarter_I = State()
    costs_quarter_II = State()
    costs_quarter_III = State()
    costs_quarter_IV = State()

