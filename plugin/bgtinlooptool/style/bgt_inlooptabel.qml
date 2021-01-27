<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis readOnly="0" styleCategories="AllStyleCategories" simplifyLocal="1" minScale="1e+08" simplifyDrawingTol="1" maxScale="0" labelsEnabled="0" hasScaleBasedVisibilityFlag="0" version="3.10.10-A Coruña" simplifyAlgorithm="0" simplifyDrawingHints="0" simplifyMaxScale="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 symbollevels="0" type="RuleRenderer" enableorderby="0" forceraster="0">
    <rules key="{8615500f-291b-43e9-9637-98f8858aa5b6}">
      <rule symbol="0" key="{e26fa1d6-5bbb-4001-b16f-2f0b34504877}" label="Hemelwaterriool 100%" filter=" &quot;hemelwaterriool&quot; = 100 and ( &quot;gemengd_riool&quot; + &quot;hemelwaterriool&quot; + &quot;vgs_hemelwaterriool&quot; + &quot;infiltratievoorziening&quot; + &quot;niet_aangesloten&quot; ) = 100"/>
      <rule symbol="1" key="{7be024ad-67fd-4f91-b658-70ec4c0e63fe}" label="VGS Hemelwaterriool 100%" filter=" &quot;vgs_hemelwaterriool&quot; = 100 and ( &quot;gemengd_riool&quot; + &quot;hemelwaterriool&quot; + &quot;vgs_hemelwaterriool&quot; + &quot;infiltratievoorziening&quot; + &quot;niet_aangesloten&quot; ) = 100"/>
      <rule symbol="2" key="{3d292b4a-48ea-4954-9649-080da78561db}" label="Gemengd 100%" filter=" &quot;gemengd_riool&quot; = 100 and ( &quot;gemengd_riool&quot; + &quot;hemelwaterriool&quot; + &quot;vgs_hemelwaterriool&quot; + &quot;infiltratievoorziening&quot; + &quot;niet_aangesloten&quot; ) = 100"/>
      <rule symbol="3" key="{a24c39d3-a09e-432d-a203-84441af42b85}" label="Hemelwaterriool en Gemengd" filter="( &quot;hemelwaterriool&quot; > 0 AND hemelwaterriool &lt; 100 AND  &quot;gemengd_riool&quot; > 0 AND gemengd_riool &lt; 100) and ( &quot;gemengd_riool&quot; + &quot;hemelwaterriool&quot; + &quot;vgs_hemelwaterriool&quot; + &quot;infiltratievoorziening&quot; + &quot;niet_aangesloten&quot; ) = 100"/>
      <rule symbol="4" key="{3d88a01b-5ca4-40e3-b4d3-935db7458ba6}" label="Niet aangesloten 100%" filter=" &quot;niet_aangesloten&quot;  = 100 and ( &quot;gemengd_riool&quot; + &quot;hemelwaterriool&quot; + &quot;vgs_hemelwaterriool&quot; + &quot;infiltratievoorziening&quot; + &quot;niet_aangesloten&quot; ) = 100"/>
      <rule symbol="5" key="{49c2c107-4207-4f1f-87e7-cf522249dc51}" label="Infiltratievoorziening 100%" filter=" &quot;infiltratievoorziening&quot; = 100 and ( &quot;gemengd_riool&quot; + &quot;hemelwaterriool&quot; + &quot;vgs_hemelwaterriool&quot; + &quot;infiltratievoorziening&quot; + &quot;niet_aangesloten&quot; ) = 100"/>
      <rule symbol="6" key="{6b9886b8-93e3-42cb-a57c-3330f89e86eb}" label="Overig (wel valide, totaal = 100)" filter="ELSE"/>
      <rule symbol="7" key="{20a36527-a20b-4bce-b851-6353175c759a}" label="Overig (niet valide, totaal ≠ 100)" filter=" ( &quot;gemengd_riool&quot; + &quot;hemelwaterriool&quot; + &quot;vgs_hemelwaterriool&quot; + &quot;infiltratievoorziening&quot; + &quot;niet_aangesloten&quot; ) != 100"/>
    </rules>
    <symbols>
      <symbol force_rhr="0" name="0" alpha="1" type="fill" clip_to_extent="1">
        <layer class="SimpleFill" enabled="1" locked="0" pass="0">
          <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
          <prop v="165,183,255,255" k="color"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="255,255,255,103" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0.2" k="outline_width"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="solid" k="style"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol force_rhr="0" name="1" alpha="1" type="fill" clip_to_extent="1">
        <layer class="SimpleFill" enabled="1" locked="0" pass="0">
          <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
          <prop v="165,183,255,255" k="color"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="255,255,255,128" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0" k="outline_width"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="solid" k="style"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer class="PointPatternFill" enabled="1" locked="0" pass="0">
          <prop v="0" k="displacement_x"/>
          <prop v="3x:0,0,0,0,0,0" k="displacement_x_map_unit_scale"/>
          <prop v="MM" k="displacement_x_unit"/>
          <prop v="0" k="displacement_y"/>
          <prop v="3x:0,0,0,0,0,0" k="displacement_y_map_unit_scale"/>
          <prop v="MM" k="displacement_y_unit"/>
          <prop v="5" k="distance_x"/>
          <prop v="3x:0,0,0,0,0,0" k="distance_x_map_unit_scale"/>
          <prop v="MM" k="distance_x_unit"/>
          <prop v="5" k="distance_y"/>
          <prop v="3x:0,0,0,0,0,0" k="distance_y_map_unit_scale"/>
          <prop v="MM" k="distance_y_unit"/>
          <prop v="0" k="offset_x"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_x_map_unit_scale"/>
          <prop v="MM" k="offset_x_unit"/>
          <prop v="0" k="offset_y"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_y_map_unit_scale"/>
          <prop v="MM" k="offset_y_unit"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol force_rhr="0" name="@1@1" alpha="1" type="marker" clip_to_extent="1">
            <layer class="SimpleMarker" enabled="1" locked="0" pass="0">
              <prop v="0" k="angle"/>
              <prop v="149,165,230,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="cross_fill" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="35,35,35,0" k="outline_color"/>
              <prop v="solid" k="outline_style"/>
              <prop v="0" k="outline_width"/>
              <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
              <prop v="MM" k="outline_width_unit"/>
              <prop v="diameter" k="scale_method"/>
              <prop v="2" k="size"/>
              <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
              <prop v="MM" k="size_unit"/>
              <prop v="1" k="vertical_anchor_point"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" type="QString" value=""/>
                  <Option name="properties"/>
                  <Option name="type" type="QString" value="collection"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol force_rhr="0" name="2" alpha="1" type="fill" clip_to_extent="1">
        <layer class="SimpleFill" enabled="1" locked="0" pass="0">
          <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
          <prop v="255,213,181,255" k="color"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="255,255,255,128" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0" k="outline_width"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="solid" k="style"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol force_rhr="0" name="3" alpha="1" type="fill" clip_to_extent="1">
        <layer class="SimpleFill" enabled="1" locked="0" pass="0">
          <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
          <prop v="255,213,181,255" k="color"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="255,255,255,128" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0.26" k="outline_width"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="solid" k="style"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer class="LinePatternFill" enabled="1" locked="0" pass="0">
          <prop v="45" k="angle"/>
          <prop v="207,20,192,255" k="color"/>
          <prop v="2" k="distance"/>
          <prop v="3x:0,0,0,0,0,0" k="distance_map_unit_scale"/>
          <prop v="MM" k="distance_unit"/>
          <prop v="0.5" k="line_width"/>
          <prop v="3x:0,0,0,0,0,0" k="line_width_map_unit_scale"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol force_rhr="0" name="@3@1" alpha="1" type="line" clip_to_extent="1">
            <layer class="SimpleLine" enabled="1" locked="0" pass="0">
              <prop v="square" k="capstyle"/>
              <prop v="5;2" k="customdash"/>
              <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
              <prop v="MM" k="customdash_unit"/>
              <prop v="0" k="draw_inside_polygon"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="165,183,255,255" k="line_color"/>
              <prop v="solid" k="line_style"/>
              <prop v="1" k="line_width"/>
              <prop v="MM" k="line_width_unit"/>
              <prop v="0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="0" k="ring_filter"/>
              <prop v="0" k="use_custom_dash"/>
              <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" type="QString" value=""/>
                  <Option name="properties"/>
                  <Option name="type" type="QString" value="collection"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol force_rhr="0" name="4" alpha="1" type="fill" clip_to_extent="1">
        <layer class="SimpleFill" enabled="1" locked="0" pass="0">
          <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
          <prop v="167,255,159,255" k="color"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="255,255,255,179" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0" k="outline_width"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="solid" k="style"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol force_rhr="0" name="5" alpha="1" type="fill" clip_to_extent="1">
        <layer class="SimpleFill" enabled="1" locked="0" pass="0">
          <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
          <prop v="163,205,185,255" k="color"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="114,133,132,64" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0" k="outline_width"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="solid" k="style"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol force_rhr="0" name="6" alpha="1" type="fill" clip_to_extent="1">
        <layer class="SimpleFill" enabled="1" locked="0" pass="0">
          <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
          <prop v="201,201,201,255" k="color"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="153,153,153,128" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0" k="outline_width"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="solid" k="style"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol force_rhr="0" name="7" alpha="1" type="fill" clip_to_extent="1">
        <layer class="SimpleFill" enabled="1" locked="0" pass="0">
          <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
          <prop v="255,1,1,255" k="color"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="255,255,255,128" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0" k="outline_width"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="solid" k="style"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
  </renderer-v2>
  <customproperties>
    <property key="dualview/previewExpressions">
      <value>"lokaalid"</value>
    </property>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Histogram">
    <DiagramCategory scaleBasedVisibility="0" sizeScale="3x:0,0,0,0,0,0" scaleDependency="Area" enabled="0" sizeType="MM" width="15" height="15" penAlpha="255" minScaleDenominator="0" diagramOrientation="Up" lineSizeType="MM" minimumSize="0" rotationOffset="270" lineSizeScale="3x:0,0,0,0,0,0" backgroundColor="#ffffff" penWidth="0" penColor="#000000" opacity="1" maxScaleDenominator="1e+08" labelPlacementMethod="XHeight" barWidth="5" backgroundAlpha="255">
      <fontProperties description="MS Shell Dlg 2,7.8,-1,5,50,0,0,0,0,0" style=""/>
      <attribute label="" field="" color="#000000"/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings obstacle="0" placement="1" showAll="1" linePlacementFlags="18" dist="0" priority="0" zIndex="0">
    <properties>
      <Option type="Map">
        <Option name="name" type="QString" value=""/>
        <Option name="properties"/>
        <Option name="type" type="QString" value="collection"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions removeDuplicateNodes="0" geometryPrecision="0">
    <activeChecks/>
    <checkConfiguration type="Map">
      <Option name="QgsGeometryGapCheck" type="Map">
        <Option name="allowedGapsBuffer" type="double" value="0"/>
        <Option name="allowedGapsEnabled" type="bool" value="false"/>
        <Option name="allowedGapsLayer" type="QString" value=""/>
      </Option>
    </checkConfiguration>
  </geometryOptions>
  <fieldConfiguration>
    <field name="id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="laatste_wijziging">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option name="allow_null" type="bool" value="true"/>
            <Option name="calendar_popup" type="bool" value="true"/>
            <Option name="display_format" type="QString" value="yyyy-MM-dd HH:mm:ss"/>
            <Option name="field_format" type="QString" value="yyyy-MM-dd HH:mm:ss"/>
            <Option name="field_iso_format" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="bgt_identificatie">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="type_verharding">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="Dak" type="QString" value="dak"/>
              </Option>
              <Option type="Map">
                <Option name="Gesloten verhard" type="QString" value="gesloten verhard"/>
              </Option>
              <Option type="Map">
                <Option name="Open verhard" type="QString" value="open verhard"/>
              </Option>
              <Option type="Map">
                <Option name="Onverhard" type="QString" value="onverhard"/>
              </Option>
              <Option type="Map">
                <Option name="Groen(blauw) dak" type="QString" value="groen(blauw) dak"/>
              </Option>
              <Option type="Map">
                <Option name="Waterpasserende verharding" type="QString" value="waterpasserende verharding"/>
              </Option>
              <Option type="Map">
                <Option name="Water" type="QString" value="water"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="graad_verharding">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option name="AllowNull" type="bool" value="true"/>
            <Option name="Max" type="double" value="100"/>
            <Option name="Min" type="double" value="0"/>
            <Option name="Precision" type="int" value="0"/>
            <Option name="Step" type="double" value="1"/>
            <Option name="Style" type="QString" value="SpinBox"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="hellingstype">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="Hellend" type="QString" value="hellend"/>
              </Option>
              <Option type="Map">
                <Option name="Vlak" type="QString" value="vlak"/>
              </Option>
              <Option type="Map">
                <Option name="Vlak, uitgestrekt" type="QString" value="vlak uitgestrekt"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="hellingspercentage">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option name="AllowNull" type="bool" value="true"/>
            <Option name="Max" type="double" value="100"/>
            <Option name="Min" type="double" value="0"/>
            <Option name="Precision" type="int" value="0"/>
            <Option name="Step" type="double" value="1"/>
            <Option name="Style" type="QString" value="SpinBox"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="berging_dak">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="putcode">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="leidingcode">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="gemengd_riool">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="hemelwaterriool">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="vgs_hemelwaterriool">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="infiltratievoorziening">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="niet_aangesloten">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias name="" index="0" field="id"/>
    <alias name="Laatste wijziging" index="1" field="laatste_wijziging"/>
    <alias name="BGT Identificatie" index="2" field="bgt_identificatie"/>
    <alias name="Type verharding" index="3" field="type_verharding"/>
    <alias name="Verhardingsgraad (%)" index="4" field="graad_verharding"/>
    <alias name="Hellingstype" index="5" field="hellingstype"/>
    <alias name="Helling (%)" index="6" field="hellingspercentage"/>
    <alias name="Berging dak (m2)" index="7" field="berging_dak"/>
    <alias name="Putcode" index="8" field="putcode"/>
    <alias name="Leidingcode" index="9" field="leidingcode"/>
    <alias name="Gemengd riool (%)" index="10" field="gemengd_riool"/>
    <alias name="Hemelwaterriool (%)" index="11" field="hemelwaterriool"/>
    <alias name="VGS Hemelwaterriool (%)" index="12" field="vgs_hemelwaterriool"/>
    <alias name="Infiltratievoorziening (%)" index="13" field="infiltratievoorziening"/>
    <alias name="Niet aangesloten (%)" index="14" field="niet_aangesloten"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" field="id" expression=""/>
    <default applyOnUpdate="0" field="laatste_wijziging" expression=""/>
    <default applyOnUpdate="0" field="bgt_identificatie" expression=""/>
    <default applyOnUpdate="0" field="type_verharding" expression=""/>
    <default applyOnUpdate="0" field="graad_verharding" expression=""/>
    <default applyOnUpdate="0" field="hellingstype" expression=""/>
    <default applyOnUpdate="0" field="hellingspercentage" expression=""/>
    <default applyOnUpdate="0" field="berging_dak" expression=""/>
    <default applyOnUpdate="0" field="putcode" expression=""/>
    <default applyOnUpdate="0" field="leidingcode" expression=""/>
    <default applyOnUpdate="0" field="gemengd_riool" expression=""/>
    <default applyOnUpdate="0" field="hemelwaterriool" expression=""/>
    <default applyOnUpdate="0" field="vgs_hemelwaterriool" expression=""/>
    <default applyOnUpdate="0" field="infiltratievoorziening" expression=""/>
    <default applyOnUpdate="0" field="niet_aangesloten" expression=""/>
  </defaults>
  <constraints>
    <constraint exp_strength="0" field="id" constraints="3" notnull_strength="1" unique_strength="1"/>
    <constraint exp_strength="0" field="laatste_wijziging" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="bgt_identificatie" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="type_verharding" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="graad_verharding" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="hellingstype" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="hellingspercentage" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="berging_dak" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="putcode" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="leidingcode" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="gemengd_riool" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="hemelwaterriool" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="vgs_hemelwaterriool" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="infiltratievoorziening" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="niet_aangesloten" constraints="0" notnull_strength="0" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="id" exp="" desc=""/>
    <constraint field="laatste_wijziging" exp="" desc=""/>
    <constraint field="bgt_identificatie" exp="" desc=""/>
    <constraint field="type_verharding" exp="" desc=""/>
    <constraint field="graad_verharding" exp="" desc=""/>
    <constraint field="hellingstype" exp="" desc=""/>
    <constraint field="hellingspercentage" exp="" desc=""/>
    <constraint field="berging_dak" exp="" desc=""/>
    <constraint field="putcode" exp="" desc=""/>
    <constraint field="leidingcode" exp="" desc=""/>
    <constraint field="gemengd_riool" exp="" desc=""/>
    <constraint field="hemelwaterriool" exp="" desc=""/>
    <constraint field="vgs_hemelwaterriool" exp="" desc=""/>
    <constraint field="infiltratievoorziening" exp="" desc=""/>
    <constraint field="niet_aangesloten" exp="" desc=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortExpression="&quot;gecheckt&quot;" actionWidgetStyle="dropDown" sortOrder="1">
    <columns>
      <column width="-1" type="actions" hidden="1"/>
      <column name="id" width="-1" type="field" hidden="0"/>
      <column name="laatste_wijziging" width="-1" type="field" hidden="0"/>
      <column name="bgt_identificatie" width="-1" type="field" hidden="0"/>
      <column name="type_verharding" width="-1" type="field" hidden="0"/>
      <column name="graad_verharding" width="-1" type="field" hidden="0"/>
      <column name="hellingstype" width="-1" type="field" hidden="0"/>
      <column name="hellingspercentage" width="-1" type="field" hidden="0"/>
      <column name="berging_dak" width="-1" type="field" hidden="0"/>
      <column name="putcode" width="-1" type="field" hidden="0"/>
      <column name="leidingcode" width="-1" type="field" hidden="0"/>
      <column name="gemengd_riool" width="-1" type="field" hidden="0"/>
      <column name="hemelwaterriool" width="-1" type="field" hidden="0"/>
      <column name="vgs_hemelwaterriool" width="-1" type="field" hidden="0"/>
      <column name="infiltratievoorziening" width="-1" type="field" hidden="0"/>
      <column name="niet_aangesloten" width="-1" type="field" hidden="0"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <storedexpressions/>
  <editform tolerant="1">L:/Extern/Projecten U (2019)/U0087 - Pilot samenwerken in AWK Rijnland/Gegevens/Layout</editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>tablayout</editorlayout>
  <attributeEditorForm>
    <attributeEditorContainer name="Vlakeigenschappen" showLabel="1" columnCount="1" visibilityExpressionEnabled="0" groupBox="1" visibilityExpression="">
      <attributeEditorField name="id" showLabel="1" index="0"/>
      <attributeEditorField name="laatste_wijziging" showLabel="1" index="1"/>
      <attributeEditorField name="bgt_identificatie" showLabel="1" index="2"/>
      <attributeEditorField name="type_verharding" showLabel="1" index="3"/>
      <attributeEditorField name="graad_verharding" showLabel="1" index="4"/>
      <attributeEditorField name="hellingstype" showLabel="1" index="5"/>
      <attributeEditorField name="hellingspercentage" showLabel="1" index="6"/>
    </attributeEditorContainer>
    <attributeEditorContainer name="Voert af naar..." showLabel="1" columnCount="1" visibilityExpressionEnabled="0" groupBox="1" visibilityExpression="">
      <attributeEditorField name="gemengd_riool" showLabel="1" index="10"/>
      <attributeEditorField name="hemelwaterriool" showLabel="1" index="11"/>
      <attributeEditorField name="vgs_hemelwaterriool" showLabel="1" index="12"/>
      <attributeEditorField name="infiltratievoorziening" showLabel="1" index="13"/>
      <attributeEditorField name="niet_aangesloten" showLabel="1" index="14"/>
      <attributeEditorField name="putcode" showLabel="1" index="8"/>
      <attributeEditorField name="leidingcode" showLabel="1" index="9"/>
    </attributeEditorContainer>
    <attributeEditorContainer name="Overzicht" showLabel="1" columnCount="1" visibilityExpressionEnabled="0" groupBox="1" visibilityExpression="">
      <attributeEditorHtmlElement name="Oppervlakken en afvoerpercentages" showLabel="1">&lt;p style="font-family:'MS Shell Dlg 2';font-size:10px">&#xd;
	&lt;b>&#xd;
		Totaal oppervlak: &#xd;
		&lt;script>&#xd;
			document.write(&#xd;
				expression.evaluate(&#xd;
					"format_number($area,2)"&#xd;
				)&#xd;
			);&#xd;
		&lt;/script>&#xd;
		 m&lt;sup>2&lt;/sup> &#xd;
	&lt;/b>&#xd;
	&lt;br>&#xd;
	&lt;br>&#xd;
&#xd;
&#xd;
&lt;table style="width:100%; font-size:10px">&#xd;
  &lt;tr>&#xd;
    &lt;td>&lt;b>Voert af naar&lt;/b>&lt;/td>&#xd;
    &lt;td>&lt;b>m&lt;sup>2&lt;/sup>&lt;/b>&lt;/td>&#xd;
    &lt;td>&lt;b>%&lt;/b>&lt;/td>&#xd;
  &lt;/tr>&#xd;
  &lt;tr>&#xd;
    &lt;td>Gemengd riool&lt;/td>&#xd;
    &lt;td>&#xd;
		&lt;script>&#xd;
			document.write(&#xd;
				expression.evaluate(&#xd;
					"format_number(\"gemengd_riool\"/100*$area,2)"&#xd;
				)&#xd;
			);&#xd;
		&lt;/script>&#xd;
	&lt;/td>&#xd;
    &lt;td>&#xd;
		&lt;script>&#xd;
			document.write(&#xd;
				expression.evaluate(&#xd;
					"\"gemengd_riool\""&#xd;
				)&#xd;
			);&#xd;
		&lt;/script>&#xd;
	&lt;/td>&#xd;
  &lt;/tr>&#xd;
  &lt;tr>&#xd;
    &lt;td>Hemelwaterriool&lt;/td>&#xd;
    &lt;td>&#xd;
		&lt;script>&#xd;
			document.write(&#xd;
				expression.evaluate(&#xd;
					"format_number(\"hemelwaterriool\"/100*$area,2)"&#xd;
				)&#xd;
			);&#xd;
		&lt;/script>	&#xd;
	&lt;/td>&#xd;
    &lt;td>&#xd;
		&lt;script>&#xd;
			document.write(&#xd;
				expression.evaluate(&#xd;
					"\"hemelwaterriool\""&#xd;
				)&#xd;
			);&#xd;
		&lt;/script>&#xd;
	&lt;/td>&#xd;
  &lt;/tr>&#xd;
  &lt;tr>&#xd;
    &lt;td>VGS Hemelwaterriool&lt;/td>&#xd;
    &lt;td>&#xd;
		&lt;script>&#xd;
			document.write(&#xd;
				expression.evaluate(&#xd;
					"format_number(\"vgs_hemelwaterriool\"/100*$area,2)"&#xd;
				)&#xd;
			);&#xd;
		&lt;/script>	&#xd;
	&lt;/td>&#xd;
    &lt;td>&#xd;
		&lt;script>&#xd;
			document.write(&#xd;
				expression.evaluate(&#xd;
					"\"vgs_hemelwaterriool\""&#xd;
				)&#xd;
			);&#xd;
		&lt;/script>&#xd;
	&lt;/td>&#xd;
  &lt;/tr>&#xd;
  &lt;tr>&#xd;
    &lt;td>Infiltratievoorziening&lt;/td>&#xd;
    &lt;td>&#xd;
		&lt;script>&#xd;
			document.write(&#xd;
				expression.evaluate(&#xd;
					"format_number(\"infiltratievoorziening\"/100*$area,2)"&#xd;
				)&#xd;
			);&#xd;
		&lt;/script>	&#xd;
	&lt;/td>&#xd;
    &lt;td>&#xd;
		&lt;script>&#xd;
			document.write(&#xd;
				expression.evaluate(&#xd;
					"\"infiltratievoorziening\""&#xd;
				)&#xd;
			);&#xd;
		&lt;/script>&#xd;
	&lt;/td>&#xd;
  &lt;/tr>&#xd;
  &lt;tr>&#xd;
    &lt;td>Niet aangesloten&lt;/td>&#xd;
    &lt;td>&#xd;
		&lt;script>&#xd;
			document.write(&#xd;
				expression.evaluate(&#xd;
					"format_number(\"niet_aangesloten\"/100*$area,2)"&#xd;
				)&#xd;
			);&#xd;
		&lt;/script>	&#xd;
	&lt;/td>&#xd;
    &lt;td>&#xd;
		&lt;script>&#xd;
			document.write(&#xd;
				expression.evaluate(&#xd;
					"\"niet_aangesloten\""&#xd;
				)&#xd;
			);&#xd;
		&lt;/script>&#xd;
	&lt;/td>&#xd;
  &lt;/tr>&#xd;
   &lt;tr>&#xd;
    &lt;td>&lt;b>TOTAAL&lt;/b>&lt;/td>&#xd;
    &lt;td>&#xd;
		&lt;b>&lt;script>&#xd;
			document.write(&#xd;
				expression.evaluate(&#xd;
					"format_number((gemengd_riool + hemelwaterriool + vgs_hemelwaterriool + infiltratievoorziening + niet_aangesloten) /100*$area,2)"&#xd;
				)&#xd;
			);&#xd;
		&lt;/script>&lt;/b>&#xd;
	&lt;/td>&#xd;
    &lt;td>&#xd;
		&lt;b>&lt;script>&#xd;
			document.write(&#xd;
				expression.evaluate(&#xd;
					"(gemengd_riool + hemelwaterriool + vgs_hemelwaterriool + infiltratievoorziening + niet_aangesloten)"&#xd;
				)&#xd;
			);&#xd;
		&lt;/script>&lt;/b>&#xd;
	&lt;/td>&#xd;
  &lt;/tr> &#xd;
&lt;/table>		&#xd;
&#xd;
&lt;/p>&#xd;
&#xd;
</attributeEditorHtmlElement>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field name="berging_dak" editable="1"/>
    <field name="bgt_identificatie" editable="1"/>
    <field name="dwa" editable="1"/>
    <field name="fid" editable="1"/>
    <field name="gecheckt" editable="1"/>
    <field name="gemengd" editable="1"/>
    <field name="gemengd_riool" editable="1"/>
    <field name="graad_verharding" editable="1"/>
    <field name="hellingspercentage" editable="1"/>
    <field name="hellingstype" editable="1"/>
    <field name="hemelwaterriool" editable="1"/>
    <field name="id" editable="1"/>
    <field name="infiltratievoorziening" editable="1"/>
    <field name="laatste_wijziging" editable="1"/>
    <field name="leidingcode" editable="1"/>
    <field name="lokaalid" editable="1"/>
    <field name="maaiveld" editable="1"/>
    <field name="niet_aangesloten" editable="1"/>
    <field name="nwrw_type_afstroming" editable="1"/>
    <field name="nwrw_type_afstroming_afwijkend" editable="1"/>
    <field name="nwrw_type_afstroming_voor_check" editable="1"/>
    <field name="openwater" editable="1"/>
    <field name="putcode" editable="1"/>
    <field name="rwa" editable="1"/>
    <field name="slope_p25" editable="1"/>
    <field name="type_verharding" editable="1"/>
    <field name="vgs_hemelwaterriool" editable="1"/>
    <field name="vlak" editable="1"/>
    <field name="vlak_type" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="berging_dak" labelOnTop="0"/>
    <field name="bgt_identificatie" labelOnTop="0"/>
    <field name="dwa" labelOnTop="0"/>
    <field name="fid" labelOnTop="0"/>
    <field name="gecheckt" labelOnTop="0"/>
    <field name="gemengd" labelOnTop="0"/>
    <field name="gemengd_riool" labelOnTop="0"/>
    <field name="graad_verharding" labelOnTop="0"/>
    <field name="hellingspercentage" labelOnTop="0"/>
    <field name="hellingstype" labelOnTop="0"/>
    <field name="hemelwaterriool" labelOnTop="0"/>
    <field name="id" labelOnTop="0"/>
    <field name="infiltratievoorziening" labelOnTop="0"/>
    <field name="laatste_wijziging" labelOnTop="0"/>
    <field name="leidingcode" labelOnTop="0"/>
    <field name="lokaalid" labelOnTop="0"/>
    <field name="maaiveld" labelOnTop="0"/>
    <field name="niet_aangesloten" labelOnTop="0"/>
    <field name="nwrw_type_afstroming" labelOnTop="0"/>
    <field name="nwrw_type_afstroming_afwijkend" labelOnTop="0"/>
    <field name="nwrw_type_afstroming_voor_check" labelOnTop="0"/>
    <field name="openwater" labelOnTop="0"/>
    <field name="putcode" labelOnTop="0"/>
    <field name="rwa" labelOnTop="0"/>
    <field name="slope_p25" labelOnTop="0"/>
    <field name="type_verharding" labelOnTop="0"/>
    <field name="vgs_hemelwaterriool" labelOnTop="0"/>
    <field name="vlak" labelOnTop="0"/>
    <field name="vlak_type" labelOnTop="0"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>"lokaalid"</previewExpression>
  <mapTip>display_name</mapTip>
  <layerGeometryType>2</layerGeometryType>
</qgis>
