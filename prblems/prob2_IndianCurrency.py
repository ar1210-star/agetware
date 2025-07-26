def format_indian_currency(number):
    if '.' in number:
        integer_part, decimal_part = number.split('.')
        decimal_part = '.' + decimal_part
    else:
        integer_part = number
        decimal_part = ''

  
    is_negative = integer_part.startswith('-')
    if is_negative:
        integer_part = integer_part[1:]


    if len(integer_part) > 3:
        last_three = integer_part[-3:]
        rest = integer_part[:-3]
        parts = []
        while len(rest) > 2:
            parts.insert(0, rest[-2:])
            rest = rest[:-2]
        if rest:
            parts.insert(0, rest)
        formatted = ','.join(parts) + ',' + last_three
    else:
        formatted = integer_part

    if is_negative:
        formatted = '-' + formatted

    return formatted + decimal_part
  
  

number = input("Enter any number: ")
indianCurrency = format_indian_currency(number)
print(indianCurrency)