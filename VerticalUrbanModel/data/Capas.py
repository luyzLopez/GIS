# -*- coding: utf-8 -*-

#Librerias para archivos raster
import gdal
from qgis.core import *

import numpy as np

class Capas:

    def __init__(self):
        pass

    def get_datos_raster(self, ruta):
        rlayer_o = gdal.Open(ruta)
        datos_raster = np.array(rlayer_o.GetRasterBand(1).ReadAsArray())

        return datos_raster
