# **Open LiDAR Tools**

![Logo]( src/plugin/open_lidar_tools/icon.png "Open LiDAR Tools")

Open LiDAR Tools is a QGIS plugin and part of the MALiAp scientific research project, which aims at the strives towards methodological maturity of airborne LiDAR in archaeology. Our intention is to provide open access tools for QGIS to assist archaeologists in processing point cloud LiDAR data. Each of the tools we are developing is based on over a decade of experience. The scientific background for the tool is/will be published in open access peer reviewed papers.
The plugin is developed by Stefan Eichert, Benjamin Štular and Edisa Lozić 2021.

Published articles in the project:

https://www.mdpi.com/2076-3263/11/1/26

https://www.mdpi.com/2072-4292/12/18/3025

### **Installation**

The easiest way to install it, is to [download the plugin ZIP file](https://github.com/stefaneichert/OpenLidarTools/raw/main/src/plugin/open_lidar_tools.zip "Download Plugin as ZIP").
Then in QGIS simply choose "Install from ZIP" from the Plugins / Manage and Install Plugins menu.
Then Open LiDAR Tools will then show up in the processing toolbox


### **Modules**

**Confidence Map**  
This algorithm calculates a DFM Confidence Map based on the CRAN decision tree. The confidence map is primarily used for the quality assessment of the DFM, but can also be used to determine the optimal resolution for the DFM.

