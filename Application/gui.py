import customtkinter
#button function
def button_callback():
    print("button clicked Haha")
#width and hieght of display
app = customtkinter.CTk()
app.geometry("1050x500")
#Buttons
button = customtkinter.CTkButton(app, text="my button", command=button_callback)
button.pack(padx=20, pady=20)
intialTextBox = customtkinter.CTK

app.mainloop()
#notes?