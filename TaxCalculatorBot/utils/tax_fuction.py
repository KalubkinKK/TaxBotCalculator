from loguru import logger

print(
    'Добрый день!\nДобро пожаловать в налоговый калькулятор!\nМы стараемся быть максимально полезными '
    'для вашего бизнеса.\n\n')


# Меню выбора правовой формы организации.
def legal_form():
    print("Выберите правовую форму:\n1. ИП\n2. ООО")
    legal_form_choise = int(input("Введите код: "))
    print()
    if legal_form_choise == 1 or legal_form_choise == 2:
        pass
    else:
        print('Ошибка ввода./nНеобходимо выбрать 1 или 2.')
        legal_form()
    return legal_form_choise


# Выбор системы налогообложения
def tax_type():
    print(
        "Выберите систему налогообложения:\n1. Классическая система налогообложения\n2. Упрощенная система "
        "налогообложения 6%\n2. Упрощенная система налогообложения 15%")
    tax_type_choise = int(input("Введите код:"))
    print()
    if tax_type_choise == 1:
        pass
    elif tax_type_choise == 2:
        pass
    elif tax_type_choise == 3:
        pass
    else:
        print('Ошибка ввода./nНеобходимо выбрать 1, 2 или 3.')
        tax_type()
    return tax_type_choise


# Утоняющий выбор "Работаете ли вы с НДС или нет"
def value_added_menu():
    print("Работаете ли вы с НДС? 1. да\t2. нет\t", end=' ')
    value_added_choise = int(input('Введите код: '))
    print()
    if value_added_choise == 1:
        pass
    elif value_added_choise == 2:
        pass
    else:
        print('Ошибка ввода./nНеобходимо выбрать 1 или 2.')
        value_added_menu()
    return value_added_choise


# Расчет выручки.
def revenue(revenue_1: float, revenue_2: float, revenue_3: float, revenue_4: float) -> float:
    count_of_revenue = revenue_1 + revenue_2 + revenue_3 + revenue_4
    return count_of_revenue


# Расчет расходов
def costs(costs_1: float, costs_2: float, costs_3: float, costs_4: float) -> float:
    count_of_costs = costs_1 + costs_2 + costs_3 + costs_4
    return count_of_costs


# Расчет НДС.
def value_added_tax(total_revenue: str) -> float:
    value_of_added_tax = float(total_revenue) * 0.20
    logger.info(f"Сумма НДС к уплате составляет {value_of_added_tax} рублей.")
    return round(value_of_added_tax, 2)


# Расчет налога 6% от выручки (УСН).
def simple_revenue_tax(
        total_revenue: float, value_added_tax_choice: str,
        value_added_tax_result: float, ceo_or_ltd_choice_choice: str
):
    count_of_tax_by_revenue = total_revenue * 0.06
    if value_added_tax_choice == '1':
        total_revenue -= value_added_tax_result
    if ceo_or_ltd_choice_choice == '1':
        if total_revenue > 300000:
            pension_contributions = (total_revenue - 300000) * 0.01
        else:
            pension_contributions = 0
        total_tax = count_of_tax_by_revenue + pension_contributions
    else:
        total_tax = count_of_tax_by_revenue
    logger.info(f"Сумма налога к уплате составляет {round(total_tax, 2)} рублей.")
    return round(total_tax, 2)


# Расчет 15% от прибыли выручки (УСН)
def simple_profit_tax(
        total_revenue: float, total_costs: float,
        value_added_tax_choice: str, value_added_tax_result: float
):
    if value_added_tax_choice == '1':
        total_revenue -= value_added_tax_result
    if total_revenue > total_costs:
        count_of_tax = (total_revenue - total_costs) * 0.15
    else:
        count_of_tax = total_revenue * 0.01
    return round(count_of_tax, 2)


# Расчет налога на прибыль.
def profit_tax(total_revenue: float, total_costs: float, value_added_tax_choice: int, value_added_tax_result: float):
    if value_added_tax_choice == '1':
        total_revenue -= value_added_tax_result
    if total_revenue > total_costs:
        count_of_tax = (total_revenue - total_costs) * 0.20
    else:
        count_of_tax = total_revenue * 0.01
    logger.debug(f'x - {round(count_of_tax, 2)}')
    return round(count_of_tax, 2)


__all__ = [
    "legal_form",
    "tax_type",
    "value_added_menu",
    "revenue",
    "costs",
    "value_added_tax",
    "simple_revenue_tax",
    "simple_profit_tax",
    "profit_tax"

]
