<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis maxScale="0" styleCategories="AllStyleCategories" minScale="1e+08" version="3.16.4-Hannover" hasScaleBasedVisibilityFlag="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <temporal fetchMode="0" enabled="0" mode="0">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <customproperties>
    <property key="WMSBackgroundLayer" value="false"/>
    <property key="WMSPublishDataSourceUrl" value="false"/>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="identify/format" value="Value"/>
  </customproperties>
  <pipe>
    <provider>
      <resampling zoomedOutResamplingMethod="nearestNeighbour" enabled="false" maxOversampling="2" zoomedInResamplingMethod="nearestNeighbour"/>
    </provider>
    <rasterrenderer alphaBand="-1" band="1" opacity="1" nodataColor="" type="paletted">
      <rasterTransparency/>
      <minMaxOrigin>
        <limits>None</limits>
        <extent>WholeRaster</extent>
        <statAccuracy>Estimated</statAccuracy>
        <cumulativeCutLower>0.02</cumulativeCutLower>
        <cumulativeCutUpper>0.98</cumulativeCutUpper>
        <stdDevFactor>2</stdDevFactor>
      </minMaxOrigin>
      <colorPalette>
        <paletteEntry alpha="255" color="#d63228" label="1" value="1"/>
        <paletteEntry alpha="255" color="#f0825a" label="2" value="2"/>
        <paletteEntry alpha="255" color="#fbd399" label="3" value="3"/>
        <paletteEntry alpha="255" color="#d9e0bf" label="4" value="4"/>
        <paletteEntry alpha="255" color="#8ca5b9" label="5" value="5"/>
        <paletteEntry alpha="255" color="#4f73b4" label="6" value="6"/>
      </colorPalette>
      <colorramp name="[source]" type="randomcolors"/>
    </rasterrenderer>
    <brightnesscontrast contrast="0" gamma="1" brightness="0"/>
    <huesaturation saturation="0" grayscaleMode="0" colorizeStrength="100" colorizeGreen="128" colorizeBlue="128" colorizeRed="255" colorizeOn="0"/>
    <rasterresampler maxOversampling="2"/>
    <resamplingStage>resamplingFilter</resamplingStage>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
