import tkinter as tk
    
from PIL import ImageTk, Image


from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import numpy as np

import random
import seabreeze.spectrometers as sb


fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)





def get_data(integration_time = 20000):
    while True:
        
        spec = sb.Spectrometer.from_serial_number()
        spec.integration_time_micros(integration_time)
        wlength = spec.wavelengths()[2:]
        intensity = spec.intensities()[2:]
        spec.close()
        ax1.clear()
        ax1.plot(wlength, intensity)
 
        return wlength, intensity

class App(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        self.running = False
        self.ani = None

        btns = tk.Frame(self)
        btns.pack()

        lbl = tk.Label(btns, text="Number of times to run")
        lbl.pack(side=tk.LEFT)

        self.points_ent = tk.Entry(btns, width=5)
        self.points_ent.insert(0, '50')
        self.points_ent.pack(side=tk.LEFT)

        lbl = tk.Label(btns, text="update interval (ms)")
        lbl.pack(side=tk.LEFT)

        self.interval = tk.Entry(btns, width=5)
        self.interval.insert(0, '100')
        self.interval.pack(side=tk.LEFT)

        self.btn = tk.Button(btns, text='Start', command=self.on_click)
        self.btn.pack(side=tk.LEFT)

        self.fig = plt.Figure()
        self.ax1 = self.fig.add_subplot(111)
        self.line, = self.ax1.plot([], [], lw=2)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()
        
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        
        self.ax1.set_ylim(0,9500)
        self.ax1.set_xlim(193,896)

    def on_click(self):

        if self.ani is None:

           return self.start()

        if self.running:

            self.ani.event_source.stop()
            self.btn.config(text='Un-Pause')
        else:

            self.ani.event_source.start()
            self.btn.config(text='Pause')
        self.running = not self.running

    def start(self):
        self.points = int(self.points_ent.get()) + 1
        self.ani = animation.FuncAnimation(
            self.fig,
            self.update_graph,
            frames=self.points,
            interval=int(self.interval.get()),
            repeat=False)
        self.running = True
        self.btn.config(text='Pause')
        self.ani._start()
        print('started animation')

    def update_graph(self, i):
        self.line.set_data(*get_data()) # update graph

        if i >= self.points - 1:

            self.btn.config(text='Start')
            self.running = False
            self.ani = None
        return self.line,

def main():
    root = tk.Tk()
    app = App(root)
    app.pack()
    root.mainloop()

if __name__ == '__main__':
    main()