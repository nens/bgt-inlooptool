#from osgeo import ogr, osr
import osr 
import ogr

ogr.UseExceptions()

SURFACE_TYPE_PAND = 'pand'
SURFACE_TYPE_WEGDEEL = 'wegdeel'
SURFACE_TYPE_ONDERSTEUNENDWEGDEEL = 'ondersteunendwegdeel'
SURFACE_TYPE_BEGROEIDTERREINDEEL = 'begroeidterreindeel'
SURFACE_TYPE_ONBEGROEIDTERREINDEEL = 'onbegroeidterreindeel'
SURFACE_TYPE_WATERDEEL = 'waterdeel'
SURFACE_TYPE_ONDERSTEUNENDWATERDEEL = 'ondersteunendwaterdeel'
SURFACE_TYPE_OVERIGBOUWWERK = 'overigbouwwerk'
SURFACE_TYPE_GEBOUWINSTALLATIE = 'gebouwinstallatie'
SURFACE_TYPE_OVERBRUGGINGSDEEL = 'overbruggingsdeel'

ALL_USED_SURFACE_TYPES = {
    SURFACE_TYPE_PAND,
    SURFACE_TYPE_WEGDEEL,
    SURFACE_TYPE_ONDERSTEUNENDWEGDEEL,
    SURFACE_TYPE_BEGROEIDTERREINDEEL,
    SURFACE_TYPE_ONBEGROEIDTERREINDEEL,
    SURFACE_TYPE_WATERDEEL,
    SURFACE_TYPE_ONDERSTEUNENDWATERDEEL,
    SURFACE_TYPE_OVERIGBOUWWERK,
    SURFACE_TYPE_GEBOUWINSTALLATIE,
    SURFACE_TYPE_OVERBRUGGINGSDEEL
}

out_gpkg_fn = 'C:/Users/chris.kerklaan/Documents/Github/bgt-inlooptool/leeg.gpkg'
out_drv = ogr.GetDriverByName("GPKG")
out_gpkg = out_drv.CreateDataSource(out_gpkg_fn)

####################################################################################
# Load data
for stype in ALL_USED_SURFACE_TYPES:
    print(stype)
    src_fn = 'C:/Users/chris.kerklaan/Documents/Github/bgt-inlooptool/test-data/extract/bgt_{}.gml'.format(stype)
    src_ds = ogr.Open(src_fn)
    src_lyr = src_ds.GetLayer(0)
    print(src_lyr.GetFeatureCount())
    out_gpkg.CopyLayer(src_layer=src_lyr, new_name=stype)
out_gpkg = None

##################################################################
# Clean up
out_gpkg = ogr.Open(out_gpkg_fn, update=1)

for stype in ALL_USED_SURFACE_TYPES:
# for stype in ['pand']:
    print('Cleaning up {}'.format(stype))
    lyr = out_gpkg.GetLayerByName(stype)
    lyr.StartTransaction()
    for f in lyr:
        geom=f.GetGeometryRef()
        geom_type = geom.GetGeometryType()
        if geom_type == ogr.wkbPolygon:
            pass
        elif geom_type == ogr.wkbCurvePolygon:
            print('Fixing Curve Polygon feature {}'.format(f.GetFID()))
            geom_linear = geom.GetLinearGeometry()
            f.SetGeometry(geom_linear)
            lyr.SetFeature(f)
        elif geom_type in [ogr.wkbMultiSurface, ogr.wkbMultiPolygon]:
            print('Fixing MultiSurface or MultiPolygon feature {}'.format(f.GetFID()))
            geom_fixed = ogr.ForceToPolygon(geom)
            f.SetGeometry(geom_fixed)
            lyr.SetFeature(f)
        elif geom_type in (ogr.wkbLineString, ogr.wkbCompoundCurve):
            print('Deleting feature {} because it is a Linestring'.format(f.GetFID()))
            lyr.DeleteFeature(f.GetFID())
        else:
            print('Fixing feature {} failed!'.format(f.GetFID()))
            raise Exception('No procedure defined to clean up geometry type {}'.format(str(geom_type)))


    lyr.CommitTransaction()

out_gpkg = None

#######################################################################################3
# register EPSG 28992 in gpkg_spatial_ref_sys if not yet exists
def gpkg_register_crs(gpkg: ogr.DataSource, srs: osr.SpatialReference):
    """gpkg must have been opened with update=1
    Only registers srs if no row of that id exists in gpkg_spatial_ref_sys"""
    if srs.IsProjected():
        cstype='PROJCS'
    elif srs.IsGeographic():
        cstype='GEOGCS'
    else:
        raise ValueError('Invalid SRS')

    sql = """SELECT * FROM gpkg_spatial_ref_sys WHERE srs_id = {}""".format(srs.GetAuthorityCode(cstype))
    result_lyr = ds.ExecuteSQL(sql)
    result_row_count = result_lyr.GetFeatureCount()
    ds.ReleaseResultSet(result_lyr)
    if result_row_count == 0:
        sql =   """
                INSERT INTO gpkg_spatial_ref_sys (
                  srs_name,
                  srs_id,
                  organization,
                  organization_coordsys_id,
                  definition,
                  description
                )
                VALUES (
                    '{srs_name}',
                    {srs_id},
                    '{organization}',
                    {organization_coordsys_id},
                    '{definition}',
                    '{description}'
                );
                """.format(
                    srs_name=srs.GetAttrValue(cstype),
                    srs_id=srs.GetAuthorityCode(cstype),
                    organization=srs.GetAuthorityName(cstype),
                    organization_coordsys_id=srs.GetAuthorityCode(cstype),
                    definition=srs.ExportToWkt(),
                    description=srs.GetAttrValue(cstype)
                )
        ds.ExecuteSQL(sql)

###############################################################
# register EPSG 28992 in geopackage
ds = ogr.Open(out_gpkg_fn, update=1)
srs = osr.SpatialReference()
srs.ImportFromEPSG(28992)
gpkg_register_crs(ds, srs)
ds = None

###############################################################
# register tables in gpkg geometry admin tables
ds = ogr.Open(out_gpkg_fn, update=1)
for stype in ALL_USED_SURFACE_TYPES:
    lyr = ds.GetLayerByName(stype)
    x0, x1, y0, y1 = lyr.GetExtent()
    srs_id = 28992
    sql = """DELETE FROM gpkg_contents WHERE table_name = '{}';""".format(stype)
    ds.ExecuteSQL(sql)
    sql =   """
            INSERT INTO gpkg_contents (
                table_name,
                data_type,
                identifier,
                description,
                min_x, max_x, min_y, max_y,
                srs_id
            )
            VALUES ('{table_name}', '{data_type}', '{identifier}', '{description}',
                    {min_x}, {max_x}, {min_y}, {max_y}, {srs_id});
            """.format(
                table_name = stype,
                data_type='features',
                identifier=stype,
                description=stype,
                min_x=x0,
                max_x=x1,
                min_y=y0,
                max_y=y1,
                srs_id=28992
            )
    ds.ExecuteSQL(sql)
    sql = """DELETE FROM gpkg_geometry_columns WHERE table_name = '{}';""".format(stype)
    ds.ExecuteSQL(sql)
    sql =   """
            INSERT INTO gpkg_geometry_columns (table_name, column_name, geometry_type_name, srs_id, z, m)
            VALUES ('{table_name}','{column_name}','{geometry_type_name}',{srs_id},{z},{m});
            """.format(
                table_name=stype,
                column_name='geom',
                geometry_type_name='POLYGON',
                srs_id=28992,
                z=0,
                m=0
            )
    ds.ExecuteSQL(sql)


ds = None

#####################################################################################
# geometry column types may now be inconsistent with type in gpkg_geometry_columns
# might have to be fixed, but for now assume it is not a problem for our purpose








