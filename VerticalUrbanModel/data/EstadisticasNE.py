# -*- coding: utf-8 -*-

#Librerias para archivos raster
import gdal
from qgis.core import *

import numpy as np

class NoEspacial:

    def get_vecindad(self, data, nivel, i, j):
        """
        Metodo que devuelve la vecindad a partir de un pixel i, j.

        :param data: np array, Datos de trabajo.
        :param nivel: int, Nivel de vecindad.
        :param i: int, Renglon actual del pixel.
        :param j: int, Columna actual del pixel.

        :return: np array, Matriz de vecindad del pixel i, j.
        """

        return data[i - nivel: i + nivel + 1, j - nivel: j + nivel + 1]  # Vecindad nivel vecinos

