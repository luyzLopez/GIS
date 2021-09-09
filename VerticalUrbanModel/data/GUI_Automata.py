#!/usr/bin/env python
# -*- coding: utf-8 -*-

# AUTOR: Luis Antonio Lopez Rivera / luyz_lopez@hotmail.com

# Librerias PyQt para la interfaz grafica
import PyQt5
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from qgis.utils import iface
from qgis.core import *

# Librerias para ejecutar acciones del SO y manipular archivos
import os, sys
from os.path import isfile, join

import numpy as np

# Librerias para leer archivos shp en QGIS
from osgeo import ogr

# Libreria para ejecutar la ayuda en el navegador
import webbrowser

# Clases auxiliares
from .EstadisticasNE import NoEspacial
from .Capas import Capas
from .EstadisticasE import Espacial

class AutomataGUI(QtWidgets.QWidget):

    def __init__(self, iface):
        QtWidgets.QWidget.__init__(self)

        self.iface = iface

        self.ruta_img = str(os.path.dirname(os.path.abspath(__file__)) + "\\Imagenes\\")

        # Variables de la tablas
        self.row_sector, self.datos_sector = 0, []
        self.row_mt, self.datos_mt = 0, []

        self.interfaz_grafica()
        self.valores_iniciales()

        self.setAttribute(Qt.WA_DeleteOnClose)

        # self.cargar_capas_combos()

        # Activar para cuando se ejecute en QGIS
        self.show()
        self.exec()


    # Metodo para dibujar toda la interfaz grafica del modelo
    def interfaz_grafica(self):
        self.posicion = QDesktopWidget()
        ancho = 420
        alto = 578

        self.setGeometry((self.posicion.width()) // 2 - (ancho // 2), ((self.posicion.height())) // 2 - (alto // 2), ancho, alto)
        self.setWindowTitle("Automata Celular")

        # -------------- Scroll Area ---------------
        widget = QWidget(self.posicion)  # Container Widget

        # Mapa de probabilidad de crecimiento
        label1 = QLabel("Seleccionar mapa de probabilidad de crecimiento", self)
        label1.setGeometry(10, 10, 241, 16)
        self.comboMapaProba = QComboBox(self)
        self.comboMapaProba.setGeometry(10, 30, 321, 22)
        self.btnMapaProba = QPushButton(self)
        self.btnMapaProba.setGeometry(350, 30, 31, 23)
        self.btnMapaProba.setText("...")
        self.btnMapaProba.setToolTip("Raster base para el automata celular.")

        label2 = QLabel("Minimo", self)
        label2.setGeometry(230, 70, 41, 16)
        label3 = QLabel("Maximo", self)
        label3.setGeometry(330, 70, 41, 16)

        # Intervalos
        label4 = QLabel("Intervalo de edificios", self)
        label4.setGeometry(10, 90, 121, 16)
        self.spinEdifMin = QDoubleSpinBox(self)
        self.spinEdifMin.setGeometry(230, 90, 51, 22)
        self.spinEdifMin.setRange(0.00, 1.00)
        self.spinEdifMin.setSingleStep(0.01)
        self.spinEdifMax = QDoubleSpinBox(self)
        self.spinEdifMax.setGeometry(330, 90, 51, 22)
        self.spinEdifMax.setRange(0.00, 1.00)
        self.spinEdifMax.setSingleStep(0.01)

        label5 = QLabel("Intervalo de agua", self)
        label5.setGeometry(10, 120, 141, 16)
        self.spinAguaMin = QDoubleSpinBox(self)
        self.spinAguaMin.setGeometry(230, 120, 51, 22)
        self.spinAguaMin.setRange(0, 1)
        self.spinAguaMin.setSingleStep(0.01)
        self.spinAguaMax = QDoubleSpinBox(self)
        self.spinAguaMax.setGeometry(330, 120, 51, 22)
        self.spinAguaMax.setRange(0, 1)
        self.spinAguaMax.setSingleStep(0.01)

        label6 = QLabel("Intervalo de terreno para construccion", self)
        label6.setGeometry(10, 150, 191, 16)
        self.spinTerConsMin = QDoubleSpinBox(self)
        self.spinTerConsMin.setGeometry(230, 150, 51, 22)
        self.spinTerConsMin.setRange(0.00, 1.00)
        self.spinTerConsMin.setSingleStep(0.01)
        self.spinTerConsMax = QDoubleSpinBox(self)
        self.spinTerConsMax.setGeometry(330, 150, 51, 22)
        self.spinTerConsMax.setRange(0.00, 1.00)
        self.spinTerConsMax.setSingleStep(0.01)

        label18 = QLabel("Intervalo de caminos-carreteras", self)
        label18.setGeometry(10, 180, 191, 16)
        self.spinCamCarMin = QDoubleSpinBox(self)
        self.spinCamCarMin.setGeometry(230, 180, 51, 22)
        self.spinCamCarMin.setRange(0.00, 1.00)
        self.spinCamCarMin.setSingleStep(0.01)
        self.spinCamCarMax = QDoubleSpinBox(self)
        self.spinCamCarMax.setGeometry(330, 180, 51, 22)
        self.spinCamCarMax.setRange(0.00, 1.00)
        self.spinCamCarMax.setSingleStep(0.01)

        label7 = QLabel("Intervalo de zona urbana", self)
        label7.setGeometry(10, 210, 151, 16)
        self.spinZonaUrMin = QDoubleSpinBox(self)
        self.spinZonaUrMin.setGeometry(230, 210, 51, 22)
        self.spinZonaUrMin.setRange(0.00, 1.00)
        self.spinZonaUrMin.setSingleStep(0.01)
        self.spinZonaUrMax = QDoubleSpinBox(self)
        self.spinZonaUrMax.setGeometry(330, 210, 51, 22)
        self.spinZonaUrMax.setRange(0.00, 1.00)
        self.spinZonaUrMax.setSingleStep(0.01)

        label8 = QLabel("Intervalo de areas verdes", self)
        label8.setGeometry(10, 240, 151, 16)
        self.spinVerdesMin = QDoubleSpinBox(self)
        self.spinVerdesMin.setGeometry(230, 240, 51, 22)
        self.spinVerdesMin.setRange(0.00, 1.00)
        self.spinVerdesMin.setSingleStep(0.01)
        self.spinVerdesMax = QDoubleSpinBox(self)
        self.spinVerdesMax.setGeometry(330, 240, 51, 22)
        self.spinVerdesMax.setRange(0.00, 1.00)
        self.spinVerdesMax.setSingleStep(0.01)

        # Mapa de calor de la zona urbana
        label9 = QLabel("Seleccionar mapa de calor", self)
        label9.setGeometry(10, 290, 241, 16)
        self.comboMapaCalor = QComboBox(self)
        self.comboMapaCalor.setGeometry(10, 310, 321, 22)
        self.btnMapaCalor = QPushButton(self)
        self.btnMapaCalor.setGeometry(350, 310, 31, 23)
        self.btnMapaCalor.setText("...")
        self.btnMapaCalor.setToolTip("Raster para cluster de edificios.")

        # Vecindad
        label10 = QLabel("Nivel de vecindad", self)
        label10.setGeometry(10, 360, 121, 16)
        self.spinVecindad = QSpinBox(self)
        self.spinVecindad.setGeometry(130, 360, 42, 22)
        self.spinVecindad.setRange(1, 6)

        # Nivel de confianza respecto a media
        label13 = QLabel("Confianza respecto a la media", self)
        label13.setGeometry(230, 350, 151, 16)

        label14 = QLabel("Minimo", self)
        label14.setGeometry(230, 380, 41, 16)
        self.spinConfianzaMin = QDoubleSpinBox(self)
        self.spinConfianzaMin.setGeometry(230, 400, 51, 22)
        self.spinConfianzaMin.setRange(0.00, 5000.00)
        self.spinConfianzaMin.setSingleStep(0.01)

        label15 = QLabel("Maximo", self)
        label15.setGeometry(330, 380, 41, 16)
        self.spinConfianzaMax = QDoubleSpinBox(self)
        self.spinConfianzaMax.setGeometry(330, 400, 51, 22)
        self.spinConfianzaMax.setRange(0.00, 5000.00)
        self.spinConfianzaMax.setSingleStep(0.01)

        # Umbral Riesgo
        label16 = QLabel("Umbral de riesgo", self)
        label16.setGeometry(10, 400, 121, 16)
        self.spinRiesgo = QDoubleSpinBox(self)
        self.spinRiesgo.setGeometry(130, 400, 51, 22)
        self.spinRiesgo.setRange(0.00, 100.00)
        self.spinRiesgo.setSingleStep(0.01)

        label17 = QLabel("Area de influencia", self)
        label17.setGeometry(210, 440, 91, 16)
        self.spinAreaInf = QDoubleSpinBox(self)
        self.spinAreaInf.setGeometry(330, 440, 51, 22)
        self.spinAreaInf.setRange(0.00, 5000.00)
        self.spinAreaInf.setSingleStep(0.01)

        # Distancia minima
        label11 = QLabel("Distancia minima", self)
        label11.setGeometry(10, 440, 91, 16)
        self.spinDistMin = QDoubleSpinBox(self)
        self.spinDistMin.setGeometry(130, 440, 51, 22)
        self.spinDistMin.setRange(0.01, 2000.00)
        self.spinDistMin.setSingleStep(0.01)

        # Ruta de salida
        label12 = QLabel("Seleccione ruta de salida", self)
        label12.setGeometry(10, 480, 151, 16)
        self.lineRutaSalida = QLineEdit(self)
        self.lineRutaSalida.setGeometry(10, 500, 321, 21)
        self.lineRutaSalida.clear()
        self.btnRutaSalida = QPushButton(self)
        self.btnRutaSalida.setGeometry(350, 500, 31, 23)
        self.btnRutaSalida.setText("...")
        self.btnRutaSalida.setToolTip("Ubicacion en el equipo donde se guardaran los resultados de la herramienta.")

    # -------------- BOTONES -------------------
        self.btnAceptar = QPushButton("Aceptar", self)
        self.btnAceptar.setGeometry(310, 540, 75, 23)
        self.btnAceptar.setToolTip("Comienza la ejecucion del modelo, en caso de no existir errores.")
        self.btnCancelar = QPushButton("Cancelar", self)
        self.btnCancelar.setGeometry(210, 540, 75, 23)
        self.btnCancelar.setToolTip("Cierra la herramienta.")

# ------------- Se termina de dibujar la interfaz grafica ----------------------------------------------

# ----------------------- Metodo que define los valores inciales de la ventana del modelo -------------------
    def valores_iniciales(self):
        self.btnMapaProba.clicked.connect(self.select_mapa_proba)
        self.btnMapaCalor.clicked.connect(self.select_mapa_calor)
        self.btnRutaSalida.clicked.connect(self.select_ruta_salida)
        self.btnAceptar.clicked.connect(self.principal)
        self.btnCancelar.clicked.connect(self.cerrar_ventana)

# ----------------- Metodos llamados por los eventos de la ventana --------------------

    # Metodo para agregar las capas que se encuentran en el panel de capas de QGIS al modelo
    def cargar_capas_combos(self):
        pass

    # Archivo Mapa probabilidad
    def select_mapa_proba(self):  # Metodo para seleccionar el shape de origen desde un file chooser
        nombre_archivo = QFileDialog.getOpenFileName(None, "Seleccionar mapa de probabilidad", "", "*.tif")
        if (nombre_archivo != ""):
            self.comboMapaProba.addItem(nombre_archivo[0])

    # Archivo Mapa de calor
    def select_mapa_calor(self):  # Metodo para seleccionar el shape de origen desde un file chooser
        nombre_archivo = QFileDialog.getOpenFileName(None, "Seleccionar mapa de calor", "", "*.tif")
        if (nombre_archivo != ""):
            self.comboMapaCalor.addItem(nombre_archivo[0])

    # Seleccionar ruta de salida
    def select_ruta_salida(self):
        file = str(QFileDialog.getExistingDirectory(None, "Seleccionar ruta de salida"))
        self.lineRutaSalida.setText(file)

    # Para cerrar la ventana principal
    def cerrar_ventana(self):
        self.close()
        del self


    # --------- Metodo para validacion de los campos ----------------------
    def validar(self):
        error = ""

        if(self.comboMapaProba.count()== 0):
            print(self.comboMapaProba.count())
            error += "Seleccionar mapa de probabilidad.\n"
        if(self.comboMapaCalor.count() == 0):
            error += "Seleccionar mapa de calor.\n"

        if(self.spinEdifMin.value() >= self.spinEdifMax.value()):
            error += "Ingrese un intervalo de edificios valido.\n"
        if(self.spinZonaUrMin.value() >= self.spinZonaUrMax.value()):
            error += "Ingrese un intervalo de zona urbana valido.\n"
        if(self.spinTerConsMin.value() >= self.spinTerConsMax.value()):
            error += "Ingrese un intervalo de terreno para construccion valido.\n"
        if(self.spinAguaMin.value() >= self.spinAguaMax.value()):
            error += "Ingrese un intervalo de agua valido.\n"
        if(self.spinVerdesMin.value() >= self.spinVerdesMax.value()):
            error += "Ingrese un intervalo de areas verdes valido.\n"
        if (self.spinConfianzaMin.value() >= self.spinConfianzaMax.value()):
            error += "Ingrese un nivel de confianza valido.\n"

        if(self.lineRutaSalida.text() == ""):
            error += "Seleccionar ruta de salida."

        if(error == ""): # Si no existen errores...
            return True
        else:
            self.set_mensaje("ERROR", "Completar todos los campos", error, QMessageBox.Critical)
            return False

# ------------ FIN Metodos llamados por los eventos de la ventana --------------------

# -------- Colocar un mensaje en pantalla ---------------
    def set_mensaje(self, title, text, error, tipo):
        msjBox = QMessageBox()
        msjBox.setIcon(tipo)
        msjBox.setText(text)
        msjBox.setInformativeText("")
        msjBox.setWindowTitle(title)
        msjBox.setDetailedText(error)
        msjBox.setStandardButtons(QMessageBox.Ok)
        msjBox.exec_()

# -------- Carpeta de salida ---------------
    def make_folders(self, output_path):
        """
        Genera las carpetas de salida donde se guardaran los resultados del modelo.
        :param output_path:  Ruta de salida
        :return:
        """
        if (not os.path.exists(output_path)):
            os.mkdir(output_path, 777)

# ------- Para elimianr archivos irrelevantes para el usuario ---------
    def delete_files(self, ruta):
        for arch in os.listdir(ruta):
            if isfile(join(ruta, arch)):
                os.remove(join(ruta, arch))



# Metodo principal, controla la ejeccion del programa
    def principal(self):
        if(self.validar()): # Si no existen errores en  los datos de entrada ...
            self.hide() # Se oculta la interfaz principal

            # Mapas
            raster_proba = self.comboMapaProba.currentText()
            raster_mc = self.comboMapaCalor.currentText()

            # Intervalos para identificar tipos de suelo
            edif_min, edif_max = self.spinEdifMin.value(), self.spinEdifMax.value()
            caminos_min, caminos_max = self.spinCamCarMin.value(), self.spinCamCarMax.value()
            zonau_min, zonau_max = self.spinZonaUrMin.value(), self.spinZonaUrMax.value()
            terreno_min, terreno_max = self.spinTerConsMin.value(), self.spinTerConsMax.value()
            agua_min, agua_max = self.spinAguaMin.value(), self.spinAguaMax.value()
            verdes_min, verdes_max = self.spinVerdesMin.value(), self.spinVerdesMax.value()

            # Umbral de riesgo
            u_riesgo = self.spinRiesgo.value()

            # Confianza respecto a la media
            nc1 = self.spinConfianzaMin.value()
            nc2 = self.spinConfianzaMax.value()
            nivel_confianza = np.arange(nc1, nc2 + 0.01, 0.01).round(2)

            # Vecindad y areas verdes
            nivel_vec = self.spinVecindad.value()
            dist_min = self.spinDistMin.value()

            # Area de influencia
            area_inf = self.spinAreaInf.value()

            # Ruta donde se generaran los archivos de salida
            op = self.lineRutaSalida.text()

            # Objetos para acceder a metodos
            capas = Capas()
            estadistica_ne = NoEspacial()
            estadistica_e = Espacial()

        # ---- Comienza el modelo ---
            espacio = capas.get_datos_raster(raster_proba)
            mapa_c = capas.get_datos_raster(raster_mc)

            rows = espacio.shape[0]
            cols = espacio.shape[1]

            proyeccion = np.copy(espacio)
            nuevos = []

            # Recorriendo los datos de la imagen satelital
            for i in range(nivel_vec, rows - nivel_vec):
                # print(f"{i-3} de {rows-vecindad}")

                for j in range(nivel_vec, cols - nivel_vec):

                    if (zonau_min < espacio[i][j] <= zonau_max):  # Si la celda a analizar esta en el intervalo de terreno para construccion o zona urbana...
                        veci = estadistica_ne.get_vecindad(espacio, nivel_vec, i, j)  # Se recupera la vecindad

                        media = np.mean(veci).round(2)  # Se calcula la media de la vecindad

                        if (media in nivel_confianza):  # Si la media se encuentra en el nivel de confianza calculado...
                            riesgo = estadistica_e.calcula_riesgo(veci, agua_max, terreno_max, caminos_max, verdes_max)  # Se calcula el estadistico de riesgo

                            if (riesgo <= u_riesgo):  # Si el riesgo es menor al umbral de riesgo permitido...

                                if (mapa_c[i][j] >= area_inf): # Si el parametro de área de influencia es mayor o igual a medio...
                                    proyeccion[i][j] = 0.35  # Aparece un edificio

                                    nuevos += 1

                                    print(f"Edificio en {i}, {j}. Total = {nuevos}")

            print("TERMINA")
            print(f"Total = {nuevos}")

            # Liberando memoria y eliminando archivos


            # FIN...