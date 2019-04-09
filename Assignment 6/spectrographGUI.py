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
import seabreeze.spectrometers as sb

#Set font, plot style and collection range of spectrograph
FONT = ('Verdana', 12)
style.use('ggplot') 
collec_range = (193,896) #Collection range in nanometers!



def get_data(integration_time = 20000):
    '''
    This function interfaces with the spectrograph and returns the
    intensity as a function of wavelength over a given integration time.
    
    Args:
        integration_time: Integration time in microsecons
        
    Return:
        wlength, intensity: arrays of wavelength and intensity of measurement
    
    '''
    
    #Connect to spectrometer, set integration time
    spec = sb.Spectrometer.from_serial_number()
    spec.integration_time_micros(integration_time)
    
    #Retrieve wavelength and intensity arrays.
    wlength = spec.wavelengths()[2:]
    intensity = spec.intensities()[2:]
    
    #Close connection
    spec.close()
 
    return wlength, intensity



class App(tk.Frame):
    '''
    Class corresponding to main application. Object is the homepage.
    '''    
    
    def __init__(self,*args,**kwargs):
        
        #Initialize homepage
        tk.Frame.__init__(self,*args,**kwargs)
        cont = tk.Frame(self)
        cont.pack(side='top',fill='both')
        
        #Set application title
        self.winfo_toplevel().title('Ocean Optics USB2000+')
        
        #Defines integration time entry box and label
        lbl = ttk.Label(cont, text="Integration time (μs):  ", font = FONT)
        lbl.pack(side=tk.LEFT)
        self.time_ent = ttk.Entry(cont, width=7)
        self.time_ent.insert(0, '20000')
        self.time_ent.pack(side=tk.LEFT)
        
        #Defines data collection button
        self.btn = ttk.Button(cont, text=' Collect ', command= self.update_graph)
        self.btn.pack(side= tk.LEFT)
        
        #Defines the main plot
        self.fig = plt.Figure(figsize= (10,8))
        self.ax1 = self.fig.add_subplot(111)
        self.ax1.set_xlim(*collec_range)
        self.ax1.set_xlabel('Wavelength (nm)',fontsize = FONT[1])
        self.ax1.set_ylabel('Intensity',fontsize = FONT[1])
        
        #Defines the canvas to insert matplotlib plot
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack()
        self.canvas._tkcanvas.pack()
        
        #Inserts the matplotlib toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        


    def update_graph(self):
        '''
        Method to update the spectrograph plot with current data.
        '''
        
        #Clear plot, retrieve updated integration time
        self.ax1.clear()
        int_time = int(self.time_ent.get())
        
        #Plot updated data, set to canvas
        self.ax1.plot(*get_data(int_time), lw=2)
        self.ax1.set_xlim(*collec_range)
        self.ax1.set_xlabel('Wavelength (nm)',fontsize = FONT[1])
        self.ax1.set_ylabel('Intensity',fontsize = FONT[1])
        self.canvas.draw()
        


def main():
    '''
    Compile and run main application.
    '''
    
    #Create object
    root = tk.Tk()
    
    #Set application icon
    root.iconbitmap(default = 'light_icon.ico')
    
    #Compile and execute application
    App(root).pack()
    root.mainloop()


if __name__ == '__main__':
    main()