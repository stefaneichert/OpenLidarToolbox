# **Open LiDAR Tools**

![Logo]( src/plugin/open_lidar_tools/icon.png "Open LiDAR Tools")

Under active development, please check for updates! (Currently only one module is available: [download the plugin ZIP file](https://github.com/stefaneichert/OpenLidarTools/raw/main/src/plugin/open_lidar_tools.zip "Download Plugin as ZIP").)

Open LiDAR Tools provides one-click processing of airborne LiDAR data from point cloud to LiDAR visualisation. The tools are optimised for archaeology, but have broader application for anyone primarily interested in visual inspection of LiDAR data.

The input required is an unclassified point cloud in LAZ /LAS format. The tool returns several outputs needed for interpretative mapping of archaeological features.

Open LiDAR Tools is a QGIS plug-in developed in collaboration between NHM Wien and ZRC SAZU as part of the MALiAp scientific research project (ARRS N6-0132), which aims at the methodological maturity of airborne LiDAR in archaeology. The scientific background for the tool is published in open access peer reviewed papers:  
https://www.mdpi.com/2076-3263/11/1/26  
https://www.mdpi.com/2072-4292/12/18/3025

# **Table of Content**
- [**Data**](#data)
- [**Metadata**](#metadata)
- [**Installation**](#installation)
- [**Dependencies**](#dependencies)
- [**Modules**](#modules)
  * [**Confidence Map**](#confidence-map)
  * [**Hybrid Interpolation**](#hybrid-interpolation)

# **Data**

  1. Classified point cloud  - LAZ
  2. Digital feature model (DFM, also known as "archaeological DEM") - GeoTIFF
  3. LiDAR visualisations (Sky View Factor, Opennes, Archaeological VAT, and Difference from Mean Elevation also known as Local Relief Model) - GeoTIFFs

# **Metadata**

  4. Ground point density - GeoTIFF, values in pnts/m2
  5. Low vegetation point density - GeoTIFF, values in pnts/m2
  6. DFM confidence map - GeoTIFF, custom values, higher is better

In addition to the one-click solution, several stand-alone modules are available:
 1. Point cloud classification
 2. Interpolation of DFM/DEM
 3. DFM confidence map
 4. Low vegetation density
 5. Ground point density.

# **Installation**

The easiest way to install it, is to [download the plugin ZIP file](https://github.com/stefaneichert/OpenLidarTools/raw/main/src/plugin/open_lidar_tools.zip "Download Plugin as ZIP").
Then in QGIS simply choose "Install from ZIP" from the Plugins / Manage and Install Plugins menu.
Then Open LiDAR Tools will then show up in the processing toolbox.
Users who need deeper access to even more settings can download individual QGIS models [here](https://github.com/stefaneichert/OpenLidarTools/main/src/models).

# **Dependencies**

Open LiDAR tools are a "shell" that uses several excellent tools under the hood: GDAL, GRASS, QGIS native tools, LAStools, Whitebox Tools and RVT. Therefore, the following plug-ins must be installed before the Open LiDAR tools: LAStools, Whitebox Tools and RVT.


# **Modules**
## **Confidence Map**  
This algorithm calculates a DFM Confidence Map based on the CRAN decision tree. The confidence map is primarily used for the quality assessment of the DFM, but can also be used to determine the optimal resolution for the DFM.
Digital Feature Model (DFM) is archaeology- specific DEM interpolated from airborne LiDAR data. This algorithm calculates DFM Confidence Map based on the CRAN decision tree. The confidence map is primarily used for the quality assessment of the DFM, but can also be used to determine the optimal resolution for the DFM.
This algorithm can also be used to calculate the prediction uncertainty map for any DEM, but the settings must be adjusted for cell size.

### **Inputs:**

***DEM/DFM Layer:***  
DFM (or any DEM) with cell size 0.5m in raster format.  

***Low Vegetation Density Layer:***  
Point density layer of low vegetation (ASPRS standard LIDAR point class 3, height 0.5-2.0 m) in raster format. Recommended cell size is 0.5 or 1.0 m. (Whitebox Tools / LidarPointDensity can be used to calculate this layer from a LAS file).
Ground Point Density Layer: Point density layer of ground (ASPRS class 2) and building (ASPRS class 6) points in raster format. Recommended cell size is 0.5 or 1.0 m. (Whitebox Tools / LidarPointDensity can be used to calculate this layer from a LAS file).

### **Parameters:**  
***Resolution:***  
DFM/DEM Resolution (multiple choice).
***Output Cell Size:***
Define the cell size of the Confidence Map. 0.5 or 1 m is recommended. (It is possible to calculate DFM Confidence Map for high resolution, e.g. 0.25 m, but display the result at lower resolution, e.g. 1 m.)

### **FAQ:**  
**I have NoData holes in my DFM/DEM**  
Wherever one of the inputs has a NoData value, the algorithm will return NoData. Common sources for NoData are too low radius setting for IDW.

**Literature:** Štular, Lozić, Eichert 2021a (in press).


## **Hybrid Interpolation**  
This algorithm calculates a hybrid interpolation of DFM/DEM. It uses IDW (Inverse Distance Weighing) interpolation in areas of low DFM confidence (levels 1-3) and TLI ( Triangulation with Linear Interpolation) interpolation in areas of high DFM confidence (levels 4-6). The user provides DFM confidence map, TLI and IDW. The module works best when TLI and IDW are calculated under very similar conditions, such as those provided by Golden Software Surfer.
This interpolator is best suited for low or medium point density data characterized by significant local variation in point density, such as an open landscape interspersed with hedgerows or other patches of dense vegetation. For high point density data, the TLI by itself usually gives better results.

### **Inputs:**  

***DFM Confidence Map:***  
Must be calculated with DFM Confidence Map module from IDW interpolation for the desired cell size.

***IDW Interpolation:***  
Input DFM/DEM interpolated with IDW (Inverse Distance Weighing). (Whitebox Tools / LidarIDWInterpolation or Golden Software Surfer can be used to calculate this layer from a LAS file.) Alternatively, any interpolator deemed to be most suitable for undersampled areas can be used.

***TLI Interpolation:***  
Input DFM/DEM interpolated with TLI ( Triangulation with Linear Interpolation). (Whitebox Tools / LidarTINGriddin or Golden Software Surfer can be used to calculate this layer from a LAS file.) Alternatively, any interpolator deemed to be most suitable for properly sampled and oversampled areas can be used.

### **Parameters:**  
***Cell Size:***  
The resolution or cell size of the final DFM/DEM. For best results, all inputs should have the same cell size.
***Grow Radius (Cell Size):***  
Grow radius for "RED" areas with low DFM confidence will increase (grow) the areas where IDW is used. Tweak this setting if you notice unwanted interpolation artefacts (noise) in contact areas between TLI and IDW.  

![correct]( src/plugin/open_lidar_tools/help/correct.jpg "Correct radius (3)")  
correct radius (3) 

![wrong]( src/plugin/open_lidar_tools/help/wrong.jpg "Wrong radius (2)")  
wrong radius (1)  


### **FAQ:**  
I have NoData holes in my DFM/DEM.
Wherever one of the inputs has a NoData value, the algorithm will return NoData. Common sources for NoData are too low radius setting for IDW.

**Literature:** Štular, Lozić, Eichert 2021a (in press).
