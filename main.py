import tkinter as tk
from tkinter import ttk, font as tkfont, messagebox
from twilio.rest import Client
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import json
import os

my_email = "YOUR MAIL"
password = "YOUR PASSWORD"

# Dictionary to store available quantities of components if data.json file Not Found !
component_availability = {
    "Arduino": 20,
    "Esp32": 20,
    "Esp8266": 20,
    "8051": 20,
    "Ultrasonic Sensor": 20,
    "Temp Sensor": 20,
    "IR Sensor": 20
}

def load_data_from_file():
    global cart_data, component_availability

    data_file_path = "data.json"

    if os.path.exists(data_file_path):
        with open(data_file_path, "r") as file:
            try:
                data = json.load(file)
                cart_data = data["cart_data"]
                component_availability = data["component_availability"]
            except json.JSONDecodeError:
                print("JSON decoding error. Creating a new data file with default data.")
                # If the file has decoding error, create a new data file with default data
                save_data_to_file()
    else:
        print("Data file not found. Creating a new data file with default data.")
        # If the file doesn't exist, create it with default data
        save_data_to_file()

def save_data_to_file():
    data = {
        "cart_data": cart_data,
        "component_availability": component_availability
    }
    data_file_path = "data.json"
    with open(data_file_path, "w") as file:
        json.dump(data, file)

def update_component_availability_after_order():
    global component_availability

    # Update the component_availability based on items in the cart after placing an order
    for item in cart_data:
        component_name, quantity = item["name"], int(item["quantity"])
        component_availability[component_name] -= quantity

    # Save the updated component_availability to the JSON file
    save_data_to_file()

admin_window_opened = False

def open_admin_window():
    global admin_window_opened

    if not admin_window_opened:
        password_window = tk.Toplevel(root)
        password_window.title("Enter Password")
        password_window.configure(bg="#F7F7F7")

        password_label = tk.Label(password_window, text="Enter Password:", font=("Helvetica", 12), bg="#F7F7F7")
        password_label.pack(pady=20)

        password_entry = tk.Entry(password_window, show="*", font=("Arial", 12))
        password_entry.pack(pady=10)
        password_entry.focus_set()

        def check_password():
            entered_password = password_entry.get()

            if entered_password == "isakey123":
                password_window.destroy()
                admin_window = tk.Toplevel(root)
                admin_window.title("ISA Admin")
                admin_window.attributes("-fullscreen", True)
                admin_window.configure(bg="#F7F7F7")

                admin_label = tk.Label(admin_window, text="Component Data", font=("Helvetica", 16, "bold"), fg="#333333",
                                       bg="#F7F7F7")
                admin_label.pack(pady=20)

                # Create a scrollable frame within the admin_window
                tree_frame = tk.Frame(admin_window)
                tree_frame.pack(fill="both", expand=True)

                # Create a treeview with scrollbar
                tree_scroll = tk.Scrollbar(tree_frame)
                tree_scroll.pack(side="right", fill="y")

                admin_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
                admin_tree.pack(fill="both", expand=True)

                tree_scroll.config(command=admin_tree.yview)

                admin_tree["columns"] = ("Box", "Component", "Available")
                admin_tree.column("#0", width=0, stretch=tk.NO)
                admin_tree.column("Box", anchor=tk.CENTER, width=100)
                admin_tree.column("Component", anchor=tk.CENTER, width=300)
                admin_tree.column("Available", anchor=tk.CENTER, width=100)

                admin_tree.heading("#0", text="", anchor=tk.CENTER)
                admin_tree.heading("Box", text="Box", anchor=tk.CENTER)
                admin_tree.heading("Component", text="Component", anchor=tk.CENTER)
                admin_tree.heading("Available", text="Available", anchor=tk.CENTER)

                add_component_button = tk.Button(admin_window, text="Add Component", font=("Arial", 16), bg="#E8E8E8",
                                                 fg="#333333", command=open_add_component_window)
                add_component_button.pack(pady=20)
                # Here you can add the new component in your desired box
                for component, quantity in component_availability.items():
                    box = "B1"
                    if component in ("LM324N", "P9624AB", "HD74LSOOP", "74LV04SN", "74LV04N", "7483 IC", "74147 IC"):
                        box = "B2"
                    elif component in ("Sharp I.R sensor", "DHT11( Temperature and humidity sensor)",
                                       "Soil Sensor (with module)", "Microwave Radar Sensor(RCWL-0516)",
                                       "Ultrasonic (HC-SR04)", "IR SENSOR (photo diode)"):
                        box = "B3"
                    elif component in (
                            "Voice sound module (WT588D)", "Voice regonition module (with mic)", "Small O-LED",
                            "4 digit 7 segment display", "8 digit 7 segment  display", "2 digit  7 segment (red colour)",
                            "1 digit 7 segment display (Big)", "1 digit 7 segment display", "LED matrix",
                            "Voltage regulator", "I2C module (RTC)*", "Crystal Oscilator", "micro crystal MS3V-T1R",
                            "Lugs", "MP3V5050g"):
                        box = "B4"
                    elif component in ("10k pot","47k Pot","470k pot","200k pot","B 1 MEG 01 pot","1k pot","103B / 10k  SMD pot","502B pot"):
                        box = "B5"
                    elif component in ("PIR sensor","Gas sensor","text to speech module","acelerometer ( adxl345) (GY521)","Microwave Radar Sensor","Hall effect sensor","GYROSCOPE(MPU92.65)"):
                        box = "B6"
                    elif component in ("37 in 1 sensor kit fir arduino","Joystick", "Laser", "Buzzer module", "IR Module", "IR sensor PCB"):
                        box = "B7"
                    elif component in ("CASTER 62858" ,"RGB LED STRIPS.0"):
                        box = "B9"
                    elif component in ("Arduino port to UART","Gear Motor Driver","POWER TRANSISTOR FITTING KIT"):
                        box = "B10"
                    elif component in ("ATMEGA32","ATMEGA8","Usb Module"):
                        box = "B11"
                    elif component in (
                        "LED","RGB","SMALL LEDS","MM74HC138N","CD74HC573E","POT","Switch","Capacitors","Connector WHITE ND BLACK",
                        "Screw","Small Leds ATMEL734","SMALL F. I H0LDER","FEMALE IC HOLDER","IC HOLDER","Diodes","PIC18F14K50","PIC18F(4520)",
                        "PIC18F(4550)","PIC16F877A AND DS13020538A5","16 pin round dip 20 pin base","DC Jack","1A Bridge Rectifier","Power Switch Dip k",
                        "89E516RD","SOP16","PCBS","Max 232  ULN 2803 16 PIN CONNECTOR","RS232 FEMALE 7805","16 pin base 18 pin base"):
                        box = "B12"
                    elif component in (
                        "OP-AMP 741 IC","NE555 IC","Fuse","10 uF capacitor","220 uF capacitor","Lever Switch","DPI Switch",
                        "BC 574 Tranisitor","N7000 MOSFET","SL100B transistor","BT136-600E TRIAC","tip122 transistor","82 pF capacitor",
                        "560 pF capacitor","15 pF capacitor","470 uF capacitor","LM324",
                        "LM386","33 pF capacitor","150 pF capacitor","100 pF capacitor","470 pF capacitor",
                        "47 pF capacitor","15 pF capacitor","68 pF capacitor","220 pF capacitor","1 k ohm resistor"
                    ):
                        box = "B13"
                    elif component in ("servo motors"):
                        box = "B14"
                    elif component in (
                        "A103J / A472J","Capacitor orange(10 uF)","IR infrared receiver","push buttons","IC 75ACOLM",
                        "HW-221 Voltage Converter","IC 7660","N7000 transistor","LDR"
                    ):
                        box = "B15"
                    elif component in (
                        "numeric keypads","single button keypad","solar panel 5V","solar panel 6V","Tact Switch (3mm)","Track Rod","solar panel 10V"
                    ):
                        box = "B16"
                    elif component in (
                        "SIM 800A/900A GSM MODULE","GSM 6M MODULE","L9110 Motor drive","Xbeee pro"
                    ):
                        box = "B18"
                    elif component in (
                        "NRF 24201 (with antenna)","PCB mount mini Speaker","Transistor 512 series","TXSS0108E Logic level Converter","Wifi Relay"
                    ):
                        box = "B19"
                    elif component in (
                        "Wire to Board Converter (Large)","Wire to Board Converter (Small)" ,"Loadcell Amplifier","Reliment","PIC 18 Development Board"
                    ):
                        box = "B20"
                    elif component in (
                        "Potentiometer","LED RED","LED GREEN","LED YELLOW","JUMBO LED RED","JUMBO LED WHITE","Relay",
                        "Jumbo LED","IR Transmitter","IR Reciever" 
                    ):
                        box = "B21"
                    elif component in (
                        "Capacitor 1 microF","Resistor","ICs","4K79 pins","4K75 pins","Ceramic capacitor 22 pF"
                    ):
                        box = "B22"
                    elif component in (
                        "JHD 16/2A(ALL)","IR SENSOR SN103810","AUX MALE TO FEMALE CONNECTOR","IIC OLED SSD1306","Camera","Pushbutton PCB"
                    ):
                        box = "B23"

                    admin_tree.insert("", "end", values=(box, component, quantity))

                back_button = tk.Button(
                    admin_window,
                    text="Back to Home",
                    font=("Arial", 12),
                    bg="#E8E8E8",
                    fg="#333333",
                    command=admin_window.destroy
                )
                back_button.pack(pady=10)

                admin_window.geometry(
                    "+{}+{}".format(int(root.winfo_screenwidth() / 2 - admin_window.winfo_reqwidth() / 2),
                                    int(root.winfo_screenheight() / 2 - admin_window.winfo_reqheight() / 2)))
            else:
                messagebox.showinfo("Access Denied", "Incorrect password entered!")

        submit_button = tk.Button(
            password_window,
            text="Submit",
            font=("Arial", 12),
            bg="#E8E8E8",
            fg="#333333",
            command=check_password
        )
        submit_button.pack(pady=10)

        password_window.geometry(
            "+{}+{}".format(int(root.winfo_screenwidth() / 2 - password_window.winfo_reqwidth() / 2),
                            int(root.winfo_screenheight() / 2 - password_window.winfo_reqheight() / 2)))


def open_cart_window():
    cart_window = tk.Toplevel(root)
    cart_window.title("Your Cart")
    cart_window.attributes("-fullscreen", True)  # Set window to fullscreen
    cart_window.configure(bg="#F7F7F7")  # Set background color

    # Add components and functionality for the cart window here
    cart_label = tk.Label(cart_window, text="Your Cart", font=("Helvetica", 16, "bold"), fg="#333333", bg="#F7F7F7")
    cart_label.pack(pady=20)

    for item in cart_data:
        component_box, component, quantity = item
        # Update the box name if the component belongs to Box B2
        if component in ("Ultrasonic Sensor", "Temp Sensor", "IR Sensor"):
            component_box = "B2"

        cart_item_label = tk.Label(
            cart_window,
            text=f"Box: {component_box} | Component: {component} | Quantity: {quantity}",
            font=("Arial", 12),
            fg="#333333",
            bg="#E8E8E8"
        )
        cart_item_label.pack(pady=5)

    # Button to place the order
    place_order_button = tk.Button(
        cart_window,
        text="Place Order",
        font=("Arial", 12),
        bg="#E8E8E8",
        fg="#333333",
        command=place_order
    )
    place_order_button.pack(pady=10)

    # Button to go back to the home screen
    back_button = tk.Button(
        cart_window,
        text="Back to Home",
        font=("Arial", 12),
        bg="#E8E8E8",
        fg="#333333",
        command=cart_window.destroy
    )
    back_button.pack(pady=10)

    # Center the window
    cart_window.geometry("+{}+{}".format(int(root.winfo_screenwidth() / 2 - cart_window.winfo_reqwidth() / 2),
                                         int(root.winfo_screenheight() / 2 - cart_window.winfo_reqheight() / 2)))


def place_order():
    # Create a pop-up window to get user input
    popup_window = tk.Toplevel(root)
    popup_window.title("Contact Information")
    popup_window.configure(bg="#F7F7F7")

    name_label = tk.Label(popup_window, text="Name:", font=("Helvetica", 12), fg="#333333", bg="#F7F7F7")
    name_label.pack(pady=10)
    name_entry = tk.Entry(popup_window, font=("Arial", 12))
    name_entry.pack(pady=5)

    classs_label = tk.Label(popup_window, text="Class:", font=("Helvetica", 12), fg="#333333", bg="#F7F7F7")
    classs_label.pack(pady=10)
    classs_entry = tk.Entry(popup_window, font=("Arial", 12))
    classs_entry.pack(pady=5)

    email_label = tk.Label(popup_window, text="Email Address:", font=("Helvetica", 12), fg="#333333", bg="#F7F7F7")
    email_label.pack(pady=10)
    email_entry = tk.Entry(popup_window, font=("Arial", 12))
    email_entry.pack(pady=5)

    contact_label = tk.Label(popup_window, text="Contact Number:", font=("Helvetica", 12), fg="#333333", bg="#F7F7F7")
    contact_label.pack(pady=10)
    contact_entry = tk.Entry(popup_window, font=("Arial", 12))
    contact_entry.pack(pady=5)

    def confirm():
        classs = classs_entry.get()
        name = name_entry.get()
        email = email_entry.get()
        contact_no = contact_entry.get()

        # Validate the entered email address and contact number
        if not email or not contact_no:
            messagebox.showwarning("Incomplete Information", "Please enter both email address and contact number.")
            return

        # Create a new window to show the order details
        order_details_window = tk.Toplevel(root)
        order_details_window.title("Order Details")
        order_details_window.attributes("-fullscreen", True)  # Set window to fullscreen
        order_details_window.configure(bg="#F7F7F7")  # Set background color

        # Add components and functionality for the order details window here
        order_label = tk.Label(order_details_window, text="Order Details", font=("Helvetica", 16, "bold"), fg="#333333",
                            bg="#F7F7F7")
        order_label.pack(pady=20)

        for item in cart_data:
            component_box, component, quantity = item
            component_box = "B1"
            if component in ("LM324N", "P9624AB", "HD74LSOOP", "74LV04SN", "74LV04N", "7483 IC", "74147 IC"):
                component_box = "B2"
            elif component in ("sharp I.R sensor", "DHT11( Temperature and humidity sensor)",
                                "Soil Sensor (with module)", "Microwave Radar Sensor(RCWL-0516)",
                                "Ultrasonic (HC-SR04)", "IR SENSOR (photo diode)"):
                component_box = "B3"
            elif component in (
                    "voice sound module (WT588D)", "voice regonition module (with mic)", "Small O-LED",
                    "4 inch 7 segment display", "8inch 7 segment  display", "2digit  7 segment (red colour)",
                    "1 digit 7 segment display (Big)", "1digit 7 segment display", "LED matrix",
                    "voltage regulator", "I2C module (RTC)*", "Crystal Oscilator", "micro crystal MS3V-T1R",
                    "Lugs", "MP3V5050g"):
                component_box = "B4"
            elif component in ("10k pot","47k Pot","470k pot","200k pot","B 1 MEG 01 pot","1k pot","103B / 10k  SMD pot","502B pot"):
                component_box = "B5"
            elif component in ("PIR sensor","Gas sensor","text to speech module","acelerometer ( adxl345) (GY521)","Microwave Radar Sensor","Hall effect sensor"):
                component_box = "B6"
            elif component in ("37 in 1 sensor kit fir arduino","Joystick", "Laser", "Buzzer module", "IR Module", "IR sensor PCB"):
                component_box = "B7"
            elif component in ("CASTER 62858" ,"RGB LED STRIPS.0"):
                component_box = "B9"
            elif component in ("Arduino port to UART","Gear Motor Driver","POWER TRANSISTOR FITTING KIT"):
                component_box = "B10"
            elif component in ("ATMEGA32","ATMEGA8"):
                component_box = "B11"
            elif component in (
                "LED","RGB","SMALL LEDS","MM74HC138N","CD74HC573E","POT","Switch","Capacitors","Connector WHITE ND BLACK",
                "Screw","Small Leds ATMEL734","SMALL F. I H0LDER","FEMALE IC HOLDER","IC HOLDER","Diodes","PIC18F14K50","PIC18F(4520)",
                "PIC18F(4550)","PIC16F877A AND DS13020538A5","16 pin round dip 20 pin base","DC Jack","1A Bridge Rectifier","Power Switch Dip k",
                "89E516RD","SOP16","PCBS","Max 232  ULN 2803 16 PIN CONNECTOR","RS232 FEMALE 7805","16 pin base 18 pin base"):
                component_box = "B12"
            elif component in (
                "OP-AMP 741 IC","NE555 IC","Fuse","10 uF capacitor","220 uF capacitor","Lever Switch","DPI Switch",
                "BC 574 Tranisitor","N7000 MOSFET","SL100B transistor","BT136-600E TRIAC","tip122 transistor","82 pF capacitor",
                "560 pF capacitor","15 pF capacitor","470 uF capacitor","LM324",
                "LM386","33 pF capacitor","150 pF capacitor","100 pF capacitor","470 pF capacitor",
                "47 pF capacitor","15 pF capacitor","68 pF capacitor","220 pF capacitor","1 k ohm resistor"
            ):
                component_box = "B13"
            elif component in ("servo motors"):
                component_box = "B14"
            elif component in (
                "A103J / A472J","Capacitor orange(10 uF)","IR infrared receiver","push buttons","IC 75ACOLM",
                "HW-221 Voltage Converter","IC 7660","N7000 transistor","LDR"
            ):
                component_box = "B15"
            elif component in (
                "numeric keypads","single button keypad","solar panel 5V","solar panel 6V","Tact Switch (3mm)","Track Rod","solar panel 10V"
            ):
                component_box = "B16"
            elif component in (
                "SIM 800A/900A GSM MODULE","GSM 6M MODULE","L9110 Motor drive","Xbeee pro"
            ):
                component_box = "B18"
            elif component in (
                "NRF 24201 (with antenna)","PCB mount mini Speaker","Transistor 512 series","TXSS0108E Logic level Converter","Wifi Relay"
            ):
                component_box = "B19"
            elif component in (
                "Wire to Board Converter (Large)","Wire to Board Converter (Small)" ,"Loadcell Amplifier","Reliment","PIC 18 Development Board"
            ):
                component_box = "B20"
            elif component in (
                "Potentiometer","LED RED","LED GREEN","LED YELLOW","JUMBO LED RED","JUMBO LED WHITE","Relay",
                "Jumbo LED","IR Transmitter","IR Reciever" 
            ):
                component_box = "B21"
            elif component in (
                "Capacitor 1 microF","Resistor","ICs","4K79 pins","4K75 pins","Ceramic capacitor 22 pF"
            ):
                component_box = "B22"
            elif component in (
                "JHD 16/2A(ALL)","IR SENSOR SN103810","AUX MALE TO FEMALE CONNECTOR","IIC OLED SSD1306"
            ):
                component_box = "B23"

            order_item_label = tk.Label(
                order_details_window,
                text=f"Box: {component_box} | Component: {component} | Quantity: {quantity}",
                font=("Arial", 12),
                fg="#333333",
                bg="#E8E8E8"
            )
            order_item_label.pack(pady=5)
            component_availability[component] -= int(quantity)  # Update component availability

        # Button to go back to the home screen
        back_button = tk.Button(
            order_details_window,
            text="Back to Home",
            font=("Arial", 12),
            bg="#E8E8E8",
            fg="#333333",
            command=order_details_window.destroy  # Close the order details window
        )
        back_button.pack(pady=10)

        # Center the window
        order_details_window.geometry(
            "+{}+{}".format(int(root.winfo_screenwidth() / 2 - order_details_window.winfo_reqwidth() / 2),
                            int(root.winfo_screenheight() / 2 - order_details_window.winfo_reqheight() / 2)))

        # Send email to the user
        msg = MIMEMultipart()
        msg['From'] = my_email
        msg['To'] = email
        msg['Subject'] = "ISA INVENTORY - Order Details"

        body = "Thank You for using ISA INVENTORY! Below Are Your Order Details:\n\n"
        body += "\n".join([f"Component: {component}, Quantity: {quantity}" for _, component, quantity in cart_data])
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(my_email, password)
            server.sendmail(my_email, email, msg.as_string())
            server.quit()

            connection = smtplib.SMTP("smtp.gmail.com")
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs="2021.shobhit.rajguru@ves.ac.in",
                msg=f"Subject:ISA INVENTORY!\n\n"+
                    "The Order Was Placed!\n\n" +
                    "Below Are Order Details:-\n\n" +
                    "\n".join([f"Name: {name}, Class: {classs}, Email: {email}, Contact: {contact_no}, Component: {component}, Quantity: {quantity}, Box: {component_box}" for _, component, quantity in cart_data]))

            # Success message
            messagebox.showinfo("Order Placed", "Your order details have been sent to your email address.")

            cart_data.clear()

            # Call the function to update components_data after placing an order
            update_component_availability_after_order()

            # Close the pop-up window
            popup_window.destroy()

        except Exception as e:
            # Error message if email sending fails
            messagebox.showerror("Error", "Failed to send email. Please check your internet connection and try again.")

    confirm_button = tk.Button(popup_window, text="Confirm", font=("Arial", 12), bg="#E8E8E8", fg="#333333",
                               command=confirm)
    confirm_button.pack(pady=10)

    # Center the pop-up window
    popup_window.geometry("+{}+{}".format(int(root.winfo_screenwidth() / 2 - popup_window.winfo_reqwidth() / 2),
                                          int(root.winfo_screenheight() / 2 - popup_window.winfo_reqheight() / 2)))

    # Stop the execution of the rest of the function until the pop-up window is closed
    root.wait_window(popup_window)

def open_orders_window():
    orders_window = tk.Toplevel(root)
    orders_window.title("Place Order")
    orders_window.attributes("-fullscreen", True)  # Set window to fullscreen
    orders_window.configure(bg="#F7F7F7")  # Set background color

    # Add components and functionality for the orders window here
    def add_to_cart():
        global component_dropdown

        selected_component = component_var.get()
        selected_quantity = quantity_entry.get()

        if component_availability[selected_component] < int(selected_quantity):
            messagebox.showinfo("Out of Stock",
                                "Sorry, We are out of stock for the component: {}".format(selected_component))
            return

        cart_data.append((selected_box.get(), selected_component, selected_quantity))
        # component_availability[selected_component] -= int(selected_quantity)  # Update component availability
        orders_window.destroy()

    # Create a frame to center the components
    center_frame = tk.Frame(orders_window, bg="#F7F7F7")
    center_frame.pack(expand=True)

    # Add a label to display the initial text
    initial_text_label = tk.Label(center_frame, text="FILL YOUR CART HERE", font=("Helvetica", 20, "bold"),
                                  fg="#333333", bg="#F7F7F7")
    initial_text_label.pack(pady=20)

    component_label = tk.Label(center_frame, text="Select Component:", font=("Arial", 12), bg="#F7F7F7")
    component_label.pack(pady=10)

    component_var = tk.StringVar()
    component_dropdown = ttk.Combobox(center_frame, textvariable=component_var, font=("Arial", 12))
    component_dropdown['values'] = tuple(component_availability.keys())  # Use component_availability dict keys
    component_dropdown.pack(pady=5)

    quantity_label = tk.Label(center_frame, text="Quantity:", font=("Arial", 12), bg="#F7F7F7")
    quantity_label.pack(pady=10)

    quantity_entry = tk.Entry(center_frame, font=("Arial", 12))
    quantity_entry.pack(pady=5)

    selected_box = tk.StringVar(value="B1")  # Default value is B1

    add_to_cart_button = tk.Button(
        center_frame,
        text="Add to Cart",
        font=("Arial", 12),
        bg="#E8E8E8",
        fg="#333333",
        command=add_to_cart
    )
    add_to_cart_button.pack(pady=10)

    # Button to go back to the home screen
    back_button = tk.Button(
        orders_window,
        text="Back to Home",
        font=("Arial", 12),
        bg="#E8E8E8",
        fg="#333333",
        command=orders_window.destroy
    )
    back_button.pack(pady=10)

    # Center the window
    orders_window.geometry(
        "+{}+{}".format(int(root.winfo_screenwidth() / 2 - orders_window.winfo_reqwidth() / 2),
                        int(root.winfo_screenheight() / 2 - orders_window.winfo_reqheight() / 2)))

def on_add_component_window_close():
    # Save the updated component_availability to the JSON file
    save_data_to_file()

def open_add_component_window():
    add_component_window = tk.Toplevel(root)
    add_component_window.title("Add Component")
    add_component_window.configure(bg="#F7F7F7")

    component_name_label = tk.Label(add_component_window, text="Component Name:", font=("Helvetica", 12),
                                     fg="#333333", bg="#F7F7F7")
    component_name_label.pack(pady=10)

    component_name_entry = tk.Entry(add_component_window, font=("Arial", 12))
    component_name_entry.pack(pady=5)

    component_quantity_label = tk.Label(add_component_window, text="Initial Quantity:", font=("Helvetica", 12),
                                        fg="#333333", bg="#F7F7F7")
    component_quantity_label.pack(pady=10)

    component_quantity_entry = tk.Entry(add_component_window, font=("Arial", 12))
    component_quantity_entry.pack(pady=5)

    def add_new_component():
        new_component_name = component_name_entry.get()
        new_component_quantity = component_quantity_entry.get()

        # Validate input
        if not new_component_name or not new_component_quantity:
            messagebox.showwarning("Incomplete Information", "Please enter both component name and initial quantity.")
            return

        # Add the new component to the availability dictionary
        component_availability[new_component_name] = int(new_component_quantity)

        # Save the updated component_availability to the JSON file
        save_data_to_file()

        add_component_window.destroy()

    confirm_button = tk.Button(add_component_window, text="Confirm", font=("Arial", 12), bg="#E8E8E8", fg="#333333",
                               command=add_new_component)
    confirm_button.pack(pady=10)

    # Center the window
    add_component_window.geometry("+{}+{}".format(int(root.winfo_screenwidth() / 2 - add_component_window.winfo_reqwidth() / 2),
                                                  int(root.winfo_screenheight() / 2 - add_component_window.winfo_reqheight() / 2)))

    
def on_exit():
    # Save data to a JSON file before exiting
    save_data_to_file()
    root.destroy()

# Create the main window
root = tk.Tk()
root.attributes("-fullscreen", True)  # Set window to fullscreen
root.configure(bg="#F7F7F7")  # Set background color
root.title("Component Ordering System")

# Initialize the cart data list
cart_data = []

# Add components and functionality for the main window here
title_label = tk.Label(root, text="Welcome to Component Ordering System", font=("Helvetica", 20, "bold"),
                       fg="#333333", bg="#F7F7F7")
title_label.pack(pady=50)


orders_button = tk.Button(root, text="Your Order", font=("Arial", 16), bg="#E8E8E8", fg="#333333",
                          command=open_orders_window)
orders_button.pack(pady=20)

cart_button = tk.Button(root, text="Your Cart", font=("Arial", 16), bg="#E8E8E8", fg="#333333",
                        command=open_cart_window)
cart_button.pack(pady=20)

admin_button = tk.Button(root, text="ISA Admin", font=("Arial", 16), bg="#E8E8E8", fg="#333333", command=open_admin_window)
admin_button.pack(pady=20)

quit_button = tk.Button(root, text="Exit", font=("Arial", 16), bg="#E8E8E8", fg="#333333", command=root.quit)
quit_button.pack(pady=20)

# Center the window
root.geometry("+{}+{}".format(int(root.winfo_screenwidth() / 2 - root.winfo_reqwidth() / 2),
                              int(root.winfo_screenheight() / 2 - root.winfo_reqheight() / 2)))

# Add this function call to load data from the JSON file upon application startup
load_data_from_file()

# Add this function call to save data to the JSON file before exiting
root.protocol("WM_DELETE_WINDOW", on_exit)

# Start the Tkinter event loop
root.mainloop()
