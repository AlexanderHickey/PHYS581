"""
@author: Alex Hickey

This program generates a graphical user interface for an Ocean Optics USB2000+
spectrograph. The interface includes a collection button, which will interface
with the spectrograph and plot the intensity versus wavelength. There is also
a text box to manually set the integration time.
"""


#Import libraries
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib import pyplot as plt
from matplotlib import style
import matplotlib.animation as animation
import seabreeze.spectrometers as sb

#Set font, plot style and collection range of spectrograph
FONT = ('Verdana', 12)
style.use('ggplot') 
collec_range = (193,896) #Collection range in nanometers!
int_range = (0,9500) #Intensity range




def get_data(integration_time = 20000):
    '''
    This function interfaces with the spectrograph and returns the
    intensity as a function of wavelength over a given integration time.
    
    Args:
        integration_time: Integration time in microsecons
        
    Return:
        wlength, intensity: arrays of wavelength and intensity of measurement
    
    '''
    
    #Enter loop to continuously update data
    while True:
        
        #Connect to spectrometer, set integration time
        spec = sb.Spectrometer.from_serial_number()
        spec.integration_time_micros(integration_time)
        
        #Retrieve wavelength and intensity arrays
        wlength = spec.wavelengths()[2:]
        intensity = spec.intensities()[2:]
        
        #Close connection
        spec.close()
 
        return wlength, intensity

def print_value(val):
    print(val)


class App(tk.Frame):
    '''
    Class corresponding to main application. Object is the homepage.
    '''
    
    def __init__(self, *args, **kwargs):
        
        #Initialize homepage
        tk.Frame.__init__(self, *args, **kwargs)
        cont = tk.Frame(self)
        cont.pack(side='top',fill='both')

        #Set application title
        self.winfo_toplevel().title('Ocean Optics USB2000+')
        
        
        scale = tk.Scale(cont, orient='horizontal', 
                          from_= 1000, to= 65000, command=print_value)
        scale.pack(side=tk.LEFT)
        
        
        #Defines integration time entry box and label
        lbl = ttk.Label(cont, text="Integration time (μs):  ", font = FONT)
        lbl.pack(side=tk.LEFT)
        self.time_ent = ttk.Entry(cont, width=7)
        self.time_ent.insert(0, '20000')
        self.time_ent.pack(side=tk.LEFT)
        
        #Attributes to track if animation is running
        self.running = False #True if animation is currently running
        self.ani = None #True if animation has started at all
        
        #Defines data collection button
        self.btn = tk.Button(cont, text=' Collect ', command=self.on_click)
        self.btn.pack(side=tk.LEFT)
        
        #Defines the main plot
        self.fig = plt.Figure(figsize= (10,8))
        self.ax1 = self.fig.add_subplot(111)
        self.ax1.set_xlim(*collec_range)
        self.ax1.set_ylim(*int_range)
        self.ax1.set_xlabel('Wavelength (nm)',fontsize = FONT[1])
        self.ax1.set_ylabel('Intensity',fontsize = FONT[1])
        self.line, = self.ax1.plot([], [], lw=2)
        
        #Defines the canvas to insert matplotlib plot
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()
        
        #Inserts the matplotlib toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
    


    def on_click(self):
        '''
        Method to decide the action of the collect button
        '''
        
        #Start live animation on first click
        if self.ani is None:

           return self.start()
       
        #If paused, stop animation
        elif self.running:

            self.ani.event_source.stop()
            self.btn.config(text=' Collect ')
        
        #If resumed, start animation
        else:

            self.ani.event_source.start()
            self.btn.config(text=' Pause ')
        
        #Change status
        self.running = not self.running

    def start(self):
        '''
        Method to start/resume animation
        '''
        
        
        self.ani = animation.FuncAnimation(
            self.fig,
            self.update_graph,
            interval=int(self.time_ent.get())/1000,
            repeat=False)
        self.running = True
        self.btn.config(text=' Pause ')
        self.ani._start()
        print('started animation')

    def update_graph(self, i):
        '''
        Method to update the spectrograph plot with current data.
        '''
        
        #Retrieve updated integration time
        int_time = int(self.time_ent.get())
        
        #Update plot
        self.line.set_data(*get_data(int_time))

        return self.line,



def main():
    '''
    Compile and run main application.
    '''
    
    #Create tk object
    root = tk.Tk()
    
    #Set application icon
    root.iconbitmap(default = 'light_icon.ico')
    
    #Compile and execute application
    App(root).pack()
    root.mainloop()
    
    
if __name__ == '__main__':
    main()