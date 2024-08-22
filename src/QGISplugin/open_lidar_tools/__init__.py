# -*- coding: utf-8 -*-
"""
/***************************************************************************
 OpenLidarTools
                                 A QGIS QGISplugin
 Open LiDAR Toolbox for Archaeology
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-03-10
        copyright            : (C) 2021 by Benjamin Štular, Edisa Lozić, Stefan Eichert
        email                : stefaneichert@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 3 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the QGISplugin, making it known to QGIS.
"""

__author__ = 'Benjamin Štular, Edisa Lozić, Stefan Eichert'
__date__ = '2021-03-10'
__copyright__ = '(C) 2021 by Benjamin Štular, Edisa Lozić, Stefan Eichert'


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load OpenLidarTools class from file OpenLidarTools.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .open_lidar_tools import OpenLidarToolsPlugin
    return OpenLidarToolsPlugin()