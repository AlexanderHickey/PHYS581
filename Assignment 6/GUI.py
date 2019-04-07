# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 21:25:58 2019

@author: Admin
"""

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import tkinter as tk
from tkinter import ttk

import seabreeze.spectrometers as sb

LARGE_FONT = ('Verdana', 12)
style.use('ggplot') #dark_background ggplot grayscale


f = Figure(figsize=(5,5), dpi = 100)
a = f.add_subplot(111)
        

def collect(integration_time = 20000):
    
    spec = sb.Spectrometer.from_serial_number()
    spec.integration_time_micros(integration_time)
    wlength = spec.wavelengths()[3:]
    intensity = spec.intensities()[3:]
    spec.close()
    
    
    return wlength, intensity


def animate(i):
    

    wlength, intensity = collect()
    a.clear()
    a.plot(wlength, intensity)

class SeaofBTCapp(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self,*args,**kwargs)
        
        tk.Tk.iconbitmap(self, default = 'light.ico')
        
        container = tk.Frame(self)
        container.pack(side='top',fill='both',expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        for F in (StartPage,):
                
            frame = F(container, self)
            
            self.frames[F] = frame
            
            frame.grid(row=0, column = 0, sticky = 'nsew')
        
        self.show_frame(StartPage)
        
        
    def show_frame(self, cont):
        
        frame = self.frames[cont]
        frame.tkraise()


 
        
class StartPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text = 'Start Page', font = LARGE_FONT)
        label.pack(pady = 10, padx = 10)
        
        button1 = ttk.Button(self, text = 'Collect', command = lambda: controller.show_frame(PageOne))
        button1.pack()
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)
        
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand= True)
        canvas._tkcanvas.pack(side = tk.BOTTOM, fill = tk.BOTH, expand = True)
      
        
        
        
        
        
app = SeaofBTCapp()
ani = animation.FuncAnimation(f, animate, interval = 1)
app.mainloop()
        