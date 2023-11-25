import time
import datetime
import threading
from tkinter import ttk
from tkinter import *
from tkinter.messagebox import askyesno
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


con = sqlite3.connect("kayit.db")

cursor = con.cursor()

def tablo_oluştur():
    cursor.execute("CREATE TABLE IF NOT EXISTS kayit (Date TEXT, Name Text, Tamamlanma INT, Süre INT)") # Sorguyu çalıştırıyoruz.
    cursor.execute("CREATE TABLE IF NOT EXISTS tabs (Tab_Name TEXT, Tab_Time INT)")
    con.commit()

tablo_oluştur()

con.close()


class Tab:
    def __init__(self,tab_name,minute,notebook) -> None:
        self.name = tab_name
        self.seconds = 60* minute 
        self.count = 0
        self.tab = ttk.Frame(notebook, width=600, height=100)
        self.timer_label = ttk.Label(self.tab, text= minute, font=("Ubuntu", 48))
        self.timer_label.pack(pady=20)
        self.counter_label = ttk.Label(self.tab, text= tab_name + " Tamamlandı: 0", font=("Ubuntu", 16))
        self.counter_label.pack(pady=10)

class PomodoroTimer:


    def __init__(self):
        # windows init stuf 
        self.root = Tk()
        self.root.geometry("600x400")
        self.root.title("Pomodoro Timer")
        
        
        self.s = ttk.Style()
        self.s.configure("TNotebook.Tab", font=("Ubuntu", 12))
        self.s.configure("TButton.Tab", font=("Ubuntu", 12))
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", pady=10, expand=True)
        self.tabs =[]

        self.Tabs = {}

        con = sqlite3.connect("kayit.db")

        cursor = con.cursor()

        cursor.execute("SELECT Tab_Name, Tab_Time FROM tabs")
        records_tabs = cursor.fetchall()
        con.commit()

        con.close()

        for i in records_tabs:
            self.Tabs[i[0]] = i[1]
        
        for tab_name,minute in self.Tabs.items():
            tab = Tab(tab_name,minute,self.notebook)
            self.tabs.append(tab)
            self.notebook.add(tab.tab,text = tab_name)

        self.grid_layout = ttk.Frame(self.root)
        self.grid_layout.pack(pady=10)
        
        self.start_button = ttk.Button(self.grid_layout, text="Başlat", command=self.baslat_thread)
        self.start_button.grid(row=0, column=0)

        self.stop_button = ttk.Button(self.grid_layout, text="Duraklat", command=self.duraklat_clock)
        self.stop_button.grid(row=0, column=1)

        self.end_button = ttk.Button(self.grid_layout, text="Bitir", command=self.bitir_clock)
        self.end_button.grid(row=0, column=2)
        
        self.ekle_button = ttk.Button(self.grid_layout, text= 'Görev Ekle', command= self.gorev_ekle)
        self.ekle_button.grid(row=0, column=3)
        
        self.sil_button = ttk.Button(self.grid_layout, text= 'Görevi Sil', command= self.gorev_sil)
        self.sil_button.grid(row=0, column=4)
        
        """self.canvas = FigureCanvasTkAgg(fig, master = self.root)
        self.canvas.get_tk_widget().pack(pady=10)"""
        
        self.duraklat = False
        self.running = False
        self.bitir = False
        
        self.root.protocol("WM_DELETE_WINDOW", self.confirm)
        self.root.mainloop()
                

        
    def baslat_thread(self):
        if not self.running:
            t = threading.Thread(target=self.baslat)
            t.start()
            self.running = True

    def baslat(self):
        self.duraklat = False
        self.bitir = False
        timer_id = self.notebook.index(self.notebook.select()) 
        

        while self.tabs[timer_id].seconds > 0 and not self.duraklat:
            minutes, seconds = divmod(self.tabs[timer_id].seconds, 60)
            self.tabs[timer_id].timer_label.configure(text=f"{minutes:02d}:{seconds:02d}")
            self.root.update()
            time.sleep(1)
            self.tabs[timer_id].seconds -= 1
            if self.duraklat or self.bitir:
                    break
        if not self.duraklat and not self.bitir:
            self.tabs[timer_id].count += 1
            self.tabs[timer_id].seconds = 60 * self.Tabs.get(self.tabs[timer_id].name)
            self.tabs[timer_id].counter_label.config(text=f"{self.tabs[timer_id].name} Tamamlandı: {self.tabs[timer_id].count}")

    def duraklat_clock(self):
        duraklat_id = self.notebook.index(self.notebook.select()) 
        self.duraklat = True
        self.bitir = False
        
        self.running = False
        
        time.sleep(0.5)

    def bitir_clock(self):
        bitir_id = self.notebook.index(self.notebook.select())
        self.duraklat = True
        self.bitir = True

        self.tabs[bitir_id].timer_label.config(text=f"{self.Tabs.get(self.tabs[bitir_id].name)}:00")
        self.tabs[bitir_id].seconds = self.Tabs.get(self.tabs[bitir_id].name) * 60
        time.sleep(0.5)
        self.running = False

    def kaydet(self):  # Close Event; Save Data
        date = datetime.date.today()
        """con = sqlite3.connect("kayit.db")

        cursor = con.cursor()

        def veri_ekle():
            cursor.execute("Insert into kayit Values(?,?,?,?)",(date,name,tamamlanma,count.seconds/60))
            con.commit()

        veri_ekle()

        con.close()"""
    
    def confirm(self):  # Close Event Handling
        ans = askyesno(title='Exit', message='Kapatmak mı istiyorsun?')
        if ans:
            self.kaydet()
            self.root.destroy()

    def gorev_ekle(self):
        self.gorev = Tk()
        self.gorev.geometry("400x100")
        self.gorev.title("Görev Ekle")

        self.grid_layout_gorev = ttk.Frame(self.gorev)
        self.grid_layout_gorev.pack(pady=10)
        
        self.name_entry_text = Label(self.grid_layout_gorev, text='Görev Adı')
        self.name_entry_text.grid(row=0, column=0)
        
        self.name_entry = Entry(self.grid_layout_gorev, width= 30, borderwidth= 3)
        self.name_entry.grid(row=0, column=1)
        
        self.time_entry_text = Label(self.grid_layout_gorev, text='Süre')
        self.time_entry_text.grid(row=1, column=0)
        
        self.time_entry = Entry(self.grid_layout_gorev, width= 30, borderwidth= 3)
        self.time_entry.grid(row=1, column=1)
        
        self.gorev_ekle_button = ttk.Button(self.grid_layout_gorev, text= 'Görevi Ekle', command= self.gorev_id_input)
        self.gorev_ekle_button.grid(row=2,column=2)
        
    def refresh_ekle(self, name_entry, time_entry):
        self.Tabs[name_entry] = int(time_entry)
        tab = Tab(name_entry,int(time_entry),self.notebook)
        self.tabs.append(tab)
        self.notebook.add(tab.tab,text = name_entry)
        
        self.refresh()
        
    def refresh_sil(self, name_entry, tab_id):
        self.notebook.forget(self.notebook.index(self.notebook.select()))
        self.Tabs.pop(name_entry)
        self.tabs.pop(tab_id)
        
        self.refresh()
          
    def refresh(self):
        self.root.update()
        self.root.update_idletasks()
    
    def gorev_id_input(self):
        tab_name_input = self.name_entry.get()
        tab_time_input = int(self.time_entry.get())
        
        con = sqlite3.connect("kayit.db")
        cursor = con.cursor()
        def tab_veri_ekle():
            cursor.execute("Insert into tabs Values(?,?)",(tab_name_input,tab_time_input))
            con.commit()
        tab_veri_ekle()
        
        con.close()
        
        self.gorev.destroy()
        self.refresh_ekle(tab_name_input,tab_time_input)
                         
    def gorev_sil(self):
        sil_id = self.notebook.index(self.notebook.select())
        tab_name_text = self.notebook.tab(sil_id)['text']
        tab_time_value = int(self.tabs[sil_id].seconds/60)
        
        
        con = sqlite3.connect("kayit.db")
        cursor = con.cursor()
        def tab_veri_sil():
            cursor.execute("DELETE FROM tabs WHERE Tab_Name= (?)", (tab_name_text,))
            cursor.execute("DELETE FROM tabs WHERE Tab_Time= (?)", (tab_time_value,))
            con.commit()
        tab_veri_sil()
        con.close()
        
        self.refresh_sil(tab_name_text, sil_id)
    
    
timer = PomodoroTimer()

