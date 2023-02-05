# receiptprinter
Python script to generate a receipt using the shopify api

(Hopefully) this script will allow you to print reciepts from an unsupported receipt printer in an admitedly janky way.

I wrote this with the intention of running it on linux but it should work on MacOS (?)

* A default printer must be set. `lpstat -d` will return the current default `lpadmin -d [printer-name]` to set a default printer. OR modify the code in app.py if you don't want to use the default. 
* Set admin api token and shop url in credentials.py
* Set r_width in app.py to the number of characters wide your receipt printer will print. If you're not sure then create a .txt file with whatever in it and use `lp file.txt` in the terminal and just count how many characters are printed on a line. I'm using a Start TSP100III/TSP143 r_width = 28
* Run app.py
* Visit localhost:5000 in a web browser

The last 3 orders will be displayed as button or enter in an order number manually.

In the future I'd like to add gift card balance remaining but I can't seem to access that info currenly unless I pay for Shopify Plus.
