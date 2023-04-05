<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis hasScaleBasedVisibilityFlag="0" readOnly="0" simplifyMaxScale="1" maxScale="0" simplifyLocal="1" minScale="100000000" version="3.16.4-Hannover" styleCategories="AllStyleCategories" simplifyAlgorithm="0" labelsEnabled="0" simplifyDrawingTol="1" simplifyDrawingHints="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <temporal fixedDuration="0" endField="" durationField="" mode="0" startExpression="" endExpression="" enabled="0" accumulate="0" startField="" durationUnit="min">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <renderer-v2 type="RuleRenderer" symbollevels="0" enableorderby="0" forceraster="0">
    <rules key="{8615500f-291b-43e9-9637-98f8858aa5b6}">
      <rule symbol="0" key="{e26fa1d6-5bbb-4001-b16f-2f0b34504877}" filter="&quot;hemelwaterriool&quot; = 100 and ( &quot;gemengd_riool&quot; + &quot;hemelwaterriool&quot; + &quot;vgs_hemelwaterriool&quot; + &quot;infiltratievoorziening&quot; + &quot;vuilwaterriool&quot; + &quot;open_water&quot; + &quot;maaiveld&quot;) = 100" label="Hemelwaterriool 100%"/>
      <rule symbol="1" key="{7be024ad-67fd-4f91-b658-70ec4c0e63fe}" filter=" &quot;vgs_hemelwaterriool&quot; = 100 and ( &quot;gemengd_riool&quot; + &quot;hemelwaterriool&quot; + &quot;vgs_hemelwaterriool&quot; + &quot;infiltratievoorziening&quot; + &quot;vuilwaterriool&quot; + &quot;open_water&quot; + &quot;maaiveld&quot;) = 100" label="VGS Hemelwaterriool 100%"/>
      <rule symbol="2" key="{3d292b4a-48ea-4954-9649-080da78561db}" filter=" &quot;gemengd_riool&quot; = 100 and ( &quot;gemengd_riool&quot; + &quot;hemelwaterriool&quot; + &quot;vgs_hemelwaterriool&quot; + &quot;infiltratievoorziening&quot; + &quot;vuilwaterriool&quot; + &quot;open_water&quot; + &quot;maaiveld&quot;) = 100" label="Gemengd 100%"/>
      <rule symbol="3" key="{a24c39d3-a09e-432d-a203-84441af42b85}" filter="( &quot;hemelwaterriool&quot; > 0 AND hemelwaterriool &lt; 100 AND  &quot;gemengd_riool&quot; > 0 AND gemengd_riool &lt; 100) and ( &quot;gemengd_riool&quot; + &quot;hemelwaterriool&quot; + &quot;vgs_hemelwaterriool&quot; + &quot;infiltratievoorziening&quot; + &quot;vuilwaterriool&quot; + &quot;open_water&quot; + &quot;maaiveld&quot;) = 100" label="Hemelwaterriool en Gemengd"/>
      <rule symbol="4" key="{49c2c107-4207-4f1f-87e7-cf522249dc51}" filter=" &quot;infiltratievoorziening&quot; = 100 and ( &quot;gemengd_riool&quot; + &quot;hemelwaterriool&quot; + &quot;vgs_hemelwaterriool&quot; + &quot;infiltratievoorziening&quot; + &quot;vuilwaterriool&quot; + &quot;open_water&quot; + &quot;maaiveld&quot;) = 100" label="Infiltratievoorziening 100%"/>
      <rule symbol="5" key="{cc14fa82-08f5-43e2-a7dd-68210119aed1}" filter=" &quot;maaiveld&quot;  = 100 and ( &quot;gemengd_riool&quot; + &quot;hemelwaterriool&quot; + &quot;vgs_hemelwaterriool&quot; + &quot;infiltratievoorziening&quot; + &quot;vuilwaterriool&quot; + &quot;open_water&quot; + &quot;maaiveld&quot;) = 100" label="Maaiveld 100%"/>
      <rule symbol="6" key="{9c50aa29-461b-4154-b33c-9806cd1ecc3a}" filter=" &quot;open_water&quot;  = 100 and ( &quot;gemengd_riool&quot; + &quot;hemelwaterriool&quot; + &quot;vgs_hemelwaterriool&quot; + &quot;infiltratievoorziening&quot; + &quot;vuilwaterriool&quot; + &quot;open_water&quot; + &quot;maaiveld&quot;) = 100" label="Open water 100%"/>
      <rule symbol="7" key="{6b9886b8-93e3-42cb-a57c-3330f89e86eb}" filter="ELSE" label="Overig (wel valide, totaal = 100)"/>
      <rule symbol="8" key="{20a36527-a20b-4bce-b851-6353175c759a}" filter="( &quot;gemengd_riool&quot; + &quot;hemelwaterriool&quot; + &quot;vgs_hemelwaterriool&quot; + &quot;infiltratievoorziening&quot; + &quot;vuilwaterriool&quot; + &quot;open_water&quot; + &quot;maaiveld&quot;) != 100" label="Overig (niet valide, totaal ≠ 100)"/>
    </rules>
    <symbols>
      <symbol type="fill" name="0" clip_to_extent="1" alpha="1" force_rhr="0">
        <layer locked="0" pass="0" enabled="1" class="SimpleFill">
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
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol type="fill" name="1" clip_to_extent="1" alpha="1" force_rhr="0">
        <layer locked="0" pass="0" enabled="1" class="SimpleFill">
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
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer locked="0" pass="0" enabled="1" class="PointPatternFill">
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
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol type="marker" name="@1@1" clip_to_extent="1" alpha="1" force_rhr="0">
            <layer locked="0" pass="0" enabled="1" class="SimpleMarker">
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
                  <Option type="QString" name="name" value=""/>
                  <Option name="properties"/>
                  <Option type="QString" name="type" value="collection"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol type="fill" name="2" clip_to_extent="1" alpha="1" force_rhr="0">
        <layer locked="0" pass="0" enabled="1" class="SimpleFill">
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
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol type="fill" name="3" clip_to_extent="1" alpha="1" force_rhr="0">
        <layer locked="0" pass="0" enabled="1" class="SimpleFill">
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
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer locked="0" pass="0" enabled="1" class="LinePatternFill">
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
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol type="line" name="@3@1" clip_to_extent="1" alpha="1" force_rhr="0">
            <layer locked="0" pass="0" enabled="1" class="SimpleLine">
              <prop v="0" k="align_dash_pattern"/>
              <prop v="square" k="capstyle"/>
              <prop v="5;2" k="customdash"/>
              <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
              <prop v="MM" k="customdash_unit"/>
              <prop v="0" k="dash_pattern_offset"/>
              <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
              <prop v="MM" k="dash_pattern_offset_unit"/>
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
              <prop v="0" k="tweak_dash_pattern_on_corners"/>
              <prop v="0" k="use_custom_dash"/>
              <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option type="QString" name="name" value=""/>
                  <Option name="properties"/>
                  <Option type="QString" name="type" value="collection"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol type="fill" name="4" clip_to_extent="1" alpha="1" force_rhr="0">
        <layer locked="0" pass="0" enabled="1" class="SimpleFill">
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
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol type="fill" name="5" clip_to_extent="1" alpha="1" force_rhr="0">
        <layer locked="0" pass="0" enabled="1" class="SimpleFill">
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
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol type="fill" name="6" clip_to_extent="1" alpha="1" force_rhr="0">
        <layer locked="0" pass="0" enabled="1" class="SimpleFill">
          <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
          <prop v="67,162,209,255" k="color"/>
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
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol type="fill" name="7" clip_to_extent="1" alpha="1" force_rhr="0">
        <layer locked="0" pass="0" enabled="1" class="SimpleFill">
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
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol type="fill" name="8" clip_to_extent="1" alpha="1" force_rhr="0">
        <layer locked="0" pass="0" enabled="1" class="SimpleFill">
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
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
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
    <DiagramCategory minScaleDenominator="0" barWidth="5" spacing="0" rotationOffset="270" minimumSize="0" spacingUnit="MM" showAxis="0" spacingUnitScale="3x:0,0,0,0,0,0" penColor="#000000" scaleBasedVisibility="0" maxScaleDenominator="1e+08" lineSizeScale="3x:0,0,0,0,0,0" sizeScale="3x:0,0,0,0,0,0" sizeType="MM" backgroundAlpha="255" diagramOrientation="Up" enabled="0" height="15" labelPlacementMethod="XHeight" opacity="1" width="15" penAlpha="255" backgroundColor="#ffffff" penWidth="0" scaleDependency="Area" direction="1" lineSizeType="MM">
      <fontProperties description="MS Shell Dlg 2,7.8,-1,5,50,0,0,0,0,0" style=""/>
      <attribute field="" color="#000000" label=""/>
      <axisSymbol>
        <symbol type="line" name="" clip_to_extent="1" alpha="1" force_rhr="0">
          <layer locked="0" pass="0" enabled="1" class="SimpleLine">
            <prop v="0" k="align_dash_pattern"/>
            <prop v="square" k="capstyle"/>
            <prop v="5;2" k="customdash"/>
            <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
            <prop v="MM" k="customdash_unit"/>
            <prop v="0" k="dash_pattern_offset"/>
            <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
            <prop v="MM" k="dash_pattern_offset_unit"/>
            <prop v="0" k="draw_inside_polygon"/>
            <prop v="bevel" k="joinstyle"/>
            <prop v="35,35,35,255" k="line_color"/>
            <prop v="solid" k="line_style"/>
            <prop v="0.26" k="line_width"/>
            <prop v="MM" k="line_width_unit"/>
            <prop v="0" k="offset"/>
            <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
            <prop v="MM" k="offset_unit"/>
            <prop v="0" k="ring_filter"/>
            <prop v="0" k="tweak_dash_pattern_on_corners"/>
            <prop v="0" k="use_custom_dash"/>
            <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
            <data_defined_properties>
              <Option type="Map">
                <Option type="QString" name="name" value=""/>
                <Option name="properties"/>
                <Option type="QString" name="type" value="collection"/>
              </Option>
            </data_defined_properties>
          </layer>
        </symbol>
      </axisSymbol>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings zIndex="0" placement="1" showAll="1" linePlacementFlags="18" obstacle="0" dist="0" priority="0">
    <properties>
      <Option type="Map">
        <Option type="QString" name="name" value=""/>
        <Option name="properties"/>
        <Option type="QString" name="type" value="collection"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions geometryPrecision="0" removeDuplicateNodes="0">
    <activeChecks/>
    <checkConfiguration type="Map">
      <Option type="Map" name="QgsGeometryGapCheck">
        <Option type="double" name="allowedGapsBuffer" value="0"/>
        <Option type="bool" name="allowedGapsEnabled" value="false"/>
        <Option type="QString" name="allowedGapsLayer" value=""/>
      </Option>
    </checkConfiguration>
  </geometryOptions>
  <legend type="default-vector"/>
  <referencedLayers/>
  <fieldConfiguration>
    <field name="id" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="laatste_wijziging" configurationFlags="None">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option type="bool" name="allow_null" value="true"/>
            <Option type="bool" name="calendar_popup" value="true"/>
            <Option type="QString" name="display_format" value="yyyy-MM-dd HH:mm:ss"/>
            <Option type="QString" name="field_format" value="yyyy-MM-dd HH:mm:ss"/>
            <Option type="bool" name="field_iso_format" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="bgt_identificatie" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="type_verharding" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option type="QString" name="Dak" value="dak"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="Gesloten verhard" value="gesloten verhard"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="Open verhard" value="open verhard"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="Onverhard" value="onverhard"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="Groen(blauw) dak" value="groen(blauw) dak"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="Waterpasserende verharding" value="waterpasserende verharding"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="Water" value="water"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="(Niet opgegeven)" value="{2839923C-8B7D-419E-B84B-CA2FE9B80EC7}"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="graad_verharding" configurationFlags="None">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option type="bool" name="AllowNull" value="true"/>
            <Option type="double" name="Max" value="100"/>
            <Option type="double" name="Min" value="0"/>
            <Option type="int" name="Precision" value="0"/>
            <Option type="double" name="Step" value="1"/>
            <Option type="QString" name="Style" value="SpinBox"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="hellingstype" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option type="QString" name="Hellend" value="hellend"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="Vlak" value="vlak"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="Vlak, uitgestrekt" value="vlak uitgestrekt"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="(Niet opgegeven)" value="{2839923C-8B7D-419E-B84B-CA2FE9B80EC7}"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="hellingspercentage" configurationFlags="None">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option type="bool" name="AllowNull" value="true"/>
            <Option type="double" name="Max" value="100"/>
            <Option type="double" name="Min" value="0"/>
            <Option type="int" name="Precision" value="0"/>
            <Option type="double" name="Step" value="1"/>
            <Option type="QString" name="Style" value="SpinBox"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="type_private_voorziening" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option type="QString" name="bovengronds met infiltratie" value="bovengronds met infiltratie"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="ondergronds met infiltratie" value="ondergronds met infiltratie"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="bovengronds zonder infiltratie" value="bovengronds zonder infiltratie"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="ondergronds zonder infiltratie" value="ondergronds zonder infiltratie"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="(Geen private voorziening)" value="{2839923C-8B7D-419E-B84B-CA2FE9B80EC7}"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="berging_private_voorziening" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="code_voorziening" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="putcode" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="leidingcode" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="gemengd_riool" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="hemelwaterriool" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="vgs_hemelwaterriool" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="vuilwaterriool" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="infiltratievoorziening" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="open_water" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="maaiveld" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias name="" field="id" index="0"/>
    <alias name="Laatste wijziging" field="laatste_wijziging" index="1"/>
    <alias name="BGT Identificatie" field="bgt_identificatie" index="2"/>
    <alias name="Type verharding" field="type_verharding" index="3"/>
    <alias name="Verhardingsgraad (%)" field="graad_verharding" index="4"/>
    <alias name="Hellingstype" field="hellingstype" index="5"/>
    <alias name="Helling (%)" field="hellingspercentage" index="6"/>
    <alias name="Type private voorziening" field="type_private_voorziening" index="7"/>
    <alias name="Berging private voorziening" field="berging_private_voorziening" index="8"/>
    <alias name="Code voorziening" field="code_voorziening" index="9"/>
    <alias name="Putcode" field="putcode" index="10"/>
    <alias name="Leidingcode" field="leidingcode" index="11"/>
    <alias name="Gemengd riool (%)" field="gemengd_riool" index="12"/>
    <alias name="Hemelwaterriool (%)" field="hemelwaterriool" index="13"/>
    <alias name="VGS Hemelwaterriool (%)" field="vgs_hemelwaterriool" index="14"/>
    <alias name="Vuilwaterriool (%)" field="vuilwaterriool" index="15"/>
    <alias name="Infiltratievoorziening (%)" field="infiltratievoorziening" index="16"/>
    <alias name="Open water (%)" field="open_water" index="17"/>
    <alias name="Maaiveld (%)" field="maaiveld" index="18"/>
  </aliases>
  <defaults>
    <default field="id" expression="" applyOnUpdate="0"/>
    <default field="laatste_wijziging" expression="" applyOnUpdate="0"/>
    <default field="bgt_identificatie" expression="" applyOnUpdate="0"/>
    <default field="type_verharding" expression="" applyOnUpdate="0"/>
    <default field="graad_verharding" expression="" applyOnUpdate="0"/>
    <default field="hellingstype" expression="" applyOnUpdate="0"/>
    <default field="hellingspercentage" expression="" applyOnUpdate="0"/>
    <default field="type_private_voorziening" expression="" applyOnUpdate="0"/>
    <default field="berging_private_voorziening" expression="" applyOnUpdate="0"/>
    <default field="code_voorziening" expression="" applyOnUpdate="0"/>
    <default field="putcode" expression="" applyOnUpdate="0"/>
    <default field="leidingcode" expression="" applyOnUpdate="0"/>
    <default field="gemengd_riool" expression="" applyOnUpdate="0"/>
    <default field="hemelwaterriool" expression="" applyOnUpdate="0"/>
    <default field="vgs_hemelwaterriool" expression="" applyOnUpdate="0"/>
    <default field="vuilwaterriool" expression="" applyOnUpdate="0"/>
    <default field="infiltratievoorziening" expression="" applyOnUpdate="0"/>
    <default field="open_water" expression="" applyOnUpdate="0"/>
    <default field="maaiveld" expression="" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint exp_strength="0" field="id" constraints="3" notnull_strength="1" unique_strength="1"/>
    <constraint exp_strength="0" field="laatste_wijziging" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="bgt_identificatie" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="type_verharding" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="graad_verharding" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="hellingstype" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="hellingspercentage" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="type_private_voorziening" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="berging_private_voorziening" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="code_voorziening" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="putcode" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="leidingcode" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="gemengd_riool" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="hemelwaterriool" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="vgs_hemelwaterriool" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="vuilwaterriool" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="infiltratievoorziening" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="open_water" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="maaiveld" constraints="0" notnull_strength="0" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" field="id" exp=""/>
    <constraint desc="" field="laatste_wijziging" exp=""/>
    <constraint desc="" field="bgt_identificatie" exp=""/>
    <constraint desc="" field="type_verharding" exp=""/>
    <constraint desc="" field="graad_verharding" exp=""/>
    <constraint desc="" field="hellingstype" exp=""/>
    <constraint desc="" field="hellingspercentage" exp=""/>
    <constraint desc="" field="type_private_voorziening" exp=""/>
    <constraint desc="" field="berging_private_voorziening" exp=""/>
    <constraint desc="" field="code_voorziening" exp=""/>
    <constraint desc="" field="putcode" exp=""/>
    <constraint desc="" field="leidingcode" exp=""/>
    <constraint desc="" field="gemengd_riool" exp=""/>
    <constraint desc="" field="hemelwaterriool" exp=""/>
    <constraint desc="" field="vgs_hemelwaterriool" exp=""/>
    <constraint desc="" field="vuilwaterriool" exp=""/>
    <constraint desc="" field="infiltratievoorziening" exp=""/>
    <constraint desc="" field="open_water" exp=""/>
    <constraint desc="" field="maaiveld" exp=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortOrder="1" sortExpression="&quot;gecheckt&quot;" actionWidgetStyle="dropDown">
    <columns>
      <column width="-1" type="actions" hidden="1"/>
      <column width="-1" type="field" name="id" hidden="0"/>
      <column width="-1" type="field" name="laatste_wijziging" hidden="0"/>
      <column width="-1" type="field" name="bgt_identificatie" hidden="0"/>
      <column width="-1" type="field" name="type_verharding" hidden="0"/>
      <column width="-1" type="field" name="graad_verharding" hidden="0"/>
      <column width="-1" type="field" name="hellingstype" hidden="0"/>
      <column width="-1" type="field" name="hellingspercentage" hidden="0"/>
      <column width="-1" type="field" name="putcode" hidden="0"/>
      <column width="-1" type="field" name="leidingcode" hidden="0"/>
      <column width="-1" type="field" name="gemengd_riool" hidden="0"/>
      <column width="-1" type="field" name="hemelwaterriool" hidden="0"/>
      <column width="-1" type="field" name="vgs_hemelwaterriool" hidden="0"/>
      <column width="-1" type="field" name="infiltratievoorziening" hidden="0"/>
      <column width="-1" type="field" name="type_private_voorziening" hidden="0"/>
      <column width="-1" type="field" name="berging_private_voorziening" hidden="0"/>
      <column width="-1" type="field" name="code_voorziening" hidden="0"/>
      <column width="-1" type="field" name="vuilwaterriool" hidden="0"/>
      <column width="-1" type="field" name="open_water" hidden="0"/>
      <column width="-1" type="field" name="maaiveld" hidden="0"/>
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
    <attributeEditorContainer showLabel="1" groupBox="1" visibilityExpressionEnabled="0" name="Vlakeigenschappen" visibilityExpression="" columnCount="1">
      <attributeEditorField showLabel="1" name="id" index="0"/>
      <attributeEditorField showLabel="1" name="laatste_wijziging" index="1"/>
      <attributeEditorField showLabel="1" name="bgt_identificatie" index="2"/>
      <attributeEditorField showLabel="1" name="type_verharding" index="3"/>
      <attributeEditorField showLabel="1" name="graad_verharding" index="4"/>
      <attributeEditorField showLabel="1" name="hellingstype" index="5"/>
      <attributeEditorField showLabel="1" name="hellingspercentage" index="6"/>
      <attributeEditorField showLabel="1" name="type_private_voorziening" index="7"/>
      <attributeEditorField showLabel="1" name="berging_private_voorziening" index="8"/>
    </attributeEditorContainer>
    <attributeEditorContainer showLabel="1" groupBox="1" visibilityExpressionEnabled="0" name="Voert af naar..." visibilityExpression="" columnCount="1">
      <attributeEditorField showLabel="1" name="gemengd_riool" index="12"/>
      <attributeEditorField showLabel="1" name="hemelwaterriool" index="13"/>
      <attributeEditorField showLabel="1" name="vgs_hemelwaterriool" index="14"/>
      <attributeEditorField showLabel="1" name="vuilwaterriool" index="15"/>
      <attributeEditorField showLabel="1" name="infiltratievoorziening" index="16"/>
      <attributeEditorField showLabel="1" name="open_water" index="17"/>
      <attributeEditorField showLabel="1" name="maaiveld" index="18"/>
      <attributeEditorField showLabel="1" name="putcode" index="10"/>
      <attributeEditorField showLabel="1" name="leidingcode" index="11"/>
      <attributeEditorField showLabel="1" name="code_voorziening" index="9"/>
    </attributeEditorContainer>
    <attributeEditorContainer showLabel="1" groupBox="1" visibilityExpressionEnabled="0" name="Overzicht" visibilityExpression="" columnCount="1">
      <attributeEditorHtmlElement showLabel="1" name="Oppervlakken en afvoerpercentages">&lt;p style="font-family:'MS Shell Dlg 2';font-size:10px">    &lt;b>        Totaal oppervlak:         &lt;script>            document.write(                expression.evaluate(                    "format_number($area,2)"                )            );        &lt;/script>         m&lt;sup>2&lt;/sup>     &lt;/b>    &lt;br>    &lt;br>&lt;table style="width:100%; font-size:10px">  &lt;tr>    &lt;td>&lt;b>Voert af naar&lt;/b>&lt;/td>    &lt;td>&lt;b>m&lt;sup>2&lt;/sup>&lt;/b>&lt;/td>    &lt;td>&lt;b>%&lt;/b>&lt;/td>  &lt;/tr>  &lt;tr>    &lt;td>Gemengd riool&lt;/td>    &lt;td>        &lt;script>            document.write(                expression.evaluate(                    "format_number(\"gemengd_riool\"/100*$area,2)"                )            );        &lt;/script>    &lt;/td>    &lt;td>        &lt;script>            document.write(                expression.evaluate(                    "\"gemengd_riool\""                )            );        &lt;/script>    &lt;/td>  &lt;/tr>  &lt;tr>    &lt;td>Hemelwaterriool&lt;/td>    &lt;td>        &lt;script>            document.write(                expression.evaluate(                    "format_number(\"hemelwaterriool\"/100*$area,2)"                )            );        &lt;/script>        &lt;/td>    &lt;td>        &lt;script>            document.write(                expression.evaluate(                    "\"hemelwaterriool\""                )            );        &lt;/script>    &lt;/td>  &lt;/tr>  &lt;tr>    &lt;td>VGS Hemelwaterriool&lt;/td>    &lt;td>        &lt;script>            document.write(                expression.evaluate(                    "format_number(\"vgs_hemelwaterriool\"/100*$area,2)"                )            );        &lt;/script>        &lt;/td>    &lt;td>        &lt;script>            document.write(                expression.evaluate(                    "\"vgs_hemelwaterriool\""                )            );        &lt;/script>    &lt;/td>  &lt;/tr>    &lt;tr>    &lt;td>Vuilwaterriool&lt;/td>    &lt;td>        &lt;script>            document.write(                expression.evaluate(                    "format_number(\"vuilwaterriool\"/100*$area,2)"                )            );        &lt;/script>        &lt;/td>    &lt;td>        &lt;script>            document.write(                expression.evaluate(                    "\"vuilwaterriool\""                )            );        &lt;/script>    &lt;/td>  &lt;/tr>  &lt;tr>    &lt;td>Infiltratievoorziening&lt;/td>    &lt;td>        &lt;script>            document.write(                expression.evaluate(                    "format_number(\"infiltratievoorziening\"/100*$area,2)"                )            );        &lt;/script>        &lt;/td>    &lt;td>        &lt;script>            document.write(                expression.evaluate(                    "\"infiltratievoorziening\""                )            );        &lt;/script>    &lt;/td>  &lt;/tr>  &lt;tr>    &lt;td>Open water&lt;/td>    &lt;td>        &lt;script>            document.write(                expression.evaluate(                    "format_number(\"open_water\"/100*$area,2)"                )            );        &lt;/script>        &lt;/td>    &lt;td>        &lt;script>            document.write(                expression.evaluate(                    "\"open_water\""                )            );        &lt;/script>    &lt;/td>  &lt;/tr>    &lt;tr>    &lt;td>Maaiveld&lt;/td>    &lt;td>        &lt;script>            document.write(                expression.evaluate(                    "format_number(\"maaiveld\"/100*$area,2)"                )            );        &lt;/script>        &lt;/td>    &lt;td>        &lt;script>            document.write(                expression.evaluate(                    "\"maaiveld\""                )            );        &lt;/script>    &lt;/td>  &lt;/tr>   &lt;tr>    &lt;td>&lt;b>TOTAAL&lt;/b>&lt;/td>    &lt;td>        &lt;b>&lt;script>            document.write(                expression.evaluate(                    "format_number((gemengd_riool + hemelwaterriool + vgs_hemelwaterriool + infiltratievoorziening + vuilwaterriool + open_water + maaiveld) /100*$area,2)"                )            );        &lt;/script>&lt;/b>    &lt;/td>    &lt;td>        &lt;b>&lt;script>            document.write(                expression.evaluate(                    "(gemengd_riool + hemelwaterriool + vgs_hemelwaterriool + infiltratievoorziening + vuilwaterriool + open_water + maaiveld)"                )            );        &lt;/script>&lt;/b>    &lt;/td>  &lt;/tr> &lt;/table>        &lt;/p></attributeEditorHtmlElement>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="berging_dak"/>
    <field editable="1" name="berging_private_voorziening"/>
    <field editable="1" name="bgt_identificatie"/>
    <field editable="1" name="code_voorziening"/>
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
    <field editable="1" name="open_water"/>
    <field editable="1" name="openwater"/>
    <field editable="1" name="putcode"/>
    <field editable="1" name="rwa"/>
    <field editable="1" name="slope_p25"/>
    <field editable="1" name="type_private_voorziening"/>
    <field editable="1" name="type_verharding"/>
    <field editable="1" name="vgs_hemelwaterriool"/>
    <field editable="1" name="vlak"/>
    <field editable="1" name="vlak_type"/>
    <field editable="1" name="vuilwaterriool"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="berging_dak"/>
    <field labelOnTop="0" name="berging_private_voorziening"/>
    <field labelOnTop="0" name="bgt_identificatie"/>
    <field labelOnTop="0" name="code_voorziening"/>
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
    <field labelOnTop="0" name="open_water"/>
    <field labelOnTop="0" name="openwater"/>
    <field labelOnTop="0" name="putcode"/>
    <field labelOnTop="0" name="rwa"/>
    <field labelOnTop="0" name="slope_p25"/>
    <field labelOnTop="0" name="type_private_voorziening"/>
    <field labelOnTop="0" name="type_verharding"/>
    <field labelOnTop="0" name="vgs_hemelwaterriool"/>
    <field labelOnTop="0" name="vlak"/>
    <field labelOnTop="0" name="vlak_type"/>
    <field labelOnTop="0" name="vuilwaterriool"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"lokaalid"</previewExpression>
  <mapTip>display_name</mapTip>
  <layerGeometryType>2</layerGeometryType>
</qgis>
