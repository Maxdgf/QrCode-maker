import customtkinter as ctk
import qrcode
import time
import os
from random import randint
import platform
import subprocess
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import colorchooser
import threading
from PIL import Image

#This is a few improved version of this program. Now you can attach the central photo to the qrcode here!
         
ctk.set_default_color_theme("green")    

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("QrCode Master")    
        self.geometry("800x800")
        self.icon_path = os.path.join(os.path.dirname(__file__), 'qrCodeLogo.ico')
        self.iconbitmap(self.icon_path)

        self.widgetFrame = ctk.CTkFrame(self, border_color="#1E90FF", border_width=5)
        #self.widgetFrame.pack_propagate(True)
        self.theme = "dark"
        ctk.set_appearance_mode(self.theme)

        self.labelName = ctk.CTkLabel(self, text="QrCode Master", text_color="#00BFFF", font=("Arial", 50))
        self.labelName.pack()

        self.description = ctk.CTkLabel(self.widgetFrame, text="Make your custom QR code", text_color="#1E90FF")
        self.description.pack(anchor="center")

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
        self.filePathFrame.pack(pady=10)

        self.sizeFrame = ctk.CTkFrame(self.widgetFrame)
        self.sizeLabeldescription = ctk.CTkLabel(self.sizeFrame, text="qrcode size: ", text_color="#00BFFF", font=("Arial", 15))
        self.sizeLabeldescription.pack(side="left")
        self.slider = ctk.CTkSlider(self.sizeFrame, from_=0, to=50, orientation="horizontal",  button_color="#1E90FF", button_hover_color="#00BBFB", command=self.slider_event)
        self.slider.pack(side="left")
        self.slider.set(10)
        self.slValue = self.slider.get()
        self.sizeLabel = ctk.CTkLabel(self.sizeFrame, text="0/50")
        self.sizeLabel.pack(side="left")
        self.sizeFrame.pack(pady=10)
        int(self.slValue)
        self.sizeLabel.configure(text=f"{self.slValue}/50")

        self.borderFrame = ctk.CTkFrame(self.widgetFrame)
        self.borderLabeldescription = ctk.CTkLabel(self.borderFrame, text="qrcode border: ", text_color="#00BFFF", font=("Arial", 15))
        self.borderLabeldescription.pack(side="left")
        self.slider2 = ctk.CTkSlider(self.borderFrame, from_=0, to=50, orientation="horizontal", button_color="#1E90FF", button_hover_color="#00BBFB", command=self.slider_event2)
        self.slider2.pack(side="left")
        self.slider2.set(5)
        self.slValue2 = self.slider2.get()
        self.borderLabel = ctk.CTkLabel(self.borderFrame, text="0/50")
        self.borderLabel.pack(side="left")
        self.borderFrame.pack(pady=10)
        int(self.slValue2)
        self.borderLabel.configure(text=f"{self.slValue2}/50")

        self.fillcFrame = ctk.CTkFrame(self.widgetFrame)
        self.descLabel = ctk.CTkLabel(self.fillcFrame, text="fill color: not selected", text_color="#00BFFF", font=("Arial", 15))
        self.descLabel.pack(side="left")
        self.colorLabel = ctk.CTkLabel(self.fillcFrame, width=80, bg_color="white", text="")
        self.colorLabel.pack(side="left")
        self.btnSelectColor = ctk.CTkButton(self.fillcFrame, text="select", fg_color="#1E90FF", hover_color="#00BFFF", command=self.fill_colorEvent)
        self.btnSelectColor.pack(side="left")
        self.fillcFrame.pack(pady=10)
        
        self.backcFrame = ctk.CTkFrame(self.widgetFrame)
        self.descLabel2 = ctk.CTkLabel(self.backcFrame, text="back color: not selcted", text_color="#00BFFF", font=("Arial", 15))
        self.descLabel2.pack(side="left")
        self.colorLabel2 = ctk.CTkLabel(self.backcFrame, width=80, bg_color="white", text="")
        self.colorLabel2.pack(side="left")
        self.btnSelectColor2 = ctk.CTkButton(self.backcFrame, text="select", fg_color="#1E90FF", hover_color="#00BFFF", command=self.back_colorEvent)
        self.btnSelectColor2.pack(side="left")
        self.backcFrame.pack(pady=10)

        self.attachFrame = ctk.CTkFrame(self.widgetFrame)
        self.btnAttachImage = ctk.CTkButton(self.attachFrame, text="attach image", fg_color="#0000FF", hover_color="#00BFFF", border_color="#1E90FF", border_width=3, command=self.attach_image)
        self.btnAttachImage.pack(side="left")
        self.attachFrame.pack_forget()

        self.attachFileInfo = ctk.CTkLabel(self.widgetFrame, text="attach file: none", text_color="#00BFFF", font=("Arial", 15))
        self.attachFileInfo.pack_forget()

        self.enableAttachFilesCheckboxFrame = ctk.CTkFrame(self.widgetFrame)
        self.enableVar = ctk.StringVar(value="off")
        self.enableAttachCheckbox = ctk.CTkCheckBox(self.enableAttachFilesCheckboxFrame, text="enable attach files: ", onvalue="on", offvalue="off", variable=self.enableVar, text_color="#00BFFF", border_color="#00BFFF", border_width=3, fg_color="#00BFFF", hover_color="#1E90FF", command=self.checkbox_event)
        self.enableAttachCheckbox.pack(side="left")
        self.enableView = ctk.CTkLabel(self.enableAttachFilesCheckboxFrame, text="off", text_color="red")
        self.enableView.pack(side="left")
        self.enableAttachFilesCheckboxFrame.pack(pady=10)

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

    def fill_colorEvent(self):
        self.fillcolor = colorchooser.askcolor(title="choose fill color")
        if self.fillcolor[1] is not None:
            self.colorLabel.configure(fg_color=self.fillcolor[1], text=self.fillcolor, text_color="black")
            self.descLabel.configure(text="fill color: selected")

    def back_colorEvent(self):
        self.backcolor = colorchooser.askcolor(title="choose back color")
        if self.backcolor[1] is not None:
            self.colorLabel2.configure(fg_color=self.backcolor[1], text=self.backcolor, text_color="black")
            self.descLabel2.configure(text="back color: selected")

    def checkbox_event(self):
        self.value = self.enableVar.get()
        if self.value == "off":
            #print("off")
            self.attachFrame.pack_forget()
            self.attachFileInfo.pack_forget()
            self.enableView.configure(text_color="red", text="off")
        elif self.value == "on":
            #print("on")
            self.attachFrame.pack(pady=10)
            self.attachFileInfo.pack(padx=5)
            self.enableView.configure(text_color="green", text="on")

    def attach_image(self):
        self.isEnabled = self.enableVar.get()
        
        self.attachImageFilePath = filedialog.askopenfilename(title="Select image file", filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])
        self.attachFileInfo.configure(text=f"attach file {self.attachImageFilePath}")

        if len(self.attachImageFilePath) == 0:
            messagebox.showwarning("Warning", "attach image not slected!")
            self.attachFileInfo.configure(text="attach file: :(")


    def slider_event(self, value):
        self.num = int(value)
        self.sizeLabel.configure(text=f"{self.num}/50")
        #print(value)

    def slider_event2(self, value):
        self.num2 = int(value)
        self.borderLabel.configure(text=f"{self.num2}/50")
        #print(value)

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
            self.file_path = filedialog.askdirectory(title="Select directory")
            str(self.file_path)
            self.pathLabael.configure(text=f"file path: {self.file_path}")
            if len(self.file_path) == 0:
                messagebox.showwarning("Warning", "File path is empty! Please fix it.")
                self.pathLabael.configure(text="file path: :(")
            #print(self.file_path)
        except:
            messagebox.showerror("Error", "Operation failed! Directory not found, please, try again.")

    def create_qrcode(self):
        self.link = self.NameString.get()
        self.format = self.FormatBox.get()
        self.name = self.filenameString.get()
        self.attachIsEnabled = self.enableVar.get()
        if len(self.name) == 0:
            self.name = f"untitled{randint(0, 1000)}"
        self.size = self.slider.get()
        self.border = self.slider2.get()
        self.qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=int(self.size), border=int(self.border))
        self.qr.add_data(self.link)
        self.qr.make(fit=True)
        self.progressBar.set(0.5)
        self.progressIndekator.configure(text="50%")
        try:
            if self.attachIsEnabled == "off":
                self.progressBar.set(1)
                self.progressIndekator.configure(text="100%")
                self.img = self.qr.make_image(fill_color=self.fillcolor[1], back_color=self.backcolor[1])
                self.img.save(self.file_path + f"/{self.name}{self.format}")
                messagebox.showinfo("Info", f"QrCode was created and saved!\nfile path: {self.file_path}/{self.name}{self.format}")
                self.path_to_file = os.path.join(self.file_path, f"{self.name}{self.format}")
                #os.startfile(self.path_to_file)
                if platform.system() == "Windows":
                    os.startfile(self.path_to_file)
                elif platform.system() == "Darwin":
                    subprocess.run(["open", self.path_to_file])
                else:
                    subprocess.run(["xdg-open", self.path_to_file])
                time.sleep(2)
                self.progressBar.set(0)
                self.progressIndekator.configure(text="0%")
            elif self.attachIsEnabled == "on":
                self.progressBar.set(0.8)
                self.progressIndekator.configure(text="80%")
                self.attachImage = Image.open(self.attachImageFilePath)
                self.width = 100
                self.wpercent = (self.width/float(self.attachImage.size[0]))
                self.height = int((float(self.attachImage.size[1])*float(self.wpercent)))
                self.attachImage = self.attachImage.resize((self.width, self.height), Image.Resampling.LANCZOS)
                
                self.img = self.qr.make_image(fill_color=self.fillcolor[1], back_color=self.backcolor[1])
                self.pos = ((self.img.size[0] - self.attachImage.size[0]) // 2, (self.img.size[1] - self.attachImage.size[1]) // 2)
                self.img.paste(self.attachImage, self.pos)
                self.img.save(self.file_path + f"/{self.name}{self.format}")
                self.progressBar.set(1)
                self.progressIndekator.configure(text="100%")
                messagebox.showinfo("Info", f"QrCode was created and saved!\nfile path: {self.file_path}/{self.name}{self.format}")
                self.path_to_file = os.path.join(self.file_path, f"{self.name}{self.format}")
                #os.startfile(self.path_to_file)
                if platform.system() == "Windows":
                    os.startfile(self.path_to_file)
                elif platform.system() == "Darwin":
                    subprocess.run(["open", self.path_to_file])
                else:
                    subprocess.run(["xdg-open", self.path_to_file])
                time.sleep(2)
                self.progressBar.set(0)
                self.progressIndekator.configure(text="0%")

        except:
            self.progressBar.stop()
            self.progressBar.set(0)
            self.progressIndekator.configure(text="0%")
            messagebox.showerror("Error", "A QrCode creation error, please check all the \nsettings(url, file format, file name, file path and other parametrs) and try again.")

    def paste_text(self):
        self.text = self.clipboard_get()
        self.NameString.insert("end", self.text)
             
if __name__ == "__main__":
    app = App()
    app.mainloop()  
