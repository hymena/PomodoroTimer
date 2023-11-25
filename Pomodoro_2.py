import time
import datetime
import threading
from tkinter import ttk
from tkinter import *
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


con = sqlite3.connect("kayit.db")

cursor = con.cursor()
print("hello there")
def tablo_oluştur():
    cursor.execute("CREATE TABLE IF NOT EXISTS kayit (Date TEXT, Ders INT, Kitap INT, Tarih INT, Arapça INT, Kuran INT, Ders_Süresi INT, Kitap_Süresi INT, Tarih_Süresi INT, Arapca_Süresi INT, Kuran_Süresi INT, Toplam_Süre INT)") # Sorguyu çalıştırıyoruz.
    con.commit()

tablo_oluştur()

cursor.execute("SELECT Date, Toplam_Süre FROM kayit")
records_date = cursor.fetchall()
con.commit()
con.close()

graph_dict = {}

for i in records_date:
    adim_no = records_date.index(i)
    if records_date.index(i) == 0:
        graph_dict[i[0]] = i[1]
    elif i[0] != records_date[(adim_no-1)][0]:
        print("burada")
        graph_dict[i[0]] = i[1]
    elif i[0] == records_date[(adim_no-1)][0]:
        print("burada2")
        graph_dict[i[0]] += i[1]

date_array = []
date_filler_array = []
toplam_array = []

for j in graph_dict.keys():
    date_array.append(j)

for m in graph_dict.values():
    toplam_array.append(m)

        
for j in range(0,len(date_array)):
    date_filler_array.append(j)


fig, ax = plt.subplots()
plt.xticks(date_filler_array, date_array)
ax.bar(date_filler_array, toplam_array)
plt.pause(0.01)

Tabs = {"Ders":180,"Kitap":90,"Tarih":60,"Arapça":30,"Kur'an-ı Kerim":20}


class Tab:
    def __init__(self,tab_name,minute,notebook) -> None:
        self.name = tab_name
        self.seconds = 60* minute 
        self.count = 0
        self.tab = ttk.Frame(notebook, width=600, height=100)
        self.timer_label = ttk.Label(self.tab, text="180:00", font=("Ubuntu", 48))
        self.timer_label.pack(pady=20)
        self.counter_label = ttk.Label(self.tab, text= tab_name + " Tamamlandı: 0", font=("Ubuntu", 16))
        self.counter_label.pack(pady=10)

class PomodoroTimer:

    def __init__(self):
        # windows init stuf 
        self.root = Tk()
        self.root.geometry("1200x800")
        self.root.title("Pomodoro Timer")
        
        
        self.s = ttk.Style()
        self.s.configure("TNotebook.Tab", font=("Ubuntu", 12))
        self.s.configure("TButton.Tab", font=("Ubuntu", 12))
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", pady=10, expand=True)
        self.tabs =[]

        # self.tab1 = ttk.Frame(self.tabs, width=600, height=100)
        # self.tab2 = ttk.Frame(self.tabs, width=600, height=100)
        # self.tab3 = ttk.Frame(self.tabs, width=600, height=100)
        # self.tab4 = ttk.Frame(self.tabs, width=600, height=100)
        # self.tab5 = ttk.Frame(self.tabs, width=600, height=100)
        # print("Line 80", self.tabs)

        for tab_name,minute in Tabs.items():
            tab = Tab(tab_name,minute,self.notebook)
            self.tabs.append(tab)
            self.notebook.add(tab.tab,text = tab_name)

        """ self.ders_timer_label = ttk.Label(self.tab1, text="180:00", font=("Ubuntu", 48))
        self.ders_timer_label.pack(pady=20)

        self.kitap_timer_label = ttk.Label(self.tab2, text="90:00", font=("Ubuntu", 48))
        self.kitap_timer_label.pack(pady=20)

        self.tarih_timer_label = ttk.Label(self.tab3, text="60:00", font=("Ubuntu", 48))
        self.tarih_timer_label.pack(pady=20)

        self.Arapca_timer_label = ttk.Label(self.tab4, text="30:00", font=("Ubuntu", 48))
        self.Arapca_timer_label.pack(pady=20)

        self.Kuran_timer_label = ttk.Label(self.tab5, text="20:00", font=("Ubuntu", 48))
        self.Kuran_timer_label.pack(pady=20)

        self.tabs.add(self.tab1, text="Ders")
        self.tabs.add(self.tab2, text="Kitap")
        self.tabs.add(self.tab3, text="Tarih")
        self.tabs.add(self.tab4, text="Arapça")
        self.tabs.add(self.tab5, text="Kur'an-ı Kerim") """

        self.grid_layout = ttk.Frame(self.root)
        self.grid_layout.pack(pady=10)
        
        self.start_button = ttk.Button(self.grid_layout, text="Başlat", command=self.baslat_thread)
        self.start_button.grid(row=0, column=0)

        self.stop_button = ttk.Button(self.grid_layout, text="Duraklat", command=self.duraklat_clock)
        self.stop_button.grid(row=0, column=1)

        self.end_button = ttk.Button(self.grid_layout, text="Bitir", command=self.bitir_clock)
        self.end_button.grid(row=0, column=2)
        
        self.kaydet_button = ttk.Button(self.grid_layout, text="Kaydet", command=self.kaydet)
        self.kaydet_button.grid(row=0, column=3)
        
        self.canvas = FigureCanvasTkAgg(fig, master = self.root)
        self.canvas.get_tk_widget().pack(pady=10)
        
        """ self.ders_counter_label = ttk.Label(self.tab1, text="Ders Tamamlandı: 0", font=("Ubuntu", 16))
        self.kitap_counter_label = ttk.Label(self.tab2, text="Kitap Tamamlandı: 0", font=("Ubuntu", 16))
        self.tarih_counter_label = ttk.Label(self.tab3, text="Tarih Tamamlandı: 0", font=("Ubuntu", 16))
        self.Arapca_counter_label = ttk.Label(self.tab4, text="Arapça Tamamlandı: 0", font=("Ubuntu", 16))
        self.Kuran_counter_label = ttk.Label(self.tab5, text="Kur'an Tamamlandı: 0", font=("Ubuntu", 16))
        self.ders_counter_label.pack(pady=10)
        self.kitap_counter_label.pack(pady=10)
        self.tarih_counter_label.pack(pady=10)
        self.Arapca_counter_label.pack(pady=10)
        self.Kuran_counter_label.pack(pady=10) """
        
        """ self.ders = 0
        self.kitap = 0
        self.tarih = 0
        self.Arapca = 0
        self.Kuran = 0
        self.ders_seconds = 60*180
        self.kitap_seconds= 60*90
        self.tarih_seconds = 60*60
        self.Arapca_seconds = 60*30
        self.Kuran_seconds = 60*20 """
        
        self.duraklat = False
        self.running = False
        self.bitir = False
        
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
            self.tabs[timer_id].seconds = 60 * Tabs.get(self.tabs[timer_id].name)
            self.tabs[timer_id].counter_label.config(text=f"{self.tabs[timer_id].name} Tamamlandı: {self.tabs[timer_id].count}")

        """  if timer_id == 1:
            
            while self.ders_seconds > 0 and not self.duraklat:
                minutes, seconds = divmod(self.ders_seconds, 60)
                self.ders_timer_label.configure(text=f"{minutes:02d}:{seconds:02d}")
                self.root.update()
                time.sleep(1)
                self.ders_seconds -= 1
                if self.duraklat or self.bitir:
                    break
            if not self.duraklat and not self.bitir:
                self.ders += 1
                self.ders_seconds = 180*60
                self.ders_counter_label.config(text=f"Ders Tamamlandı: {self.ders}")
                self.running = False

        elif timer_id == 2:
            while self.kitap_seconds > 0 and not self.duraklat:
                minutes, seconds = divmod(self.kitap_seconds, 60)
                self.kitap_timer_label.configure(text=f"{minutes:02d}:{seconds:02d}")
                self.root.update()
                time.sleep(1)
                self.kitap_seconds -= 1
                if self.duraklat:
                    break
            if not self.duraklat or self.bitir:
                self.kitap += 1
                self.kitap_seconds = 90*60
                self.kitap_counter_label.config(text=f"Kitap Tamamlandı: {self.kitap}")
                self.running = False

        elif timer_id == 3:
            while self.tarih_seconds > 0 and not self.duraklat:
                minutes, seconds = divmod(self.tarih_seconds, 60)
                self.tarih_timer_label.configure(text=f"{minutes:02d}:{seconds:02d}")
                self.root.update()
                time.sleep(1)
                self.tarih_seconds -= 1
                if self.duraklat:
                    break
            if not self.duraklat or self.bitir:
                self.tarih += 1
                self.tarih_seconds = 60*60
                self.tarih_counter_label.config(text=f"Tarih Tamamlandı: {self.tarih}")
                self.running = False

        elif timer_id == 4:
            while self.Arapca_seconds > 0 and not self.duraklat:
                minutes, seconds = divmod(self.Arapca_seconds, 60)
                self.Arapca_timer_label.configure(text=f"{minutes:02d}:{seconds:02d}")
                self.root.update()
                time.sleep(1)
                self.Arapca_seconds -= 1
                if self.duraklat:
                    break
            if not self.duraklat or self.bitir:
                self.Arapca += 1
                self.Arapca_seconds = 30*60
                self.Arapca_counter_label.config(text=f"Arapça Tamamlandı: {self.Arapca}")
                self.running = False
                
        elif timer_id == 5:
            while self.Kuran_seconds > 0 and not self.duraklat:
                minutes, seconds = divmod(self.Kuran_seconds, 60)
                self.Kuran_timer_label.configure(text=f"{minutes:02d}:{seconds:02d}")
                self.root.update()
                time.sleep(1)
                self.Kuran_seconds -= 1
                if self.duraklat:
                    break
            if not self.duraklat or self.bitir:
                self.Kuran += 1
                self.Kuran_seconds = 20*60
                self.Kuran_counter_label.config(text=f"Kur'an Tamamlandı: {self.Kuran}")
                self.running = False """

        # else:
        #     pass

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

        self.tabs[bitir_id].timer_label.config(text=f"{Tabs.get(self.tabs[bitir_id].name)}:00")
        self.tabs[bitir_id].seconds = Tabs.get(self.tabs[bitir_id].name) * 60
        """ if bitir_id == 1:
            self.ders_timer_label.config(text="180:00")
            self.ders_seconds = 180*60
        elif bitir_id == 2:   
            self.kitap_timer_label.config(text="90:00")
            self.kitap_seconds = 90*60
        elif bitir_id == 3:    
            self.tarih_timer_label.config(text="60:00")
            self.tarih_seconds = 60*60
        elif bitir_id == 4:
            self.Arapca_timer_label.config(text="30:00")
            self.Arapca_seconds = 30*60
        elif bitir_id == 5:    
            self.Kuran_timer_label.config(text="20:00")
            self.Kuran_seconds = 20*60 """
        time.sleep(0.5)
        self.running = False

    def kaydet(self):
        global value_ders
        global value_kitap
        global value_tarih
        global value_Arapca
        global value_Kuran
        value_ders = self.ders
        value_kitap = self.kitap
        value_tarih = self.tarih
        value_Arapca = self.Arapca
        value_Kuran = self.Kuran
        
timer = PomodoroTimer()


toplam_sure = value_ders*180 + value_kitap*90 + value_tarih*60 + value_Arapca*30 + value_Kuran*20

date = datetime.date.today()

con = sqlite3.connect("kayit.db")

cursor = con.cursor()



def veri_ekle():
    cursor.execute("Insert into kayit Values(?,?,?,?,?,?,?,?,?,?,?,?)",(date,value_ders,value_kitap,value_tarih,value_Arapca,value_Kuran,value_ders*180,value_kitap*90,value_tarih*60,value_Arapca*30,value_Kuran*20,toplam_sure))
    con.commit()

veri_ekle()

con.close()
