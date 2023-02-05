from flask import Flask, request, render_template

import shopify
import os
import credentials

access_token = credentials.access_token
shop_url = credentials.shop_url
api_version = "2023-01"
session = shopify.Session(shop_url, api_version, access_token)

reciept_txt = "output.txt"
r_width = 28

app = Flask(__name__, template_folder='templates')
@app.route("/", methods=['GET', 'POST'])

def index():
    shopify.ShopifyResource.activate_session(session)
    shop = shopify.Shop.current()
    orders = shopify.Order.find(status="any", limit=3)

    order1 = orders[0].order_number
    order2 = orders[1].order_number
    order3 = orders[2].order_number

    if request.method == 'POST':
        if request.form.get('action1'):
            print ('printing receipt for order number ' + str(order1))
            printSlip(shop, orders[0])
        elif request.form.get('action2'):
            print ('printing receipt for order number ' + str(order2))
            printSlip(shop, orders[1])
        elif request.form.get('action3'):
            print ('printing receipt for order number ' + str(order3))
            printSlip(shop, orders[2])
        else:
            pass
    elif request.method == 'GET':
        return render_template('form.html', VALUE1=order1, VALUE2=order2, VALUE3=order3)
    else:
        pass
    if request.form["input_value"]:
        input_value = request.form["input_value"]
        print("getting order number " + input_value)
        input_value2 = ("#" + input_value)
        orderRequest = shopify.Order.find(name=input_value2, status="any")
        print(orderRequest)
        printSlip(shop, orderRequest[0])
    else:
        pass
    shopify.ShopifyResource.clear_session()
    
    return render_template('form.html', VALUE1=order1, VALUE2=order2, VALUE3=order3)

def printSlip(shop, currOrder): #generates a receipt in output.txt file and prints that file using lp
    global r_width
    global reciept_txt
    with open(reciept_txt, "w") as f:
        print (shop.name, file=f)
        print (shop.address2 + "-" + shop.address1, file=f)
        print (shop.city + ", " + shop.province_code, file=f)
        print (shop.zip, file=f)
        print (shop.phone, file=f)
        print (shop.customer_email, file=f)
        print (" ", file=f)
        spaces = 10
        print ("ORDER NUMBER:" + (" " * spaces) + "#" + str(currOrder.order_number), file=f)
        print (" ", file=f)
        for line_item in currOrder.line_items:
            line = (line_item.title + " x " + str(line_item.quantity))
            spaces = r_width - ((len(line) + len(line_item.price))%r_width)
            print (line + (" " * spaces) + line_item.price, file=f)
        print (" ", file=f)
        spaces = r_width - ((15 + len(currOrder.subtotal_price))%r_width)
        print ("Subtotal price:" + (" " * spaces) + currOrder.subtotal_price, file=f)
        spaces = r_width - ((9 + len(currOrder.total_discounts))%r_width)
        if currOrder.total_discounts != '0.00':
            print ("Discount:" + (" " * spaces) + currOrder.total_discounts, file=f)
        else:
            pass
        print ("Taxes:", file=f)
        for tax in currOrder.tax_lines:
            spaces = r_width - ((8 + len(tax.title) + len(tax.price))%r_width)
            print("\t" + tax.title + (" " * spaces) + tax.price, file=f)
        spaces = r_width - ((12 + len(currOrder.total_price))%r_width)
        print("Total Price:" + (" " * spaces) + currOrder.total_price, file=f)
        print (" ", file=f)
        print ("Payment Details", file=f)
        transactions = currOrder.transactions()
        giftcards = []
        for transaction in transactions:
            if transaction.gateway == "cash":
                print ("CASH", file=f)
            elif transaction.gateway == "gift_card":
                print ("Gift Card", file=f)
                giftcardstatus = True
                giftcards.append(transaction.receipt.gift_card_id)
            elif transaction.gateway == "shopify_payments":
                print (transaction.payment_details.credit_card_company, file=f)
                print (transaction.payment_details.credit_card_number, file=f)
            else:
                print ("error", file=f)
            spaces = r_width - ((len(transaction.status) + len(transaction.amount))%r_width)
            print (transaction.status + (" " * spaces) + transaction.amount, file=f)
            print (transaction.processed_at, file=f)
            
        if currOrder.total_outstanding != "0.00":
            spaces = r_width - ((17 + len(currOrder.total_outstanding))%r_width)
            print ('*' * r_width, file=f)
            print ('\n\n' + 'TOTAL OUTSTANDING' + spaces + currOrder.total_outstanding, file=f)
            print ('*' * r_width, file=f)
        print ("\n\n" + "Thanks for shopping at \n" + shop.name, file=f)

    os.system("lp " + reciept_txt)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5000, debug=True)
