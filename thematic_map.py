# -*- coding: utf-8 -*-
"""
/***************************************************************************
 thematicMap
                                 A QGIS plugin
 Classifica dados para gerar mapas temáticos com base no livro de Robbi et al.
                              -------------------
        begin                : 2017-03-21
        git sha              : $Format:%H$
        copyright            : (C) 2017 by pedropsfarias
        email                : pedropsfariasAtgmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon, QMessageBox
from qgis.gui import QgsFieldComboBox, QgsMapLayerComboBox,QgsMapLayerProxyModel, QgsFieldProxyModel
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from thematic_map_dialog import thematicMapDialog
import os.path
from inspect import getmembers
import numpy as np
import matplotlib.pyplot as plt


class thematicMap:
    """QGIS Plugin Implementation."""

    valores = np.empty(shape=(0), dtype='d')

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'thematicMap_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Thematic Map')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'thematicMap')
        self.toolbar.setObjectName(u'thematicMap')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('thematicMap', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = thematicMapDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/thematicMap/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Mapas Temáticos'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Thematic Map'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar



    def run(self):
        """Run method that performs all the real work"""
        
        self.dlg.grafico.clicked.connect(self.geraGrafico)
        self.dlg.histograma.clicked.connect(self.geraHistograma)

        layerAtivo = self.dlg.nomeLayer
        campo = self.dlg.campo

        layerAtivo.setFilters(QgsMapLayerProxyModel.VectorLayer)
        layerAtivo.layerChanged.connect(self.mudouLayer)
        layerAtivo.layerChanged.connect(campo.setLayer)

        campo.setFilters(QgsFieldProxyModel.Numeric)
        campo.fieldChanged.connect(self.mudouCampo)


        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()

        layer  = layerAtivo.currentLayer()

        #print campo.currentField()
        #print layer.fieldNameIndex(campo.currentField())
        iter = layer.getFeatures()
        for feature in iter:
            # retrieve every feature with its geometry and attributes
            # fetch geometry
            geom = feature.geometry()
            #print "Feature ID %d: " % feature.id()


            # fetch attributes
            #attrs = feature.attributes(campo.currentField())

            # attrs is a list. It contains all the attribute values of this feature
            #print attrs



        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass

    #Funções editadas por pedropsfarias
    

    def mudouLayer(self):
        """Run method that performs all the real work"""

        print "Mudou Layer"
        # msg = QMessageBox()
        # msg.setIcon(QMessageBox.Information)

        # msg.setText("This is a message box")
        # msg.setInformativeText("This is additional information")
        # msg.setWindowTitle("MessageBox demo")
        # msg.setDetailedText("The details are as follows:")
        # msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        # msg.exec_()

    def mudouCampo(self):
        """Run method that performs all the real work"""

        campo = self.dlg.campo
        layerAtivo = self.dlg.nomeLayer
        layer = layerAtivo.currentLayer()
        indice = layer.fieldNameIndex(campo.currentField())

        valores = self.valores
        valores = np.empty(shape=(0), dtype='d')
        iter = layer.getFeatures()
        for feature in iter:
            # Varre todas as geometrias, lê o campo e add p/ vetor
            geom = feature.geometry()
            #print "Feature ID %d: " % feature.id()


            # fetch attributes
            attrs = feature.attributes()

            # attrs is a list. It contains all the attribute values of this feature
            
            valores = np.append(valores, attrs[indice])

        self.dlg.media.setText(str(np.mean(valores)))
        self.dlg.amostra.setText(str(np.size(valores)))
        self.dlg.desvio.setText(str(np.std(valores)))
        self.dlg.mediana.setText(str(np.median(valores)))
        self.dlg.min.setText(str(np.min(valores)))
        self.dlg.max.setText(str(np.max(valores)))
        self.dlg.amplitude.setText(str(np.max(valores)-np.min(valores)))
        
        print "Mudou Campo"
        self.valores = valores

    def geraGrafico(self):
        
        vetor =  np.sort(self.valores)

        plt.plot(vetor)
        plt.show()
    
    def geraHistograma(self):
        plt.hist(self.valores)
        plt.show()
             


