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

import inspect
import os
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterEnum
from qgis.core import QgsProcessingParameterCrs
from qgis.core import QgsProcessingParameterString
from qgis.core import QgsProcessingUtils
import processing
from os.path import exists
from .utils.utils import getHelpText, setCrs, randomfilename


class dfmConfidenceMap(QgsProcessingAlgorithm):
    OUTPUT = 'OUTPUT'
    INPUT = 'INPUT'

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterRasterLayer(
            'DEMDFM',
            'DEM/DFM Layer',
            defaultValue=None))
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                'Groundlayer',
                'Ground Point Density Layer',
                defaultValue=None))
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                'LowVegetation',
                'Low Vegetation Density Layer',
                defaultValue=None))
        self.addParameter(QgsProcessingParameterCrs(
            'CRS',
            'Source Files Coordinate System',
            defaultValue=setCrs()))
        self.addParameter(QgsProcessingParameterEnum(
            'Createconfidencemapfor',
            'Resolution of target DFM',
            options=['0.25m', '0.5m', '1m', '2m'],
            allowMultiple=True,
            defaultValue=[0, 1, 2, 3]))
        self.addParameter(
            QgsProcessingParameterNumber(
                'SetCellSize',
                'Output Cell Size:',
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
            'loadCFM',
            'Add results to map ',
            optional=False,
            defaultValue=True))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress
        # reports are adjusted for the overall progress through the model
        confidenceParams = (parameters['Createconfidencemapfor'])
        steps = len(confidenceParams) * 19 + 8
        feedback = QgsProcessingMultiStepFeedback(steps, model_feedback)
        results = {}
        outputs = {}

        # reclass tables
        half_meter = {
            'denshi': [0, 4, 0, 4.000000001, 100000, 1],
            'densmid': [0, 2, 0, 2.000001, 4, 1, 4.000001, 100000, 0],
            'denslow': [0, 1, 0, 1.00000001, 2, 1, 2.00000001, 100000, 0],
            'densvlow': [0, 1, 1, 1.00000001, 100000, 0],
            'veghigh': [0, 4, 0, 4.00000001, 100000, 1],
            'veglow': [0, 4, 1, 4.00000001, 100000, 0]
        }
        quarter_meter = {
            'denshi': [0, 16, 0, 16.000000001, 100000, 1],
            'densmid': [0, 8, 0, 8.000001, 16, 1, 16.000001, 100000, 0],
            'denslow': [0, 4, 0, 4.00000001, 8, 1, 8.00000001, 100000, 0],
            'densvlow': [0, 4, 1, 4.00000001, 100000, 0],
            'veghigh': [0, 16, 0, 16.00000001, 100000, 1],
            'veglow': [0, 16, 1, 16.00000001, 100000, 0]
        }
        one_meter = {
            'denshi': [0, 1, 0, 1.000000001, 100000, 1],
            'densmid': [0, 0.5, 0, 0.5000001, 1, 1, 1.000001, 100000, 0],
            'denslow': [0, 0.25, 0, 0.25000001, 0.5, 1, 0.50000001, 100000, 0],
            'densvlow': [0, 0.25, 1, 0.25000001, 100000, 0],
            'veghigh': [0, 1, 0, 1.00000001, 100000, 1],
            'veglow': [0, 1, 1, 1.00000001, 100000, 0]
        }
        two_meter = {
            'denshi': [0, 0.25, 0, 0.250000001, 100000, 1],
            'densmid': [0, 0.125, 0, 0.1250001, 0.25, 1, 0.2500001, 100000, 0],
            'denslow': [0, 0.0625, 0, 0.06250001, 0.125, 1, 0.12500001, 100000,
                        0],
            'densvlow': [0, 0.0625, 1, 0.06250001, 100000, 0],
            'veghigh': [0, 0.25, 0, 0.25000001, 100000, 1],
            'veglow': [0, 0.25, 1, 0.25000001, 100000, 0]
        }

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # resampleVEG
        feedback.pushInfo('')
        feedback.pushInfo('*****************************')
        feedback.pushInfo(' Open LiDAR Toolbox ')
        feedback.pushInfo(' Resampling Vegetation ')
        feedback.pushInfo('*****************************')
        feedback.pushInfo('')

        feedback.pushInfo(str(parameters))

        alg_params = {
            'GRASS_RASTER_FORMAT_META': '',
            'GRASS_RASTER_FORMAT_OPT': '',
            'GRASS_REGION_CELLSIZE_PARAMETER': parameters['SetCellSize'],
            'GRASS_REGION_PARAMETER': parameters['DEMDFM'],
            'input': parameters['LowVegetation'],
            'output': QgsProcessingUtils.generateTempFilename(
                randomfilename())
        }
        outputs['Resampleveg'] = processing.run(
            'grass7:r.resample',
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # resampleGPD
        feedback.pushInfo('')
        feedback.pushInfo('*****************************')
        feedback.pushInfo(' Open LiDAR Toolbox ')
        feedback.pushInfo(' Resampling Ground Points ')
        feedback.pushInfo('*****************************')
        feedback.pushInfo('')

        alg_params = {
            'GRASS_RASTER_FORMAT_META': '',
            'GRASS_RASTER_FORMAT_OPT': '',
            'GRASS_REGION_CELLSIZE_PARAMETER': parameters['SetCellSize'],
            'GRASS_REGION_PARAMETER': parameters['DEMDFM'],
            'input': parameters['Groundlayer'],
            'output': QgsProcessingUtils.generateTempFilename(
                randomfilename())
        }
        outputs['Resamplegpd'] = processing.run(
            'grass7:r.resample',
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # resampleDEM
        feedback.pushInfo('')
        feedback.pushInfo('*****************************')
        feedback.pushInfo(' Open LiDAR Toolbox ')
        feedback.pushInfo(' Resampling DEM ')
        feedback.pushInfo('*****************************')
        feedback.pushInfo('')
        alg_params = {
            'GRASS_RASTER_FORMAT_META': '',
            'GRASS_RASTER_FORMAT_OPT': '',
            'GRASS_REGION_CELLSIZE_PARAMETER': parameters['SetCellSize'],
            'GRASS_REGION_PARAMETER': parameters['DEMDFM'],
            'input': parameters['DEMDFM'],
            'output': QgsProcessingUtils.generateTempFilename(
                randomfilename())
        }
        outputs['Resampledem'] = processing.run(
            'grass7:r.resample',
            alg_params, context=context,
            feedback=feedback,
            is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        step = 4

        for row in confidenceParams:
            if row == 0:
                intermed_params = quarter_meter
                appendix = ' 0.25m'
            if row == 1:
                intermed_params = half_meter
                appendix = ' 0.5m'
            if row == 2:
                intermed_params = one_meter
                appendix = ' 1m'
            if row == 3:
                intermed_params = two_meter
                appendix = ' 2m'

            # Density Hi

            feedback.pushInfo('')
            feedback.pushInfo('*****************************')
            feedback.pushInfo(' Open LiDAR Toolbox ')
            feedback.pushInfo(' Density High ')
            feedback.pushInfo('*****************************')
            feedback.pushInfo('')

            alg_params = {
                'DATA_TYPE': 3,
                'INPUT_RASTER': outputs['Resamplegpd']['output'],
                'NODATA_FOR_MISSING': True,
                'NO_DATA': -9999,
                'RANGE_BOUNDARIES': 2,
                'RASTER_BAND': 1,
                'TABLE': intermed_params['denshi'],
                'OUTPUT': QgsProcessingUtils.generateTempFilename(
                randomfilename())
            }
            outputs['DensityHi' + appendix] = processing.run(
                'native:reclassifybytable',
                alg_params,
                context=context,
                feedback=feedback,
                is_child_algorithm=True)

            step += 1
            feedback.setCurrentStep(step)
            if feedback.isCanceled():
                return {}

            # Density Mid
            feedback.pushInfo('')
            feedback.pushInfo('*****************************')
            feedback.pushInfo(' Open LiDAR Toolbox ')
            feedback.pushInfo(' Density Mid ')
            feedback.pushInfo('*****************************')
            feedback.pushInfo('')

            alg_params = {
                'DATA_TYPE': 3,
                'INPUT_RASTER': outputs['Resamplegpd']['output'],
                'NODATA_FOR_MISSING': True,
                'NO_DATA': -9999,
                'RANGE_BOUNDARIES': 2,
                'RASTER_BAND': 1,
                'TABLE': intermed_params['densmid'],
                'OUTPUT': QgsProcessingUtils.generateTempFilename(
                randomfilename())
            }
            outputs['DensityMid' + appendix] = processing.run(
                'native:reclassifybytable',
                alg_params,
                context=context,
                feedback=feedback, is_child_algorithm=True)

            step += 1
            feedback.setCurrentStep(step)
            if feedback.isCanceled():
                return {}

            # Density Low
            feedback.pushInfo('')
            feedback.pushInfo('*****************************')
            feedback.pushInfo(' Open LiDAR Toolbox ')
            feedback.pushInfo(' Density Low ')
            feedback.pushInfo('*****************************')
            feedback.pushInfo('')

            alg_params = {
                'DATA_TYPE': 3,
                'INPUT_RASTER': outputs['Resamplegpd']['output'],
                'NODATA_FOR_MISSING': True,
                'NO_DATA': -9999,
                'RANGE_BOUNDARIES': 1,
                'RASTER_BAND': 1,
                'TABLE': intermed_params['denslow'],
                'OUTPUT': QgsProcessingUtils.generateTempFilename(
                randomfilename())
            }
            outputs['DensityLow' + appendix] = processing.run(
                'native:reclassifybytable',
                alg_params,
                context=context,
                feedback=feedback,
                is_child_algorithm=True)

            step += 1
            feedback.setCurrentStep(step)
            if feedback.isCanceled():
                return {}

            # Density Vlow
            feedback.pushInfo('')
            feedback.pushInfo('*****************************')
            feedback.pushInfo(' Open LiDAR Toolbox ')
            feedback.pushInfo(' Density Vlow ')
            feedback.pushInfo('*****************************')
            feedback.pushInfo('')

            alg_params = {
                'DATA_TYPE': 3,
                'INPUT_RASTER': outputs['Resamplegpd']['output'],
                'NODATA_FOR_MISSING': True,
                'NO_DATA': -9999,
                'RANGE_BOUNDARIES': 1,
                'RASTER_BAND': 1,
                'TABLE': intermed_params['densvlow'],
                'OUTPUT': QgsProcessingUtils.generateTempFilename(
                randomfilename())
            }
            outputs['DensityVlow' + appendix] = processing.run(
                'native:reclassifybytable',
                alg_params,
                context=context,
                feedback=feedback,
                is_child_algorithm=True)

            step += 1
            feedback.setCurrentStep(step)
            if feedback.isCanceled():
                return {}

            # VegLow

            feedback.pushInfo('')
            feedback.pushInfo('*****************************')
            feedback.pushInfo(' Open LiDAR Toolbox ')
            feedback.pushInfo(' Vegetation Low ')
            feedback.pushInfo('*****************************')
            feedback.pushInfo('')

            alg_params = {
                'DATA_TYPE': 3,
                'INPUT_RASTER': outputs['Resampleveg']['output'],
                'NODATA_FOR_MISSING': True,
                'NO_DATA': -9999,
                'RANGE_BOUNDARIES': 2,
                'RASTER_BAND': 1,
                'TABLE': intermed_params['veglow'],
                'OUTPUT': QgsProcessingUtils.generateTempFilename(
                randomfilename())
            }
            outputs['Veglow' + appendix] = processing.run(
                'native:reclassifybytable',
                alg_params,
                context=context,
                feedback=feedback,
                is_child_algorithm=True)

            step += 1
            feedback.setCurrentStep(step)
            if feedback.isCanceled():
                return {}

            # VegHi

            feedback.pushInfo('')
            feedback.pushInfo('*****************************')
            feedback.pushInfo(' Open LiDAR Toolbox ')
            feedback.pushInfo(' Vegetation High ')
            feedback.pushInfo('*****************************')
            feedback.pushInfo('')

            alg_params = {
                'DATA_TYPE': 3,
                'INPUT_RASTER': outputs['Resampleveg']['output'],
                'NODATA_FOR_MISSING': True,
                'NO_DATA': -9999,
                'RANGE_BOUNDARIES': 2,
                'RASTER_BAND': 1,
                'TABLE': intermed_params['veghigh'],
                'OUTPUT': QgsProcessingUtils.generateTempFilename(
                randomfilename())
            }
            outputs['Veghi' + appendix] = processing.run(
                'native:reclassifybytable',
                alg_params,
                context=context,
                feedback=feedback,
                is_child_algorithm=True)

            step += 1
            feedback.setCurrentStep(step)
            if feedback.isCanceled():
                return {}

        # Slope Qgis

        feedback.pushInfo('')
        feedback.pushInfo('*****************************')
        feedback.pushInfo(' Open LiDAR Toolbox ')
        feedback.pushInfo(' Slope ')
        feedback.pushInfo('*****************************')
        feedback.pushInfo('')

        alg_params = {
            'INPUT': outputs['Resampledem']['output'],
            'Z_FACTOR': 1,
            'OUTPUT': QgsProcessingUtils.generateTempFilename(
                randomfilename())
        }
        outputs['SlopeQgis'] = processing.run(
            'native:slope',
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True)

        step += 1
        feedback.setCurrentStep(step)
        if feedback.isCanceled():
            return {}

        feedback.pushInfo('')
        feedback.pushInfo('*****************************')
        feedback.pushInfo(' Open LiDAR Toolbox ')
        feedback.pushInfo(' Reclassify Slope ')
        feedback.pushInfo('*****************************')
        feedback.pushInfo('')

        # Slope 12
        alg_params = {
            'DATA_TYPE': 3,
            'INPUT_RASTER': outputs['SlopeQgis']['OUTPUT'],
            'NODATA_FOR_MISSING': True,
            'NO_DATA': -9999,
            'RANGE_BOUNDARIES': 2,
            'RASTER_BAND': 1,
            'TABLE': [0, 12.5, 1, 12.5000001, 90, 0],
            'OUTPUT': QgsProcessingUtils.generateTempFilename(
                randomfilename())
        }
        outputs['Slope12'] = processing.run(
            'native:reclassifybytable',
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True)

        step += 1
        feedback.setCurrentStep(step)
        if feedback.isCanceled():
            return {}

        # Slope 22
        alg_params = {
            'DATA_TYPE': 3,
            'INPUT_RASTER': outputs['SlopeQgis']['OUTPUT'],
            'NODATA_FOR_MISSING': True,
            'NO_DATA': -9999,
            'RANGE_BOUNDARIES': 2,
            'RASTER_BAND': 1,
            'TABLE': [0, 12.5, 0, 12.500000001, 22.5, 1, 22.500000001, 90, 0],
            'OUTPUT': QgsProcessingUtils.generateTempFilename(
                randomfilename())
        }
        outputs['Slope22'] = processing.run(
            'native:reclassifybytable',
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True)

        step += 1
        feedback.setCurrentStep(step)
        if feedback.isCanceled():
            return {}

        # Slope 42
        alg_params = {
            'DATA_TYPE': 3,
            'INPUT_RASTER': outputs['SlopeQgis']['OUTPUT'],
            'NODATA_FOR_MISSING': True,
            'NO_DATA': -9999,
            'RANGE_BOUNDARIES': 2,
            'RASTER_BAND': 1,
            'TABLE': [0, 22.5, 0, 22.50000001, 42.5, 1, 42.50000001, 90, 0],
            'OUTPUT': QgsProcessingUtils.generateTempFilename(
                randomfilename())
        }
        outputs['Slope42'] = processing.run(
            'native:reclassifybytable',
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True)

        step += 1
        feedback.setCurrentStep(step)
        if feedback.isCanceled():
            return {}

        # Slope 90
        alg_params = {
            'DATA_TYPE': 3,
            'INPUT_RASTER': outputs['SlopeQgis']['OUTPUT'],
            'NODATA_FOR_MISSING': True,
            'NO_DATA': -9999,
            'RANGE_BOUNDARIES': 2,
            'RASTER_BAND': 1,
            'TABLE': [0, 42.5, 0, 42.50000001, 90, 1],
            'OUTPUT': QgsProcessingUtils.generateTempFilename(
                randomfilename())
        }
        outputs['Slope90'] = processing.run(
            'native:reclassifybytable',
            alg_params, context=context,
            feedback=feedback,
            is_child_algorithm=True)

        step += 1
        feedback.setCurrentStep(step)
        if feedback.isCanceled():
            return {}

        for row in confidenceParams:
            if row == 0:
                appendix = ' 0.25m'
            if row == 1:
                appendix = ' 0.5m'
            if row == 2:
                appendix = ' 1m'
            if row == 3:
                appendix = ' 2m'

            feedback.pushInfo('')
            feedback.pushInfo('*****************************')
            feedback.pushInfo(' Open LiDAR Toolbox ')
            feedback.pushInfo(' Calculating CFM for' + appendix)
            feedback.pushInfo('*****************************')
            feedback.pushInfo('')

            # Calc 1a
            alg_params = {
                'BAND_A': 1,
                'BAND_B': 1,
                'BAND_C': 1,
                'BAND_D': None,
                'BAND_E': None,
                'BAND_F': None,
                'EXTRA': '',
                'FORMULA': '(A+B+C)*D',
                'INPUT_A': outputs['DensityMid' + appendix]['OUTPUT'],
                'INPUT_B': outputs['DensityLow' + appendix]['OUTPUT'],
                'INPUT_C': outputs['DensityVlow' + appendix]['OUTPUT'],
                'INPUT_D': outputs['Slope90']['OUTPUT'],
                'INPUT_E': None,
                'INPUT_F': None,
                'NO_DATA': None,
                'OPTIONS': '',
                'RTYPE': 4,
                'OUTPUT': QgsProcessingUtils.generateTempFilename(
                randomfilename())
            }
            outputs['Calc1a' + appendix] = processing.run(
                'gdal:rastercalculator',
                alg_params,
                context=context,
                feedback=feedback,
                is_child_algorithm=True)

            step += 1
            feedback.setCurrentStep(step)
            if feedback.isCanceled():
                return {}

            # Calc 1b
            alg_params = {
                'BAND_A': 1,
                'BAND_B': 1,
                'BAND_C': 1,
                'BAND_D': None,
                'BAND_E': None,
                'BAND_F': None,
                'EXTRA': '',
                'FORMULA': 'A*(B+C)',
                'INPUT_A': outputs['DensityVlow' + appendix]['OUTPUT'],
                'INPUT_B': outputs['Slope12']['OUTPUT'],
                'INPUT_C': outputs['Slope22']['OUTPUT'],
                'INPUT_D': None,
                'INPUT_E': None,
                'INPUT_F': None,
                'NO_DATA': None,
                'OPTIONS': '',
                'RTYPE': 4,
                'OUTPUT': QgsProcessingUtils.generateTempFilename(
                randomfilename())
            }
            outputs['Calc1b' + appendix] = processing.run(
                'gdal:rastercalculator',
                alg_params,
                context=context,
                feedback=feedback,
                is_child_algorithm=True)

            step += 1
            feedback.setCurrentStep(step)
            if feedback.isCanceled():
                return {}

            # Calc 2
            alg_params = {
                'BAND_A': 1,
                'BAND_B': 1,
                'BAND_C': 1,
                'BAND_D': None,
                'BAND_E': None,
                'BAND_F': None,
                'EXTRA': '',
                'FORMULA': '(A+B+C)*D*2',
                'INPUT_A': outputs['DensityMid' + appendix]['OUTPUT'],
                'INPUT_B': outputs['DensityLow' + appendix]['OUTPUT'],
                'INPUT_C': outputs['DensityVlow' + appendix]['OUTPUT'],
                'INPUT_D': outputs['Slope42']['OUTPUT'],
                'INPUT_E': None,
                'INPUT_F': None,
                'NO_DATA': None,
                'OPTIONS': '',
                'RTYPE': 4,
                'OUTPUT': QgsProcessingUtils.generateTempFilename(
                randomfilename())
            }
            outputs['Calc2' + appendix] = processing.run(
                'gdal:rastercalculator',
                alg_params,
                context=context,
                feedback=feedback,
                is_child_algorithm=True)

            step += 1
            feedback.setCurrentStep(step)
            if feedback.isCanceled():
                return {}

            # Calc 3
            alg_params = {
                'BAND_A': 1,
                'BAND_B': 1,
                'BAND_C': 1,
                'BAND_D': None,
                'BAND_E': None,
                'BAND_F': None,
                'EXTRA': '',
                'FORMULA': 'A*(B+C)*3',
                'INPUT_A': outputs['DensityLow' + appendix]['OUTPUT'],
                'INPUT_B': outputs['Slope12']['OUTPUT'],
                'INPUT_C': outputs['Slope22']['OUTPUT'],
                'INPUT_D': None,
                'INPUT_E': None,
                'INPUT_F': None,
                'NO_DATA': None,
                'OPTIONS': '',
                'RTYPE': 4,
                'OUTPUT': QgsProcessingUtils.generateTempFilename(
                randomfilename())
            }
            outputs['Calc3' + appendix] = processing.run(
                'gdal:rastercalculator',
                alg_params,
                context=context,
                feedback=feedback,
                is_child_algorithm=True)

            step += 1
            feedback.setCurrentStep(step)
            if feedback.isCanceled():
                return {}

            # Calc 4a
            alg_params = {
                'BAND_A': 1,
                'BAND_B': 1,
                'BAND_C': 1,
                'BAND_D': 1,
                'BAND_E': 1,
                'BAND_F': None,
                'EXTRA': '',
                'FORMULA': 'A*(B+C+D)*E*4',
                'INPUT_A': outputs['DensityHi' + appendix]['OUTPUT'],
                'INPUT_B': outputs['Slope22']['OUTPUT'],
                'INPUT_C': outputs['Slope42']['OUTPUT'],
                'INPUT_D': outputs['Slope90']['OUTPUT'],
                'INPUT_E': outputs['Veghi' + appendix]['OUTPUT'],
                'INPUT_F': None,
                'NO_DATA': None,
                'OPTIONS': '',
                'RTYPE': 4,
                'OUTPUT': QgsProcessingUtils.generateTempFilename(
                randomfilename())
            }
            outputs['Calc4a' + appendix] = processing.run(
                'gdal:rastercalculator',
                alg_params,
                context=context,
                feedback=feedback,
                is_child_algorithm=True)

            step += 1
            feedback.setCurrentStep(step)
            if feedback.isCanceled():
                return {}

            # Calc 4b
            alg_params = {
                'BAND_A': 1,
                'BAND_B': 1,
                'BAND_C': 1,
                'BAND_D': None,
                'BAND_E': None,
                'BAND_F': None,
                'EXTRA': '',
                'FORMULA': 'A*(B+C)*4',
                'INPUT_A': outputs['DensityMid' + appendix]['OUTPUT'],
                'INPUT_B': outputs['Slope12']['OUTPUT'],
                'INPUT_C': outputs['Slope22']['OUTPUT'],
                'INPUT_D': None,
                'INPUT_E': None,
                'INPUT_F': None,
                'NO_DATA': None,
                'OPTIONS': '',
                'RTYPE': 4,
                'OUTPUT': QgsProcessingUtils.generateTempFilename(
                randomfilename())
            }
            outputs['Calc4b' + appendix] = processing.run(
                'gdal:rastercalculator',
                alg_params,
                context=context,
                feedback=feedback,
                is_child_algorithm=True)

            step += 1
            feedback.setCurrentStep(step)
            if feedback.isCanceled():
                return {}

            # Calc 5a
            alg_params = {
                'BAND_A': 1,
                'BAND_B': 1,
                'BAND_C': 1,
                'BAND_D': None,
                'BAND_E': None,
                'BAND_F': None,
                'EXTRA': '',
                'FORMULA': 'A*B*C*5',
                'INPUT_A': outputs['DensityHi' + appendix]['OUTPUT'],
                'INPUT_B': outputs['Slope12']['OUTPUT'],
                'INPUT_C': outputs['Veghi' + appendix]['OUTPUT'],
                'INPUT_D': None,
                'INPUT_E': None,
                'INPUT_F': None,
                'NO_DATA': None,
                'OPTIONS': '',
                'RTYPE': 4,
                'OUTPUT': QgsProcessingUtils.generateTempFilename(
                randomfilename())
            }
            outputs['Calc5a' + appendix] = processing.run(
                'gdal:rastercalculator',
                alg_params,
                context=context,
                feedback=feedback,
                is_child_algorithm=True)

            step += 1
            feedback.setCurrentStep(step)
            if feedback.isCanceled():
                return {}

            # Calc 5b
            alg_params = {
                'BAND_A': 1,
                'BAND_B': 1,
                'BAND_C': 1,
                'BAND_D': 1,
                'BAND_E': 1,
                'BAND_F': None,
                'EXTRA': '',
                'FORMULA': 'A*(B+C+D)*E*5',
                'INPUT_A': outputs['DensityHi' + appendix]['OUTPUT'],
                'INPUT_B': outputs['Slope22']['OUTPUT'],
                'INPUT_C': outputs['Slope42']['OUTPUT'],
                'INPUT_D': outputs['Slope90']['OUTPUT'],
                'INPUT_E': outputs['Veglow' + appendix]['OUTPUT'],
                'INPUT_F': None,
                'NO_DATA': None,
                'OPTIONS': '',
                'RTYPE': 4,
                'OUTPUT': QgsProcessingUtils.generateTempFilename(
                randomfilename())
            }
            outputs['Calc5b' + appendix] = processing.run(
                'gdal:rastercalculator',
                alg_params,
                context=context,
                feedback=feedback,
                is_child_algorithm=True)

            step += 1
            feedback.setCurrentStep(step)
            if feedback.isCanceled():
                return {}

            # Calc 6
            alg_params = {
                'BAND_A': 1,
                'BAND_B': 1,
                'BAND_C': 1,
                'BAND_D': None,
                'BAND_E': None,
                'BAND_F': None,
                'EXTRA': '',
                'FORMULA': 'A*B*C*6',
                'INPUT_A': outputs['DensityHi' + appendix]['OUTPUT'],
                'INPUT_B': outputs['Slope12']['OUTPUT'],
                'INPUT_C': outputs['Veglow' + appendix]['OUTPUT'],
                'INPUT_D': None,
                'INPUT_E': None,
                'INPUT_F': None,
                'NO_DATA': None,
                'OPTIONS': '',
                'RTYPE': 4,
                'OUTPUT': QgsProcessingUtils.generateTempFilename(
                randomfilename())
            }
            outputs['Calc6' + appendix] = processing.run(
                'gdal:rastercalculator',
                alg_params,
                context=context,
                feedback=feedback,
                is_child_algorithm=True)

            step += 1
            feedback.setCurrentStep(step)
            if feedback.isCanceled():
                return {}

            # CalcCran1
            alg_params = {
                'BAND_A': 1,
                'BAND_B': 1,
                'BAND_C': 1,
                'BAND_D': 1,
                'BAND_E': 1,
                'BAND_F': 1,
                'EXTRA': '',
                'FORMULA': 'A+B+C+D+E+F',
                'INPUT_A': outputs['Calc6' + appendix]['OUTPUT'],
                'INPUT_B': outputs['Calc5a' + appendix]['OUTPUT'],
                'INPUT_C': outputs['Calc5b' + appendix]['OUTPUT'],
                'INPUT_D': outputs['Calc4a' + appendix]['OUTPUT'],
                'INPUT_E': outputs['Calc4b' + appendix]['OUTPUT'],
                'INPUT_F': outputs['Calc3' + appendix]['OUTPUT'],
                'NO_DATA': None,
                'OPTIONS': '',
                'RTYPE': 4,
                'OUTPUT': QgsProcessingUtils.generateTempFilename(
                randomfilename())
            }
            outputs['Calccran1' + appendix] = processing.run(
                'gdal:rastercalculator',
                alg_params,
                context=context,
                feedback=feedback,
                is_child_algorithm=True)

            step += 1
            feedback.setCurrentStep(step)
            if feedback.isCanceled():
                return {}

            # CalcCranFinal
            alg_params = {
                'BAND_A': 1,
                'BAND_B': 1,
                'BAND_C': 1,
                'BAND_D': 1,
                'BAND_E': None,
                'BAND_F': None,
                'EXTRA': '',
                'FORMULA': 'A+B+C+D',
                'INPUT_A': outputs['Calccran1' + appendix]['OUTPUT'],
                'INPUT_B': outputs['Calc2' + appendix]['OUTPUT'],
                'INPUT_C': outputs['Calc1a' + appendix]['OUTPUT'],
                'INPUT_D': outputs['Calc1b' + appendix]['OUTPUT'],
                'INPUT_E': None,
                'INPUT_F': None,
                'NO_DATA': None,
                'OPTIONS': '',
                'RTYPE': 4,
                'OUTPUT': QgsProcessingUtils.generateTempFilename(
                randomfilename())
            }

            outputs['Calccranfinal' + appendix] = processing.run(
                'gdal:rastercalculator',
                alg_params,
                context=context,
                feedback=feedback,
                is_child_algorithm=True)

            results['ConfidenceMap' + appendix] = \
                outputs['Calccranfinal' + appendix]['OUTPUT']

            cfm = outputs['Calccranfinal' + appendix]['OUTPUT']

            step += 1
            feedback.setCurrentStep(step)
            if feedback.isCanceled():
                return {}

            # Warp (reproject)
            alg_params = {
                'DATA_TYPE': 0,
                'EXTRA': '',
                'INPUT': cfm,
                'MULTITHREADING': False,
                'NODATA': None,
                'OPTIONS': '',
                'RESAMPLING': 0,
                'SOURCE_CRS': parameters['CRS'],
                'TARGET_CRS': parameters['CRS'],
                'TARGET_EXTENT': None,
                'TARGET_EXTENT_CRS': None,
                'TARGET_RESOLUTION': None,
                'OUTPUT': QgsProcessingUtils.generateTempFilename(
                    'cfm' + appendix + '.tif')
            }

            outputs['WarpReproject'] = processing.run(
                'gdal:warpreproject',
                alg_params,
                context=context,
                feedback=feedback,
                is_child_algorithm=True)

            cfm = alg_params['OUTPUT']

            feedback.setCurrentStep(44)
            if feedback.isCanceled():
                return {}

            # Set style for raster layer
            folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]
            styleFile = os.path.join(
                os.path.join(folder, 'stylefiles/DFMconfidenceMap.qml'))

            alg_params = {
                'INPUT': cfm,
                'STYLE': styleFile
            }
            if exists(styleFile) == True:
                outputs['SetStyleForRasterLayer'] = processing.run(
                    'qgis:setstyleforrasterlayer',
                    alg_params,
                    context=context,
                    feedback=feedback,
                    is_child_algorithm=True)

            if parameters['loadCFM']:
                # Load result
                alg_params = {
                    'INPUT': cfm,
                    'NAME': parameters['prefix'] + 'DFM CM' + appendix
                }
                outputs['LoadResult'] = processing.run(
                    'native:loadlayer',
                    alg_params,
                    context=context,
                    feedback=feedback,
                    is_child_algorithm=True)

                step += 1
                feedback.setCurrentStep(step)
                if feedback.isCanceled():
                    return {}

            results['CFM' + appendix] = cfm

        return results

    def name(self):
        return 'DFM confidence map'

    def displayName(self):
        return 'DFM confidence map'

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr(self.groupId())

    def icon(self):
        cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]
        icon = QIcon(os.path.join(
            os.path.join(cmd_folder, 'icons/2_0_confidencemap.png')))
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
                    <p>This algorithm calculates a DFM Confidence Map based on 
                    the CRAN decision tree. The confidence map is primarily used
                    for quality assessment of the DFM (archaeology- specific 
                    DEM, combining ground and buildings) or DEM, but can also 
                    be used to determine the optimal resolution of the DFM/DEM.
                    </p>
                    <h2>Input parameters</h2>"""

        conclusion = """
                    <br><br>
                    DFM confidence map incorporates parts of GDAL, GRASS GIS, 
                    and QGIS core tools.<br><br>
                    <p><b>References:</b><br><br> Štular, B.; Lozić, E.; 
                    Eichert, S. Airborne LiDAR-Derived Digital Elevation Model 
                    for Archaeology. Remote Sens. 2021, 13, 1855. 
                    <a href="https://doi.org/10.3390/rs13091855">
                    https://doi.org/10.3390/rs13091855</a></p><br>
                    <a href="https://stefaneichert.github.io/OpenLidarToolbox/">
                    Website</a><br><p align="right">Algorithm author: 
                    Benjamin Štular, Edisa Lozić, Stefan Eichert </p>
                    <p align="right">Help author: Benjamin Štular, Edisa Lozić,
                    Stefan Eichert</p></body></html>"""


        helpText = title + getHelpText(['cfMap', 'crs', 'prefix',
                                        'faq', 'nodata']) + conclusion

        helpText = " ".join((helpText.replace('\n', '')).split())
        return helpText

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return dfmConfidenceMap()
