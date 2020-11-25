if __name__=="__main__":
    from csvmanager import CSVManager
else:
    from .csvmanager import CSVManager
import PySimpleGUI as sg
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.pyplot as plt

class BarGraphManager:
    
    def __init__(self):
        self.v1,self.v2,self.v3,self.v4,self.v5=0,0,0,0,0
        csvmanager=CSVManager()
        dataset=csvmanager.list_od_from_csv()
        self.ages=[]
        for entry in dataset:
           self.ages.append(int(entry["AGE"]))
        self.fig=self.bar_graph()
    def draw_figure(self,canvas, figure, loc=(0, 0)):
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        return figure_canvas_agg
    def bar_graph(self):
       
        for i in range(len(self.ages)):
            a=self.ages[i]
            print(a)
            if a>=1 and a<=20:
                self.v1+=1
            elif a>=21 and a<=40:
                self.v2+=1
            elif a>=41 and a<=60:
                self.v3+=1
            elif a>=61 and a<=80:
                self.v4+=1
            elif a>=81:
                self.v5+=1
        values_to_plot = (self.v1,self.v2,self.v3,self.v4,self.v5)
        ind = np.arange(len(values_to_plot))
        width = 0.4

        p1 = plt.bar(ind, values_to_plot, width)

        plt.ylabel('NO.OF.CASES')
        plt.title('AGE VS CASES')
        plt.xticks(ind, ('1-20', '21-40', '41-60', '61-80','81-100'))
        plt.yticks(np.arange(0, 31, 5))
        plt.legend((p1[0],), ('AGE LIMIT',))





        sg.theme('Light Brown 3')

        fig = plt.gcf() 
        figure_x, figure_y, figure_w, figure_h = fig.bbox.bounds


        self.layout = [[sg.Text('BAR GRAPH', font='Any 18')],
                  [sg.Canvas(size=(figure_w, figure_h), key='-CANVAS-')],
                  [sg.OK(pad=((figure_w / 2, 0), 3), size=(4, 2))]]
        return fig
    

if __name__=="__main__":
    a=BarGraphManager()
    window = sg.Window('Demo Application - Embedding Matplotlib In PySimpleGUI',a.layout, force_toplevel=True, finalize=True)
    fig_photo = a.draw_figure(window['-CANVAS-'].TKCanvas,a.fig)
    event, values = window.read()
    window.close()    
