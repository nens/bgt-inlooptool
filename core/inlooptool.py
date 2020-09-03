import os
from osgeo import ogr
from osgeo import gdal
import pandas as pd
import numpy as np

IMPORT_SURFACES = [
    "pand",
    "wegdeel",
    "ondersteunendwegdeel",
    "begroeidterreindeel",
    "onbegroeidterreindeel",
    "waterdeel",
    "ondersteunendwaterdeel",
    "overigbouwwerk",
    "gebouwinstallatie",
    "overbruggingsdeel",
]

gdal.UseExceptions()
GPKG_DRIVER = ogr.GetDriverByName("GPKG")

class BGTInloopTool:
    
    def __init__(self):
        pass

    def calculate_runoff_targets(self):

        bgt_testdata = "C:/Users/Emile.deBadts/Documents/Projecten/v0099_bgt_inlooptool/testdata/extract.zip"
        gwsw_testdata = "C:/Users/Emile.deBadts/Documents/Projecten/v0099_bgt_inlooptool/testdata/getGeoPackage_1179.gpkg"

        # TODO get defaults from gui
        database = Database()
        parameters = InputParameters()

        database.import_surfaces(bgt_zip_file=bgt_testdata)
        database.import_pipes(datasource=gwsw_testdata)

        database.calculate_distances(parameters)

        inlooptabel = pd.DataFrame(columns=["surface_id", "afwatering"])

        bgt_surfaces = database.mem_database.GetLayerByName("bgt_surfaces")

        for surface in bgt_surfaces:
            afwatering = self.decision_tree(surface, parameters)
            inlooptabel = inlooptabel.append(
                pd.DataFrame({"surface_id": surface.gml_id, "afwatering": afwatering}),
                sort=False,
            )

    def decision_tree(self, surface, parameters):

        if surface.surface_type not in [
            "pand",
            "wegdeel",
            "ondersteunendwegdeel",
            "onbegroeidterreindeel",
            "overigbouwwerk",
        ]:
            afwateringskenmerk = "maaiveld"

        elif not any(
            [
                surface.distance_hwa,
                surface.distance_dwa,
                surface.distance_gi,
                surface.distance_gemengd,
                surface.distance_water,
            ]
        ):
            afwateringskenmerk = "maaiveld"

        elif surface.surface_type == "pand":
            pass

        elif surface.fysiek_voorkomen == "verhard":

            if surface.distance_water or np.inf < parameters.max_afstand_vlak_oppwater:
                afwateringskenmerk = "water"

            elif (
                surface.distance_gemengd
                or np.inf
                - min(surface.distance_hwa or np.inf, surface.distance_gi or np.inf)
                < parameters.max_afstand_afgekoppeld
            ):

                if surface.distance_hwa or np.inf < surface.distance_gi or np.inf:
                    afwateringskenmerk = "hwa"
                else:
                    afwateringskenmerk = "infiltratieriool"

            elif (
                surface.distance_gemengd
                or np.inf
                - min(surface.distance_hwa or np.inf, surface.distance_gi or np.inf)
                > parameters.max_afstand_afgekoppeld
            ):

                if surface.distance_gemengd or np.inf < min(
                    surface.distance_hwa or np.inf, surface.distance_gi or np.inf
                ):
                    afwateringskenmerk = "gemengd"

                elif surface.distance_hwa or np.inf < surface.distance_gi or np.inf:
                    afwateringskenmerk = "hwa"

                else:
                    afwateringskenmerk = "infiltratieriool"

        else:
            afwateringskenmerk = "maaiveld"

        return afwateringskenmerk


class InputParameters:
    
    def __init__(self):

        self.max_afstand_vlak_afwateringsvoorziening = 40
        self.max_afstand_vlak_oppwater = 2
        self.max_afstand_pand_oppwater = 6
        self.max_afstand_vlak_kolk = 30
        self.max_afstand_afgekoppeld = 3
        self.max_afstand_drievoudig = 4
        self.afkoppelen_hellende_daken = True
        self.bouwjaar_gescheiden_binnenhuisriolering = 1992

    def from_file(self):
        pass

    def to_file(self):
        pass


class Database:

    def __init__(self):
        self.mem_database = GPKG_DRIVER.CreateDataSource('/vsimem/database.gpkg')

    def import_pipes(self, datasource):
        lines_gpkg = ogr.Open(datasource)
        self.mem_database.CopyLayer(lines_gpkg.GetLayerByName("default_lijn"), "pipes")

    def import_surfaces(self, bgt_zip_file):

        dest_srs = ogr.osr.SpatialReference()
        dest_srs.ImportFromEPSG(28992)
        dest_layer = self.mem_database.CreateLayer(
            "bgt_surfaces", dest_srs, 3, ["OVERWRITE=YES", "GEOMETRY_NAME=geom"]
        )

        # adding fields to new layer
        add_text_fields = ["gml_id", "surface_type", "fysiek_voorkomen"]

        for field in add_text_fields:
            field_name = ogr.FieldDefn(field, ogr.OFTString)
            field_name.SetWidth(60)
            new_field = dest_layer.CreateField(field_name)

        add_real_fields = [
            "distance_water",
            "distance_hwa",
            "distance_dwa",
            "distance_gi",
            "distance_gemengd",
        ]

        for field in add_real_fields:
            
            field_name = ogr.FieldDefn(field, ogr.OFTReal)
            field_name.SetWidth(20)
            new_field = dest_layer.CreateField(field_name)

        for surface in IMPORT_SURFACES:

            print(surface)
            surface_source = ogr.Open(
                os.path.join("/vsizip/" + bgt_zip_file, f"bgt_{surface}.gml")
            )
            input_layer = surface_source.GetLayerByName(f"{surface}")

            # TODO voor alle features, langzame import

            for i in range(0, input_layer.GetFeatureCount()):
                feature = input_layer.GetFeature(i)

                if feature:

                    # TODO aparte filter voor panden met plus-status uit bag
                    if feature["eindRegistratie"] is not None:
                        continue

                    else:

                        new_feature = ogr.Feature(dest_layer.GetLayerDefn())
                        new_feature.SetField("gml_id", feature.gml_id)
                        new_feature.SetField("surface_type", f"{surface}")

                        if surface in [
                            "wegdeel",
                            "onbegroeidterreindeel",
                            "ondersteunendwegdeel",
                        ]:

                            if "verharding" in feature["bgt-fysiekVoorkomen"]:

                                new_feature["fysiek_voorkomen"] = "verhard"

                            else:
                                new_feature["fysiek_voorkomen"] = None

                        else:
                            new_feature["fysiek_voorkomen"] = None

                        target_geometry = ogr.ForceToPolygon(feature.geometry())
                        target_geometry.AssignSpatialReference(dest_srs)
                        new_feature.SetGeometry(target_geometry)
                        dest_layer.CreateFeature(new_feature)

                        target_geometry = None
                        new_feature = None

            surface_source = None
            input_layer = None

        dest_layer = None

    def import_buildings(self, datasource, field_map):
        pass

    def clean_surfaces(self):
        pass

    def add_build_year_to_surface(self):
        pass

    def calculate_distances(self, parameters):
 
        calculate_distance_pipe_sql = f"""SELECT surface.gml_id, pipe."Naam" as pipe_name, pipe."TypeNaam" as pipe_type, ST_Distance(pipe.geom, surface.geom) as distance 
                                           FROM pipes as pipe, bgt_surfaces as surface 
                                           WHERE PtDistWithin(pipe.geom, surface.geom, {parameters.max_afstand_vlak_afwateringsvoorziening})
                                           GROUP BY surface.gml_id, pipe."TypeNaam" ORDER BY surface.gml_id, ST_Distance(pipe.geom, surface.geom) asc;"""

        pipe_distance_layer = self.mem_database.ExecuteSQL(calculate_distance_pipe_sql)
        new_layer = self.mem_database.CopyLayer(pipe_distance_layer, "pipe_distances")
        new_layer = None

        calculate_distance_water_sql = f"""SELECT surface1.gml_id as gml_id, ST_Distance(surface1.geom, surface2.geom) as distance
                                            FROM bgt_surfaces as surface1, bgt_surfaces as surface2
                                            WHERE surface1.surface_type != 'waterdeel' AND surface2.surface_type = 'waterdeel'
                                            AND PtDistWithin(surface1.geom, surface2.geom, {parameters.max_afstand_vlak_afwateringsvoorziening})
                                            GROUP BY surface1.gml_id ORDER BY ST_Distance(surface1.geom, surface2.geom) asc;"""

        water_distance_layer = self.mem_database.ExecuteSQL(
            calculate_distance_water_sql
        )
        new_layer = self.mem_database.CopyLayer(water_distance_layer, "water_distances")
        new_layer = None

        # Update water distances
        update_water_distances = os.path.join(__file__, "update_water_distances.sql")
        with open(update_water_distances, "r") as file:
            update_water_distances_sql = file.read()
        self.mem_database.ExecuteSQL(update_water_distances_sql)

        # Udpate pipe distnacse
        update_pipe_distances = os.path.join(__file__, "update_pipe_distances.sql")
        with open(update_pipe_distances, "r") as file:
            update_pipe_distances_sql = file.read()
        self.mem_database.ExecuteSQL(update_pipe_distances_sql)


