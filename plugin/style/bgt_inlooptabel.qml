<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.10.10-A Coruña" readOnly="0" simplifyDrawingTol="1" simplifyLocal="1" simplifyDrawingHints="0" styleCategories="AllStyleCategories" simplifyMaxScale="1" simplifyAlgorithm="0" hasScaleBasedVisibilityFlag="0" minScale="1e+08" maxScale="0" labelsEnabled="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 forceraster="0" symbollevels="0" enableorderby="0" type="RuleRenderer">
    <rules key="{8615500f-291b-43e9-9637-98f8858aa5b6}">
      <rule filter=" &quot;hemelwaterriool&quot; = 100 and ( &quot;gemengd_riool&quot; + &quot;hemelwaterriool&quot; + &quot;vgs_hemelwaterriool&quot; + &quot;infiltratievoorziening&quot; + &quot;niet_aangesloten&quot; ) = 100" label="Hemelwaterriool 100%" key="{e26fa1d6-5bbb-4001-b16f-2f0b34504877}" symbol="0"/>
      <rule filter=" &quot;vgs_hemelwaterriool&quot; = 100 and ( &quot;gemengd_riool&quot; + &quot;hemelwaterriool&quot; + &quot;vgs_hemelwaterriool&quot; + &quot;infiltratievoorziening&quot; + &quot;niet_aangesloten&quot; ) = 100" label="VGS Hemelwaterriool 100%" key="{7be024ad-67fd-4f91-b658-70ec4c0e63fe}" symbol="1"/>
      <rule filter=" &quot;gemengd_riool&quot; = 100 and ( &quot;gemengd_riool&quot; + &quot;hemelwaterriool&quot; + &quot;vgs_hemelwaterriool&quot; + &quot;infiltratievoorziening&quot; + &quot;niet_aangesloten&quot; ) = 100" label="Gemengd 100%" key="{3d292b4a-48ea-4954-9649-080da78561db}" symbol="2"/>
      <rule filter="( &quot;hemelwaterriool&quot; > 0 AND hemelwaterriool &lt; 100 AND  &quot;gemengd_riool&quot; > 0 AND gemengd_riool &lt; 100) and ( &quot;gemengd_riool&quot; + &quot;hemelwaterriool&quot; + &quot;vgs_hemelwaterriool&quot; + &quot;infiltratievoorziening&quot; + &quot;niet_aangesloten&quot; ) = 100" label="Hemelwaterriool en Gemengd" key="{a24c39d3-a09e-432d-a203-84441af42b85}" symbol="3"/>
      <rule filter=" &quot;niet_aangesloten&quot;  = 100 and ( &quot;gemengd_riool&quot; + &quot;hemelwaterriool&quot; + &quot;vgs_hemelwaterriool&quot; + &quot;infiltratievoorziening&quot; + &quot;niet_aangesloten&quot; ) = 100" label="Niet aangesloten 100%" key="{3d88a01b-5ca4-40e3-b4d3-935db7458ba6}" symbol="4"/>
      <rule filter=" &quot;infiltratievoorziening&quot; = 100 and ( &quot;gemengd_riool&quot; + &quot;hemelwaterriool&quot; + &quot;vgs_hemelwaterriool&quot; + &quot;infiltratievoorziening&quot; + &quot;niet_aangesloten&quot; ) = 100" label="Infiltratievoorziening 100%" key="{49c2c107-4207-4f1f-87e7-cf522249dc51}" symbol="5"/>
      <rule filter="ELSE" label="Overig (wel valide, totaal = 100)" key="{6b9886b8-93e3-42cb-a57c-3330f89e86eb}" symbol="6"/>
      <rule filter=" ( &quot;gemengd_riool&quot; + &quot;hemelwaterriool&quot; + &quot;vgs_hemelwaterriool&quot; + &quot;infiltratievoorziening&quot; + &quot;niet_aangesloten&quot; ) != 100" label="Overig (niet valide, totaal ≠ 100)" key="{20a36527-a20b-4bce-b851-6353175c759a}" symbol="7"/>
    </rules>
    <symbols>
      <symbol clip_to_extent="1" name="0" type="fill" alpha="1" force_rhr="0">
        <layer locked="0" class="SimpleFill" pass="0" enabled="1">
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="165,183,255,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="255,255,255,26"/>
          <prop k="outline_style" v="no"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" name="1" type="fill" alpha="1" force_rhr="0">
        <layer locked="0" class="SimpleFill" pass="0" enabled="1">
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="165,183,255,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="255,255,255,26"/>
          <prop k="outline_style" v="no"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer locked="0" class="PointPatternFill" pass="0" enabled="1">
          <prop k="displacement_x" v="0"/>
          <prop k="displacement_x_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="displacement_x_unit" v="MM"/>
          <prop k="displacement_y" v="0"/>
          <prop k="displacement_y_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="displacement_y_unit" v="MM"/>
          <prop k="distance_x" v="5"/>
          <prop k="distance_x_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="distance_x_unit" v="MM"/>
          <prop k="distance_y" v="5"/>
          <prop k="distance_y_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="distance_y_unit" v="MM"/>
          <prop k="offset_x" v="0"/>
          <prop k="offset_x_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_x_unit" v="MM"/>
          <prop k="offset_y" v="0"/>
          <prop k="offset_y_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_y_unit" v="MM"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol clip_to_extent="1" name="@1@1" type="marker" alpha="1" force_rhr="0">
            <layer locked="0" class="SimpleMarker" pass="0" enabled="1">
              <prop k="angle" v="0"/>
              <prop k="color" v="149,165,230,255"/>
              <prop k="horizontal_anchor_point" v="1"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="name" v="cross_fill"/>
              <prop k="offset" v="0,0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="outline_color" v="35,35,35,0"/>
              <prop k="outline_style" v="solid"/>
              <prop k="outline_width" v="0"/>
              <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="outline_width_unit" v="MM"/>
              <prop k="scale_method" v="diameter"/>
              <prop k="size" v="2"/>
              <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="size_unit" v="MM"/>
              <prop k="vertical_anchor_point" v="1"/>
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
      <symbol clip_to_extent="1" name="2" type="fill" alpha="1" force_rhr="0">
        <layer locked="0" class="SimpleFill" pass="0" enabled="1">
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="255,213,181,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="255,255,255,26"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" name="3" type="fill" alpha="1" force_rhr="0">
        <layer locked="0" class="SimpleFill" pass="0" enabled="1">
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="255,213,181,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="255,255,255,128"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.26"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer locked="0" class="LinePatternFill" pass="0" enabled="1">
          <prop k="angle" v="45"/>
          <prop k="color" v="207,20,192,255"/>
          <prop k="distance" v="2"/>
          <prop k="distance_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="distance_unit" v="MM"/>
          <prop k="line_width" v="0.5"/>
          <prop k="line_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol clip_to_extent="1" name="@3@1" type="line" alpha="1" force_rhr="0">
            <layer locked="0" class="SimpleLine" pass="0" enabled="1">
              <prop k="capstyle" v="square"/>
              <prop k="customdash" v="5;2"/>
              <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="customdash_unit" v="MM"/>
              <prop k="draw_inside_polygon" v="0"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="line_color" v="165,183,255,255"/>
              <prop k="line_style" v="solid"/>
              <prop k="line_width" v="1"/>
              <prop k="line_width_unit" v="MM"/>
              <prop k="offset" v="0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="ring_filter" v="0"/>
              <prop k="use_custom_dash" v="0"/>
              <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
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
      <symbol clip_to_extent="1" name="4" type="fill" alpha="1" force_rhr="0">
        <layer locked="0" class="SimpleFill" pass="0" enabled="1">
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="167,255,159,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="35,35,35,255"/>
          <prop k="outline_style" v="no"/>
          <prop k="outline_width" v="0.26"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" name="5" type="fill" alpha="1" force_rhr="0">
        <layer locked="0" class="SimpleFill" pass="0" enabled="1">
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="163,205,185,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="114,133,132,255"/>
          <prop k="outline_style" v="no"/>
          <prop k="outline_width" v="0.26"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" name="6" type="fill" alpha="1" force_rhr="0">
        <layer locked="0" class="SimpleFill" pass="0" enabled="1">
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="201,201,201,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="255,255,255,26"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol clip_to_extent="1" name="7" type="fill" alpha="1" force_rhr="0">
        <layer locked="0" class="SimpleFill" pass="0" enabled="1">
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="255,1,1,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="255,255,255,26"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="style" v="solid"/>
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
    <property key="dualview/previewExpressions" value="&quot;lokaalid&quot;"/>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Histogram">
    <DiagramCategory lineSizeScale="3x:0,0,0,0,0,0" minScaleDenominator="0" enabled="0" lineSizeType="MM" scaleBasedVisibility="0" minimumSize="0" width="15" barWidth="5" rotationOffset="270" scaleDependency="Area" labelPlacementMethod="XHeight" penColor="#000000" sizeScale="3x:0,0,0,0,0,0" opacity="1" height="15" diagramOrientation="Up" backgroundAlpha="255" backgroundColor="#ffffff" maxScaleDenominator="1e+08" penAlpha="255" sizeType="MM" penWidth="0">
      <fontProperties style="" description="MS Shell Dlg 2,7.8,-1,5,50,0,0,0,0,0"/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings linePlacementFlags="18" showAll="1" priority="0" obstacle="0" zIndex="0" placement="1" dist="0">
    <properties>
      <Option type="Map">
        <Option name="name" type="QString" value=""/>
        <Option name="properties"/>
        <Option name="type" type="QString" value="collection"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions geometryPrecision="0" removeDuplicateNodes="0">
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
    <field name="fid">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
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
    <alias field="fid" name="" index="0"/>
    <alias field="id" name="" index="1"/>
    <alias field="laatste_wijziging" name="Laatste wijziging" index="2"/>
    <alias field="bgt_identificatie" name="BGT Identificatie" index="3"/>
    <alias field="type_verharding" name="Type verharding" index="4"/>
    <alias field="graad_verharding" name="Verhardingsgraad (%)" index="5"/>
    <alias field="hellingstype" name="Hellingstype" index="6"/>
    <alias field="hellingspercentage" name="Helling (%)" index="7"/>
    <alias field="berging_dak" name="Berging dak (m2)" index="8"/>
    <alias field="putcode" name="Putcode" index="9"/>
    <alias field="leidingcode" name="Leidingcode" index="10"/>
    <alias field="gemengd_riool" name="Gemengd riool (%)" index="11"/>
    <alias field="hemelwaterriool" name="Hemelwaterriool (%)" index="12"/>
    <alias field="vgs_hemelwaterriool" name="VGS Hemelwaterriool (%)" index="13"/>
    <alias field="infiltratievoorziening" name="Infiltratievoorziening (%)" index="14"/>
    <alias field="niet_aangesloten" name="Niet aangesloten (%)" index="15"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default field="fid" expression="" applyOnUpdate="0"/>
    <default field="id" expression="" applyOnUpdate="0"/>
    <default field="laatste_wijziging" expression="" applyOnUpdate="0"/>
    <default field="bgt_identificatie" expression="" applyOnUpdate="0"/>
    <default field="type_verharding" expression="" applyOnUpdate="0"/>
    <default field="graad_verharding" expression="" applyOnUpdate="0"/>
    <default field="hellingstype" expression="" applyOnUpdate="0"/>
    <default field="hellingspercentage" expression="" applyOnUpdate="0"/>
    <default field="berging_dak" expression="" applyOnUpdate="0"/>
    <default field="putcode" expression="" applyOnUpdate="0"/>
    <default field="leidingcode" expression="" applyOnUpdate="0"/>
    <default field="gemengd_riool" expression="" applyOnUpdate="0"/>
    <default field="hemelwaterriool" expression="" applyOnUpdate="0"/>
    <default field="vgs_hemelwaterriool" expression="" applyOnUpdate="0"/>
    <default field="infiltratievoorziening" expression="" applyOnUpdate="0"/>
    <default field="niet_aangesloten" expression="" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint field="fid" constraints="3" unique_strength="1" notnull_strength="1" exp_strength="0"/>
    <constraint field="id" constraints="3" unique_strength="1" notnull_strength="1" exp_strength="0"/>
    <constraint field="laatste_wijziging" constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="bgt_identificatie" constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="type_verharding" constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="graad_verharding" constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="hellingstype" constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="hellingspercentage" constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="berging_dak" constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="putcode" constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="leidingcode" constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="gemengd_riool" constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="hemelwaterriool" constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="vgs_hemelwaterriool" constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="infiltratievoorziening" constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="niet_aangesloten" constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="fid" desc="" exp=""/>
    <constraint field="id" desc="" exp=""/>
    <constraint field="laatste_wijziging" desc="" exp=""/>
    <constraint field="bgt_identificatie" desc="" exp=""/>
    <constraint field="type_verharding" desc="" exp=""/>
    <constraint field="graad_verharding" desc="" exp=""/>
    <constraint field="hellingstype" desc="" exp=""/>
    <constraint field="hellingspercentage" desc="" exp=""/>
    <constraint field="berging_dak" desc="" exp=""/>
    <constraint field="putcode" desc="" exp=""/>
    <constraint field="leidingcode" desc="" exp=""/>
    <constraint field="gemengd_riool" desc="" exp=""/>
    <constraint field="hemelwaterriool" desc="" exp=""/>
    <constraint field="vgs_hemelwaterriool" desc="" exp=""/>
    <constraint field="infiltratievoorziening" desc="" exp=""/>
    <constraint field="niet_aangesloten" desc="" exp=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortOrder="1" sortExpression="&quot;gecheckt&quot;" actionWidgetStyle="dropDown">
    <columns>
      <column hidden="1" type="actions" width="-1"/>
      <column name="id" hidden="0" type="field" width="-1"/>
      <column name="laatste_wijziging" hidden="0" type="field" width="-1"/>
      <column name="bgt_identificatie" hidden="0" type="field" width="-1"/>
      <column name="type_verharding" hidden="0" type="field" width="-1"/>
      <column name="graad_verharding" hidden="0" type="field" width="-1"/>
      <column name="hellingstype" hidden="0" type="field" width="-1"/>
      <column name="hellingspercentage" hidden="0" type="field" width="-1"/>
      <column name="berging_dak" hidden="0" type="field" width="-1"/>
      <column name="putcode" hidden="0" type="field" width="-1"/>
      <column name="leidingcode" hidden="0" type="field" width="-1"/>
      <column name="gemengd_riool" hidden="0" type="field" width="-1"/>
      <column name="hemelwaterriool" hidden="0" type="field" width="-1"/>
      <column name="vgs_hemelwaterriool" hidden="0" type="field" width="-1"/>
      <column name="infiltratievoorziening" hidden="0" type="field" width="-1"/>
      <column name="niet_aangesloten" hidden="0" type="field" width="-1"/>
      <column name="fid" hidden="0" type="field" width="-1"/>
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
    <attributeEditorContainer columnCount="1" name="Vlakeigenschappen" groupBox="1" visibilityExpression="" visibilityExpressionEnabled="0" showLabel="1">
      <attributeEditorField name="id" index="1" showLabel="1"/>
      <attributeEditorField name="laatste_wijziging" index="2" showLabel="1"/>
      <attributeEditorField name="bgt_identificatie" index="3" showLabel="1"/>
      <attributeEditorField name="type_verharding" index="4" showLabel="1"/>
      <attributeEditorField name="graad_verharding" index="5" showLabel="1"/>
      <attributeEditorField name="hellingstype" index="6" showLabel="1"/>
      <attributeEditorField name="hellingspercentage" index="7" showLabel="1"/>
    </attributeEditorContainer>
    <attributeEditorContainer columnCount="1" name="Voert af naar..." groupBox="1" visibilityExpression="" visibilityExpressionEnabled="0" showLabel="1">
      <attributeEditorField name="gemengd_riool" index="11" showLabel="1"/>
      <attributeEditorField name="hemelwaterriool" index="12" showLabel="1"/>
      <attributeEditorField name="vgs_hemelwaterriool" index="13" showLabel="1"/>
      <attributeEditorField name="infiltratievoorziening" index="14" showLabel="1"/>
      <attributeEditorField name="niet_aangesloten" index="15" showLabel="1"/>
      <attributeEditorField name="putcode" index="9" showLabel="1"/>
      <attributeEditorField name="leidingcode" index="10" showLabel="1"/>
    </attributeEditorContainer>
    <attributeEditorContainer columnCount="1" name="Overzicht" groupBox="1" visibilityExpression="" visibilityExpressionEnabled="0" showLabel="1">
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
    <field editable="1" name="berging_dak"/>
    <field editable="1" name="bgt_identificatie"/>
    <field editable="1" name="dwa"/>
    <field editable="1" name="fid"/>
    <field editable="1" name="gecheckt"/>
    <field editable="1" name="gemengd"/>
    <field editable="1" name="gemengd_riool"/>
    <field editable="1" name="graad_verharding"/>
    <field editable="1" name="hellingspercentage"/>
    <field editable="1" name="hellingstype"/>
    <field editable="1" name="hemelwaterriool"/>
    <field editable="1" name="id"/>
    <field editable="1" name="infiltratievoorziening"/>
    <field editable="1" name="laatste_wijziging"/>
    <field editable="1" name="leidingcode"/>
    <field editable="1" name="lokaalid"/>
    <field editable="1" name="maaiveld"/>
    <field editable="1" name="niet_aangesloten"/>
    <field editable="1" name="nwrw_type_afstroming"/>
    <field editable="1" name="nwrw_type_afstroming_afwijkend"/>
    <field editable="1" name="nwrw_type_afstroming_voor_check"/>
    <field editable="1" name="openwater"/>
    <field editable="1" name="putcode"/>
    <field editable="1" name="rwa"/>
    <field editable="1" name="slope_p25"/>
    <field editable="1" name="type_verharding"/>
    <field editable="1" name="vgs_hemelwaterriool"/>
    <field editable="1" name="vlak"/>
    <field editable="1" name="vlak_type"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="berging_dak"/>
    <field labelOnTop="0" name="bgt_identificatie"/>
    <field labelOnTop="0" name="dwa"/>
    <field labelOnTop="0" name="fid"/>
    <field labelOnTop="0" name="gecheckt"/>
    <field labelOnTop="0" name="gemengd"/>
    <field labelOnTop="0" name="gemengd_riool"/>
    <field labelOnTop="0" name="graad_verharding"/>
    <field labelOnTop="0" name="hellingspercentage"/>
    <field labelOnTop="0" name="hellingstype"/>
    <field labelOnTop="0" name="hemelwaterriool"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="infiltratievoorziening"/>
    <field labelOnTop="0" name="laatste_wijziging"/>
    <field labelOnTop="0" name="leidingcode"/>
    <field labelOnTop="0" name="lokaalid"/>
    <field labelOnTop="0" name="maaiveld"/>
    <field labelOnTop="0" name="niet_aangesloten"/>
    <field labelOnTop="0" name="nwrw_type_afstroming"/>
    <field labelOnTop="0" name="nwrw_type_afstroming_afwijkend"/>
    <field labelOnTop="0" name="nwrw_type_afstroming_voor_check"/>
    <field labelOnTop="0" name="openwater"/>
    <field labelOnTop="0" name="putcode"/>
    <field labelOnTop="0" name="rwa"/>
    <field labelOnTop="0" name="slope_p25"/>
    <field labelOnTop="0" name="type_verharding"/>
    <field labelOnTop="0" name="vgs_hemelwaterriool"/>
    <field labelOnTop="0" name="vlak"/>
    <field labelOnTop="0" name="vlak_type"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>"lokaalid"</previewExpression>
  <mapTip>display_name</mapTip>
  <layerGeometryType>2</layerGeometryType>
</qgis>
