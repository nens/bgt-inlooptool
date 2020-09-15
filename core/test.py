import sys
print(sys.path)
from inlooptool import *

ogr.UseExceptions()

TEST_DATA_DIR = os.path.join(__file__, '../../test-data')
print(TEST_DATA_DIR)

BGT_TESTDATA = os.path.join(TEST_DATA_DIR, 'extract.zip')
gwsw_testdata = os.path.join(TEST_DATA_DIR, 'getGeoPackage_1179.gpkg')
test_output_dir = 'C:/Users/leendert.vanwolfswin/Documents/bgtinlooptool/test'

input_parameters = InputParameters()
bgt_inlooptool = BGTInloopTool(input_parameters)


def empty_result_table():
    hard_gpkg_driver = ogr.GetDriverByName('GPKG')
    out_gpkg_fn = os.path.join(test_output_dir, 'empty_result.gpkg')
    if os.path.exists(out_gpkg_fn):
        os.remove(out_gpkg_fn)
    hard_gpkg_ds = hard_gpkg_driver.CreateDataSource(out_gpkg_fn)
    src_lyr = bgt_inlooptool.database.result_table
    hard_gpkg_ds.CopyLayer(src_lyr, 'bgt_inlooptabel')
    hard_gpkg_ds = None
    result = ogr.Open(out_gpkg_fn)
    if isinstance(result, ogr.DataSource):
        return True
    else:
        return False


def import_surfaces():
    bgt_inlooptool.database.import_surfaces(bgt_zip_file=BGT_TESTDATA)


print('Test result for empty_result_table: {}'.format(empty_result_table()))
print('Test result for import_surfaces: {}'.format(import_surfaces()))

# bgt_inlooptool.database.import_surfaces(bgt_zip_file=BGT_TESTDATA)
# bgt_inlooptool.database.import_pipes(datasource=gwsw_testdata)
# bgt_inlooptool.database.calculate_distances(parameters)
