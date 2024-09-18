import customtkinter as ctk
import qrcode
import time
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk, Image
         
ctk.set_default_color_theme("green")    

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("QrCode Master")    
        self.geometry("800x500")

        self.widgetFrame = ctk.CTkFrame(self)
        #self.widgetFrame.pack_propagate(True)
        self.theme = "dark"
        ctk.set_appearance_mode(self.theme)

        self.labelName = ctk.CTkLabel(self, text="QrCode Master", text_color="#00BFFF", font=("Arial", 50))
        self.labelName.pack()

        self.switchVar = ctk.StringVar(value="off")
        self.switchTheme = ctk.CTkSwitch(self, text="dark/light theme", fg_color="#1E90FF", command=self.switch_theme, variable=self.switchVar, onvalue="on", offvalue="off")
        self.switchTheme.place(x=0, y=0)

        self.urlFrame = ctk.CTkFrame(self.widgetFrame)
        self.NameString = ctk.CTkEntry(self.urlFrame, width=600, placeholder_text="enter url", border_color="#00BBFB", border_width=3)
        self.NameString.pack(side="left")   
        self.btnPaste = ctk.CTkButton(self.urlFrame, width=10, text="paste", fg_color="#1E90FF", hover_color="#00BFFF", command=self.paste_text) #00BFFF  #1E90FF
        self.btnPaste.pack(side="left")
        self.urlFrame.pack(pady=20)

        self.formatFrame = ctk.CTkFrame(self.widgetFrame)
        self.labelName2 = ctk.CTkLabel(self.formatFrame, text="select file format ", text_color="#00BFFF", font=("Arial", 15))
        self.labelName2.pack(side="left")
        self.FormatBox = ctk.CTkComboBox(self.formatFrame, values=[".png", ".jpg", ".jpeg", ".bmp"], border_color="#00BFFF", border_width=3, width=100)
        self.FormatBox.pack(side="left")
        self.formatFrame.pack()

        self.filePathFrame = ctk.CTkFrame(self.widgetFrame)
        self.pathLabael = ctk.CTkLabel(self.filePathFrame, text="file path: select file path! ", text_color="#00BFFF", font=("Arial", 15))
        self.pathLabael.pack(side="left")
        self.btnSelectPath = ctk.CTkButton(self.filePathFrame, text="select", fg_color="#1E90FF", hover_color="#00BFFF", command=self.open_filedialog)
        self.btnSelectPath.pack(side="left")
        self.filePathFrame.pack(pady=30)

        self.filenameString = ctk.CTkEntry(self.widgetFrame, width=500, placeholder_text="enter filename", border_color="#00BBFB", border_width=3)
        self.filenameString.pack()

        self.progressFrame = ctk.CTkFrame(self.widgetFrame)
        self.progressBar = ctk.CTkProgressBar(self.progressFrame, orientation="horizontal", width=300, )
        self.progressBar.pack(side="left")
        self.progressBar.set(0)
        self.progressIndekator = ctk.CTkLabel(self.progressFrame, text="0%")
        self.progressIndekator.pack(side="left")
        self.progressFrame.pack(pady=10)

        self.btnStart = ctk.CTkButton(self.widgetFrame, width=300, height=100, text="Create QrCode", fg_color="#1E90FF", hover_color="#00BFFF", command=self.create_qrcode)
        self.btnStart.pack(pady=10)

        self.widgetFrame.pack(expand=True)

    def switch_theme(self):
        #print("value:" + self.switchVar.get())
        self.value = self.switchVar.get()
        if self.value == "off":
            self.theme = "dark"
            ctk.set_appearance_mode(self.theme)
        elif self.value == "on":
            self.theme = "light"
            ctk.set_appearance_mode(self.theme)

    def open_filedialog(self):
        try:
            self.file_path = filedialog.askdirectory()
            str(self.file_path)
            self.pathLabael.configure(text="file path: " + self.file_path + " ")
            if len(self.file_path) == 0:
                messagebox.showwarning("Warning", "File path is empty! Please fix it.")
            #print(self.file_path)
        except:
            messagebox.showerror("Error", "Operation failed! Directory not found, please, try again.")

    def create_qrcode(self):
        self.link = self.NameString.get()
        self.format = self.FormatBox.get()
        self.name = self.filenameString.get()
        self.img = qrcode.make(self.link)
        self.progressBar.set(0.5)
        self.progressIndekator.configure(text="50%")
        try:
            self.progressBar.set(1)
            self.progressIndekator.configure(text="100%")
            type(self.img)
            self.img.save(self.file_path + f"/{self.name}{self.format}")
            messagebox.showinfo("Info", f"QrCode was created and saved!\nfile path: {self.file_path}/{self.name}{self.format}")
            time.sleep(2)
            self.progressBar.set(0)
            self.progressIndekator.configure(text="0%")
        except:
            self.progressBar.stop()
            self.progressBar.set(0)
            self.progressIndekator.configure(text="0%")
            messagebox.showerror("Error", "A QrCode creation error, please check all the settings and try again.")

    def paste_text(self):
        self.text = self.clipboard_get()
        self.NameString.insert("end", "text")
             
if __name__ == "__main__":
    app = App()
    app.mainloop()  
