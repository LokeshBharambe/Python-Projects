import tkinter as tk

def decimal_to_binary():
    try:
        decimal_num = int(input_field.get())
        binary_num = bin(decimal_num).replace("0b", "")
        output_label.config(text=f"Binary: {binary_num}")
    except ValueError:
        output_label.config(text="Invalid input. Please enter a decimal number.")

def binary_to_decimal():
    try:
        binary_num = input_field.get()
        decimal_num = int(binary_num, 2)
        output_label.config(text=f"Decimal: {decimal_num}")
    except ValueError:
        output_label.config(text="Invalid input. Please enter a valid binary number.")

def clear_output():
    output_label.config(text="")

def convert():
    input_text = input_field.get()
    if input_text.isdigit():
        decimal_to_binary()
    else:
        try:
            int(input_text, 2)  # Check if input is a valid binary number
            binary_to_decimal()
        except ValueError:
            output_label.config(text="Invalid input. Please enter a valid number.")

root = tk.Tk()
root.title("Binary-Decimal Converter")

menu_frame = tk.Frame(root)
menu_frame.grid(row=0, column=0, columnspan=2, pady=10)

decimal_to_binary_button = tk.Button(menu_frame, text="Decimal to Binary", command=decimal_to_binary, width=15)
decimal_to_binary_button.grid(row=0, column=0, padx=5)

binary_to_decimal_button = tk.Button(menu_frame, text="Binary to Decimal", command=binary_to_decimal, width=15)
binary_to_decimal_button.grid(row=0, column=1, padx=5)

clear_button = tk.Button(root, text="Clear", command=clear_output, width=10)
clear_button.grid(row=1, column=0, pady=5)

convert_button = tk.Button(root, text="Convert", command=convert, width=10)
convert_button.grid(row=1, column=1, pady=5)

input_field = tk.Entry(root, width=30)
input_field.grid(row=2, column=0, columnspan=2, pady=5)

output_label = tk.Label(root, text="", pady=20, width=30, height=3, bg="white", relief="sunken", anchor="w")
output_label.grid(row=3, column=0, columnspan=2, pady=10, padx=10)

root.mainloop()
