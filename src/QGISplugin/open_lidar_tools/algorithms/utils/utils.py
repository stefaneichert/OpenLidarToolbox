from qgis.core import QgsCoordinateReferenceSystem
from qgis.utils import iface

def setCrs():
    crs = QgsCoordinateReferenceSystem(
        iface.mapCanvas().mapSettings().destinationCrs().authid())
    epsg = 'EPSG:3857'
    print("CRS Units: {}".format(crs.mapUnits()))
    if crs.isValid() and crs.isGeographic() != True and crs.mapUnits() == 0:
        epsg = (crs.authid())
        print('hallo')
    return epsg

def getHelpText(array):

    helpText = ''

    if 'hyb' in array:
        helpText += """
        <h3>DFM Confidence Map</h3>
        <p>Must be calculated with DFM Confidence Map module from IDW/TLI 
        interpolation for the desired cell size.</p>
        <h3>IDW Interpolation</h3>
        <p>Input DFM/DEM interpolated with IDW (Inverse Distance Weighing; use 
        Create base data tool or, if available, Golden Software Surfer).</p>
        <h3>TLI Interpolation</h3>
        <p>Input DFM/DEM interpolated with TLI (Triangulation with Linear 
        Interpolation; use Create base data tool).</p>"""

    if 'cfMap' in array:
        helpText += """
        <h3>DEM/DFM Layer</h3>
        <p>DFM (or any DEM) with a recommended cell size of 0.5m in raster 
        format (use Create DFM tool)</p>
        <h3>Ground Point Density Layer</h3>
        <p>Point density layer of ground (ASPRS class 2) and building (ASPRS 
        class 6) points in raster format. Recommended cell size is 0.5 or 1.0 m 
        (use Create base data tool).</p>
        <h3>Low Vegetation Density Layer</h3>
        <p>Point density layer of low vegetation (ASPRS standard LIDAR point 
        class 3, height 0.5-2.0 m) in raster format. Recommended cell size is 
        0.5 or 1.0 m (use Create base data tool).</p>"""

    if 'lasfile' in array:
        helpText += """    
        <h3>Input LAS/LAZ File</h3>
        <p>Point cloud in LAS or LAZ format. Noise classified as ASPRS class 7 
        will be exempt from the processing, all other preexisting classification
        will be ignored.
        <br><b>Point clouds with more than 30 million points will fail or will 
        take very long to process.</b></p>"""

    if 'las' in array:
        helpText += """
        <h3>The input LAS/LAZ file is already classified</h3>
        <p>Please tick this box, if your file (LAS/LAZ format) is already 
        classified. If it is not, or you are not sure, leave it blank.</p>"""

    if 'noise' in array:
        helpText += """
        <h3>Remove low noise</h3>
        <p>Please tick this box if your data suffers from unclassified low noise
        that causes the "Swiss cheese” effect (sharp holes where there are 
        none). This will not work for low density datasets (less than 1 ground
        point per m2).</p>"""

    if 'crs' in array:
        helpText +="""
        <h3>Source File Coordinate System</h3>
        <p>Select the Coordinate Reference System (CRS) of the input LAS /LAZ 
        file. Make sure the CRS is Cartesian (x and y in meters, not degrees). 
        If you are not sure which is the correct CRS and you only need it 
        temporarily, you can select any Cartesian CRS, for example, EPSG:3857. 
        XYZ should be in m. <b> <br>The tool will not work correctly with data 
        in feet, km, cm etc.</b><br>Per default the project CRS is selected. If 
        you did not yet define it respectively if it is not cartesian, EPSG 3857
        is selected.  </p>"""

    if 'cell' in array:
        helpText +="""
        <h3>Cell Size</h3>
        <p>DFM grid resolution, default value is 0.5 m. Optimal resolution for 
        any given point cloud can be calculated with the DFM Confidence Map 
        tool.</p>"""

    if 'cfMap' in array:
        helpText += """
        <h3>Resolution of target DFM</h3>
        <p>DFM/DEM resolution (multiple choice ) refers to the cell size of the 
        target DFM for which the confidence is calculated (i.e., 0.5 m provides 
        information about the confidence level if 0.5 m DFM is calculated in the
         next step).</p>
        <h3>Output Cell Size:</h3>
        <p>Define the cell size of the Confidence Map. 0.5 or 1 m is 
        recommended. (It is possible to calculate DFM Confidence Map for high 
        resolution, e.g. 0.25 m, but display the result at lower resolution, 
        e.g. 1 m.)</p>"""

    if 'hyb' in array:
        helpText += """
        <h3>Grow Radius (Cells) </h3>
        <p>Grow radius in raster cells for "RED" areas with low DFM confidence 
        will increase (grow) the areas where IDW is used. Tweak this setting if
        you notice unwanted interpolation artefacts (noise) in contact areas 
        between TLI and IDW.</p>"""

    if 'dfmin' in array:
        helpText += """
        <h3>DFM/DEM</h3><p>DFM or DEM in any raster format supported by QGIS, 
        e.g., GeoTIFF.</p>"""

    if 'prefix' in array:
        helpText += """
        <h3>Name prefix for layers</h3>
        <p>The output layers are added to the map as temporary layers with 
        default names. They can then be saved as files. To distinguish them from
        files previously created with the same tool, a prefix should be defined
        to prevent duplication (which may cause errors on some systems).</p>"""

    helpText += '<h2>Output</h2>'

    if 'dfm' in array:
        helpText += """
        <p><b>DFM: </b>Digital Feature Model (archaeology-specific DEM, 
        combining ground and buildings)</p>"""

    if 'tli' in array:
        helpText += '<p><b>TLI:</b> Triangulated interpolation of DFM</p>'

    if 'idw' in array:
        helpText += '<p><b>IDW:</b> Inverse distance weighting interpolation ' \
                    'of DFM</p>'

    if 'gpd' in array:
        helpText += '<p><b>Ground Point Density</b></p>'

    if 'lvd' in array:
        helpText += '<p><b>Low Vegetation Density</b></p>'

    if 'cfm' in array:
        helpText += """
        <p><b>Confidence Map: </b> DFM Confidence Map for 0.5 m resolution (if 
        other resolutions are needed – e.g., the map is either completely red or
        completely blue – use the dedicated tool)</p>"""

    if 'vis' in array:
        helpText += '<p><b>Visualisations:</b></p>'

    if 'vat' in array:
        helpText += """
        <p><b>VAT: </b> Visualisation for archaeological topography</p>"""

    if 'svf' in array:
        helpText += """<p><b>SVF: </b> Sky view factor</p>"""

    if 'opn' in array:
        helpText += '<p><b>Opennes: </b> Openness – positive</p>'

    if 'dme' in array:
        helpText += '<p><b>DME: </b> Difference from mean elevation</p>'

    if 'hls' in array:
        helpText += '<p><b>Hillshade: </b> Hillshade/Relief shading</p>'

    if 'outlas' in array:
        helpText += """
        <p><b>Classified LAS/LAZ file: </b> Classified point cloud. 
        Please Specify folder and file name.</p>"""

    if 'faq' in array:
        helpText +='<h2>FAQ</h2>'

    if 'blk' in array:
        helpText += """
        <h3>The edges of my outputs are black</h3>
        <p>This is due to what is known as the edge effect. In 0NE processing, 
        the values are computed from surrounding points; since there are no 
        surrounding points at the edge, the output values are "strange", e.g., 
        they are displayed as black in most visualisations. This cannot be 
        avoided and the only solution is to process larger areas or create 
        overlapping mosaics.</p>"""

    if 'qua' in array:
        helpText += """
        <h3>The quality of classification does not meet my expectations, how can
        I improve it?</h3><p>This tool is one-size-fits-all and is designed for 
        simplicity. Like any other tool without user-defined parameters, it will
        produce OK results for any dataset, but it will often not return the 
        best possible result. We recommend specialized software, such as 
        LAStools or Whitebox tools, to optimize results.</p>"""

    if 'nodata' in array:
        helpText += """
        <h3>I have NoData holes in my DFM/DEM</h3>
        <p>Wherever one of the inputs has a NoData value, the algorithm will 
        return NoData. Common sources for NoData are too low radius setting for 
        IDW.</p>"""

    if 'hyb' in array:
        helpText += """
        <h3>The artifacts (noise) in the contact areas are too big and tweaking 
        the Grow radius doesn't help</h3><p>Some amount of artifacts is 
        inevitable. In our testing the artifacts were significantly smaller when
        the input layers have been calculated with Golden Software Surfer, 
        since exactly same parameters for neighborhood search can be set. If 
        the artifacts are so strong, that they can misguide archaeological 
        interpretation, then we suggest using IDW interpolation instead.</p>"""

    return helpText


