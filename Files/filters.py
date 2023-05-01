#22011032_Jacob_Craig_
import locale

def gbp(value):
    locale.setlocale(locale.LC_ALL, 'en_GB.UTF-8')
    return locale.currency(value, symbol=True, grouping=True)
