# **Open LiDAR Tools**

![Logo]( src/plugin/open_lidar_tools/icon.png "Open LiDAR Tools")

Under active development, please check for updates! (Currently only one module is available)

Open LiDAR Tools provides one-click processing of airborne LiDAR data from point cloud to LiDAR visualisation. The tools are optimised for archaeology, but have broader application for anyone primarily interested in visual inspection of LiDAR data.

The input required is an unclassified point cloud in LAZ /LAS format. The tool returns several outputs needed for interpretative mapping of archaeological features. 

**Data**
  1. Classified point cloud  - LAZ
  2. Digital feature model (DFM, also known as "archaeological DEM") - GeoTIFF
  3. LiDAR visualisations (Sky View Factor, Opennes, Archaeological VAT, and Difference from Mean Elevation also known as Local Relief Model) - GeoTIFFs

**Metadata**

  4. Ground point density - GeoTIFF, values in pnts/m2
  5. Low vegetation point density - GeoTIFF, values in pnts/m2
  6. DFM confidence map -  - GeoTIFF, custom values, higher is better

In addition to the one-click solution, several stand-alone modules are available:
1. Point cloud classification
2. Interpolation of DFM/DEM
3. DFM confidence map
4. Low vegetation density
5. Ground point density.

Open LiDAR Tools is a QGIS plug-in developed in collaboration between NHM Wien and ZRC SAZU as part of the MALiAp scientific research project (ARRS N6-0132), which aims at the methodological maturity of airborne LiDAR in archaeology. The scientific background for the tool is published in open access peer reviewed papers:
https://www.mdpi.com/2076-3263/11/1/26
https://www.mdpi.com/2072-4292/12/18/3025

### **Installation**

The easiest way to install it, is to [download the plugin ZIP file](https://github.com/stefaneichert/OpenLidarTools/raw/main/src/plugin/open_lidar_tools.zip "Download Plugin as ZIP").
Then in QGIS simply choose "Install from ZIP" from the Plugins / Manage and Install Plugins menu.
Then Open LiDAR Tools will then show up in the processing toolbox.
Users who need deeper access to even more settings can download individual QGIS models here.

### **Dependencies**

Open LiDAR tools are a "shell" that uses several excellent tools under the hood: GDAL, GRASS, QGIS native tools, LAStools, Whitebox Tools and RVT. Therefore, the following plug-ins must be installed before the Open LiDAR tools: LAStools, Whitebox Tools and RVT.


### **Modules**

**Confidence Map**  
This algorithm calculates a DFM Confidence Map based on the CRAN decision tree. The confidence map is primarily used for the quality assessment of the DFM, but can also be used to determine the optimal resolution for the DFM.

