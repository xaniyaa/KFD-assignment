import os
import random


user_money = {
    "RUB": 1_000_000,
    "USD": 0,
    "USDT": 0,
    "EUR": 0,
    "BTC": 0,
}

terminal_money = {
    "RUB": 10_000,
    "USD": 1_000,
    "USDT": 1_000,
    "EUR": 1_000,
    "BTC": 1.5,
}

currency_pairs = {
    "RUB/USD": 91,
    "RUB/EUR": 100,
    "USD/EUR": 1.1,
    "USD/USDT": 1,
    "USD/BTC": 68_000,
}

currency_choice_pairs = {
    1: "RUB/USD",
    2: "RUB/EUR",
    3: "USD/EUR",
    4: "USD/USDT",
    5: "USD/BTC",
}


def print_balance():
    print(f"> Ваш Баланс:")
    for currency, amount in user_money.items():
        if amount != 0:
            print(f">\t{currency}: {amount}")

    print("> Доступный для приобретения:")
    for currency, amount in terminal_money.items():
        if amount != 0:
            print(f">\t{currency}: {amount}")

    print("> Текущий курс:")
    for currency, amount in currency_pairs.items():
        print(f">\t{currency}: {amount}")


def change_courses():
    for currency, amount in currency_pairs.items():
        currency_pairs[currency] = round(amount * random.uniform(0.95, 1.05), 2)


def handle_transaction(action: str, amount: int, currency_pair: str) -> None:
    """Handle the transaction and change currency pair rate by 5%. Returns True if success or False if not"""
    if (type(action) != str) or not (action == "sell" or action == "buy"):
        raise ValueError("Неверная операция.")

    change_rate = currency_pairs[currency_pair]

    if action == "sell":
        if (user_money[currency_pair.split("/")[0]] - amount) < 0:
            raise ValueError(
                f"Недостаточно средств у вас для продажи {currency_pair.split("/")[0]}."
            )
        if (terminal_money[currency_pair.split("/")[1]] - (amount / change_rate)) < 0:
            raise ValueError(
                f"Недостаточно средств у терминала для продажи {currency_pair.split("/")[0]}."
            )

        cost = amount / change_rate

        user_money[currency_pair.split("/")[1]] += round(cost, 2)
        user_money[currency_pair.split("/")[0]] -= amount
        terminal_money[currency_pair.split("/")[1]] = round(
            terminal_money[currency_pair.split("/")[1]] - cost, 2
        )
        terminal_money[currency_pair.split("/")[0]] += amount

    if action == "buy":
        if (user_money[currency_pair.split("/")[0]] - amount * change_rate) < 0:
            raise ValueError(
                f"Недостаточно средств для покупки {currency_pair.split("/")[1]}."
            )
        if (terminal_money[currency_pair.split("/")[1]] - amount) < 0:
            raise ValueError(
                f"Недостаточно средств для покупки {currency_pair.split("/")[1]}."
            )

        user_money[currency_pair.split("/")[0]] = round(
            user_money[currency_pair.split("/")[0]] - amount * change_rate
        )
        user_money[currency_pair.split("/")[1]] = amount
        terminal_money[currency_pair.split("/")[0]] = round(
            user_money[currency_pair.split("/")[0]] - amount * change_rate
        )
        terminal_money[currency_pair.split("/")[1]] -= amount

    print("[*] Вы успешно проверили транзакцию.")


def main():
    while True:
        print_balance()
        print("--------------------------------")
        try:
            action = input("> Введите действие (buy/sell/quit)\n> ")

            if action.lower() == "q" or action.lower() == "quit":
                break

            currency_pair = int(
                input(
                    "> Выберите валютную пару:\n>\t1. RUB/USD\n>\t2. RUB/EUR\n>\t3. USD/EUR\n>\t4. USD/USDT\n>\t5. USD/BTC\n> "
                )
            )

            if not (1 <= currency_pair <= 5):
                raise ValueError("Неверный выбор.")

            amount = float(input(f"> Введите желаемую сумму операции\n> "))

            choice = input(
                f"> Введенный вами данные верны (Y/N)?\n > Действие: {action}\n > Валютную пара: {currency_choice_pairs[currency_pair]}\n > Cумму операции: {amount}\n> "
            )

            if choice.lower() == "y":
                handle_transaction(action, amount, currency_choice_pairs[currency_pair])
                change_courses()
            os.system("cls")
        except ValueError as e:
            os.system("cls")
            print(f"[ERROR] {e}")
            print("--------------------------------")


if __name__ == "__main__":
    main()
