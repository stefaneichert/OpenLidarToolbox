# -*- coding: utf-8 -*-

"""
/***************************************************************************
 OpenLidarTools
                                 A QGIS QGISplugin
 Open LiDAR Toolbox
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-03-10
        copyright            : (C) 2021 by Benjamin Štular, Edisa Lozić,
                                                            Stefan Eichert
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
"""

__author__ = 'Benjamin Štular, Edisa Lozić, Stefan Eichert'
__date__ = '2021-03-10'
__copyright__ = '(C) 2021 by Benjamin Štular, Edisa Lozić, Stefan Eichert'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

"""
Model exported as python.
Name : Lidar Pipeline
Group : OpenLidarToolbox
With QGIS : 31604
"""

import inspect
import os
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import QgsProcessingUtils
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFile
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterCrs
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterString
import processing
from .utils.utils import getHelpText, setCrs, randomfilename


class CreateDfm(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):

        self.addParameter(
            QgsProcessingParameterFile(
                'InputFilelaslaz',
                'Input LAS/LAZ File',
                behavior=QgsProcessingParameterFile.File,
                fileFilter='Lidar Files (*.las *.laz)',
                defaultValue=None))
        self.addParameter(
            QgsProcessingParameterBoolean(
                'classLas',
                'The input LAS/LAZ file is already classified',
                optional=False,
                defaultValue=False))
        self.addParameter(
            QgsProcessingParameterBoolean(
                'LowNoise',
                'Remove low noise',
                optional=False,
                defaultValue=False))
        self.addParameter(QgsProcessingParameterCrs(
            'CRS',
            'Source File Coordinate System',
            defaultValue=setCrs()))
        self.addParameter(
            QgsProcessingParameterNumber(
                'SetCellSize',
                'Cell Size',
                type=QgsProcessingParameterNumber.Double,
                minValue=0,
                maxValue=1.79769e+308,
                defaultValue=0.5))
        self.addParameter(QgsProcessingParameterString(
            'prefix',
            'Name prefix for layers',
            multiLine=False,
            defaultValue='',
            optional=True))
        self.addParameter(QgsProcessingParameterBoolean(
            'VisualisationDFM',
            'Add DFM to map',
            optional=False,
            defaultValue=True))


    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress
        # reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(6, model_feedback)
        results = {}
        outputs = {}

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        if parameters['classLas'] == False:
            alg_params = {
                'InputFilelaslaz': parameters['InputFilelaslaz'],
                'LAS':
                    QgsProcessingUtils.generateTempFilename('lasheightCl.las'),
                'LowNoise': parameters['LowNoise']
            }
            outputs['ClassifyLaslaz'] = processing.run(
                'Open LiDAR Toolbox:ToClassLas',
                alg_params,
                context=context,
                feedback=feedback,
                is_child_algorithm=True)
            lasheightclassifyfile = outputs['ClassifyLaslaz']['classifiedLAZ']
            results['LAS'] = outputs['ClassifyLaslaz']['classifiedLAZ']

        if parameters['classLas']:
            lasheightclassifyfile = parameters['InputFilelaslaz']

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Create base data
        alg_params = {
            'CRS': parameters['CRS'],
            'GPD': False,
            'IDW': False,
            'LowNoise': parameters['LowNoise'],
            'InputFilelaslaz': lasheightclassifyfile,
            'LVD': False,
            'SetCellSize': parameters['SetCellSize'],
            'TIN': False,
            'prefix': parameters['prefix'],
            'classLas': parameters['classLas']
        }
        outputs['CreateBaseData'] = processing.run(
            'Open LiDAR Toolbox:basedata',
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True)


        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # DFM Confidence Map
        alg_params = {
            'CRS': parameters['CRS'],
            'Createconfidencemapfor': [1],
            'DEMDFM': outputs['CreateBaseData']['DEM'],
            'Groundlayer': outputs['CreateBaseData']['GPD'],
            'LowVegetation': outputs['CreateBaseData']['LVD'],
            'SetCellSize': parameters['SetCellSize'],
            'loadCFM': False
        }
        outputs['DfmConfidenceMap'] = processing.run(
            'Open LiDAR Toolbox:DFM confidence map',
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}


        # Hybrid Interpolation
        alg_params = {
            'CRS': parameters['CRS'],
            'CellSize': parameters['SetCellSize'],
            'ConfidenceMapRaster': outputs['DfmConfidenceMap']['CFM 0.5m'],
            'IDW': outputs['CreateBaseData']['IDW'],
            'REDgrowradiusinrastercells': 3,
            'TLI': outputs['CreateBaseData']['DEM'],
            'loadDFM': False
        }
        outputs['HybridInterpolation'] = processing.run(
            'Open LiDAR Toolbox:Hybrid interpolation',
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True)

        results['DFM'] = outputs['HybridInterpolation']['Dfm']

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        if parameters['VisualisationDFM']:
            # Load result
            alg_params = {
                'INPUT': outputs['HybridInterpolation']['Dfm'],
                'NAME': parameters['prefix'] + 'DFM'
            }
            outputs['LoadResult'] = processing.run(
                'native:loadlayer',
                alg_params,
                context=context,
                feedback=feedback,
                is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}


        return results

    def name(self):
        return 'CreateDFM'

    def displayName(self):
        return 'Create DFM'

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr(self.groupId())

    def icon(self):
        cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]
        icon = QIcon(os.path.join(
            os.path.join(cmd_folder, 'icons/2_2_Create_DFM.png')))
        return icon

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return ''

    def shortHelpString(self):
        title = """
        <html><body><h2>Algorithm description</h2>
        <p>This is an algorithm pipeline that takes an airborne LiDAR point 
        cloud to produce a digital feature model (DFM), which is 
        archaeology-specific DEM, combining ground and buildings.</p>
        <h2>Input parameters</h2>"""

        conclusion = """
        <br><br>
        Create DFM incorporates parts of Lastools, Whitebox tools, GDAL, GRASS
        GIS, and QGIS core tools.<br><br>
        <p><b>References:</b><br><br> Štular, B.; Eichert, S.; Lozić, E. 
        Airborne LiDAR Point Cloud Processing for Archaeology. Pipeline and QGIS
        Toolbox. Remote Sens. 2021, 16, 3225. 
        <a href="https://doi.org/10.3390/rs13163225">
        https://doi.org/10.3390/rs13163225</a></p>
        <br><a href="https://stefaneichert.github.io/OpenLidarToolbox/">
        Website</a>
        <br><p align="right">Algorithm author: Benjamin Štular, Edisa Lozić, 
        Stefan Eichert </p><p align="right">
        Help author: Benjamin Štular, Edisa Lozić, Stefan Eichert</p>
        </body></html>"""

        helpText = title + getHelpText(['lasfile', 'las', 'noise', 'crs',
                                        'cell', 'prefix', 'dfm', 'faq',
                                        'blk']) + conclusion

        helpText = " ".join((helpText.replace('\n', '')).split())

        return helpText

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return CreateDfm()