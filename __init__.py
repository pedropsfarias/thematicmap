# -*- coding: utf-8 -*-
"""
/***************************************************************************
 thematicMap
                                 A QGIS plugin
 Classifica dados para gerar mapas temáticos com base no livro de Robbi et al.
                             -------------------
        begin                : 2017-03-21
        copyright            : (C) 2017 by pedropsfarias
        email                : pedropsfariasAtgmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load thematicMap class from file thematicMap.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .thematic_map import thematicMap
    return thematicMap(iface)
