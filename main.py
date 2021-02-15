from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.properties import ObjectProperty, StringProperty
# from kivy.clock import Clock
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
# from kivy.garden.graph import Graph, MeshLinePlot
from graphploter import Graph, MeshLinePlot
import numpy as np
#import sys


'''Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'multisamples', '0')'''

# root = Builder.load_file('graph_plotter (2).kv')

a = open('graph_plotter (2).kv', 'r')
kv_string = a.read()
a.close()

root = Builder.load_string(kv_string)


x1 = np.linspace(-10, 10, 1001)
y = np.ndarray
#y = x1
expression = ''
popup_first = False


def rgb(hex_str):
    if len(hex_str) == 6:
        R = hex_str[0:2]
        G = hex_str[2:4]
        B = hex_str[4:6]

        #print(R, G, B)

        R = int(R, 16)
        G = int(G, 16)
        B = int(B, 16)

        #print(R, G, B)

        fR = round(R / 255.0, 2)      #For Kivy
        fG = round(G / 255.0, 2)
        fB = round(B / 255.0, 2)

        #print(fR, fG, fB)

        fR = str(fR)
        fG = str(fG)
        fB = str(fB)

        #print(fR, fG, fB)

        RGB = []
        RGB.append(fR)
        RGB.append(fG)
        RGB.append(fB)
        #print(RGB)
        #print('')
        return RGB


class MainScreen(GridLayout, Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.x1 = x1

class LabelEntrada(Label):
    def __init__(self, **kwargs):
        super(LabelEntrada, self).__init__(**kwargs)
        self.text = 'Insira a função a ser plotada:'

class TextBox(TextInput):
    def __init__(self, **kwargs):
        super(TextBox, self).__init__(**kwargs)
        self.bind(text=self.update)

    def update(self, *args):
        print(self.text)

    def make_func_oficial(self, expr, x):
        d = {'x': x, 'np': np}
        a = np.ndarray
        funcstr = '''a = {e}'''.format(e=expr)
        print(funcstr)
        exec(funcstr, d)
        # print(d['a'])  # OK!
        # return d['a']
        global y
        y = d['a']
        print(y)
        global expression
        expression = expr

        if expr == 'np.tan(x)':
            tol = 10
            y[y > tol] = np.nan
            y[y < -tol] = np.nan
            print(y)

        index = []
        a = np.isnan(y)
        for i in range(np.size(a)):
            if a[i] == True:
                index.append(i)

        b = np.isinf(y)
        for i in range(np.size(b)):
            if b[i] == True:
                index.append(i)

        print(index)

        new_y = np.delete(y, index)
        print(new_y)
        y = new_y
        #print('Tamanho de y:', sys.getsizeof(y))


class ButtonOk(Button):
    #pop = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ButtonOk, self).__init__(**kwargs)

    def on_press(self):
        #global popup_first
        #print(self.pop)
        #pop = None

        '''if popup_first == False:
            pop = PopupGraph()
            pop.bind(on_dismiss=self.my_callback)
            pop.open()
            print('Tamanho de pop:', sys.getsizeof(pop))
            popup_first = True
        else:
            #print(self.pop)
            #del self.pop
            #print(self.pop)
            #self.pop = ObjectProperty(None)
            # print('Tamanho de pop (after deleting):', sys.getsizeof(self.pop))
            pop = PopupGraph()
            pop.bind(on_dismiss=self.my_callback)
            pop.open()
            print('Tamanho de pop:', sys.getsizeof(pop))'''
        pop = PopupGraph()
        print(pop)
        #pop.bind(on_dismiss=self.my_callback)
        pop.open()
        del pop
        #self.parent.parent.parent.switch_to(GraphScreen(name='graph_screen'))


    '''def my_callback(self, instance):
        print('Popup', instance, 'is being dismissed but is prevented!')
        # del instance
        # print('deleted')'''



class PopupGraph(Popup):
    titulo = StringProperty('Gráfico')
    _none = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(PopupGraph, self).__init__(**kwargs)
        '''plt.plot(x1, y)
        plt.xlabel(expression)
        plt.grid()
        self.ids.BoxLayout_Graph.add_widget(FigureCanvasKivyAgg(plt.gcf()))'''

    def on_open(self):
        instance = self.content
        print('on_open1:', instance)
        self.content = SetGraph()
        del instance
        print('on_open:', self.content)

    def on_dismiss(self):
        #print(self.ids.BoxLayout_Graph)
        #self.remove_widget(self.ids.BoxLayout_Graph)
        #del self.ids.BoxLayout_Graph
        # self.content = ObjectProperty(None)
        instance = self.content
        print(instance)
        self.content = BLayoutVoid()
        del instance
        print(self.content)


class SetGraph(BoxLayout):
    #graph = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(SetGraph, self).__init__(**kwargs)
        print(int(x1[0]), int(x1[-1]))
        print(int(round(np.amin(y))), int(round(np.amax(y))))

        self.y_grid = False
        self.y_grid_label = False

        self.graph = Graph(xlabel=expression, ylabel='Y', x_ticks_minor=5,
                           x_ticks_major=25, y_ticks_minor=5, y_ticks_major=25,
                           y_grid_label=self.y_grid_label, x_grid_label=True, padding=5,
                           x_grid=True, y_grid=self.y_grid, xmin=int(x1[0]), xmax=int(x1[-1]),
                           ymin=int(round(np.amin(y))), ymax=int(round(np.amax(y))),
                           border_color=[1, 1, 0, 1], tick_color=[1, 0, 0, .7],
                           label_options={'color': [0, 1, 1, 1], 'bold': True},
                           background_color=rgb('333300'))
        plot = MeshLinePlot(color=[0, 0, 1, 1])
        #plot.points = [(x, np.sin(x / 10.)) for x in range(0, 101)]
        plot.points = [(i, j) for i, j in zip(x1, y)]
        self.graph.add_plot(plot)
        #print('Tamanho de graph:', sys.getsizeof(self.graph))
        self.add_widget(self.graph)

    '''def delete(self):
        #self.graph = None
        #del self.graph
        self.graph = ObjectProperty(None)
        print('delete')'''


class BLayoutVoid(BoxLayout):
    pass


class teste23(App):
    def build(self):
        self.title = 'Graph Plotter App'
        self.icon = 'icone.png'
        return MainScreen()
        #return root


if __name__ == "__main__":
    teste23().run()
