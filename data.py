import re

kotak_bank_email = 'Bankalerts@kotak.com'
kotak_debit_bank_email = 'BankAlerts@kotak.com'
kotak_bank_email_1 = 'BankAlerts@kotak.com <BankAlerts@kotak.com>'
kotak_cc_transc_subject = "Kotak Credit Card Transaction Alert"
kotak_debit_transc_subject = "Transaction Success Alert - Debit Card Transaction at Merchant\r\n Establishment"
kotak_debit_cash_widthdrawl = "Transaction Success Alert - ATM Cash Withdrawal"


kotak_cc_transaction_regex = re.compile("A Transaction.*Credit Limit")
kotak_cc_transaction_line_regex = re.compile("Credit Card No.*on")

kotak_debit_transaction_regex = re.compile("Debit Card.*Account")

RESTARURANT = 'restaurant'
ONLINE = 'online'
OTHER = 'other'
TRAVEL = 'travel'
SHOPPING = 'shopping'
MOVIES = 'movies'

vendors = {"PRATAPRESTAURANT": RESTARURANT,
           "AMAZON ONLINE D S PVT LTD":ONLINE,
           "BLANCO BY BUENA":RESTARURANT,
           "BOMBAY BREEZE CAFE": RESTARURANT,
           "CAFE COFFEE DAY":RESTARURANT,
           "FLIPKART INTERNET PRIVATE": ONLINE,
           "FMPL": OTHER,
           "INORDINATE TRADING": OTHER,
           "MUMBAI TAVA": RESTARURANT,
           "PAPILLON PARK": RESTARURANT,
           "PAPPILON PLUS":RESTARURANT,
           "PRATAP RESTAURANT": RESTARURANT,
           "REDBUS IN": TRAVEL,
           "SAI BABA FOODS": RESTARURANT,
           "SHIVSAGAR,": RESTARURANT,
           "SHREE NAKODA.": RESTARURANT,
           "SHREEJI F AND B CO":RESTARURANT,
           "SKECHERS INFINITY": SHOPPING,
           "THE THIRD HOUSE":RESTARURANT,
           "UBER INDIA SYSTEMS PVT": TRAVEL,
           "WOK EXPRESS": RESTARURANT,
           "WWW OLACABS COM": TRAVEL,
           "WWW URBANCLAP COM": ONLINE,
           "Zomato Online Order":RESTARURANT,
           "CITRUSPAY ZOMATO": RESTARURANT,
           "KAILASH PRABAT": RESTARURANT,
           "Book My Show": MOVIES,
           "WWW.GODADDY.COM": ONLINE,
           "HTTP WWW ZOMATO COM": RESTARURANT,
           "MIRA BELLA FASHIONS FI": SHOPPING,
           "YOKO SIZZLERS": RESTARURANT,
           "RAZORPAY ZOMATO ONLINE": RESTARURANT,
           "ROYALTY FOODS": RESTARURANT,
           "THE IRISH HOUSE": RESTARURANT,
           "CINEPOLIS INDIA PVT LTD": MOVIES,
           "CAFE LEOPOLD": RESTARURANT,
           "Citrusp* vacationlabs": TRAVEL
           }