# -*- encoding: utf-8 -*-
import pango
DEBUG = False
SHOW_SESSION_TRACE = True
FONT = 'sans 10'  
SMALL_FONT = 'sans 9'

class Config:
    "Singleton class"

    def __init__(self):
        # TODO: cargar todos los parámetros desde un archivo "~/.pybox.conf".
        self._create_theme_round()
        #self._create_theme_classic()

    def _create_theme_round(self):
        self.text_theme = {
                'font': FONT,
                'text': '',
                'alignment': pango.ALIGN_CENTER,
                'fill_color': 'black',
                'use_markup': True,
                }
        self.box_theme = {
                'stroke_color': 'black',
                'line_width': 2.0,
                'fill_color': 'white',
                'radius_x': 5,
                'radius_y': 5,
                }
        self.division_theme = {
                'stroke_color': 'black',
                'line_width': 2.0,
                }

    def _create_theme_classic(self):
        self.text_theme = {
                'font': FONT,
                'text': '',
                'alignment': pango.ALIGN_CENTER,
                'fill_color': 'black',
                'use_markup': True,
                }
        self.box_theme = {
                'stroke_color': 'black',
                'line_width': 2,
                'fill_color': '#f1f3e5',
                }
        self.division_theme = {
                'stroke_color': 'black',
                'line_width': 2,
                }
