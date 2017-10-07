import smtplib
import time
import imaplib
import email
from bs4 import BeautifulSoup
import re
import locale
import vincent

locale.setlocale(locale.LC_MONETARY, )
# -------------------------------------------------
#
# Utility to read email from Gmail Using Python
#
# ------------------------------------------------
from constants import *
import data

global count, total_cost, debit_card_transaction_total_cost, total_cash_withdrawl

result_map = {}
category_map = {}
category_map[data.OTHER] = 0
count = 0
total_transaction_check = 100
total_cost = 0
debit_card_transaction_total_cost = 0
total_cash_withdrawl = 0

def read_email_from_gmail():
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('inbox')

        type, data = mail.search(None, 'ALL')
        mail_ids = data[0]

        id_list = mail_ids.split()
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        for i in range(latest_email_id,first_email_id, -1):
            typ, data = mail.fetch(str(i), '(RFC822)')

            for response_part in data:
                if isinstance(response_part, tuple):
                    try:
                        msg = email.message_from_string(response_part[1].decode('utf-8'))
                        if filter_emails(msg):
                            return
                    except Exception as e:
                        print(e)
    except Exception as e:
        print(e)


def filter_emails(msg):
    global count, debit_card_transaction_total_cost, total_cash_withdrawl
    email_subject = msg['subject']
    email_from = msg['from']

    if email_from == data.kotak_bank_email or email_from == data.kotak_bank_email_1 or email_from == data.kotak_debit_bank_email:
        if email_subject == data.kotak_cc_transc_subject:
            if msg.is_multipart():
                for payload in msg.get_payload():
                    # if payload.is_multipart(): ...
                    soup = BeautifulSoup(payload.get_payload(), 'html.parser')
                    text = soup.get_text()
                    data_arr = re.findall(data.kotak_cc_transaction_regex, text)
                    vendor_name_list = re.findall(data.kotak_cc_transaction_line_regex, data_arr[0])
                    dd = data_arr[0].split(" ")
                    cost = dd[3]
                    vendor_name = vendor_name_list[0].split(" ")
                    ff = []
                    flag = True
                    for i in vendor_name:
                        if i != 'at':
                            if flag:
                                continue
                        if i == 'on':
                            break
                        else:
                            flag = False
                            ff.append(i)

                    print("Vendor:{0} and Cost:{1}".format(''.join(ff), cost))
                    update_result(ff, cost)
                    count += 1
                    if count < total_transaction_check:
                        print("Count: {0}".format(count))
                        return False
                    else:
                        return True
        elif email_subject == data.kotak_debit_transc_subject:
            text = ''
            if msg.is_multipart():
                for payload in msg.get_payload():
                    soup = BeautifulSoup(payload.get_payload(), 'html.parser')
                    text = soup.get_text()
            else:
                soup = BeautifulSoup(msg.get_payload(), 'html.parser')
                text = soup.get_text()
            data_arr = re.findall(data.kotak_debit_transaction_regex, text.replace('\n', ' ').replace('\r', '').replace('=',''))
            data_arr = data_arr[0].split(' ')
            print(data_arr)
            debit_card_transaction_total_cost += int(float(data_arr[5]))
            count += 1
            if count < total_transaction_check:
                print("Count: {0}".format(count))
                return False
            else:
                return True
        elif email_subject == data.kotak_debit_cash_widthdrawl:
            text = ''
            if msg.is_multipart():
                for payload in msg.get_payload():
                    soup = BeautifulSoup(payload.get_payload(), 'html.parser')
                    text = soup.get_text()
            else:
                soup = BeautifulSoup(msg.get_payload(), 'html.parser')
                text = soup.get_text()
                text = text.replace('\n', ' ').replace('\r', '').replace('=','')
            data_arr = re.findall(data.kotak_debit_transaction_regex, text)
            data_arr = data_arr[0].split(' ')
            total_cash_withdrawl += int(float(data_arr[10].split('.')[1]))
            count += 1
            if count < total_transaction_check:
                print("Count: {0}".format(count))
                return False
            else:
                return True



    return False


def update_result(vendor_name_list, cost):
    global total_cost
    vendor_name = ' '.join(vendor_name_list[1:]).strip()
    price = int(cost.split('.')[1])
    total_cost += price
    if vendor_name in result_map:
        result_map[vendor_name] += price
    else:
        result_map[vendor_name] = price

    if vendor_name not in data.vendors:
        category_map[data.OTHER] += price
    elif data.vendors[vendor_name] in category_map:
        category_map[data.vendors[vendor_name]] += price
    else:
        category_map[data.vendors[vendor_name]] = price



read_email_from_gmail()

bar = vincent.Bar(result_map)
bar1 = vincent.Bar(category_map)
print("Total Credit card Cost: {0}".format(total_cost))
print("Total Debit Card Transaction: {0}".format(debit_card_transaction_total_cost))
print("Total Cash Withdrawl: {0}".format(total_cash_withdrawl))
bar.to_json('11', html_out=True, html_path='ww1.html')
bar1.to_json('12', html_out=True, html_path='ww1.html')