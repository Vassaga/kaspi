from decimal import Decimal


# метод конвертации валют (курс пока задается в ручную)
def currency_converter(amount, out_currency, in_currency):
    if in_currency == 'KZT' and out_currency == 'USD':
        result = amount * 400
    elif in_currency == 'USD' and out_currency == 'KZT':
        result = amount / 400
    elif in_currency == 'KZT' and out_currency == 'EUR':
        result = amount * 350
    elif in_currency == 'EUR' and out_currency == 'KZT':
        result = amount / 350
    elif in_currency == 'USD' and out_currency == 'EUR':
        result = amount * 0.9
    elif in_currency == 'EUR' and out_currency == 'USD':
        result = amount / 0.9
    elif in_currency == 'KZT' and out_currency == 'RUB':
        result = amount * 5
    elif in_currency == 'RUB' and out_currency == 'KZT':
        result = amount / 5
    elif in_currency == 'RUB' and out_currency == 'USD':
        result = amount * 80 
    elif in_currency == 'USD' and out_currency == 'RUB':
        result = amount / 80
    elif in_currency == 'RUB' and out_currency == 'EUR':
        result = amount * 90
    elif in_currency == 'EUR' and out_currency == 'RUB':
        result = amount / 90
    else:
        result = amount
    print(f"From {amount} {out_currency} converted in {result} {in_currency}") # проверка корректности конвертации
    return Decimal(str(result)) # конвертируем float/int в децимал для передачи его в объект трансфера