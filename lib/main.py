from kivy.config import Config

import os
os.environ["QT_MAC_WANTS_LAYER"] = "1"

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
#  Se importan los siguientes paquetes
# Matplotlib es necesario para mostrar en pantalla texto en latex
import matplotlib
from matplotlib import pyplot as plt
import matplotlib

matplotlib.use("module://kivy.garden.matplotlib.backend_kivy")
# Kivy administra la parte grafica
from kivy.garden.matplotlib.backend_kivyagg import \
    FigureCanvasKivyAgg  # Cada elemento de Kivy hay que importarlo por aparte
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
# Sympy es el paquete que permite hacer manipulaciones matemáticas
from sympy import *
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.graphics.context_instructions import Color
from kivy.graphics import Rectangle
from kivy.core.audio import Sound
from kivy.core.audio import SoundLoader
from kivy.uix.image import Image

# from PIL import Image

# Estas son las dimensiones de la ventana.  Aún hace falta averiguar como tomar las dimensiones fisicas del dispositivo.
WIDTH = 375
HEIGHT = 667

Window.size = (WIDTH, HEIGHT)  # iPhone 8

# Permite que sympy imprima texto en latex
init_printing()


# En kivy es necesario que cada Pantalla sea creada con una clase diferente

## Clase de la pagina de inicio

class PaginaInicio(Screen):
    def __init__(self, **kwargs):
        super(PaginaInicio, self).__init__(**kwargs)

        # Esta sección establece el color del fondo.  Realmente no sé bien cómo funciona

        self.bind(
            size=self._update_rect,
            pos=self._update_rect
        )
        # BACKGROUND = (.15, .74, .96, 1)
        with self.canvas.before:
            Color(1, 1, 1, 1)  ## Aquí va el color
            self.rect = Rectangle(
                size=self.size,
                pos=self.pos
            )

        # Se crean 3 layouts verticales.  Los de los lados están en blanco y el del centro tiene los botones
        layoutIzq = GridLayout(cols=1, spacing=40, size_hint_y=None, size_hint_x=0.3)
        layoutDer = GridLayout(cols=1, spacing=40, size_hint_y=None, size_hint_x=0.3)
        layout = GridLayout(cols=1, spacing=40, size_hint_y=None, size_hint_x=0.4)
        layoutFinal = GridLayout(cols=3, spacing=40, size_hint_y=1)
        # Es importante siempre usar el font "DejaVuSans.ttf" porque es el que permite escribir con índices y subíndices
        self.botonCreditos = Button(background_normal="Resources/images/BlueRectangleButton.png",
                                    background_down="Resources/images/BlueDarkRectangleButton.png", border=(1, 1, 1, 1),
                                    text="Créditos", size_hint=[1, None], height=150, font_name="DejaVuSans.ttf")
        self.botonNiveles = Button(background_normal="Resources/images/BlueRectangleButton.png",
                                   background_down="Resources/images/BlueDarkRectangleButton.png", border=(1, 1, 1, 1),
                                   text="Niveles", size_hint=[1, None], height=150, font_name="DejaVuSans.ttf")
        layout.add_widget(GridLayout(cols=1, spacing=40, size_hint_y=0.3, size_hint_x=0.3))
        layout.add_widget(BoxLayout(size_hint=[1, None], height=150))  # Espacio
        layout.add_widget(Label(text="PROYECTO NEWTON", color="black", font_name="DejaVuSans.ttf"))
        layout.add_widget(GridLayout(cols=1, spacing=40, size_hint_y=0.3, size_hint_x=0.3))
        layout.add_widget(self.botonNiveles)
        layout.add_widget(self.botonCreditos)
        layoutFinal.add_widget(layoutIzq)
        layoutFinal.add_widget(layout)
        layoutFinal.add_widget(layoutDer)
        self.add_widget(layoutFinal)

    # Todas las ventanas tendrán este método. Su úniva utilidad es ayudar a establecer el color de fondo
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


## Clase de pagina de tips

class PaginaTips(Screen):
    def __init__(self, infografia, **kwargs):
        super(PaginaTips, self).__init__(**kwargs)

        # Esta sección establece el color del fondo.  Realmente no sé bien cómo funciona

        self.bind(
            size=self._update_rect,
            pos=self._update_rect
        )

        with self.canvas.before:
            Color(1, 1, 1, 1)  ## Aquí va el color
            self.rect = Rectangle(
                size=self.size,
                pos=self.pos
            )

        layoutTips = GridLayout(cols=1, spacing=40, size_hint=[1, 1])
        layoutSuperior = GridLayout(cols=2, spacing=40, size_hint=[1, None], height=80)

        layoutSuperior.add_widget(
            BoxLayout(size_hint=[None, 1], width=int((2 * WIDTH - 3 * 150) / (3 + 1))))  # Haciendo espacio

        self.botonRegreso = Button(background_normal="Resources/images/BlueRectangleButton.png",
                                   background_down="Resources/images/BlueDarkRectangleButton.png", border=(1, 1, 1, 1),
                                   text="Regreso", size_hint=[None, 1], width=150, font_name="DejaVuSans.ttf")

        layoutSuperior.add_widget(self.botonRegreso)

        layoutTips.add_widget(GridLayout(size_hint=[None, 0.15]))  # Para hacer espacio
        layoutTips.add_widget(layoutSuperior)

        # Aqui voy a crear el panel de Scroll
        scrollLayout = ScrollView(size_hint=(1, None), size=(Window.width, 2 * HEIGHT))
        scrollLayout.do_scroll_x = False
        scrollLayout.do_scroll_y = True
        # scrollLayout.minimum_height = scrollLayout.setter('height')

        # loading image
        self.img = Image(source=infografia)

        layoutFinal = GridLayout(cols=1, spacing=40, size_hint_y=None, height=self.img.texture_size[
                                                                                  1] + 180)  # Solución temporal.  Hay que ver como obtener el tamaño exacto.
        layoutFinal.add_widget(self.img)
        scrollLayout.add_widget(layoutFinal)
        layoutTips.add_widget(scrollLayout)

        self.add_widget(layoutTips)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class PagConversiones(Screen):
    def __init__(self, **kwargs):
        super(PagConversiones, self).__init__(**kwargs)

        # Esta sección establece el color del fondo.  Realmente no sé bien cómo funciona

        self.bind(
            size=self._update_rect,
            pos=self._update_rect
        )

        with self.canvas.before:
            Color(1, 1, 1, 1)  ## Aquí va el color
            self.rect = Rectangle(
                size=self.size,
                pos=self.pos
            )

        layoutConversiones = GridLayout(cols=1, spacing=40, size_hint=[1, 1])
        layoutSuperior = GridLayout(cols=2, spacing=40, size_hint=[1, None], height=80)

        layoutSuperior.add_widget(
            BoxLayout(size_hint=[None, 1], width=int((2 * WIDTH - 3 * 150) / (3 + 1))))  # Haciendo espacio

        self.botonRegreso = Button(background_normal="Resources/images/BlueRectangleButton.png",
                                   background_down="Resources/images/BlueDarkRectangleButton.png", border=(1, 1, 1, 1),
                                   text="Regreso", size_hint=[None, 1], width=150, font_name="DejaVuSans.ttf")

        layoutSuperior.add_widget(self.botonRegreso)

        layoutConversiones.add_widget(BoxLayout(size_hint=[1, 0.015]))  # Para hacer espacio
        layoutConversiones.add_widget(layoutSuperior)
        layoutConversiones.add_widget(GridLayout(size_hint=[1, 0.015]))  # Para hacer espacio

        layoutBotones = GridLayout(cols=2, spacing=40, size_hint_y=1, size_hint_x=1)

        self.botonConversiones1 = Button(background_normal="Resources/images/BlueRectangleButton.png",
                                         background_down="Resources/images/BlueDarkRectangleButton.png",
                                         border=(1, 1, 1, 1), text="Nivel 1", size_hint=[1, None], height=100,
                                         font_name="DejaVuSans.ttf")
        layoutBotones.add_widget(self.botonConversiones1)

        self.botonConversiones2 = Button(background_normal="Resources/images/BlueRectangleButton.png",
                                         background_down="Resources/images/BlueDarkRectangleButton.png",
                                         border=(1, 1, 1, 1), text="Nivel 2", size_hint=[1, None], height=100,
                                         font_name="DejaVuSans.ttf")
        layoutBotones.add_widget(self.botonConversiones2)

        self.botonConversiones3 = Button(background_normal="Resources/images/BlueRectangleButton.png",
                                         background_down="Resources/images/BlueDarkRectangleButton.png",
                                         border=(1, 1, 1, 1), text="Nivel 3", size_hint=[1, None], height=100,
                                         font_name="DejaVuSans.ttf")
        layoutBotones.add_widget(self.botonConversiones3)

        self.botonConversiones4 = Button(background_normal="Resources/images/BlueRectangleButton.png",
                                         background_down="Resources/images/BlueDarkRectangleButton.png",
                                         border=(1, 1, 1, 1), text="Nivel 4", size_hint=[1, None], height=100,
                                         font_name="DejaVuSans.ttf")
        layoutBotones.add_widget(self.botonConversiones4)

        self.botonConversiones5 = Button(background_normal="Resources/images/BlueRectangleButton.png",
                                         background_down="Resources/images/BlueDarkRectangleButton.png",
                                         border=(1, 1, 1, 1), text="Nivel 5", size_hint=[1, None], height=100,
                                         font_name="DejaVuSans.ttf")
        layoutBotones.add_widget(self.botonConversiones5)

        layoutConversiones.add_widget(layoutBotones)

        self.add_widget(layoutConversiones)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class PagMRU(Screen):
    def __init__(self, **kwargs):
        super(PagMRU, self).__init__(**kwargs)

        # Esta sección establece el color del fondo.  Realmente no sé bien cómo funciona

        self.bind(
            size=self._update_rect,
            pos=self._update_rect
        )

        with self.canvas.before:
            Color(1, 1, 1, 1)  ## Aquí va el color
            self.rect = Rectangle(
                size=self.size,
                pos=self.pos
            )

        layoutMRU = GridLayout(cols=1, spacing=40, size_hint=[1, 1])
        layoutSuperior = GridLayout(cols=2, spacing=40, size_hint=[1, None], height=80)

        layoutSuperior.add_widget(
            BoxLayout(size_hint=[None, 1], width=int((2 * WIDTH - 3 * 150) / (3 + 1))))  # Haciendo espacio

        self.botonRegreso = Button(background_normal="Resources/images/BlueRectangleButton.png",
                                   background_down="Resources/images/BlueDarkRectangleButton.png", border=(1, 1, 1, 1),
                                   text="Regreso", size_hint=[None, 1], width=150, font_name="DejaVuSans.ttf")

        layoutSuperior.add_widget(self.botonRegreso)

        layoutMRU.add_widget(BoxLayout(size_hint=[1, 0.015]))  # Para hacer espacio
        layoutMRU.add_widget(layoutSuperior)
        layoutMRU.add_widget(GridLayout(size_hint=[1, 0.015]))  # Para hacer espacio

        layoutBotones = GridLayout(cols=2, spacing=40, size_hint_y=1, size_hint_x=1)

        self.boton1 = Button(background_normal="Resources/images/BlueRectangleButton.png",
                             background_down="Resources/images/BlueDarkRectangleButton.png", border=(1, 1, 1, 1),
                             text="v=d/t, despeje d", size_hint=[1, None], height=100, font_name="DejaVuSans.ttf")
        layoutBotones.add_widget(self.boton1)

        self.boton2 = Button(background_normal="Resources/images/BlueRectangleButton.png",
                             background_down="Resources/images/BlueDarkRectangleButton.png", border=(1, 1, 1, 1),
                             text="v=d/t, despeje t", size_hint=[1, None], height=100, font_name="DejaVuSans.ttf")
        layoutBotones.add_widget(self.boton2)

        layoutMRU.add_widget(layoutBotones)

        self.add_widget(layoutMRU)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class PagMRUA(Screen):
    def __init__(self, **kwargs):
        super(PagMRUA, self).__init__(**kwargs)

        # Esta sección establece el color del fondo.  Realmente no sé bien cómo funciona

        self.bind(
            size=self._update_rect,
            pos=self._update_rect
        )

        with self.canvas.before:
            Color(1, 1, 1, 1)  ## Aquí va el color
            self.rect = Rectangle(
                size=self.size,
                pos=self.pos
            )

        layoutMRUA = GridLayout(cols=1, spacing=40, size_hint=[1, 1])
        layoutSuperior = GridLayout(cols=2, spacing=40, size_hint=[1, None], height=80)

        layoutSuperior.add_widget(
            BoxLayout(size_hint=[None, 1], width=int((2 * WIDTH - 3 * 150) / (3 + 1))))  # Haciendo espacio

        self.botonRegreso = Button(background_normal="Resources/images/BlueRectangleButton.png",
                                   background_down="Resources/images/BlueDarkRectangleButton.png", border=(1, 1, 1, 1),
                                   text="Regreso", size_hint=[None, 1], width=150, font_name="DejaVuSans.ttf")

        layoutSuperior.add_widget(self.botonRegreso)

        layoutMRUA.add_widget(BoxLayout(size_hint=[1, 0.015]))  # Para hacer espacio
        layoutMRUA.add_widget(layoutSuperior)
        layoutMRUA.add_widget(GridLayout(size_hint=[1, 0.015]))  # Para hacer espacio

        layoutBotones = GridLayout(cols=2, spacing=40, size_hint_y=1, size_hint_x=1)

        self.boton3 = Button(background_normal="Resources/images/BlueRectangleButton.png",
                             background_down="Resources/images/BlueDarkRectangleButton.png", border=(1, 1, 1, 1),
                             text="a=(vբ-vᵢ)/t, despeje vբ", size_hint=[1, None], height=100,
                             font_name="DejaVuSans.ttf", font_size=25)
        layoutBotones.add_widget(self.boton3)

        self.boton4 = Button(background_normal="Resources/images/BlueRectangleButton.png",
                             background_down="Resources/images/BlueDarkRectangleButton.png", border=(1, 1, 1, 1),
                             text="a=(vբ-vᵢ)/t, despeje vᵢ", size_hint=[1, None], height=100,
                             font_name="DejaVuSans.ttf", font_size=25)
        layoutBotones.add_widget(self.boton4)

        self.boton5 = Button(background_normal="Resources/images/BlueRectangleButton.png",
                             background_down="Resources/images/BlueDarkRectangleButton.png", border=(1, 1, 1, 1),
                             text="a=(vբ-vᵢ)/t, despeje t", size_hint=[1, None], height=100,
                             font_name="DejaVuSans.ttf", font_size=25)
        layoutBotones.add_widget(self.boton5)

        self.boton6 = Button(background_normal="Resources/images/BlueRectangleButton.png",
                             background_down="Resources/images/BlueDarkRectangleButton.png", border=(1, 1, 1, 1),
                             text="vբ²=vᵢ²+2*a*d, despeje vբ", size_hint=[1, None], height=100,
                             font_name="DejaVuSans.ttf", font_size=25)
        layoutBotones.add_widget(self.boton6)

        self.boton7 = Button(background_normal="Resources/images/BlueRectangleButton.png",
                             background_down="Resources/images/BlueDarkRectangleButton.png", border=(1, 1, 1, 1),
                             text="vբ²=vᵢ²+2*a*d, despeje vᵢ", size_hint=[1, None], height=100,
                             font_name="DejaVuSans.ttf", font_size=25)
        layoutBotones.add_widget(self.boton7)

        self.boton8 = Button(background_normal="Resources/images/BlueRectangleButton.png",
                             background_down="Resources/images/BlueDarkRectangleButton.png", border=(1, 1, 1, 1),
                             text="vբ²=vᵢ²+2*a*d, despeje a", size_hint=[1, None], height=100,
                             font_name="DejaVuSans.ttf", font_size=25)
        layoutBotones.add_widget(self.boton8)

        self.boton9 = Button(background_normal="Resources/images/BlueRectangleButton.png",
                             background_down="Resources/images/BlueDarkRectangleButton.png", border=(1, 1, 1, 1),
                             text="vբ²=vᵢ²+2*a*d, despeje d", size_hint=[1, None], height=100,
                             font_name="DejaVuSans.ttf", font_size=25)
        layoutBotones.add_widget(self.boton9)

        self.boton10 = Button(background_normal="Resources/images/BlueRectangleButton.png",
                              background_down="Resources/images/BlueDarkRectangleButton.png", border=(1, 1, 1, 1),
                              text="d=vᵢ*t+a*t²/2, despeje vᵢ", size_hint=[1, None], height=100,
                              font_name="DejaVuSans.ttf", font_size=25)
        layoutBotones.add_widget(self.boton10)

        self.boton11 = Button(background_normal="Resources/images/BlueRectangleButton.png",
                              background_down="Resources/images/BlueDarkRectangleButton.png", border=(1, 1, 1, 1),
                              text="d=vᵢ*t+a*t²/2, despeje a", size_hint=[1, None], height=100,
                              font_name="DejaVuSans.ttf", font_size=25)
        layoutBotones.add_widget(self.boton11)

        self.boton12 = Button(background_normal="Resources/images/BlueRectangleButton.png",
                              background_down="Resources/images/BlueDarkRectangleButton.png", border=(1, 1, 1, 1),
                              text="d=vᵢ*t+a*t²/2, despeje t", size_hint=[1, None], height=100,
                              font_name="DejaVuSans.ttf", font_size=25)
        layoutBotones.add_widget(self.boton12)

        # layoutBotones.add_widget(layoutBotones)

        layoutMRUA.add_widget(layoutBotones)

        self.add_widget(layoutMRUA)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class PagMovimientoParabolico(Screen):
    def __init__(self, **kwargs):
        super(PagMovimientoParabolico, self).__init__(**kwargs)

        # Esta sección establece el color del fondo.  Realmente no sé bien cómo funciona

        self.bind(
            size=self._update_rect,
            pos=self._update_rect
        )

        with self.canvas.before:
            Color(1, 1, 1, 1)  ## Aquí va el color
            self.rect = Rectangle(
                size=self.size,
                pos=self.pos
            )

        layoutMRU = GridLayout(cols=1, spacing=40, size_hint=[1, 1])
        layoutSuperior = GridLayout(cols=2, spacing=40, size_hint=[1, None], height=80)

        layoutSuperior.add_widget(
            BoxLayout(size_hint=[None, 1], width=int((2 * WIDTH - 3 * 150) / (3 + 1))))  # Haciendo espacio

        self.botonRegreso = Button(background_normal="Resources/images/BlueRectangleButton.png",
                                   background_down="Resources/images/BlueDarkRectangleButton.png", border=(1, 1, 1, 1),
                                   text="Regreso", size_hint=[None, 1], width=150, font_name="DejaVuSans.ttf")

        layoutSuperior.add_widget(self.botonRegreso)

        layoutMRU.add_widget(BoxLayout(size_hint=[1, 0.015]))  # Para hacer espacio
        layoutMRU.add_widget(layoutSuperior)
        layoutMRU.add_widget(GridLayout(size_hint=[1, 0.015]))  # Para hacer espacio

        layoutBotones = GridLayout(cols=2, spacing=40, size_hint_y=1, size_hint_x=1)

        self.boton13 = Button(background_normal="Resources/images/BlueRectangleButton.png",
                              background_down="Resources/images/BlueDarkRectangleButton.png", border=(1, 1, 1, 1),
                              text="yբ=yᵢ+vᵢsin(θ)t-gt²/2, despeje vᵢ", size_hint=[1, None], height=100,
                              font_name="DejaVuSans.ttf", font_size=20)
        layoutBotones.add_widget(self.boton13)

        self.boton14 = Button(background_normal="Resources/images/BlueRectangleButton.png",
                              background_down="Resources/images/BlueDarkRectangleButton.png", border=(1, 1, 1, 1),
                              text="yբ=yᵢ+vᵢsin(θ)t-gt²/2, despeje θ", size_hint=[1, None], height=100,
                              font_name="DejaVuSans.ttf", font_size=20)
        layoutBotones.add_widget(self.boton14)

        layoutMRU.add_widget(layoutBotones)

        self.add_widget(layoutMRU)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


#  Pagina que controla los niveles de dinamica
class PagDinamica(Screen):
    def __init__(self, **kwargs):
        super(PagDinamica, self).__init__(**kwargs)

        # Esta sección establece el color del fondo.  Realmente no sé bien cómo funciona

        self.bind(
            size=self._update_rect,
            pos=self._update_rect
        )

        with self.canvas.before:
            Color(1, 1, 1, 1)  ## Aquí va el color
            self.rect = Rectangle(
                size=self.size,
                pos=self.pos
            )

        layoutDinamica = GridLayout(cols=1, spacing=40, size_hint=[1, 1])
        layoutSuperior = GridLayout(cols=2, spacing=40, size_hint=[1, None], height=80)

        layoutSuperior.add_widget(
            BoxLayout(size_hint=[None, 1], width=int((2 * WIDTH - 3 * 150) / (3 + 1))))  # Haciendo espacio

        self.botonRegreso = Button(background_normal="Resources/images/BlueRectangleButton.png",
                                   background_down="Resources/images/BlueDarkRectangleButton.png", border=(1, 1, 1, 1),
                                   text="Regreso", size_hint=[None, 1], width=150, font_name="DejaVuSans.ttf")

        layoutSuperior.add_widget(self.botonRegreso)

        layoutDinamica.add_widget(BoxLayout(size_hint=[1, 0.015]))  # Para hacer espacio
        layoutDinamica.add_widget(layoutSuperior)
        layoutDinamica.add_widget(GridLayout(size_hint=[1, 0.015]))  # Para hacer espacio

        layoutBotones = GridLayout(cols=2, spacing=40, size_hint_y=1, size_hint_x=1)

        self.botonDinámica1 = Button(background_normal="Resources/images/BlueRectangleButton.png",
                                     background_down="Resources/images/BlueDarkRectangleButton.png",
                                     border=(1, 1, 1, 1),
                                     text="Nivel 1",
                                     size_hint=[1, None], height=100, font_name="DejaVuSans.ttf")
        layoutBotones.add_widget(self.botonDinámica1)

        self.botonDinámica2 = Button(background_normal="Resources/images/BlueRectangleButton.png",
                                     background_down="Resources/images/BlueDarkRectangleButton.png",
                                     border=(1, 1, 1, 1),
                                     text="Nivel 2",
                                     size_hint=[1, None], height=100, font_name="DejaVuSans.ttf")
        layoutBotones.add_widget(self.botonDinámica2)

        layoutDinamica.add_widget(layoutBotones)

        self.add_widget(layoutDinamica)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


#  Clase que define el menu de niveles
class PaginaNiveles(Screen):
    def __init__(self, **kwargs):
        super(PaginaNiveles, self).__init__(**kwargs)

        # Esta sección establece el color del fondo.  Realmente no sé bien cómo funciona

        self.bind(
            size=self._update_rect,
            pos=self._update_rect
        )

        with self.canvas.before:
            Color(1, 1, 1, 1)  ## Aquí va el color
            self.rect = Rectangle(
                size=self.size,
                pos=self.pos
            )

        # Los layouts de los lados están vacíos
        layoutIzq = GridLayout(cols=1, spacing=40, size_hint_y=None, size_hint_x=0.2)
        layoutDer = GridLayout(cols=1, spacing=40, size_hint_y=None, size_hint_x=0.2)
        layout = GridLayout(cols=1, spacing=40, size_hint_y=None, size_hint_x=0.6)

        self.botonRegreso = Button(background_normal="Resources/images/BlueRectangleButton.png",
                                   background_down="Resources/images/BlueDarkRectangleButton.png", border=(1, 1, 1, 1),
                                   text="Regreso", size_hint=[None, 1], width=150, font_name="DejaVuSans.ttf")
        # layoutIzq.add_widget(self.botonRegreso)
        layout.add_widget(GridLayout(cols=1, spacing=40, size_hint_y=0.3, size_hint_x=0.3))

        layout.add_widget(Label(text="Conversiones", color="black", font_name="DejaVuSans.ttf"))

        self.botonNivelesConversiones = Button(background_normal="Resources/images/BlueRectangleButton.png",
                                               background_down="Resources/images/BlueDarkRectangleButton.png",
                                               border=(1, 1, 1, 1), text="Niveles", size_hint=[1, None], height=100,
                                               font_name="DejaVuSans.ttf")
        layout.add_widget(self.botonNivelesConversiones)

        layout.add_widget(Label(text="MRU", color="black", font_name="DejaVuSans.ttf"))

        self.botonTipMRU = Button(background_normal="Resources/images/BlueRectangleButton.png",
                                  background_down="Resources/images/BlueDarkRectangleButton.png", border=(1, 1, 1, 1),
                                  text="Tips", size_hint=[1, None], height=100, font_name="DejaVuSans.ttf")
        layout.add_widget(self.botonTipMRU)

        self.botonNivelesMRU = Button(background_normal="Resources/images/BlueRectangleButton.png",
                                      background_down="Resources/images/BlueDarkRectangleButton.png",
                                      border=(1, 1, 1, 1), text="Niveles",
                                      size_hint=[1, None], height=100, font_name="DejaVuSans.ttf")
        layout.add_widget(self.botonNivelesMRU)

        layout.add_widget(Label(text="MRUA", color="black", font_name="DejaVuSans.ttf"))

        self.botonTipMRUA = Button(background_normal="Resources/images/BlueRectangleButton.png",
                                   background_down="Resources/images/BlueDarkRectangleButton.png", border=(1, 1, 1, 1),
                                   text="Tips", size_hint=[1, None], height=100, font_name="DejaVuSans.ttf")
        layout.add_widget(self.botonTipMRUA)

        self.botonNivelesMRUA = Button(background_normal="Resources/images/BlueRectangleButton.png",
                                       background_down="Resources/images/BlueDarkRectangleButton.png",
                                       border=(1, 1, 1, 1), text="Niveles",
                                       size_hint=[1, None], height=100, font_name="DejaVuSans.ttf")
        layout.add_widget(self.botonNivelesMRUA)

        layout.add_widget(Label(text="Movimiento Parabólico", color="black", font_name="DejaVuSans.ttf"))
        self.botonTipMovimientoParabólico = Button(background_normal="Resources/images/BlueRectangleButton.png",
                                                   background_down="BlueDarkRectangleButton.png", border=(1, 1, 1, 1),
                                                   text="Tips", size_hint=[1, None], height=100,
                                                   font_name="DejaVuSans.ttf")
        layout.add_widget(self.botonTipMovimientoParabólico)
        self.botonNivelesMovimientoParabólico = Button(background_normal="BlueRectangleButton.png",
                                                       background_down="Resources/images/BlueDarkRectangleButton.png",
                                                       border=(1, 1, 1, 1), text="Niveles",
                                                       size_hint=[1, None], height=100, font_name="DejaVuSans.ttf")
        layout.add_widget(self.botonNivelesMovimientoParabólico)

        layout.add_widget(Label(text="Dinámica", color="black", font_name="DejaVuSans.ttf"))
        self.botonDinámica = Button(background_normal="Resources/images/BlueRectangleButton.png",
                                    background_down="Resources/images/BlueDarkRectangleButton.png", border=(1, 1, 1, 1),
                                    text="Niveles",
                                    size_hint=[1, None], height=100, font_name="DejaVuSans.ttf")
        layout.add_widget(self.botonDinámica)

        # Aqui voy a crear el panel de Scroll
        scrollLayout = ScrollView(size_hint=(1, None), size=(Window.width, 2 * HEIGHT))
        scrollLayout.do_scroll_x = False
        scrollLayout.do_scroll_y = True
        # scrollLayout.minimum_height = scrollLayout.setter('height')
        layoutFinal = GridLayout(cols=3, spacing=40, size_hint_y=None,
                                 height=5000)  # Solución temporal.  Hay que ver como obtener el tamaño exacto.

        layoutFinal.add_widget(layoutIzq)
        layoutFinal.add_widget(layout)
        layoutFinal.add_widget(layoutDer)
        scrollLayout.add_widget(layoutFinal)

        layoutNiveles = GridLayout(cols=1, spacing=40, size_hint=[1, 1])
        layoutSuperior = GridLayout(cols=2, spacing=40, size_hint=[1, None], height=80)

        layoutSuperior.add_widget(
            BoxLayout(size_hint=[None, 1], width=int((2 * WIDTH - 3 * 150) / (3 + 1))))  # Haciendo espacio
        layoutSuperior.add_widget(self.botonRegreso)

        layoutNiveles.add_widget(GridLayout(size_hint=[None, 0.15]))  # Para hacer espacio
        layoutNiveles.add_widget(layoutSuperior)
        layoutNiveles.add_widget(GridLayout(size_hint=[None, 0.15]))  # Para hacer espacio
        layoutNiveles.add_widget(scrollLayout)

        self.add_widget(layoutNiveles)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


#  Clase experimental que usa sympy para practicar ejercicios de conversion de unidades
class Conversion:
    def __init__(self):
        self.cantidad = None
        self.eq = []
        self.eqRight = []
        self.eqLeft = []
        self.sol = None
        self.Listo = False
        self.texto = None
        self.plotTexto = None
        self.factores = 0
        self.units = None

    def setEquation(self):
        self.cantidad_sym = parse_expr(self.cantidad)
        self.eqLeft.append(latex(self.cantidad_sym))
        self.eqRight.append(self.cantidad_sym)
        self.eq.append(self.eqLeft[-1] + "=" + latex(self.eqRight[-1]))
        print("self.eq", self.eq[-1])
        fig = plt.figure()
        text = fig.text(0.1, 0.5, r"$%s$" % self.eq[-1], fontsize=30, color="black")
        fig.show()
        self.plot = plt.gcf()
        figLeft = plt.figure()
        textLeft = figLeft.text(0.1, 0.5, r"$%s$" % self.eqLeft[-1], fontsize=30, color="black")
        figLeft.show()
        self.plotLeft = plt.gcf()
        figRight = plt.figure()
        textRight = figRight.text(0.1, 0.5, r"= $%s$" % latex(self.eqRight[-1]), fontsize=30, color="black")
        figRight.show()
        self.plotRight = plt.gcf()
        self.texto = "Convierta la siguiente\ncantidad a unidades de " + self.units + "."
        figTexto = plt.figure(facecolor=matplotlib.colors.to_rgba([1, 1, 1], 1))
        textTexto = figTexto.text(0.1, 0.5, self.texto, fontsize=30, color="black")
        figTexto.show()
        self.plotTexto = plt.gcf()
        self.factores = 0
        print("self.factores", self.factores)

    def askForDeshacer(self):
        if len(self.eqRight) > 1:
            self.eqRight = self.eqRight[:-1]
            self.eqLeft = self.eqLeft[:-1]
            self.eq = self.eq[:-1]
            fig = plt.figure()
            text = fig.text(0.1, 0.5, r"$%s$" % self.eq[-1].replace(r"\mathtt{\text{\textbackslashtimes}}", r"\times"),
                            fontsize=30, color="black")
            fig.show()
            self.plot = plt.gcf()
            figLeft = plt.figure()
            textLeft = figLeft.text(0.1, 0.5, r"$%s$" % self.eqLeft[-1].replace(r"\mathtt{\text{\textbackslashtimes}}",
                                                                                r"\times"), fontsize=30, color="black")
            figLeft.show()
            self.plotLeft = plt.gcf()
            figRight = plt.figure()
            textRight = figRight.text(0.1, 0.5, r"= $%s$" % latex(self.eqRight[-1]).replace(
                r"\mathtt{\text{\textbackslashtimes}}", r"\times"), fontsize=30, color="black")
            figRight.show()
            self.plotRight = plt.gcf()
            self.factores = self.factores - 1
            print("self.factores", self.factores)

    def askForResetear(self):
        if len(self.eqRight) > 1:
            self.eqRight.append(self.eqRight[0])
            self.eqLeft.append(self.eqLeft[0])
            self.eq.append(self.eq[0])
            fig = plt.figure()
            text = fig.text(0.1, 0.5, r"$%s$" % self.eq[-1].replace(r"\mathtt{\text{\textbackslashtimes}}", r"\times"),
                            fontsize=30, color="black")
            fig.show()
            self.plot = plt.gcf()
            figLeft = plt.figure()
            textLeft = figLeft.text(0.1, 0.5, r"$%s$" % self.eqLeft[-1].replace(r"\mathtt{\text{\textbackslashtimes}}",
                                                                                r"\times"), fontsize=30, color="black")
            figLeft.show()
            self.plotLeft = plt.gcf()
            figRight = plt.figure()
            textRight = figRight.text(0.1, 0.5, r"= $%s$" % latex(self.eqRight[-1]).replace(
                r"\mathtt{\text{\textbackslashtimes}}", r"\times"), fontsize=30, color="black")
            figRight.show()
            self.plotRight = plt.gcf()
            self.factores = 0
            print("self.factores", self.factores)

    def setInchCm(self):
        inch = Symbol("inch")
        cm = Symbol("cm")
        self.eqRight.append(N(self.eqRight[-1] * parse_expr(r"1*inch/(2.54 * cm)"), 3))
        self.eqLeft.append(self.eqLeft[-1] + latex(r"\times") + r"\frac{1 inch}{2.54 cm}")
        self.eq.append(self.eqLeft[-1] + "=" + latex(self.eqRight[-1]))
        print("self.eq", self.eq[-1])
        fig = plt.figure()
        text = fig.text(0.1, 0.5, r"$%s$" % self.eq[-1].replace(r"\mathtt{\text{\textbackslashtimes}}", r"\times"),
                        fontsize=30, color="black")
        fig.show()
        self.plot = plt.gcf()
        figLeft = plt.figure()
        textLeft = figLeft.text(0.1, 0.5,
                                r"$%s$" % self.eqLeft[-1].replace(r"\mathtt{\text{\textbackslashtimes}}", r"\times"),
                                fontsize=30, color="black")
        figLeft.show()
        self.plotLeft = plt.gcf()
        figRight = plt.figure()
        textRight = figRight.text(0.1, 0.5,
                                  r"= $%s$" % latex(self.eqRight[-1]).replace(r"\mathtt{\text{\textbackslashtimes}}",
                                                                              r"\times"), fontsize=30, color="black")
        figRight.show()
        self.plotRight = plt.gcf()
        self.factores = self.factores + 1
        print("self.factores", self.factores)

    def setCmInch(self):
        inch = Symbol("inch")
        cm = Symbol("cm")
        self.eqRight.append(N(self.eqRight[-1] * parse_expr(r"(2.54*cm)/(1*inch)"), 3))
        self.eqLeft.append(self.eqLeft[-1] + latex(r"\times") + r"\frac{2.54 cm}{1 inch}")
        self.eq.append(self.eqLeft[-1] + "=" + latex(self.eqRight))
        print("self.eq", self.eq[-1])
        fig = plt.figure()
        text = fig.text(0.1, 0.5, r"$%s$" % self.eq[-1].replace(r"\mathtt{\text{\textbackslashtimes}}", r"\times"),
                        fontsize=30, color="black")
        fig.show()
        self.plot = plt.gcf()
        figLeft = plt.figure()
        textLeft = figLeft.text(0.1, 0.5,
                                r"$%s$" % self.eqLeft[-1].replace(r"\mathtt{\text{\textbackslashtimes}}", r"\times"),
                                fontsize=30, color="black")
        figLeft.show()
        self.plotLeft = plt.gcf()
        figRight = plt.figure()
        textRight = figRight.text(0.1, 0.5,
                                  r"$= %s$" % latex(self.eqRight[-1]).replace(r"\mathtt{\text{\textbackslashtimes}}",
                                                                              r"\times"), fontsize=30, color="black")
        figRight.show()
        self.plotRight = plt.gcf()
        self.factores = self.factores + 1
        print("self.factores", self.factores)

    def setCmM(self):
        m = Symbol("m")
        cm = Symbol("cm")
        self.eqRight.append(N(self.eqRight[-1] * parse_expr(r"(100*cm)/(1*m)"), 3))
        self.eqLeft.append(self.eqLeft[-1] + latex(r"\times") + r"\frac{100 cm}{1 m}")
        self.eq.append(self.eqLeft[-1] + "=" + latex(self.eqRight))
        print("self.eq", self.eq[-1])
        fig = plt.figure()
        text = fig.text(0.1, 0.5, r"$%s$" % self.eq[-1].replace(r"\mathtt{\text{\textbackslashtimes}}", r"\times"),
                        fontsize=30, color="black")
        fig.show()
        self.plot = plt.gcf()
        figLeft = plt.figure()
        textLeft = figLeft.text(0.1, 0.5,
                                r"$%s$" % self.eqLeft[-1].replace(r"\mathtt{\text{\textbackslashtimes}}", r"\times"),
                                fontsize=30, color="black")
        figLeft.show()
        self.plotLeft = plt.gcf()
        figRight = plt.figure()
        textRight = figRight.text(0.1, 0.5,
                                  r"$= %s$" % latex(self.eqRight[-1]).replace(r"\mathtt{\text{\textbackslashtimes}}",
                                                                              r"\times"), fontsize=30, color="black")
        figRight.show()
        self.plotRight = plt.gcf()
        self.factores = self.factores + 1
        print("self.factores", self.factores)

    def setMCm(self):
        m = Symbol("m")
        cm = Symbol("cm")
        self.eqRight.append(N(self.eqRight[-1] * parse_expr(r"(1*m)/(100*cm)"), 3))
        self.eqLeft.append(self.eqLeft[-1] + latex(r"\times") + r"\frac{1 m}{100 cm}")
        self.eq.append(self.eqLeft[-1] + "=" + latex(self.eqRight))
        print("self.eq", self.eq[-1])
        fig = plt.figure()
        text = fig.text(0.1, 0.5, r"$%s$" % self.eq[-1].replace(r"\mathtt{\text{\textbackslashtimes}}", r"\times"),
                        fontsize=30, color="black")
        fig.show()
        self.plot = plt.gcf()
        figLeft = plt.figure()
        textLeft = figLeft.text(0.1, 0.5,
                                r"$%s$" % self.eqLeft[-1].replace(r"\mathtt{\text{\textbackslashtimes}}", r"\times"),
                                fontsize=30, color="black")
        figLeft.show()
        self.plotLeft = plt.gcf()
        figRight = plt.figure()
        textRight = figRight.text(0.1, 0.5,
                                  r"$= %s$" % latex(self.eqRight[-1]).replace(r"\mathtt{\text{\textbackslashtimes}}",
                                                                              r"\times"), fontsize=30, color="black")
        figRight.show()
        self.plotRight = plt.gcf()
        self.factores = self.factores + 1
        print("self.factores", self.factores)

    def setMKm(self):
        m = Symbol("m")
        km = Symbol("km")
        self.eqRight.append(N(self.eqRight[-1] * parse_expr(r"(1000*m)/(1*km)"), 3))
        self.eqLeft.append(self.eqLeft[-1] + latex(r"\times") + r"\frac{1000 m}{1 km}")
        self.eq.append(self.eqLeft[-1] + "=" + latex(self.eqRight))
        print("self.eq", self.eq[-1])
        fig = plt.figure()
        text = fig.text(0.1, 0.5, r"$%s$" % self.eq[-1].replace(r"\mathtt{\text{\textbackslashtimes}}", r"\times"),
                        fontsize=30, color="black")
        fig.show()
        self.plot = plt.gcf()
        figLeft = plt.figure()
        textLeft = figLeft.text(0.1, 0.5,
                                r"$%s$" % self.eqLeft[-1].replace(r"\mathtt{\text{\textbackslashtimes}}", r"\times"),
                                fontsize=30, color="black")
        figLeft.show()
        self.plotLeft = plt.gcf()
        figRight = plt.figure()
        textRight = figRight.text(0.1, 0.5,
                                  r"$= %s$" % latex(self.eqRight[-1]).replace(r"\mathtt{\text{\textbackslashtimes}}",
                                                                              r"\times"), fontsize=30, color="black")
        figRight.show()
        self.plotRight = plt.gcf()
        self.factores = self.factores + 1
        print("self.factores", self.factores)

    def setKmM(self):
        m = Symbol("m")
        km = Symbol("km")
        self.eqRight.append(N(self.eqRight[-1] * parse_expr(r"(1*km)/(1000*m)"), 3))
        self.eqLeft.append(self.eqLeft[-1] + latex(r"\times") + r"\frac{1 km}{1000 m}")
        self.eq.append(self.eqLeft[-1] + "=" + latex(self.eqRight))
        print("self.eq", self.eq[-1])
        fig = plt.figure()
        text = fig.text(0.1, 0.5, r"$%s$" % self.eq[-1].replace(r"\mathtt{\text{\textbackslashtimes}}", r"\times"),
                        fontsize=30, color="black")
        fig.show()
        self.plot = plt.gcf()
        figLeft = plt.figure()
        textLeft = figLeft.text(0.1, 0.5,
                                r"$%s$" % self.eqLeft[-1].replace(r"\mathtt{\text{\textbackslashtimes}}", r"\times"),
                                fontsize=30, color="black")
        figLeft.show()
        self.plotLeft = plt.gcf()
        figRight = plt.figure()
        textRight = figRight.text(0.1, 0.5,
                                  r"$= %s$" % latex(self.eqRight[-1]).replace(r"\mathtt{\text{\textbackslashtimes}}",
                                                                              r"\times"), fontsize=30, color="black")
        figRight.show()
        self.plotRight = plt.gcf()
        self.factores = self.factores + 1
        print("self.factores", self.factores)

    def setHS(self):
        h = Symbol("h")
        s = Symbol("s")
        self.eqRight.append(N(self.eqRight[-1] * parse_expr(r"(1*h)/(3600*s)"), 3))
        self.eqLeft.append(self.eqLeft[-1] + latex(r"\times") + r"\frac{1 h}{3600 s}")
        self.eq.append(self.eqLeft[-1] + "=" + latex(self.eqRight))
        print("self.eq", self.eq[-1])
        fig = plt.figure()
        text = fig.text(0.1, 0.5, r"$%s$" % self.eq[-1].replace(r"\mathtt{\text{\textbackslashtimes}}", r"\times"),
                        fontsize=30, color="black")
        fig.show()
        self.plot = plt.gcf()
        figLeft = plt.figure()
        textLeft = figLeft.text(0.1, 0.5,
                                r"$%s$" % self.eqLeft[-1].replace(r"\mathtt{\text{\textbackslashtimes}}", r"\times"),
                                fontsize=30, color="black")
        figLeft.show()
        self.plotLeft = plt.gcf()
        figRight = plt.figure()
        textRight = figRight.text(0.1, 0.5,
                                  r"$= %s$" % latex(self.eqRight[-1]).replace(r"\mathtt{\text{\textbackslashtimes}}",
                                                                              r"\times"), fontsize=30, color="black")
        figRight.show()
        self.plotRight = plt.gcf()
        self.factores = self.factores + 1
        print("self.factores", self.factores)

    def setSH(self):
        h = Symbol("h")
        s = Symbol("s")
        self.eqRight.append(N(self.eqRight[-1] * parse_expr(r"(3600*s)/(1*h)"), 3))
        self.eqLeft.append(self.eqLeft[-1] + latex(r"\times") + r"\frac{3600 s}{1 h}")
        self.eq.append(self.eqLeft[-1] + "=" + latex(self.eqRight))
        print("self.eq", self.eq[-1])
        fig = plt.figure()
        text = fig.text(0.1, 0.5, r"$%s$" % self.eq[-1].replace(r"\mathtt{\text{\textbackslashtimes}}", r"\times"),
                        fontsize=30, color="black")
        fig.show()
        self.plot = plt.gcf()
        figLeft = plt.figure()
        textLeft = figLeft.text(0.1, 0.5,
                                r"$%s$" % self.eqLeft[-1].replace(r"\mathtt{\text{\textbackslashtimes}}", r"\times"),
                                fontsize=30, color="black")
        figLeft.show()
        self.plotLeft = plt.gcf()
        figRight = plt.figure()
        textRight = figRight.text(0.1, 0.5,
                                  r"$= %s$" % latex(self.eqRight[-1]).replace(r"\mathtt{\text{\textbackslashtimes}}",
                                                                              r"\times"), fontsize=30, color="black")
        figRight.show()
        self.plotRight = plt.gcf()
        self.factores = self.factores + 1
        print("self.factores", self.factores)

    def setOperation(self, termino):
        if termino == "1Inch/2.54cm":
            self.setInchCm()
            print("/" + str(self.eqRight[-1]) + "/")
            print("/" + str(self.sol) + "/")
        elif termino == "2.54cm/1Inch":
            self.setCmInch()
            print("/" + str(self.eqRight[-1]) + "/")
            print("/" + str(self.sol) + "/")
        elif termino == "100cm/1m":
            self.setCmM()
        elif termino == "1m/100cm":
            self.setMCm()
        elif termino == "1000m/1km":
            self.setMKm()
        elif termino == "1km/1000m":
            self.setKmM()
        elif termino == "1h/3600s":
            self.setHS()
        elif termino == "3600s/1h":
            self.setSH()
        else:
            print("Error, el programa no reconoce la operacion")

    def askForSolve(self):
        if str(self.eqRight[-1]) == str(self.sol):
            print("listo!")
            self.Listo = True
            self.texto = "Problema Resuelto."
            figTexto = plt.figure(facecolor=matplotlib.colors.to_rgba([1, 1, 1], 1))
            textTexto = figTexto.text(0.1, 0.5, self.texto, fontsize=30, color="black")
            figTexto.show()
            self.plotTexto = plt.gcf()
            SoundLoader.load("Resources/sound/complete.wav").play()
        elif self.factores >= 3:
            print("Se pasó el numero de intentos")
            # self.askForDeshacer()
            self.askForDeshacer()
            self.Listo = False
            self.texto = "Alcanzó el número máximo\nde factores permitido."
            figTexto = plt.figure(facecolor=matplotlib.colors.to_rgba([1, 1, 1], 1))
            textTexto = figTexto.text(0.1, 0.5, self.texto, fontsize=30, color="black")
            figTexto.show()
            self.plotTexto = plt.gcf()
            SoundLoader.load("Resources/sound/jump.wav").play()
        else:
            print("Aún no está listo")
            self.Listo = False
            self.texto = "Convierta la siguiente\ncantidad a unidades de " + self.units + "."
            figTexto = plt.figure(facecolor=matplotlib.colors.to_rgba([1, 1, 1], 1))
            textTexto = figTexto.text(0.1, 0.5, self.texto, fontsize=30, color="black")
            figTexto.show()
            self.plotTexto = plt.gcf()
            SoundLoader.load("Resources/sound/jump.wav").play()
        print("self.factores", self.factores)
        print("self.eqRight", self.eqRight)


# Clase que incluye los métodos de sympy para despejar ecuaciones.  Esta parte es muy importante porque hace las manipulaciones matemáticas
class equation:

    def __init__(self):  # Metodo constructor
        self.eq = None  # String de la ecuacion
        self.eqLeft = []  # Objeto que guarda el lado izquierdo de la ecuacion, de cada intento
        self.eqRight = []  # Objeto que guarda el lado derecho de la ecuaicon, de cada intento
        self.eqLatex = None  # Objeto con la actual ecuacion en latex
        self.plot = None  # Plot de matplotlib con la ecuacion
        self.operacion = None  # +, -, *, /
        self.sol = None  # Literal con la variable que se pretende despejar en una ecuacion
        self.sol_sym = None  # Mismo que el anterior pero en formato sympy
        self.listo = False  # Booleano: Ecuación resuelta o no
        self.texto = None  # Texto que se desplega en la parte superior de la pantalla. Indica la variable que hay que despejar.
        self.plotTexto = None  # Texto anterior en formato matplotlib
        self.intentos = []  # Se van guardando los intentos que se hacen por si fuera necesario retroceder

    def setEquation(self):  # Una vez que se establece la variable self.eq, este metodo genera la version en latex
        parts = self.eq.split("=")  # Divide los dos lados de la ecuacion en el igual
        self.sol_sym = parse_expr(self.sol)  # Guarda la solución en formato sympy
        self.eqLeft.append(parse_expr(parts[0]))  # Guarda el lado izquierdo de la ecuación en formato sympy
        self.eqRight.append(parse_expr(parts[1]))  # Guarda el lado derecho de la ecuación en formato sympy
        self.eqLatex = latex(Eq(self.eqLeft[-1], self.eqRight[-1]))  # Genera la ecuación en latex
        self.intentos.append(self.eqLatex)  # Guarda la ecuación como el intento más reciente
        fig = plt.figure(facecolor=matplotlib.colors.to_rgba([1, 1, 1], 1))  # Genera la figura
        text = fig.text(0.1, 0.5, r"$%s$" % (self.eqLatex), fontsize=30, color="black")  # El estilo se especifica aquí.
        fig.show()
        self.plot = plt.gcf()
        size = fig.get_size_inches() * fig.dpi  # size in pixels
        print("Tamaño", size)
        # Esta es la variable que se recupera luego para mostrar la ecuacion en pantalla
        self.texto = r"Despeje la variable " + r"$%s$" % (self.sol)  # Despeje tal variable
        figTexto = plt.figure(facecolor=matplotlib.colors.to_rgba([1, 1, 1], 1))  # Se genera la figura
        textTexto = figTexto.text(0.1, 0.5, self.texto, fontsize=30, color="black")  # El estilo se especifica aquí.
        figTexto.show()
        self.plotTexto = plt.gcf()  # Esta variable muestra la etiqueta en pantalla

    # Este método regresa el estado del juego al estado anterior
    def askForDeshacer(self):

        # Si se llega al primer intento, ya no se puede regresar más

        if len(self.eqLeft) > 1:  # Solo se puede regresar hasta el primer intento
            self.intentos = self.intentos[:-1]  # Elimina el ultimo elemento

            self.eqRight = self.eqRight[:-1]  # Elimina la ultima ecuacion
            self.eqLeft = self.eqLeft[:-1]  # Elimina la ultima ecuacion

            self.eqLatex = latex(Eq(self.eqLeft[-1], self.eqRight[-1]))  # Ecuacion actual
            fig = plt.figure(facecolor=matplotlib.colors.to_rgba([1, 1, 1], 1))
            text = fig.text(0.1, 0.5, r"$%s$" % (self.eqLatex), fontsize=30,
                            color="black")  # El estilo se especifica aquí.
            fig.show()
            self.plot = plt.gcf()
            self.listo = False  # Aún no está listo
            self.texto = r"Despeje la variable " + r"$%s$" % (self.sol)
            print("Se ejecutó el setEquation, la ecuacion es" + self.eq)
            figTexto = plt.figure(facecolor=matplotlib.colors.to_rgba([1, 1, 1], 1))
            textTexto = figTexto.text(0.1, 0.5, self.texto, fontsize=30, color="black")  # El estilo se especifica aquí.
            figTexto.show()
            self.plotTexto = plt.gcf()

    # Devuelve el estado del juego hacia el inicio
    def askForResetear(self):
        self.eqLatex = self.intentos[0]  # Aquí es donde se resetea
        parts = self.eq.split("=")
        self.sol_sym = parse_expr(self.sol)
        self.eqLeft.append(parse_expr(parts[0]))
        self.eqRight.append(parse_expr(parts[1]))
        fig = plt.figure(facecolor=matplotlib.colors.to_rgba([1, 1, 1], 1))
        text = fig.text(0.1, 0.5, r"$%s$" % (self.eqLatex), fontsize=30,
                        color="black")  # El estilo se especifica aquí.
        fig.show()
        self.plot = plt.gcf()
        self.listo = False
        self.texto = r"Despeje la variable " + r"$%s$" % (self.sol)
        print("Se ejecutó el setEquation, la ecuacion es" + self.eq)
        figTexto = plt.figure(facecolor=matplotlib.colors.to_rgba([1, 1, 1], 1))
        textTexto = figTexto.text(0.1, 0.5, self.texto, fontsize=30, color="black")  # El estilo se especifica aquí.
        figTexto.show()
        self.plotTexto = plt.gcf()

    # Método de prueba.  Lo único que hace es sumar 1 a ambos lados de la ecuacion
    def sumaUno(self):  # Metodo de prueba; se suma 1 a cada lado de ecuacion
        self.eqLeft.append(self.eqLeft[-1] + 1)  # Aquí se lleva a cabo la suma de 1
        self.eqRight.append(self.eqRight[-1] + 1)  # Aquí se lleva a cabo la suma de 1
        self.eqLatex = latex(Eq(self.eqLeft[-1], self.eqRight[-1]))
        self.intentos.append(self.eqLatex)
        fig = plt.figure(facecolor=matplotlib.colors.to_rgba([1, 1, 1], 1))
        text = fig.text(0.1, 0.5, r"$%s$" % (self.eqLatex), fontsize=30, color="black")
        fig.show()
        self.plot = plt.gcf()

    # Se suma la variable termino a ambos lados de la ecuación
    def add(self, termino):  # Se suma el termino a cada lado de la ecuacion
        self.eqLeft.append(self.eqLeft[-1] + parse_expr(termino))  # Se suma termino del lado izquierdo
        self.eqRight.append(self.eqRight[-1] + parse_expr(termino))  # Se suma termino del lado derecho
        self.eqLatex = latex(Eq(self.eqLeft[-1], self.eqRight[-1]))
        self.intentos.append(self.eqLatex)
        print("tamaño", len(self.eqLatex))
        fig = plt.figure(facecolor=matplotlib.colors.to_rgba([1, 1, 1], 1))

        text = fig.text(0.1, 0.5, r"$%s$" % (self.eqLatex), fontsize=30, color="black")
        fig.show()
        self.plot = plt.gcf()

    # Se sustrae termrino de ambos lados
    def subs(self, termino):  # Se resta el termino a cada lado de la ecuacion
        self.eqLeft.append(self.eqLeft[-1] - parse_expr(termino))  # Se resta
        self.eqRight.append(self.eqRight[-1] - parse_expr(termino))  # Se resta
        self.eqLatex = latex(Eq(self.eqLeft[-1], self.eqRight[-1]))
        self.intentos.append(self.eqLatex)
        fig = plt.figure(facecolor=matplotlib.colors.to_rgba([1, 1, 1], 1))
        text = fig.text(0.1, 0.5, r"$%s$" % (self.eqLatex), fontsize=30, color="black")
        fig.show()
        self.plot = plt.gcf()

    # Se multiplica termino a ambos lados
    def mult(self, termino):  # Se multiplica el termino a cada lado de la ecuacion
        self.eqLeft.append(self.eqLeft[-1] * parse_expr(termino))  # Se multiplica
        self.eqRight.append(self.eqRight[-1] * parse_expr(termino))  # Se multiplica
        self.eqLatex = latex(Eq(self.eqLeft[-1], self.eqRight[-1]))
        self.intentos.append(self.eqLatex)
        fig = plt.figure(facecolor=matplotlib.colors.to_rgba([1, 1, 1], 1))
        text = fig.text(0.1, 0.5, r"$%s$" % (self.eqLatex), fontsize=30, color="black")
        fig.show()
        self.plot = plt.gcf()

    # Se divide termino a ambos lados
    def div(self, termino):  # Se divide el termino a cada lado de la ecuacion
        self.eqLeft.append(self.eqLeft[-1] / parse_expr(termino))  # Se divide
        self.eqRight.append(self.eqRight[-1] / parse_expr(termino))  # Se divide
        self.eqLatex = latex(Eq(self.eqLeft[-1], self.eqRight[-1]))
        self.intentos.append(self.eqLatex)
        fig = plt.figure(facecolor=matplotlib.colors.to_rgba([1, 1, 1], 1))
        text = fig.text(0.1, 0.5, r"$%s$" % (self.eqLatex), fontsize=30, color="black")
        fig.show()
        self.plot = plt.gcf()

    # Se simplifican a ambos lados
    def askForSimplify(self):
        self.eqLeft.append(powdenest(simplify(self.eqLeft[-1], inverse=True), force=True))
        self.eqRight.append(powdenest(simplify(self.eqRight[-1], inverse=True), force=True))
        self.eqLatex = latex(Eq(self.eqLeft[-1], self.eqRight[-1]))
        self.intentos.append(self.eqLatex)
        fig = plt.figure(facecolor=matplotlib.colors.to_rgba([1, 1, 1], 1))
        text = fig.text(0.1, 0.5, r"$%s$" % (self.eqLatex), fontsize=30, color="black")
        fig.show()
        self.plot = plt.gcf()

    # Se factorizan a ambos lados
    def askForFactor(self):
        self.eqLeft.append(factor(self.eqLeft[-1]))
        self.eqRight.append(factor(self.eqRight[-1]))
        self.eqLatex = latex(Eq(self.eqLeft[-1], self.eqRight[-1]))
        self.intentos.append(self.eqLatex)
        fig = plt.figure(facecolor=matplotlib.colors.to_rgba([1, 1, 1], 1))
        text = fig.text(0.1, 0.5, r"$%s$" % (self.eqLatex), fontsize=30, color="black")
        fig.show()
        self.plot = plt.gcf()

    # Se expanden ambos lados
    def askForExpand(self):
        self.eqLeft.append(expand(self.eqLeft[-1]))
        self.eqRight.append(expand(self.eqRight[-1]))
        self.eqLatex = latex(Eq(self.eqLeft[-1], self.eqRight[-1]))
        self.intentos.append(self.eqLatex)
        fig = plt.figure(facecolor=matplotlib.colors.to_rgba([1, 1, 1], 1))
        text = fig.text(0.1, 0.5, r"$%s$" % (self.eqLatex), fontsize=30, color="black")
        fig.show()
        self.plot = plt.gcf()

    # Se obtiene el cuadrado de abmos lados
    def askForSquare(self):
        self.eqLeft.append(self.eqLeft[-1] ** 2)
        self.eqRight.append(self.eqRight[-1] ** 2)
        self.eqLatex = latex(Eq(self.eqLeft[-1], self.eqRight[-1]))
        self.intentos.append(self.eqLatex)
        fig = plt.figure(facecolor=matplotlib.colors.to_rgba([1, 1, 1], 1))
        text = fig.text(0.1, 0.5, r"$%s$" % (self.eqLatex), fontsize=30, color="black")
        fig.show()
        self.plot = plt.gcf()

    # Se obtiene la raíz cuadrada de ambos lados
    def askForRoot(self):
        self.eqLeft.append(powdenest(root(self.eqLeft[-1], 2),
                                     force=True))  # Es necesario que el código asuma que todas las variables son reales
        self.eqRight.append(powdenest(root(self.eqRight[-1], 2),
                                      force=True))  # Es necesario que el código asuma que todas las variables son reales
        self.eqLatex = latex(Eq(self.eqLeft[-1], self.eqRight[-1]))
        self.intentos.append(self.eqLatex)
        fig = plt.figure(facecolor=matplotlib.colors.to_rgba([1, 1, 1], 1))
        text = fig.text(0.1, 0.5, r"$%s$" % (self.eqLatex), fontsize=30, color="black")
        fig.show()
        self.plot = plt.gcf()

    def askForCos(self):
        self.eqLeft.append(cos(self.eqLeft[-1]))
        self.eqRight.append(cos(self.eqRight[-1]))
        self.eqLatex = latex(Eq(self.eqLeft[-1], self.eqRight[-1]))
        self.intentos.append(self.eqLatex)
        fig = plt.figure(facecolor=matplotlib.colors.to_rgba([1, 1, 1], 1))
        text = fig.text(0.1, 0.5, r"$%s$" % (self.eqLatex), fontsize=30, color="black")
        fig.show()
        self.plot = plt.gcf()

    def askForACos(self):
        self.eqLeft.append(acos(self.eqLeft[-1]))
        self.eqRight.append(acos(self.eqRight[-1]))
        self.eqLatex = latex(Eq(self.eqLeft[-1], self.eqRight[-1]))
        self.intentos.append(self.eqLatex)
        fig = plt.figure(facecolor=matplotlib.colors.to_rgba([1, 1, 1], 1))
        text = fig.text(0.1, 0.5, r"$%s$" % (self.eqLatex), fontsize=30, color="black")
        fig.show()
        self.plot = plt.gcf()

    def askForSin(self):
        self.eqLeft.append(sin(self.eqLeft[-1]))
        self.eqRight.append(sin(self.eqRight[-1]))
        self.eqLatex = latex(Eq(self.eqLeft[-1], self.eqRight[-1]))
        self.intentos.append(self.eqLatex)
        fig = plt.figure(facecolor=matplotlib.colors.to_rgba([1, 1, 1], 1))
        text = fig.text(0.1, 0.5, r"$%s$" % (self.eqLatex), fontsize=30, color="black")
        fig.show()
        self.plot = plt.gcf()

    def askForASin(self):
        self.eqLeft.append(asin(self.eqLeft[-1]))
        self.eqRight.append(asin(self.eqRight[-1]))
        self.eqLatex = latex(Eq(self.eqLeft[-1], self.eqRight[-1]))
        self.intentos.append(self.eqLatex)
        fig = plt.figure(facecolor=matplotlib.colors.to_rgba([1, 1, 1], 1))
        text = fig.text(0.1, 0.5, r"$%s$" % (self.eqLatex), fontsize=30, color="black")
        fig.show()
        self.plot = plt.gcf()

    def askForTan(self):
        self.eqLeft.append(tan(self.eqLeft[-1]))
        self.eqRight.append(tan(self.eqRight[-1]))
        self.eqLatex = latex(Eq(self.eqLeft[-1], self.eqRight[-1]))
        self.intentos.append(self.eqLatex)
        fig = plt.figure(facecolor=matplotlib.colors.to_rgba([1, 1, 1], 1))
        text = fig.text(0.1, 0.5, r"$%s$" % (self.eqLatex), fontsize=30, color="black")
        fig.show()
        self.plot = plt.gcf()

    def askForATan(self):
        self.eqLeft.append(atan(self.eqLeft[-1]))
        self.eqRight.append(atan(self.eqRight[-1]))
        self.eqLatex = latex(Eq(self.eqLeft[-1], self.eqRight[-1]))
        self.intentos.append(self.eqLatex)
        fig = plt.figure(facecolor=matplotlib.colors.to_rgba([1, 1, 1], 1))
        text = fig.text(0.1, 0.5, r"$%s$" % (self.eqLatex), fontsize=30, color="black")
        fig.show()
        self.plot = plt.gcf()

    # Se elige la operación elemental a utilizar
    def setOperacion(self, termino):
        if self.operacion == "+":
            self.add(termino)
        elif self.operacion == "-":
            self.subs(termino)
        elif self.operacion == "*":
            self.mult(termino)
        elif self.operacion == "/":
            self.div(termino)
        else:
            print("Error de operacion")

    # Se elige la operacion especial a utilizar
    def setOperacionEspecial(self, termino):
        if termino == "Simplify":
            self.askForSimplify()
        elif termino == "Factor":
            self.askForFactor()
        elif termino == "Expand":
            self.askForExpand()
        elif termino == "√□":
            self.askForRoot()
        elif termino == "□²":
            self.askForSquare()
        elif termino == "cos(□)":
            self.askForCos()
        elif termino == "acos(□)":
            self.askForACos()
        elif termino == "sin(□)":
            self.askForSin()
        elif termino == "asin(□)":
            self.askForASin()
        elif termino == "tan(□)":
            self.askForTan()
        elif termino == "atan(□)":
            self.askForAtan()
        else:
            print("Error. No se entiende de qué es este botón")

    # Este método determina si la ecuación ya ha sido resuelta o no
    def askForSolve(self):

        a1 = str(self.eqLeft[-1]) == str(
            self.sol)  # El lado izquierdo de la ecuación es exactamente igual a la variable a resolver
        a2 = str(self.eqRight[-1]) == str(
            self.sol)  # El lado derecho de la ecuación es exactamente igual a la variable a resolver
        b1 = str(self.sol) in str(self.eqLeft[-1]).replace("sqrt",
                                                           "")  # La variable a resolver se encuentra del lado izquierdo.  Con el propósito de que no crea que t está en sqrt
        b2 = str(self.sol) in str(self.eqRight[-1]).replace("sqrt",
                                                            "")  # La variable a resolver se encuentra del lado derecho.  Con el propósito de que no crea que t está en sqrt

        # Si la variable a resolver es igual al lado izquierdo, y no se encuentra del lado derecho
        # la ecuación está resuelta
        if a1 and not b2:
            self.listo = True
            self.texto = r"Ecuacion despejada ¡Muchas felicidades!"
            print("Ecuacion despejada ¡Muchas felicidades! CASO !")
            figTexto = plt.figure(facecolor=matplotlib.colors.to_rgba([1, 1, 1], 1))
            textTexto = figTexto.text(0.1, 0.5, self.texto, fontsize=20,
                                      color="black")  # El estilo se especifica aquí.
            figTexto.show()
            self.plotTexto = plt.gcf()
            SoundLoader.load("Resources/sound/complete.wav").play()

        # Si la variable a resolver es igual al lado derecho, y no se encuentra del lado izquierdo
        # la ecuación está resuelta
        elif a2 and not b1:
            self.listo = True
            self.texto = r"Ecuacion despejada ¡Muchas felicidades!"
            print("Ecuacion despejada ¡Muchas felicidades! CASO 2")
            figTexto = plt.figure(facecolor=matplotlib.colors.to_rgba([1, 1, 1], 1))
            textTexto = figTexto.text(0.1, 0.5, self.texto, fontsize=20,
                                      color="black")  # El estilo se especifica aquí.
            figTexto.show()
            self.plotTexto = plt.gcf()
            SoundLoader.load("Resources/sound/complete.wav").play()

        # En cualquier otro caso se considera que la ecuación no esta resuelta
        else:
            self.listo = False
            self.texto = r"Despeje la variable " + r"$%s$" % (self.sol)
            print("Se ejecutó el setEquation, la ecuacion es" + self.eq + "CASO 3")
            figTexto = plt.figure(facecolor=matplotlib.colors.to_rgba([1, 1, 1], 1))
            textTexto = figTexto.text(0.1, 0.5, self.texto, fontsize=30, color="black")  # El estilo se especifica aquí.
            figTexto.show()
            self.plotTexto = plt.gcf()
            SoundLoader.load("Resources/sound/jump.wav").play()

    # Una estructura semejante se puede usar para otros metodos
    # Elevar exponentes, sacar raices a ambos lados, sen, sen-1, ... etc
    # Conforme se van añadiendo ecuaciones se pueden ir añadiendo otros metodos


# Clase que maneja las ecuaciones de la segudna ley de Newton

class eqNewton:
    def __init__(self):
        self.eqLeft = []
        self.eqLeft.append(parse_expr("0"))
        self.a = None
        self.plotLeft = None
        self.plotRight = None
        self.operacion = None
        self.sol = None
        self.Listo = None
        self.Texto = None
        self.plotTexto = None

    def setEquation(self):
        if self.a == "ax":
            figRight = plt.figure()
            textRight = figRight.text(0.1, 0.6, r"= $m a_x$", fontsize=30, color="black")
            figRight.show()
            self.plotRight = plt.gcf()
        elif self.a == "ay":
            figRight = plt.figure()
            textRight = figRight.text(0.1, 0.6, r"= $m a_y$", fontsize=30, color="black")
            figRight.show()
            self.plotRight = plt.gcf()
        else:
            print("Resultado para a no válido.")

        figLeft = plt.figure()
        textLeft = figLeft.text(0.1, 0.5, r"$%s$" % latex(self.eqLeft[-1]), fontsize=30, color="black")
        figLeft.show()
        self.plotLeft = plt.gcf()

        self.texto = "Construya la segunda\nley de Newton"  # Despeje tal variable
        figTexto = plt.figure(facecolor=matplotlib.colors.to_rgba([1, 1, 1], 1))  # Se genera la figura
        textTexto = figTexto.text(0.1, 0.3, self.texto, fontsize=30, color="black")  # El estilo se especifica aquí.
        figTexto.show()
        self.plotTexto = plt.gcf()

    def askForDeshacer(self):
        if len(self.eqLeft) > 1:
            self.eqLeft = self.eqLeft[:-1]
            figLeft = plt.figure()
            textLeft = figLeft.text(0.1, 0.5, r"$%s$" % latex(self.eqLeft[-1]), fontsize=30, color="black")
            figLeft.show()
            self.plotLeft = plt.gcf()

    def askForResetear(self):
        if len(self.eqLeft) > 1:
            self.eqLeft.append(self.eqLeft[0])
            figLeft = plt.figure()
            textLeft = figLeft.text(0.1, 0.5, r"$%s$" % latex(self.eqLeft[-1]), fontsize=30, color="black")
            figLeft.show()
            self.plotLeft = plt.gcf()

    def add(self, termino):
        self.eqLeft.append(self.eqLeft[-1] + parse_expr(termino))
        figLeft = plt.figure()
        textLeft = figLeft.text(0.1, 0.5, r"$%s$" % latex(self.eqLeft[-1]), fontsize=30, color="black")
        figLeft.show()
        self.plotLeft = plt.gcf()

    def subs(self, termino):
        self.eqLeft.append(self.eqLeft[-1] - parse_expr(termino))
        figLeft = plt.figure()
        textLeft = figLeft.text(0.1, 0.5, r"$%s$" % latex(self.eqLeft[-1]), fontsize=30, color="black")
        figLeft.show()
        self.plotLeft = plt.gcf()

    def mult(self, termino):
        self.eqLeft.append(self.eqLeft[-1] * parse_expr(termino))
        figLeft = plt.figure()
        textLeft = figLeft.text(0.1, 0.5, r"$%s$" % latex(self.eqLeft[-1]), fontsize=30, color="black")
        figLeft.show()
        self.plotLeft = plt.gcf()

    def div(self, termino):
        self.eqLeft.append(self.eqLeft[-1] * parse_expr(termino))
        figLeft = plt.figure()
        textLeft = figLeft.text(0.1, 0.5, r"$%s$" % latex(self.eqLeft[-1]), fontsize=30, color="black")
        figLeft.show()
        self.plotLeft = plt.gcf()

    # Se elige la operación elemental a utilizar
    def setOperacion(self, termino):
        if self.operacion == "+":
            self.add(termino)
        elif self.operacion == "-":
            self.subs(termino)
        elif self.operacion == "*":
            self.mult(termino)
        elif self.operacion == "/":
            self.div(termino)
        else:
            print("Error de operacion")

    def askForSolve(self):
        if self.eqLeft[-1] == self.sol:
            self.Listo = True
            self.texto = r"¡Ecuación construida!"  # Despeje tal variable
            figTexto = plt.figure(facecolor=matplotlib.colors.to_rgba([1, 1, 1], 1))  # Se genera la figura
            textTexto = figTexto.text(0.1, 0.5, self.texto, fontsize=30, color="black")  # El estilo se especifica aquí.
            figTexto.show()
            self.plotTexto = plt.gcf()
            SoundLoader.load("Resources/sound/complete.wav").play()
            print(self.eqLeft[-1])
            print(self.sol)
        else:
            self.Listo = False
            self.texto = "Construya la segunda\nley de Newton"  # Despeje tal variable
            figTexto = plt.figure(facecolor=matplotlib.colors.to_rgba([1, 1, 1], 1))  # Se genera la figura
            textTexto = figTexto.text(0.1, 0.3, self.texto, fontsize=30, color="black")  # El estilo se especifica aquí.
            figTexto.show()
            self.plotTexto = plt.gcf()
            SoundLoader.load("Resources/sound/jump.wav").play()
            print(self.eqLeft[-1])
            print(self.sol)


# Clase epxperimental que define el diseño de un nivel donde se hace un cambio de unidades

class RootWidgetConversiones(Screen):
    def __init__(self, cantidad, sol, buttons, units, **kwargs):
        super(RootWidgetConversiones, self).__init__(**kwargs)

        # Esta sección establece el color del fondo.  Realmente no sé bien cómo funciona

        self.bind(
            size=self._update_rect,
            pos=self._update_rect
        )
        # BACKGROUND = (.15, .74, .96, 1)
        with self.canvas.before:
            Color(1, 1, 1, 1)  ## Aquí va el color
            self.rect = Rectangle(
                size=self.size,
                pos=self.pos
            )

        ecuacion = Conversion()
        ecuacion.units = units
        ecuacion.cantidad = cantidad  # "5.0 * cm"
        ecuacion.sol = sol  # "1.97*inch"
        ecuacion.setEquation()

        # Layout para botones
        buttonLayout = BoxLayout(size_hint=[None, None], width=450, height=80,
                                 spacing=int((2 * WIDTH - 3 * 150) / (3 + 1)))  # Porque son 3 botones
        # Layout con el mensaje
        mensaje = BoxLayout(size_hint=[1, None], height=200)
        self.botonRegreso = Button(background_normal="Resources/images/BlueRectangleButton.png",
                                   background_down="Resources/images/BlueDarkRectangleButton.png", border=(1, 1, 1, 1),
                                   text="Regreso", size_hint=[None, None], width=150, height=80,
                                   font_name="DejaVuSans.ttf")
        self.botonDeshacer = Button(background_normal="Resources/images/BlueRectangleButton.png",
                                    background_down="Resources/images/BlueDarkRectangleButton.png", border=(1, 1, 1, 1),
                                    text="Deshacer", size_hint=[None, None], width=150, height=80,
                                    font_name="DejaVuSans.ttf")
        self.botonResetear = Button(background_normal="Resources/images/BlueRectangleButton.png",
                                    background_down="Resources/images/BlueDarkRectangleButton.png", border=(1, 1, 1, 1),
                                    text="Resetear", size_hint=[None, None], width=150, height=80,
                                    font_name="DejaVuSans.ttf")
        buttonLayout.add_widget(
            BoxLayout(size_hint=[1, 1], spacing=int((2 * WIDTH - 3 * 150) / (3 + 1))))  # Haciendo espacio
        buttonLayout.add_widget(self.botonRegreso)
        buttonLayout.add_widget(self.botonDeshacer)
        buttonLayout.add_widget(self.botonResetear)
        textoJuego = FigureCanvasKivyAgg(ecuacion.plotTexto)
        mensaje.add_widget(textoJuego)

        pantalla1 = RelativeLayout()  # La pantalla es la seccion donde sale la ecuacion
        expresionLeft = FigureCanvasKivyAgg(ecuacion.plotLeft)
        pantalla1.add_widget(expresionLeft)

        pantalla2 = RelativeLayout()  # La pantalla es la seccion donde sale la ecuacion
        expresionRight = FigureCanvasKivyAgg(ecuacion.plotRight)
        pantalla2.add_widget(expresionRight)

        layoutBotonesOperaciones = BoxLayout(orientation="horizontal", padding=2, size_hint=[1, None], height=150,
                                             spacing=int((2 * WIDTH - 150 - 4 * 120) / (4 + 2)))

        stringButtonsOperations = buttons.split()  # "1Inch/2.54cm 2.54cm/1Inch".split()
        buttonsOperationsList = []

        for i in stringButtonsOperations:
            buttonsOperationsList.append(Button(background_normal="Resources/images/BlueRectangleButton.png",
                                                background_down="Resources/images/BlueDarkRectangleButton.png",
                                                border=(1, 1, 1, 1), text=i, size_hint=[None, None], width=150,
                                                height=150 / 2, font_name="DejaVuSans.ttf", font_size=20))

        layoutMenuOperaciones = GridLayout(size_hint=[1, 1], cols=4, padding=2,
                                           spacing=int((2 * WIDTH - 150 - 4 * 120) / (4 + 3)))

        for j in buttonsOperationsList:
            layoutMenuOperaciones.add_widget(j)

        layoutBotonesOperaciones.add_widget(
            GridLayout(size_hint=[1 / (4 + 3) - (150 + 4 * 120) / ((4 + 3) * 2 * WIDTH), None]))  # Por hacer espacio
        layoutBotonesOperaciones.add_widget(layoutMenuOperaciones)

        # Se añade cada elemento

        def _update_rect(layoutFinal, instance, value):
            self.rect.pos = instance.pos
            self.rect.size = instance.size

        layoutFinal = BoxLayout(orientation="vertical", spacing=40)

        layoutFinal.add_widget(GridLayout(size_hint=[None, 0.15]))  # Para hacer espacio
        layoutFinal.add_widget(buttonLayout)
        layoutFinal.add_widget(GridLayout(size_hint=[None, 0.15]))  # Para hacer espacio
        layoutFinal.add_widget(mensaje)
        layoutFinal.add_widget(pantalla1)
        layoutFinal.add_widget(pantalla2)
        layoutFinal.add_widget(GridLayout(size_hint=[None, 0.15]))  # Para hacer espacio
        layoutFinal.add_widget(layoutBotonesOperaciones)
        layoutFinal.add_widget(GridLayout(size_hint=[None, 0.15]))  # Para hacer espacio

        self.add_widget(layoutFinal)

        def setEquation(self):
            ecuacion.setEquation()
            pantalla1.add_widget(FigureCanvasKivyAgg(ecuacion.plotLeft))
            pantalla2.add_widget(FigureCanvasKivyAgg(ecuacion.plotRight))
            ecuacion.askForSolve()
            mensaje.clear_widgets()
            textoJuego = FigureCanvasKivyAgg(ecuacion.plotTexto)
            mensaje.add_widget(textoJuego)

        def setDeshacer(self):
            ecuacion.askForDeshacer()
            pantalla1.add_widget(FigureCanvasKivyAgg(ecuacion.plotLeft))
            pantalla2.add_widget(FigureCanvasKivyAgg(ecuacion.plotRight))
            ecuacion.askForSolve()
            mensaje.clear_widgets()
            textoJuego = FigureCanvasKivyAgg(ecuacion.plotTexto)
            mensaje.add_widget(textoJuego)

        def setResetear(self):
            ecuacion.askForResetear()
            pantalla1.add_widget(FigureCanvasKivyAgg(ecuacion.plotLeft))
            pantalla2.add_widget(FigureCanvasKivyAgg(ecuacion.plotRight))
            ecuacion.askForSolve()
            mensaje.clear_widgets()
            textoJuego = FigureCanvasKivyAgg(ecuacion.plotTexto)
            mensaje.add_widget(textoJuego)

        self.botonRegreso.bind(on_press=setEquation)
        self.botonDeshacer.bind(on_press=setDeshacer)
        self.botonResetear.bind(on_press=setResetear)

        def setButtonOperaciones(self):
            termino = self.text
            print("La operacion es: " + termino)
            ecuacion.setOperation(termino)  # setOperacionEspecial(termino)
            expresionLeft = FigureCanvasKivyAgg(ecuacion.plotLeft)
            pantalla1.add_widget(expresionLeft)
            expresionRight = FigureCanvasKivyAgg(ecuacion.plotRight)
            pantalla2.add_widget(expresionRight)

            ecuacion.askForSolve()
            mensaje.clear_widgets()
            textoJuego = FigureCanvasKivyAgg(ecuacion.plotTexto)
            mensaje.add_widget(textoJuego)

            # Conforme se vayan creando más botones se puede pensar en operaciones semejantes

        for k in buttonsOperationsList:
            k.bind(on_press=setButtonOperaciones)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


# La clase que determina una pantalla donde se hace el juego
# Toma como parametros un string con los buttons (terminos que el juegador puede sumar, restar, dividir o multiplicar)
# ec es un literal con la ecuacion que debe despejar
# sol es la variable que debe despejar
# buttonsOperations se refiere a as demás operaciones permitidas, sacar raices, exponentes, factorizar, etc..
class RootWidget(Screen):
    def __init__(self, buttons, ec, sol, buttonsOperations, **kwargs):
        super(RootWidget, self).__init__(**kwargs)

        # Esta sección establece el color del fondo.  Realmente no sé bien cómo funciona

        self.bind(
            size=self._update_rect,
            pos=self._update_rect
        )
        # BACKGROUND = (.15, .74, .96, 1)
        with self.canvas.before:
            Color(1, 1, 1, 1)  ## Aquí va el color
            self.rect = Rectangle(
                size=self.size,
                pos=self.pos
            )

        self.ec = ec

        ecuacion = equation()
        ecuacion.eq = self.ec
        ecuacion.sol = sol
        ecuacion.setEquation()

        # Layout para botones
        buttonLayout = BoxLayout(size_hint=[None, None], width=450, height=80,
                                 spacing=int((2 * WIDTH - 3 * 150) / (3 + 1)))  # Porque son 3 botones
        # Layout con el mensaje
        mensaje = BoxLayout(size_hint=[1, None], height=150)
        self.botonRegreso = Button(background_normal="Resources/images/BlueRectangleButton.png",
                                   background_down="Resources/images/BlueDarkRectangleButton.png", border=(1, 1, 1, 1),
                                   text="Regreso", size_hint=[None, None], width=150, height=80,
                                   font_name="DejaVuSans.ttf")
        self.botonDeshacer = Button(background_normal="Resources/images/BlueRectangleButton.png",
                                    background_down="Resources/images/BlueDarkRectangleButton.png", border=(1, 1, 1, 1),
                                    text="Deshacer", size_hint=[None, None], width=150, height=80,
                                    font_name="DejaVuSans.ttf")
        self.botonResetear = Button(background_normal="Resources/images/BlueRectangleButton.png",
                                    background_down="Resources/images/BlueDarkRectangleButton.png", border=(1, 1, 1, 1),
                                    text="Resetear", size_hint=[None, None], width=150, height=80,
                                    font_name="DejaVuSans.ttf")
        buttonLayout.add_widget(
            BoxLayout(size_hint=[1, 1], spacing=int((2 * WIDTH - 3 * 150) / (3 + 1))))  # Haciendo espacio
        buttonLayout.add_widget(self.botonRegreso)
        buttonLayout.add_widget(self.botonDeshacer)
        buttonLayout.add_widget(self.botonResetear)
        textoJuego = FigureCanvasKivyAgg(ecuacion.plotTexto)
        mensaje.add_widget(textoJuego)
        # layoutSuperior.add_widget(buttonLayout)
        # layoutSuperior.add_widget(mensaje)

        pantalla = RelativeLayout()  # La pantalla es la seccion donde sale la ecuacion
        expresion = FigureCanvasKivyAgg(ecuacion.plot)
        pantalla.add_widget(expresion)

        stringButtons = buttons  # "t v d"
        stringsButtons = stringButtons.split()

        buttonsTerms = []

        # Este for permite crear los buttons de manera iteractiva
        for i in stringsButtons:
            buttonsTerms.append(Button(background_normal="Resources/images/BlueButton.png",
                                       background_down="Resources/images/BlueDarkButton.png", border=(1, 1, 1, 1),
                                       text=i, size_hint=[None, None], width=100, height=100,
                                       font_name="DejaVuSans.ttf", font_size=20))

        NBotones = len(stringsButtons)
        print("El ancho es", Window.size[0])
        if NBotones < 5:
            espaciamiento = int((2 * WIDTH - NBotones * 100) / (NBotones + 1))
            espaciamientoBlanco = (1 / (NBotones + 1) - NBotones * 100 / ((NBotones + 1) * 2 * 375))
        else:
            espaciamiento = int((2 * WIDTH - (5) * 100) / (5 + 1))
            espaciamientoBlanco = (1 / (5 + 1) - 5 * 100 / ((5 + 1) * 2 * 375))
        print("espaciamientoBlanco", espaciamientoBlanco)
        # Se crea el layout con los botones con los términos que se desean añadir
        layoutMedio = BoxLayout(orientation="horizontal", height=200)
        # espaciamientoBlanco = int(( 2*WIDTH - (5) * 100) / (5 + 1))
        layoutMedio.add_widget(GridLayout(size_hint=[espaciamientoBlanco, 1]))  # Por hacer espacio
        layoutBotonesTerminos = GridLayout(cols=5, padding=2, spacing=espaciamiento, size_hint=[1, None], height=200)

        for j in buttonsTerms:
            layoutBotonesTerminos.add_widget(j)

        layoutMedio.add_widget(layoutBotonesTerminos)
        # Se crea el layout con los botones con las operaciones que se desean añadir
        # Por defecto, se empieza con una suma
        layoutBotonesOperaciones = BoxLayout(orientation="horizontal", padding=2, size_hint=[1, None], height=150,
                                             spacing=int((2 * WIDTH - 150 - 4 * 120) / (4 + 2)))
        # Layout 2x2 de botones de operaciones matematicas
        cuadroBotones = GridLayout(size_hint=[None, 1], width=150, cols=2, padding=2)
        buttonMas = ToggleButton(background_normal="Resources/images/BlueButton.png",
                                 background_down="Resources/images/BlueDarkButton.png", border=(1, 1, 1, 1), text="+",
                                 group="operaciones", state="down", font_name="DejaVuSans.ttf")
        ecuacion.operacion = "+"
        cuadroBotones.add_widget(buttonMas)
        buttonMenos = ToggleButton(background_normal="Resources/images/BlueButton.png",
                                   background_down="Resources/images/BlueDarkButton.png", border=(1, 1, 1, 1), text="-",
                                   group="operaciones", font_name="DejaVuSans.ttf")
        cuadroBotones.add_widget(buttonMenos)
        buttonPor = ToggleButton(background_normal="Resources/images/BlueButton.png",
                                 background_down="Resources/images/BlueDarkButton.png", border=(1, 1, 1, 1), text="*",
                                 group="operaciones", font_name="DejaVuSans.ttf")
        cuadroBotones.add_widget(buttonPor)
        buttonEntre = ToggleButton(background_normal="Resources/images/BlueButton.png",
                                   background_down="Resources/images/BlueDarkButton.png", border=(1, 1, 1, 1), text="/",
                                   group="operaciones", font_name="DejaVuSans.ttf")
        cuadroBotones.add_widget(buttonEntre)

        stringButtonsOperations = buttonsOperations.split()
        buttonsOperationsList = []

        for i in stringButtonsOperations:
            buttonsOperationsList.append(Button(background_normal="Resources/images/BlueRectangleButton.png",
                                                background_down="Resources/images/BlueDarkRectangleButton.png",
                                                border=(1, 1, 1, 1), text=i, size_hint=[None, None], width=120,
                                                height=150 / 2, font_name="DejaVuSans.ttf", font_size=20))

        layoutMenuOperaciones = GridLayout(size_hint=[1, 1], cols=4, padding=2,
                                           spacing=int((2 * WIDTH - 150 - 4 * 120) / (4 + 3)))
        # layoutMenuOperaciones.spacing = 40

        for j in buttonsOperationsList:
            layoutMenuOperaciones.add_widget(j)

        # layoutBotonesOperaciones.spacing = 40
        layoutBotonesOperaciones.add_widget(
            GridLayout(size_hint=[1 / (4 + 3) - (150 + 4 * 120) / ((4 + 3) * 2 * WIDTH), None]))  # Por hacer espacio
        layoutBotonesOperaciones.add_widget(cuadroBotones)
        layoutBotonesOperaciones.add_widget(layoutMenuOperaciones)

        # Se añade cada elemento

        def _update_rect(layoutFinal, instance, value):
            self.rect.pos = instance.pos
            self.rect.size = instance.size

        layoutFinal = BoxLayout(orientation="vertical", spacing=40)

        layoutFinal.add_widget(GridLayout(size_hint=[None, 0.15]))  # Para hacer espacio
        layoutFinal.add_widget(buttonLayout)
        layoutFinal.add_widget(mensaje)
        layoutFinal.add_widget(pantalla)
        layoutFinal.add_widget(layoutMedio)
        layoutFinal.add_widget(GridLayout(size_hint=[None, 0.15]))  # Para hacer espacio
        layoutFinal.add_widget(layoutBotonesOperaciones)
        layoutFinal.add_widget(GridLayout(size_hint=[None, 0.15]))  # Para hacer espacio

        self.add_widget(layoutFinal)

        # A continuacion se especifican las funciones de los botones de operaciones

        def setMultiplicar(self):
            ecuacion.operacion = "*"
            print("La operacion es: " + ecuacion.operacion)

        def setDividir(self):
            ecuacion.operacion = "/"
            print("La operacion es: " + ecuacion.operacion)

        def setSumar(self):
            ecuacion.operacion = "+"
            print("La operacion es: " + ecuacion.operacion)

        def setRestar(self):
            ecuacion.operacion = "-"
            print("La operacion es: " + ecuacion.operacion)

        def setEquation(self):
            ecuacion.setEquation()
            pantalla.add_widget(FigureCanvasKivyAgg(ecuacion.plot))
            ecuacion.askForSolve()
            mensaje.clear_widgets()
            textoJuego = FigureCanvasKivyAgg(ecuacion.plotTexto)
            mensaje.add_widget(textoJuego)

        def setDeshacer(self):
            ecuacion.askForDeshacer()
            pantalla.add_widget(FigureCanvasKivyAgg(ecuacion.plot))
            ecuacion.askForSolve()
            mensaje.clear_widgets()
            textoJuego = FigureCanvasKivyAgg(ecuacion.plotTexto)
            mensaje.add_widget(textoJuego)

        def setResetear(self):
            ecuacion.askForResetear()
            pantalla.add_widget(FigureCanvasKivyAgg(ecuacion.plot))
            ecuacion.askForSolve()
            mensaje.clear_widgets()
            textoJuego = FigureCanvasKivyAgg(ecuacion.plotTexto)
            mensaje.add_widget(textoJuego)

        buttonMas.bind(on_press=setSumar)
        buttonMenos.bind(on_press=setRestar)
        buttonPor.bind(on_press=setMultiplicar)
        buttonEntre.bind(on_press=setDividir)
        self.botonRegreso.bind(on_press=setEquation)
        self.botonDeshacer.bind(on_press=setDeshacer)
        self.botonResetear.bind(on_press=setResetear)

        def setButton(self):
            termino = self.text
            if "²" in termino:
                termino = termino.replace("²", "**2")
            print("La operacion es: " + ecuacion.operacion)
            ecuacion.setOperacion(termino)
            pantalla.add_widget(FigureCanvasKivyAgg(ecuacion.plot))
            ecuacion.askForSolve()
            mensaje.clear_widgets()
            textoJuego = FigureCanvasKivyAgg(ecuacion.plotTexto)
            mensaje.add_widget(textoJuego)

        for k in buttonsTerms:
            k.bind(on_press=setButton)

        # Método que describe todas las funciones de los botones de operaciones especiales
        def setButtonOperaciones(self):
            termino = self.text
            print("La operacion es: " + termino)
            ecuacion.setOperacionEspecial(termino)
            pantalla.add_widget(FigureCanvasKivyAgg(ecuacion.plot))
            ecuacion.askForSolve()
            mensaje.clear_widgets()
            textoJuego = FigureCanvasKivyAgg(ecuacion.plotTexto)
            mensaje.add_widget(textoJuego)

            # Conforme se vayan creando más botones se puede pensar en operaciones semejantes

        for k in buttonsOperationsList:
            k.bind(on_press=setButtonOperaciones)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


## Clase que maneja la screen del juego de la segunda ley de Newton

class RootWidgetNewton(Screen):
    def __init__(self, a, sol, buttons, img, **kwargs):
        super(RootWidgetNewton, self).__init__(**kwargs)

        # Esta sección establece el color del fondo.  Realmente no sé bien cómo funciona

        self.bind(
            size=self._update_rect,
            pos=self._update_rect
        )
        # BACKGROUND = (.15, .74, .96, 1)
        with self.canvas.before:
            Color(1, 1, 1, 1)  ## Aquí va el color
            self.rect = Rectangle(
                size=self.size,
                pos=self.pos
            )

        ecuacion = eqNewton()
        ecuacion.a = a  # "ax"
        ecuacion.sol = sol  # parse_expr("F₂ * cos(θ₁) - F₁")
        ecuacion.setEquation()

        # Layout para botones
        buttonLayout = BoxLayout(size_hint=[None, None], width=450, height=80,
                                 spacing=int((2 * WIDTH - 3 * 150) / (3 + 1)))  # Porque son 3 botones
        # Layout con el mensaje
        mensaje = BoxLayout(size_hint=[1, None], height=150)
        self.botonRegreso = Button(background_normal="Resources/images/BlueRectangleButton.png",
                                   background_down="Resources/images/BlueDarkRectangleButton.png", border=(1, 1, 1, 1),
                                   text="Regreso", size_hint=[None, None], width=150, height=80,
                                   font_name="DejaVuSans.ttf")
        self.botonDeshacer = Button(background_normal="Resources/images/BlueRectangleButton.png",
                                    background_down="Resources/images/BlueDarkRectangleButton.png", border=(1, 1, 1, 1),
                                    text="Deshacer", size_hint=[None, None], width=150, height=80,
                                    font_name="DejaVuSans.ttf")
        self.botonResetear = Button(background_normal="Resources/images/BlueRectangleButton.png",
                                    background_down="Resources/images/BlueDarkRectangleButton.png", border=(1, 1, 1, 1),
                                    text="Resetear", size_hint=[None, None], width=150, height=80,
                                    font_name="DejaVuSans.ttf")
        buttonLayout.add_widget(
            BoxLayout(size_hint=[1, 1], spacing=int((2 * WIDTH - 3 * 150) / (3 + 1))))  # Haciendo espacio
        buttonLayout.add_widget(self.botonRegreso)
        buttonLayout.add_widget(self.botonDeshacer)
        buttonLayout.add_widget(self.botonResetear)
        textoJuego = FigureCanvasKivyAgg(ecuacion.plotTexto)
        mensaje.add_widget(textoJuego)

        # Layout donde sale el diagrama
        # self.img = Image(source= "Diagrama1.png", size_hint_y = 1)
        self.img = Image(source=img, size_hint_y=1)
        layoutDiagrama = GridLayout(cols=1, spacing=40, size_hint_y=None, height=280)
        layoutDiagrama.add_widget(self.img)

        pantalla1 = RelativeLayout()  # La pantalla es la seccion donde sale la ecuacion
        expresion1 = FigureCanvasKivyAgg(ecuacion.plotLeft)
        pantalla1.add_widget(expresion1)

        pantalla2 = RelativeLayout()  # La pantalla es la seccion donde sale la ecuacion
        expresion2 = FigureCanvasKivyAgg(ecuacion.plotRight)
        pantalla2.add_widget(expresion2)

        stringButtons = buttons  # "F₂*cos(θ₁) F₂*sin(θ₁) F₂ F₁ M*g N"  #"t v d"
        stringsButtons = stringButtons.split()

        buttonsTerms = []

        # Este for permite crear los buttons de manera iteractiva
        for i in stringsButtons:
            buttonsTerms.append(Button(background_normal="Resources/images/BlueButton.png",
                                       background_down="Resources/images/BlueDarkButton.png", border=(1, 1, 1, 1),
                                       text=i, size_hint=[None, None], width=120, height=100,
                                       font_name="DejaVuSans.ttf", font_size=20))

        NBotones = len(stringsButtons)
        print("El ancho es", Window.size[0])
        if NBotones < 5:
            espaciamiento = int((2 * WIDTH - NBotones * 120) / (NBotones + 1))
            espaciamientoBlanco = (1 / (NBotones + 1) - NBotones * 120 / ((NBotones + 1) * 2 * 375))
        else:
            espaciamiento = int((2 * WIDTH - (5) * 120) / (5 + 1))
            espaciamientoBlanco = (1 / (5 + 1) - 5 * 120 / ((5 + 1) * 2 * 375))
        print("espaciamientoBlanco", espaciamientoBlanco)
        # Se crea el layout con los botones con los términos que se desean añadir
        layoutMedio = BoxLayout(orientation="horizontal", height=200)
        # espaciamientoBlanco = int(( 2*WIDTH - (5) * 100) / (5 + 1))
        layoutMedio.add_widget(GridLayout(size_hint=[espaciamientoBlanco, 1]))  # Por hacer espacio
        layoutBotonesTerminos = GridLayout(cols=5, padding=2, spacing=espaciamiento, size_hint=[1, None], height=200)

        for j in buttonsTerms:
            layoutBotonesTerminos.add_widget(j)

        layoutMedio.add_widget(layoutBotonesTerminos)
        # Se crea el layout con los botones con las operaciones que se desean añadir
        # Por defecto, se empieza con una suma
        layoutBotonesOperaciones = BoxLayout(orientation="horizontal", padding=2, size_hint=[1, None], height=150,
                                             spacing=int((2 * WIDTH - 150 - 4 * 120) / (4 + 2)))
        # Layout 2x2 de botones de operaciones matematicas
        cuadroBotones = GridLayout(size_hint=[None, 1], width=150, cols=2, padding=2)
        buttonMas = ToggleButton(background_normal="Resources/images/BlueButton.png",
                                 background_down="Resources/images/BlueDarkButton.png", border=(1, 1, 1, 1), text="+",
                                 group="operaciones", state="down", font_name="DejaVuSans.ttf")
        ecuacion.operacion = "+"
        cuadroBotones.add_widget(buttonMas)
        buttonMenos = ToggleButton(background_normal="Resources/images/BlueButton.png",
                                   background_down="Resources/images/BlueDarkButton.png", border=(1, 1, 1, 1), text="-",
                                   group="operaciones", font_name="DejaVuSans.ttf")
        cuadroBotones.add_widget(buttonMenos)
        buttonPor = ToggleButton(background_normal="Resources/images/BlueButton.png",
                                 background_down="Resources/images/BlueDarkButton.png", border=(1, 1, 1, 1), text="*",
                                 group="operaciones", font_name="DejaVuSans.ttf")
        cuadroBotones.add_widget(buttonPor)
        buttonEntre = ToggleButton(background_normal="Resources/images/BlueButton.png",
                                   background_down="Resources/images/BlueDarkButton.png", border=(1, 1, 1, 1), text="/",
                                   group="operaciones", font_name="DejaVuSans.ttf")
        cuadroBotones.add_widget(buttonEntre)

        # stringButtonsOperations = buttonsOperations.split()
        # buttonsOperationsList = []

        # for i in stringButtonsOperations:
        #    buttonsOperationsList.append(Button(background_normal = "BlueRectangleButton.png", background_down = "BlueDarkRectangleButton.png", border = (1, 1, 1, 1) , text = i, size_hint = [None, None], width = 120, height = 150/2, font_name = "DejaVuSans.ttf", font_size = 20))

        layoutMenuOperaciones = GridLayout(size_hint=[1, 1], cols=4, padding=2,
                                           spacing=int((2 * WIDTH - 150 - 4 * 120) / (4 + 3)))
        # layoutMenuOperaciones.spacing = 40

        # self.botonRevisar = Button(background_normal = "BlueRectangleButton.png", background_down = "BlueDarkRectangleButton.png", border = (1, 1, 1, 1) , text = "REVISAR", size_hint = [None, None], width = 150, height = 150/2, font_name = "DejaVuSans.ttf", font_size = 20)

        # for j in buttonsOperationsList:
        # layoutMenuOperaciones.add_widget(self.botonRevisar)

        # layoutBotonesOperaciones.spacing = 40
        layoutBotonesOperaciones.add_widget(
            GridLayout(size_hint=[1 / (4 + 3) - (150 + 4 * 120) / ((4 + 3) * 2 * WIDTH), None]))  # Por hacer espacio
        layoutBotonesOperaciones.add_widget(cuadroBotones)
        layoutBotonesOperaciones.add_widget(layoutMenuOperaciones)

        # Se añade cada elemento

        # def _update_rect(layoutFinal, instance, value):
        #     self.rect.pos = instance.pos
        #     self.rect.size = instance.size

        layoutFinal = BoxLayout(orientation="vertical", spacing=40)

        layoutFinal.add_widget(GridLayout(size_hint=[None, 0.15]))  # Para hacer espacio
        layoutFinal.add_widget(buttonLayout)
        layoutFinal.add_widget(mensaje)
        layoutFinal.add_widget(layoutDiagrama)
        layoutFinal.add_widget(pantalla1)
        layoutFinal.add_widget(pantalla2)
        layoutFinal.add_widget(GridLayout(size_hint=[None, 0.20]))  # Para hacer espacio
        layoutFinal.add_widget(layoutMedio)
        layoutFinal.add_widget(GridLayout(size_hint=[None, 0.15]))  # Para hacer espacio
        layoutFinal.add_widget(layoutBotonesOperaciones)
        layoutFinal.add_widget(GridLayout(size_hint=[None, 0.15]))  # Para hacer espacio

        self.add_widget(layoutFinal)

        # A continuacion se especifican las funciones de los botones de operaciones

        def setMultiplicar(self):
            ecuacion.operacion = "*"
            print("La operacion es: " + ecuacion.operacion)

        def setDividir(self):
            ecuacion.operacion = "/"
            print("La operacion es: " + ecuacion.operacion)

        def setSumar(self):
            ecuacion.operacion = "+"
            print("La operacion es: " + ecuacion.operacion)

        def setRestar(self):
            ecuacion.operacion = "-"
            print("La operacion es: " + ecuacion.operacion)

        def setEquation(self):
            ecuacion.setEquation()
            pantalla1.add_widget(FigureCanvasKivyAgg(ecuacion.plotLeft))
            ecuacion.askForSolve()
            mensaje.clear_widgets()
            textoJuego = FigureCanvasKivyAgg(ecuacion.plotTexto)
            mensaje.add_widget(textoJuego)

        def setDeshacer(self):
            ecuacion.askForDeshacer()
            pantalla1.add_widget(FigureCanvasKivyAgg(ecuacion.plotLeft))
            ecuacion.askForSolve()
            mensaje.clear_widgets()
            textoJuego = FigureCanvasKivyAgg(ecuacion.plotTexto)
            mensaje.add_widget(textoJuego)

        def setResetear(self):
            ecuacion.askForResetear()
            pantalla1.add_widget(FigureCanvasKivyAgg(ecuacion.plotLeft))
            ecuacion.askForSolve()
            mensaje.clear_widgets()
            textoJuego = FigureCanvasKivyAgg(ecuacion.plotTexto)
            mensaje.add_widget(textoJuego)

        buttonMas.bind(on_press=setSumar)
        buttonMenos.bind(on_press=setRestar)
        buttonPor.bind(on_press=setMultiplicar)
        buttonEntre.bind(on_press=setDividir)
        self.botonRegreso.bind(on_press=setResetear)
        self.botonDeshacer.bind(on_press=setDeshacer)
        self.botonResetear.bind(on_press=setResetear)

        def setButton(self):
            termino = self.text
            if "²" in termino:
                termino = termino.replace("²", "**2")
            print("La operacion es: " + ecuacion.operacion)
            ecuacion.setOperacion(termino)
            pantalla1.add_widget(FigureCanvasKivyAgg(ecuacion.plotLeft))
            ecuacion.askForSolve()
            mensaje.clear_widgets()
            textoJuego = FigureCanvasKivyAgg(ecuacion.plotTexto)
            mensaje.add_widget(textoJuego)

        for k in buttonsTerms:
            k.bind(on_press=setButton)

        # Método que describe todas las funciones de los botones de operaciones especiales
        # def setButtonOperaciones(self):
        #    termino = self.text
        #    print("La operacion es: " + termino)
        # ecuacion.askForSolve()
        #    pantalla1.add_widget(FigureCanvasKivyAgg(ecuacion.plotLeft))
        #    ecuacion.askForSolve()
        #    mensaje.clear_widgets()
        #    textoJuego = FigureCanvasKivyAgg(ecuacion.plotTexto)
        #    mensaje.add_widget(textoJuego)

        # Conforme se vayan creando más botones se puede pensar en operaciones semejantes

        # for k in buttonsOperationsList:
        # self.botonRevisar.bind(on_press = setButtonOperaciones)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


### Clase que hace los niveles de la segunda ley de Newton

class RootWidget(Screen):
    def __init__(self, buttons, ec, sol, buttonsOperations, **kwargs):
        super(RootWidget, self).__init__(**kwargs)

        # Esta sección establece el color del fondo.  Realmente no sé bien cómo funciona

        self.bind(
            size=self._update_rect,
            pos=self._update_rect
        )
        # BACKGROUND = (.15, .74, .96, 1)
        with self.canvas.before:
            Color(1, 1, 1, 1)  ## Aquí va el color
            self.rect = Rectangle(
                size=self.size,
                pos=self.pos
            )

        self.ec = ec

        ecuacion = equation()
        ecuacion.eq = self.ec
        ecuacion.sol = sol
        ecuacion.setEquation()

        # Layout para botones
        buttonLayout = BoxLayout(size_hint=[None, None], width=450, height=80,
                                 spacing=int((2 * WIDTH - 3 * 150) / (3 + 1)))  # Porque son 3 botones
        # Layout con el mensaje
        mensaje = BoxLayout(size_hint=[1, None], height=150)
        self.botonRegreso = Button(background_normal="Resources/images/BlueRectangleButton.png",
                                   background_down="Resources/images/BlueDarkRectangleButton.png", border=(1, 1, 1, 1),
                                   text="Regreso", size_hint=[None, None], width=150, height=80,
                                   font_name="DejaVuSans.ttf")
        self.botonDeshacer = Button(background_normal="Resources/images/BlueRectangleButton.png",
                                    background_down="Resources/images/BlueDarkRectangleButton.png", border=(1, 1, 1, 1),
                                    text="Deshacer", size_hint=[None, None], width=150, height=80,
                                    font_name="DejaVuSans.ttf")
        self.botonResetear = Button(background_normal="Resources/images/BlueRectangleButton.png",
                                    background_down="Resources/images/BlueDarkRectangleButton.png", border=(1, 1, 1, 1),
                                    text="Resetear", size_hint=[None, None], width=150, height=80,
                                    font_name="DejaVuSans.ttf")
        buttonLayout.add_widget(
            BoxLayout(size_hint=[1, 1], spacing=int((2 * WIDTH - 3 * 150) / (3 + 1))))  # Haciendo espacio
        buttonLayout.add_widget(self.botonRegreso)
        buttonLayout.add_widget(self.botonDeshacer)
        buttonLayout.add_widget(self.botonResetear)
        textoJuego = FigureCanvasKivyAgg(ecuacion.plotTexto)
        mensaje.add_widget(textoJuego)
        # layoutSuperior.add_widget(buttonLayout)
        # layoutSuperior.add_widget(mensaje)

        pantalla = RelativeLayout()  # La pantalla es la seccion donde sale la ecuacion
        expresion = FigureCanvasKivyAgg(ecuacion.plot)
        pantalla.add_widget(expresion)

        stringButtons = buttons  # "t v d"
        stringsButtons = stringButtons.split()

        buttonsTerms = []

        # Este for permite crear los buttons de manera iteractiva
        for i in stringsButtons:
            buttonsTerms.append(Button(background_normal="Resources/images/BlueButton.png",
                                       background_down="Resources/images/BlueDarkButton.png", border=(1, 1, 1, 1),
                                       text=i, size_hint=[None, None], width=100, height=100,
                                       font_name="DejaVuSans.ttf", font_size=20))

        NBotones = len(stringsButtons)
        print("El ancho es", Window.size[0])
        if NBotones < 5:
            espaciamiento = int((2 * WIDTH - NBotones * 100) / (NBotones + 1))
            espaciamientoBlanco = (1 / (NBotones + 1) - NBotones * 100 / ((NBotones + 1) * 2 * 375))
        else:
            espaciamiento = int((2 * WIDTH - (5) * 100) / (5 + 1))
            espaciamientoBlanco = (1 / (5 + 1) - 5 * 100 / ((5 + 1) * 2 * 375))
        print("espaciamientoBlanco", espaciamientoBlanco)
        # Se crea el layout con los botones con los términos que se desean añadir
        layoutMedio = BoxLayout(orientation="horizontal", height=200)
        # espaciamientoBlanco = int(( 2*WIDTH - (5) * 100) / (5 + 1))
        layoutMedio.add_widget(GridLayout(size_hint=[espaciamientoBlanco, 1]))  # Por hacer espacio
        layoutBotonesTerminos = GridLayout(cols=5, padding=2, spacing=espaciamiento, size_hint=[1, None], height=200)

        for j in buttonsTerms:
            layoutBotonesTerminos.add_widget(j)

        layoutMedio.add_widget(layoutBotonesTerminos)
        # Se crea el layout con los botones con las operaciones que se desean añadir
        # Por defecto, se empieza con una suma
        layoutBotonesOperaciones = BoxLayout(orientation="horizontal", padding=2, size_hint=[1, None], height=150,
                                             spacing=int((2 * WIDTH - 150 - 4 * 120) / (4 + 2)))
        # Layout 2x2 de botones de operaciones matematicas
        cuadroBotones = GridLayout(size_hint=[None, 1], width=150, cols=2, padding=2)
        buttonMas = ToggleButton(background_normal="Resources/images/BlueButton.png",
                                 background_down="Resources/images/BlueDarkButton.png", border=(1, 1, 1, 1), text="+",
                                 group="operaciones", state="down", font_name="DejaVuSans.ttf")
        ecuacion.operacion = "+"
        cuadroBotones.add_widget(buttonMas)
        buttonMenos = ToggleButton(background_normal="Resources/images/BlueButton.png",
                                   background_down="Resources/images/BlueDarkButton.png", border=(1, 1, 1, 1), text="-",
                                   group="operaciones", font_name="DejaVuSans.ttf")
        cuadroBotones.add_widget(buttonMenos)
        buttonPor = ToggleButton(background_normal="Resources/images/BlueButton.png",
                                 background_down="Resources/images/BlueDarkButton.png", border=(1, 1, 1, 1), text="*",
                                 group="operaciones", font_name="DejaVuSans.ttf")
        cuadroBotones.add_widget(buttonPor)
        buttonEntre = ToggleButton(background_normal="Resources/images/BlueButton.png",
                                   background_down="Resources/images/BlueDarkButton.png", border=(1, 1, 1, 1), text="/",
                                   group="operaciones", font_name="DejaVuSans.ttf")
        cuadroBotones.add_widget(buttonEntre)

        stringButtonsOperations = buttonsOperations.split()
        buttonsOperationsList = []

        for i in stringButtonsOperations:
            buttonsOperationsList.append(Button(background_normal="Resources/images/BlueRectangleButton.png",
                                                background_down="Resources/images/BlueDarkRectangleButton.png",
                                                border=(1, 1, 1, 1), text=i, size_hint=[None, None], width=120,
                                                height=150 / 2, font_name="DejaVuSans.ttf", font_size=20))

        layoutMenuOperaciones = GridLayout(size_hint=[1, 1], cols=4, padding=2,
                                           spacing=int((2 * WIDTH - 150 - 4 * 120) / (4 + 3)))
        # layoutMenuOperaciones.spacing = 40

        for j in buttonsOperationsList:
            layoutMenuOperaciones.add_widget(j)

        # layoutBotonesOperaciones.spacing = 40
        layoutBotonesOperaciones.add_widget(
            GridLayout(size_hint=[1 / (4 + 3) - (150 + 4 * 120) / ((4 + 3) * 2 * WIDTH), None]))  # Por hacer espacio
        layoutBotonesOperaciones.add_widget(cuadroBotones)
        layoutBotonesOperaciones.add_widget(layoutMenuOperaciones)

        # Se añade cada elemento

        def _update_rect(layoutFinal, instance, value):
            self.rect.pos = instance.pos
            self.rect.size = instance.size

        layoutFinal = BoxLayout(orientation="vertical", spacing=40)

        layoutFinal.add_widget(GridLayout(size_hint=[None, 0.15]))  # Para hacer espacio
        layoutFinal.add_widget(buttonLayout)
        layoutFinal.add_widget(mensaje)
        layoutFinal.add_widget(pantalla)
        layoutFinal.add_widget(layoutMedio)
        layoutFinal.add_widget(GridLayout(size_hint=[None, 0.15]))  # Para hacer espacio
        layoutFinal.add_widget(layoutBotonesOperaciones)
        layoutFinal.add_widget(GridLayout(size_hint=[None, 0.15]))  # Para hacer espacio

        self.add_widget(layoutFinal)

        # A continuacion se especifican las funciones de los botones de operaciones

        def setMultiplicar(self):
            ecuacion.operacion = "*"
            print("La operacion es: " + ecuacion.operacion)

        def setDividir(self):
            ecuacion.operacion = "/"
            print("La operacion es: " + ecuacion.operacion)

        def setSumar(self):
            ecuacion.operacion = "+"
            print("La operacion es: " + ecuacion.operacion)

        def setRestar(self):
            ecuacion.operacion = "-"
            print("La operacion es: " + ecuacion.operacion)

        def setEquation(self):
            ecuacion.setEquation()
            pantalla.add_widget(FigureCanvasKivyAgg(ecuacion.plot))
            ecuacion.askForSolve()
            mensaje.clear_widgets()
            textoJuego = FigureCanvasKivyAgg(ecuacion.plotTexto)
            mensaje.add_widget(textoJuego)

        def setDeshacer(self):
            ecuacion.askForDeshacer()
            pantalla.add_widget(FigureCanvasKivyAgg(ecuacion.plot))
            ecuacion.askForSolve()
            mensaje.clear_widgets()
            textoJuego = FigureCanvasKivyAgg(ecuacion.plotTexto)
            mensaje.add_widget(textoJuego)

        def setResetear(self):
            ecuacion.askForResetear()
            pantalla.add_widget(FigureCanvasKivyAgg(ecuacion.plot))
            ecuacion.askForSolve()
            mensaje.clear_widgets()
            textoJuego = FigureCanvasKivyAgg(ecuacion.plotTexto)
            mensaje.add_widget(textoJuego)

        buttonMas.bind(on_press=setSumar)
        buttonMenos.bind(on_press=setRestar)
        buttonPor.bind(on_press=setMultiplicar)
        buttonEntre.bind(on_press=setDividir)
        self.botonRegreso.bind(on_press=setEquation)
        self.botonDeshacer.bind(on_press=setDeshacer)
        self.botonResetear.bind(on_press=setResetear)

        def setButton(self):
            termino = self.text
            if "²" in termino:
                termino = termino.replace("²", "**2")
            print("La operacion es: " + ecuacion.operacion)
            ecuacion.setOperacion(termino)
            pantalla.add_widget(FigureCanvasKivyAgg(ecuacion.plot))
            ecuacion.askForSolve()
            mensaje.clear_widgets()
            textoJuego = FigureCanvasKivyAgg(ecuacion.plotTexto)
            mensaje.add_widget(textoJuego)

        for k in buttonsTerms:
            k.bind(on_press=setButton)

        # Método que describe todas las funciones de los botones de operaciones especiales
        def setButtonOperaciones(self):
            termino = self.text
            print("La operacion es: " + termino)
            ecuacion.setOperacionEspecial(termino)
            pantalla.add_widget(FigureCanvasKivyAgg(ecuacion.plot))
            ecuacion.askForSolve()
            mensaje.clear_widgets()
            textoJuego = FigureCanvasKivyAgg(ecuacion.plotTexto)
            mensaje.add_widget(textoJuego)

            # Conforme se vayan creando más botones se puede pensar en operaciones semejantes

        for k in buttonsOperationsList:
            k.bind(on_press=setButtonOperaciones)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


# La clase que construye la aplicacion
class TestApp(App):
    def build(self):
        # Create the screen manager
        # dir_path = os.path.dirname(os.path.realpath(__file__)) #Actual directorio
        # for file in os.listdir(dir_path):# Elimina lo que temrina en .png
        #    if file.endswith(".png"):
        #        os.remove(file)
        sm = ScreenManager()
        inicio = PaginaInicio(name="Inicio")
        creditos = PaginaTips("Resources/images/Creditos.png")  # PaginaCreditos(name = "Creditos")
        niveles = PaginaNiveles(name="Niveles")

        # Seccion de Niveles Conversiones

        NivelesConversiones = PagConversiones()

        # Primer nivel de conversiones

        cantidad1 = "5.00 * cm"
        sol1 = "1.97*inch"
        buttons1 = "1Inch/2.54cm 2.54cm/1Inch"
        units1 = "Inch"
        NivelConversiones1 = RootWidgetConversiones(cantidad1, sol1, buttons1, units1)

        # segundo nivel de conversiones

        cantidad2 = "15.0 * inch"
        sol2 = "0.381*m"
        buttons2 = "1Inch/2.54cm 2.54cm/1Inch 100cm/1m 1m/100cm"
        units2 = "m"
        NivelConversiones2 = RootWidgetConversiones(cantidad2, sol2, buttons2, units2)

        # tercer nivel de conversiones

        cantidad3 = "500 * cm**2"
        sol3 = "0.05*m**2"
        buttons3 = "1Inch/2.54cm 2.54cm/1Inch 100cm/1m 1m/100cm"
        units3 = "m²"
        NivelConversiones3 = RootWidgetConversiones(cantidad3, sol3, buttons3, units3)

        # cuarto nivel de conversiones

        cantidad4 = "25.0 * m /s"
        sol4 = "90.0*km/h"
        buttons4 = "1km/1000m 1000m/1km 100cm/1m 1m/100cm 1h/3600s 3600s/1h"
        units4 = "km/h"
        NivelConversiones4 = RootWidgetConversiones(cantidad4, sol4, buttons4, units4)

        cantidad5 = "300 * cm**3"
        sol5 = "0.0003*m**3"
        buttons5 = "1km/1000m 1000m/1km 100cm/1m 1m/100cm"
        units5 = "m³"
        NivelConversiones5 = RootWidgetConversiones(cantidad5, sol5, buttons5, units5)

        # Seccion de Tips MRU

        TipsMRU = PaginaTips("Resources/images/MRU.png")

        # Seccion de Niveles MRU

        NivelesMRU = PagMRU()

        # Seccion de Tips MRUA

        TipsMRUA = PaginaTips("Resources/images/MRUA.png")

        # Seccion de Niveles MRUA

        NivelesMRUA = PagMRUA()

        # Seccion de Niveles Movimiento Parabólico

        NivelesMovimientoParabolico = PagMovimientoParabolico()

        # Seccion de Niveles Dinámica

        NivelesDinamica = PagDinamica()

        # Seccion del nivel 1
        buttons1 = "t v d"  # "t v d"
        ec1 = "v=d/t"  # "v=d/t"
        sol1 = "d"
        buttonsOperations1 = "Simplify Factor Expand"
        nivel1 = RootWidget(buttons1, ec1, sol1, buttonsOperations1)

        # Seccion del nivel 2
        buttons2 = "t v d"  # "t v d"
        ec2 = "v=d/t"  # "v=d/t"
        sol2 = "t"
        buttonsOperations2 = "Simplify Factor Expand"
        nivel2 = RootWidget(buttons2, ec2, sol2, buttonsOperations2)

        # Seccion del nivel 3
        buttons3 = "a vբ vᵢ t a*t"  # "t v d"
        ec3 = "a=(vբ-vᵢ)/t"  # "v=d/t"
        sol3 = "vբ"
        buttonsOperations3 = "Simplify Factor Expand"
        nivel3 = RootWidget(buttons3, ec3, sol3, buttonsOperations3)

        # Seccion del nivel 4
        buttons4 = "a vբ vᵢ t a*t"  # "t v d"
        ec4 = "a=(vբ-vᵢ)/t"  # "v=d/t"
        sol4 = "vᵢ"
        buttonsOperations4 = "Simplify Factor Expand"
        nivel4 = RootWidget(buttons4, ec4, sol4, buttonsOperations4)

        # Seccion del nivel 5
        buttons5 = "a vբ vᵢ t a*t"  # "t v d"
        ec5 = "a=(vբ-vᵢ)/t"  # "v=d/t"
        sol5 = "t"
        buttonsOperations5 = "Simplify Factor Expand"
        nivel5 = RootWidget(buttons5, ec5, sol5, buttonsOperations5)

        # Seccion del nivel 6
        buttons6 = "a d vբ vᵢ t 2 a*d vբ² vᵢ²"  # "t v d"
        ec6 = "vբ**2=vᵢ**2+2*a*d"  # "v=d/t"
        sol6 = "vբ"
        buttonsOperations6 = "Simplify Factor Expand □² √□"
        nivel6 = RootWidget(buttons6, ec6, sol6, buttonsOperations6)

        # Seccion del nivel 7
        buttons7 = "a d vբ vᵢ t 2 a*d vբ² vᵢ²"  # "t v d"
        ec7 = "vբ**2=vᵢ**2+2*a*d"  # "v=d/t"
        sol7 = "vᵢ"
        buttonsOperations7 = "Simplify Factor Expand □² √□"
        nivel7 = RootWidget(buttons7, ec7, sol7, buttonsOperations7)

        # Seccion del nivel 8
        buttons8 = "a d vբ vᵢ t 2 a*d vբ² vᵢ²"  # "t v d"
        ec8 = "vբ**2=vᵢ**2+2*a*d"  # "v=d/t"
        sol8 = "a"
        buttonsOperations8 = "Simplify Factor Expand □² √□"
        nivel8 = RootWidget(buttons8, ec8, sol8, buttonsOperations8)

        # Seccion del nivel 9
        buttons9 = "a d vբ vᵢ t 2 a*d vբ² vᵢ²"  # "t v d"
        ec9 = "vբ**2=vᵢ**2+2*a*d"  # "v=d/t"
        sol9 = "d"
        buttonsOperations9 = "Simplify Factor Expand □² √□"
        nivel9 = RootWidget(buttons9, ec9, sol9, buttonsOperations9)

        # Seccion del nivel 10
        buttons10 = "d vᵢ a t 2 vᵢ*t a*t²/2 vᵢ²/a²"  # "t v d"
        ec10 = "d=vᵢ*t+a*t**2/2"  # "v=d/t"
        sol10 = "vᵢ"
        buttonsOperations10 = "Simplify Factor Expand □² √□"
        nivel10 = RootWidget(buttons10, ec10, sol10, buttonsOperations10)

        # Seccion del nivel 11
        buttons11 = "d vᵢ a t 2 vᵢ*t a*t²/2 vᵢ²/a²"  # "t v d"
        ec11 = "d=vᵢ*t+a*t**2/2"  # "v=d/t"
        sol11 = "a"
        buttonsOperations11 = "Simplify Factor Expand □² √□"
        nivel11 = RootWidget(buttons11, ec11, sol11, buttonsOperations11)

        # Seccion del nivel 12
        buttons12 = "d vᵢ a t 2 vᵢ*t a*t²/2 vᵢ²/a²"  # "t v d"
        ec12 = "d=vᵢ*t+a*t**2/2"  # "v=d/t"
        sol12 = "t"
        buttonsOperations12 = "Simplify Factor Expand □² √□"
        nivel12 = RootWidget(buttons12, ec12, sol12, buttonsOperations12)

        # Seccion del nivel 13
        buttons13 = "yբ yᵢ vᵢ sin(θ) g t vᵢ*sin(θ)*t g*t²/2"  # "t v d"
        ec13 = "yբ = yᵢ +vᵢ*sin(θ)*t - g*t**2/2"  # "v=d/t"
        sol13 = "vᵢ"
        buttonsOperations13 = "Simplify Factor Expand sin(□) asin(□)"
        nivel13 = RootWidget(buttons13, ec13, sol13, buttonsOperations13)

        # Seccion del nivel 14
        buttons14 = "yբ yᵢ vᵢ sin(θ) g t vᵢ*sin(θ)*t g*t²/2"  # "t v d"
        ec14 = "yբ = yᵢ +vᵢ*sin(θ)*t - g*t**2/2"  # "v=d/t"
        sol14 = "θ"
        buttonsOperations14 = "Simplify Factor Expand sin(□) asin(□)"
        nivel14 = RootWidget(buttons14, ec14, sol14, buttonsOperations14)

        # Primer Nivel de dinamica
        a1 = "ax"
        sol1 = parse_expr("F₂ * cos(θ₁) - F₁")
        buttons1 = "F₂*cos(θ₁) F₂*sin(θ₁) F₂ F₁ M*g N"  # "t v d"
        img1 = "Resources/images/Diagrama1.png"
        Dinamica1 = RootWidgetNewton(a1, sol1, buttons1, img1)

        # segundo Nivel de dinamica
        a2 = "ax"
        sol2 = parse_expr("F₂ * cos(θ₂) - F₁* sin(θ₁)")
        buttons2 = "F₂*cos(θ₂) F₂*sin(θ₂) F₁*cos(θ₁) F₁*sin(θ₁) F₂ F₁ M*g N"  # "t v d"
        img2 = "Resources/images/Diagrama2.png"
        Dinamica2 = RootWidgetNewton(a2, sol2, buttons2, img2)

        def ir_a_pagina_inicio(self):
            sm.switch_to(inicio)

        def ir_a_creditos(self):
            sm.switch_to(creditos)

        def ir_a_menu_niveles(self):
            sm.switch_to(niveles)

        def ir_a_nivel_conversiones_1(self):
            sm.switch_to(NivelConversiones1)

        def ir_a_nivel_conversiones_2(self):
            sm.switch_to(NivelConversiones2)

        def ir_a_nivel_conversiones_3(self):
            sm.switch_to(NivelConversiones3)

        def ir_a_nivel_conversiones_4(self):
            sm.switch_to(NivelConversiones4)

        def ir_a_nivel_conversiones_5(self):
            sm.switch_to(NivelConversiones5)

        def ir_a_MRU(self):
            sm.switch_to(TipsMRU)

        def ir_a_MRUA(self):
            sm.switch_to(TipsMRUA)

        def ir_a_Niveles_MRU(self):
            sm.switch_to(NivelesMRU)

        def ir_a_Niveles_MRUA(self):
            sm.switch_to(NivelesMRUA)

        def ir_a_Niveles_MovimientoParabolico(self):
            sm.switch_to(NivelesMovimientoParabolico)

        def ir_a_Niveles_Dinamica(self):
            sm.switch_to(NivelesDinamica)

        def ir_a_Niveles_Conversiones(self):
            sm.switch_to(NivelesConversiones)

        def ir_a_nivel_1(self):
            nivel1.ec = "v=d/t"
            sm.switch_to(nivel1)

        def ir_a_nivel_2(self):
            nivel2.ec = "v=d/t"
            sm.switch_to(nivel2)

        def ir_a_nivel_3(self):
            nivel3.ec = "a=(vբ-vᵢ)/t"
            sm.switch_to(nivel3)

        def ir_a_nivel_4(self):
            sm.switch_to(nivel4)

        def ir_a_nivel_5(self):
            sm.switch_to(nivel5)

        def ir_a_nivel_6(self):
            sm.switch_to(nivel6)

        def ir_a_nivel_7(self):
            sm.switch_to(nivel7)

        def ir_a_nivel_8(self):
            sm.switch_to(nivel8)

        def ir_a_nivel_9(self):
            sm.switch_to(nivel9)

        def ir_a_nivel_10(self):
            sm.switch_to(nivel10)

        def ir_a_nivel_11(self):
            sm.switch_to(nivel11)

        def ir_a_nivel_12(self):
            sm.switch_to(nivel12)

        def ir_a_nivel_13(self):
            sm.switch_to(nivel13)

        def ir_a_nivel_14(self):
            sm.switch_to(nivel14)

        def ir_a_dinamica_1(self):
            sm.switch_to(Dinamica1)

        def ir_a_dinamica_2(self):
            sm.switch_to(Dinamica2)

        inicio.botonCreditos.bind(on_press=ir_a_creditos)
        inicio.botonNiveles.bind(on_press=ir_a_menu_niveles)

        creditos.botonRegreso.bind(on_press=ir_a_pagina_inicio)

        niveles.botonRegreso.bind(on_press=ir_a_pagina_inicio)

        niveles.botonNivelesConversiones.bind(on_press=ir_a_Niveles_Conversiones)

        niveles.botonTipMRU.bind(on_press=ir_a_MRU)
        niveles.botonNivelesMRU.bind(on_press=ir_a_Niveles_MRU)
        niveles.botonTipMRUA.bind(on_press=ir_a_MRUA)
        niveles.botonNivelesMRUA.bind(on_press=ir_a_Niveles_MRUA)
        niveles.botonNivelesMovimientoParabólico.bind(on_press=ir_a_Niveles_MovimientoParabolico)
        niveles.botonDinámica.bind(on_press=ir_a_Niveles_Dinamica)

        NivelesConversiones.botonRegreso.bind(on_press=ir_a_menu_niveles)
        NivelesConversiones.botonConversiones1.bind(on_press=ir_a_nivel_conversiones_1)
        NivelesConversiones.botonConversiones2.bind(on_press=ir_a_nivel_conversiones_2)
        NivelesConversiones.botonConversiones3.bind(on_press=ir_a_nivel_conversiones_3)
        NivelesConversiones.botonConversiones4.bind(on_press=ir_a_nivel_conversiones_4)
        NivelesConversiones.botonConversiones5.bind(on_press=ir_a_nivel_conversiones_5)

        NivelesMRU.boton1.bind(on_press=ir_a_nivel_1)
        NivelesMRU.boton2.bind(on_press=ir_a_nivel_2)
        NivelesMRU.botonRegreso.bind(on_press=ir_a_menu_niveles)
        NivelesMRUA.boton3.bind(on_press=ir_a_nivel_3)
        NivelesMRUA.boton4.bind(on_press=ir_a_nivel_4)
        NivelesMRUA.boton5.bind(on_press=ir_a_nivel_5)
        NivelesMRUA.boton6.bind(on_press=ir_a_nivel_6)
        NivelesMRUA.boton7.bind(on_press=ir_a_nivel_7)
        NivelesMRUA.boton8.bind(on_press=ir_a_nivel_8)
        NivelesMRUA.boton9.bind(on_press=ir_a_nivel_9)
        NivelesMRUA.boton10.bind(on_press=ir_a_nivel_10)
        NivelesMRUA.boton11.bind(on_press=ir_a_nivel_11)
        NivelesMRUA.boton12.bind(on_press=ir_a_nivel_12)
        NivelesMRUA.botonRegreso.bind(on_press=ir_a_menu_niveles)
        NivelesMovimientoParabolico.boton13.bind(on_press=ir_a_nivel_13)
        NivelesMovimientoParabolico.boton14.bind(on_press=ir_a_nivel_14)

        NivelConversiones1.botonRegreso.bind(on_press=ir_a_menu_niveles)
        NivelConversiones2.botonRegreso.bind(on_press=ir_a_menu_niveles)
        NivelConversiones3.botonRegreso.bind(on_press=ir_a_menu_niveles)
        NivelConversiones4.botonRegreso.bind(on_press=ir_a_menu_niveles)
        NivelConversiones5.botonRegreso.bind(on_press=ir_a_menu_niveles)

        NivelesDinamica.botonRegreso.bind(on_press=ir_a_menu_niveles)
        NivelesDinamica.botonDinámica1.bind(on_press=ir_a_dinamica_1)
        NivelesDinamica.botonDinámica2.bind(on_press=ir_a_dinamica_2)

        TipsMRU.botonRegreso.bind(on_press=ir_a_menu_niveles)
        TipsMRUA.botonRegreso.bind(on_press=ir_a_menu_niveles)

        nivel1.botonRegreso.bind(on_press=ir_a_Niveles_MRU)
        nivel2.botonRegreso.bind(on_press=ir_a_Niveles_MRU)
        nivel3.botonRegreso.bind(on_press=ir_a_menu_niveles)
        nivel4.botonRegreso.bind(on_press=ir_a_menu_niveles)
        nivel5.botonRegreso.bind(on_press=ir_a_menu_niveles)
        nivel6.botonRegreso.bind(on_press=ir_a_menu_niveles)

        nivel7.botonRegreso.bind(on_press=ir_a_menu_niveles)
        nivel8.botonRegreso.bind(on_press=ir_a_menu_niveles)
        nivel9.botonRegreso.bind(on_press=ir_a_menu_niveles)
        nivel10.botonRegreso.bind(on_press=ir_a_menu_niveles)
        nivel11.botonRegreso.bind(on_press=ir_a_menu_niveles)
        nivel12.botonRegreso.bind(on_press=ir_a_menu_niveles)
        nivel13.botonRegreso.bind(on_press=ir_a_menu_niveles)
        nivel14.botonRegreso.bind(on_press=ir_a_menu_niveles)

        Dinamica1.botonRegreso.bind(on_press=ir_a_menu_niveles)
        Dinamica2.botonRegreso.bind(on_press=ir_a_menu_niveles)

        sm.add_widget(inicio)
        sm.add_widget(creditos)
        sm.add_widget(niveles)

        return sm


# Se ejecuta la app
if __name__ == '__main__':
    TestApp().run()