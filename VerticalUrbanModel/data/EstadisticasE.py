# -*- coding: utf-8 -*-

#Librerias para archivos raster
import gdal
from qgis.core import *

import numpy as np

class Espacial:

    def calcula_riesgo(self, vecindad, n1, n2, n3, n4):
        """
        Funcion para calcular el nivel de riesgo propuesto.

        :param vecindad: np array, Con los datos de vecindad de la celda de interes.
        :param n1: float, Valor del primer limite del intervalo.
        :param n2: float, Valor del segundo limite del intervalo.
        :param n3: float, Valor del tercer limite del intervalo.
        :param n4: float, Valor del cuarto limite del intervalo.

        :return: float, Nivel de riesgo calculado.
        """
        tc, ca, zu, av, ag = 0, 0, 0, 0, 0

        vecindad = np.ravel(vecindad)
        vecindad = np.delete(vecindad, 40)

        for nivel in vecindad:
            if (0 > nivel <= n1):
                ag += 1
            elif (n1 > nivel <= n2):
                tc += 1
            elif (n2 > nivel <= n3):
                ca += 1
            elif (n3 > nivel <= n4):
                zu += 1
            else:
                av += 1

        if (tc + ca + zu + av + ag != 80):
            print(f"{tc + ca + zu + av + ag} ERROR EN CALCULO!!!!")

        return (tc * 0.2 + ca * 0.4 + zu * 0.6 + av * 0.8 + ag * 1.0) / 80.0
