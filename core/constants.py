PSEUDO_INFINITE = float(99999)

SURFACE_TYPE_PAND = "pand"
SURFACE_TYPE_WEGDEEL = "wegdeel"
SURFACE_TYPE_ONDERSTEUNENDWEGDEEL = "ondersteunendwegdeel"
SURFACE_TYPE_BEGROEIDTERREINDEEL = "begroeidterreindeel"
SURFACE_TYPE_ONBEGROEIDTERREINDEEL = "onbegroeidterreindeel"
SURFACE_TYPE_WATERDEEL = "waterdeel"
SURFACE_TYPE_ONDERSTEUNENDWATERDEEL = "ondersteunendwaterdeel"
SURFACE_TYPE_OVERIGBOUWWERK = "overigbouwwerk"
SURFACE_TYPE_GEBOUWINSTALLATIE = "gebouwinstallatie"
SURFACE_TYPE_OVERBRUGGINGSDEEL = "overbruggingsdeel"

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
    SURFACE_TYPE_OVERBRUGGINGSDEEL,
}

CONNECTABLE_SURFACE_TYPES = {
    SURFACE_TYPE_PAND,
    SURFACE_TYPE_WEGDEEL,
    SURFACE_TYPE_ONDERSTEUNENDWEGDEEL,
    SURFACE_TYPE_ONBEGROEIDTERREINDEEL,
    SURFACE_TYPE_OVERIGBOUWWERK,
}

NON_CONNECTABLE_SURFACE_TYPES = {
    SURFACE_TYPE_BEGROEIDTERREINDEEL,
    SURFACE_TYPE_WATERDEEL,
    SURFACE_TYPE_ONDERSTEUNENDWATERDEEL,
    SURFACE_TYPE_GEBOUWINSTALLATIE,
    SURFACE_TYPE_OVERBRUGGINGSDEEL,
}

assert (
    CONNECTABLE_SURFACE_TYPES.union(NON_CONNECTABLE_SURFACE_TYPES)
    == ALL_USED_SURFACE_TYPES
)

KOLK_CONNECTABLE_SURFACE_TYPES = {
    SURFACE_TYPE_WEGDEEL,
    SURFACE_TYPE_ONDERSTEUNENDWEGDEEL,
    SURFACE_TYPE_ONBEGROEIDTERREINDEEL,
}

SURFACE_TYPES_MET_FYSIEK_VOORKOMEN = {
    SURFACE_TYPE_WEGDEEL,
    SURFACE_TYPE_ONBEGROEIDTERREINDEEL,
    SURFACE_TYPE_BEGROEIDTERREINDEEL,
    SURFACE_TYPE_ONDERSTEUNENDWEGDEEL,
}

MULTIPLE_GEOMETRY_SURFACE_TYPES = {
    SURFACE_TYPE_WEGDEEL,
    SURFACE_TYPE_ONBEGROEIDTERREINDEEL,
    SURFACE_TYPE_BEGROEIDTERREINDEEL,
    SURFACE_TYPE_ONDERSTEUNENDWEGDEEL,
}

###############################


VERHARDINGSTYPE_PAND = "dak"
VERHARDINGSTYPE_WATER = "water"
VERHARDINGSTYPE_ONVERHARD = "onverhard"
VERHARDINGSTYPE_OPEN_VERHARD = "open verhard"
VERHARDINGSTYPE_GESLOTEN_VERHARD = "gesloten verhard"
VERHARDINGSTYPE_WATERPASSEREND_VERHARD = "waterpasserende verharding"
VERHARDINGSTYPE_GROEN_DAK = "groen(blauw) dak"

SOURCE_PIPES_TABLE_NAME = "default_lijn"

SURFACES_TABLE_NAME = "bgt_oppervlak"

PIPES_TABLE_NAME = "pipes"
GWSW_PIPE_TYPE_FIELD = "type"
GWSW_PIPE_TYPE_AANSLUITLEIDING = "Aansluitleiding"
GWSW_PIPE_TYPE_BERGINGSLEIDING = "Bergingsleiding"
GWSW_PIPE_TYPE_DRAIN = "Drain"
GWSW_PIPE_TYPE_DRUKLEIDING = "Drukleiding"
GWSW_PIPE_TYPE_DUIKER = "Duiker"
GWSW_PIPE_TYPE_DWAPERCEELAANSLUITLEIDING = "DwaPerceelaansluitleiding"
GWSW_PIPE_TYPE_GEMENGDEPERCEELAANSLUITLEIDING = "GemengdePerceelaansluitleiding"
GWSW_PIPE_TYPE_GEMENGDRIOOL = "GemengdRiool"
GWSW_PIPE_TYPE_HEMELWATERRIOOL = "Hemelwaterriool"
GWSW_PIPE_TYPE_HWAPERCEELAANSLUITLEIDING = "HwaPerceelaansluitleiding"
GWSW_PIPE_TYPE_INFILTRATIERIOOL = "Infiltratieriool"
GWSW_PIPE_TYPE_LOZELEIDING = "LozeLeiding"
GWSW_PIPE_TYPE_LUCHTPERSLEIDING = "Luchtpersleiding"
GWSW_PIPE_TYPE_MANTELBUIS = "Mantelbuis"
GWSW_PIPE_TYPE_OVERSTORTLEIDING = "Overstortleiding"
GWSW_PIPE_TYPE_PERCEELAANSLUITLEIDING = "Perceelaansluitleiding"
GWSW_PIPE_TYPE_PERSLEIDING = "Persleiding"
GWSW_PIPE_TYPE_TRANSPORTRIOOLLEIDING = "Transportrioolleiding"
GWSW_PIPE_TYPE_VUILWATERRIOOL = "Vuilwaterriool"
GWSW_PIPE_TYPE_DITRIOOL = "DIT_riool"

GWSW_STELSEL_TYPE_FIELD = "stelseltype"
GWSW_STELSEL_TYPE_VERBETERDHEMELWATERSTELSEL = "VerbeterdHemelwaterstelsel"

INTERNAL_PIPE_TYPE_FIELD = "pipe_type"
INTERNAL_PIPE_TYPE_IGNORE = "negeer"
INTERNAL_PIPE_TYPE_GEMENGD_RIOOL = "gemengd_riool"
INTERNAL_PIPE_TYPE_HEMELWATERRIOOL = "hemelwaterriool"
INTERNAL_PIPE_TYPE_VGS_HEMELWATERRIOOL = "vgs_hemelwaterriool"
INTERNAL_PIPE_TYPE_VUILWATERRIOOL = "vuilwaterriool"
INTERNAL_PIPE_TYPE_INFILTRATIEVOORZIENING = "infiltratievoorziening"

PIPE_MAP = {
    GWSW_PIPE_TYPE_AANSLUITLEIDING: INTERNAL_PIPE_TYPE_IGNORE,
    GWSW_PIPE_TYPE_BERGINGSLEIDING: INTERNAL_PIPE_TYPE_IGNORE,
    GWSW_PIPE_TYPE_DRAIN: INTERNAL_PIPE_TYPE_IGNORE,
    GWSW_PIPE_TYPE_DRUKLEIDING: INTERNAL_PIPE_TYPE_IGNORE,
    GWSW_PIPE_TYPE_DUIKER: INTERNAL_PIPE_TYPE_IGNORE,
    GWSW_PIPE_TYPE_DWAPERCEELAANSLUITLEIDING: INTERNAL_PIPE_TYPE_IGNORE,
    GWSW_PIPE_TYPE_GEMENGDEPERCEELAANSLUITLEIDING: INTERNAL_PIPE_TYPE_IGNORE,
    GWSW_PIPE_TYPE_GEMENGDRIOOL: INTERNAL_PIPE_TYPE_GEMENGD_RIOOL,
    GWSW_PIPE_TYPE_HEMELWATERRIOOL: INTERNAL_PIPE_TYPE_HEMELWATERRIOOL,
    GWSW_PIPE_TYPE_HWAPERCEELAANSLUITLEIDING: INTERNAL_PIPE_TYPE_IGNORE,
    GWSW_PIPE_TYPE_INFILTRATIERIOOL: INTERNAL_PIPE_TYPE_INFILTRATIEVOORZIENING,
    GWSW_PIPE_TYPE_LOZELEIDING: INTERNAL_PIPE_TYPE_IGNORE,
    GWSW_PIPE_TYPE_LUCHTPERSLEIDING: INTERNAL_PIPE_TYPE_IGNORE,
    GWSW_PIPE_TYPE_MANTELBUIS: INTERNAL_PIPE_TYPE_IGNORE,
    GWSW_PIPE_TYPE_OVERSTORTLEIDING: INTERNAL_PIPE_TYPE_IGNORE,
    GWSW_PIPE_TYPE_PERCEELAANSLUITLEIDING: INTERNAL_PIPE_TYPE_IGNORE,
    GWSW_PIPE_TYPE_PERSLEIDING: INTERNAL_PIPE_TYPE_IGNORE,
    GWSW_PIPE_TYPE_TRANSPORTRIOOLLEIDING: INTERNAL_PIPE_TYPE_IGNORE,
    GWSW_PIPE_TYPE_VUILWATERRIOOL: INTERNAL_PIPE_TYPE_VUILWATERRIOOL,
    GWSW_PIPE_TYPE_DITRIOOL: INTERNAL_PIPE_TYPE_INFILTRATIEVOORZIENING,
}

KOLK = "kolk"
OPEN_WATER = "open_water"

BUILDINGS_TABLE_NAME = "buildings"
KOLKEN_TABLE_NAME = "kolken"
RESULT_TABLE_NAME = "bgt_inlooptabel"
RESULT_TABLE_NAME_PREV = "bgt_inlooptabel_oud"

RESULT_TABLE_FIELD_ID = "id"
RESULT_TABLE_FIELD_LAATSTE_WIJZIGING = "laatste_wijziging"
RESULT_TABLE_FIELD_BGT_IDENTIFICATIE = "bgt_identificatie"
RESULT_TABLE_FIELD_TYPE_VERHARDING = "type_verharding"
RESULT_TABLE_FIELD_GRAAD_VERHARDING = "graad_verharding"
RESULT_TABLE_FIELD_HELLINGSTYPE = "hellingstype"
RESULT_TABLE_FIELD_HELLINGSPERCENTAGE = "hellingspercentage"
# RESULT_TABLE_FIELD_BERGING_DAK = 'berging_dak'
RESULT_TABLE_FIELD_TYPE_PRIVATE_VOORZIENING = "type_private_voorziening"
RESULT_TABLE_FIELD_BERGING_PRIVATE_VOORZIENING = "berging_private_voorziening"
RESULT_TABLE_FIELD_CODE_GEMENGD = "leidingcode_gemengd"
RESULT_TABLE_FIELD_CODE_HWA = "leidingcode_hwa"
RESULT_TABLE_FIELD_CODE_DWA = "leidingcode_dwa"
RESULT_TABLE_FIELD_CODE_INFILTRATIE = "leidingcode_infiltratie"
RESULT_TABLE_FIELD_WIJZIGING = "wijziging"

TARGET_TYPE_GEMENGD_RIOOL = "gemengd_riool"
TARGET_TYPE_HEMELWATERRIOOL = "hemelwaterriool"
TARGET_TYPE_VGS_HEMELWATERRIOOL = "vgs_hemelwaterriool"
TARGET_TYPE_VUILWATERRIOOL = "vuilwaterriool"
TARGET_TYPE_INFILTRATIEVOORZIENING = "infiltratievoorziening"
TARGET_TYPE_OPEN_WATER = "open_water"
TARGET_TYPE_MAAIVELD = "maaiveld"

TARGET_TYPES = {
    TARGET_TYPE_GEMENGD_RIOOL,
    TARGET_TYPE_HEMELWATERRIOOL,
    TARGET_TYPE_VGS_HEMELWATERRIOOL,
    TARGET_TYPE_VUILWATERRIOOL,
    TARGET_TYPE_INFILTRATIEVOORZIENING,
    TARGET_TYPE_OPEN_WATER,
    TARGET_TYPE_MAAIVELD,
}

DISTANCE_TYPES = {
    INTERNAL_PIPE_TYPE_GEMENGD_RIOOL,
    INTERNAL_PIPE_TYPE_HEMELWATERRIOOL,
    INTERNAL_PIPE_TYPE_VGS_HEMELWATERRIOOL,
    INTERNAL_PIPE_TYPE_VUILWATERRIOOL,
    INTERNAL_PIPE_TYPE_INFILTRATIEVOORZIENING,
    KOLK,
    OPEN_WATER,
}

SETTINGS_TABLE_NAME = "rekeninstellingen"
SETTINGS_TABLE_NAME_PREV = "rekeninstellingen_oud"
INF_PAVEMENT_TABLE_NAME_PREV = "waterpasserende_verharding_oud"

SETTINGS_TABLE_FIELD_ID = "run_id"
SETTINGS_TABLE_FIELD_TIJD_START = "tijd_start"
SETTINGS_TABLE_FIELD_TIJD_EIND = "tijd_eind"
SETTINGS_TABLE_FIELD_DOWNLOAD_BGT = "download_bgt"
SETTINGS_TABLE_FIELD_DOWNLOAD_GWSW = "download_gwsw"
SETTINGS_TABLE_FIELD_DOWNLOAD_BAG = "download_bag"
SETTINGS_TABLE_FIELD_PAD_BGT = "pad_bgt"
SETTINGS_TABLE_FIELD_PAD_GWSW = "pad_gwsw"
SETTINGS_TABLE_FIELD_PAD_BAG = "pad_bag"
SETTINGS_TABLE_FIELD_PAD_KOLKEN = "pad_kolken"
SETTINGS_TABLE_FIELD_AFSTAND_AFWATERINGSVOORZIENING = "afstand_afwateringsvoorziening"
SETTINGS_TABLE_FIELD_AFSTAND_VERHARD_OPP_WATER = "afstand_verhard_opp_water"
SETTINGS_TABLE_FIELD_AFSTAND_PAND_OPP_WATER = "afstand_pand_opp_water"
SETTINGS_TABLE_FIELD_AFSTAND_VERHARD_KOLK = "afstand_verhard_kolk"
SETTINGS_TABLE_FIELD_AFSTAND_AFKOPPELD = "afstand_afgekoppeld"
SETTINGS_TABLE_FIELD_AFSTAND_DRIEVOUDIG = "afstand_drievoudig"
SETTINGS_TABLE_FIELD_VERHARDINGSGRAAD_ERF = "verhardingsgraad_erf"
SETTINGS_TABLE_FIELD_VERHARDINGSGRAAD_HALF_VERHARD = "verhardingsgraad_half_verhard"
SETTINGS_TABLE_FIELD_AFKOPPELEN_HELLEND = "afkoppelen_hellend"
SETTINGS_TABLE_FIELD_BOUWJAAR_GESCHEIDEN_BINNENHUIS = "bouwjaar_gescheiden_binnenhuis"
SETTINGS_TABLE_FIELD_LEIDINGCODES_KOPPELEN = "leidingcodes_koppelen"

STATISTICS_TABLE_NAME = "statistieken"

STATISTICS_TABLE_FIELD_ID = "id"
STATISTICS_TABLE_FIELD_OPP_TOTAAL = "opp_totaal"
STATISTICS_TABLE_FIELD_OPP_GEMENGD = "opp_gemengd"
STATISTICS_TABLE_FIELD_OPP_HWA = "opp_hwa"
STATISTICS_TABLE_FIELD_OPP_VGS = "opp_vgs"
STATISTICS_TABLE_FIELD_OPP_DWA = "opp_dwa"
STATISTICS_TABLE_FIELD_OPP_INFILTRATIEVOORZIENING = "opp_infiltratievoorziening"
STATISTICS_TABLE_FIELD_OPP_OPEN_WATER = "opp_open_water"
STATISTICS_TABLE_FIELD_OPP_MAAIVELD = "opp_maaiveld"
STATISTICS_TABLE_FIELD_PERC_GEMENGD = "perc_gemengd"
STATISTICS_TABLE_FIELD_PERC_HWA = "perc_hwa"
STATISTICS_TABLE_FIELD_PERC_VGS = "perc_vgs"
STATISTICS_TABLE_FIELD_PERC_DWA = "perc_dwa"
STATISTICS_TABLE_FIELD_PERC_INFILTRATIEVOORZIENING = "perc_infiltratievoorziening"
STATISTICS_TABLE_FIELD_PERC_OPEN_WATER = "perc_open_water"
STATISTICS_TABLE_FIELD_PERC_MAAIVELD = "perc_maaiveld"
STATISTICS_TABLE_FIELD_OPP_TOTAAL_DAK = "opp_totaal_dak"
STATISTICS_TABLE_FIELD_OPP_TOTAAL_GESL_VERH = "opp_totaal_gesl_verh"
STATISTICS_TABLE_FIELD_OPP_TOTAAL_OPEN_VERH = "opp_totaal_open_verh"
STATISTICS_TABLE_FIELD_OPP_TOTAAL_ONVERHARD = "opp_totaal_onverhard"
STATISTICS_TABLE_FIELD_OPP_GEMENGD_DAK = "opp_gemengd_dak"
STATISTICS_TABLE_FIELD_OPP_GEMENGD_GESL_VERH = "opp_gemengd_gesl_verh"
STATISTICS_TABLE_FIELD_OPP_GEMENGD_OPEN_VERH = "opp_gemengd_open_verh"
STATISTICS_TABLE_FIELD_OPP_GEMENGD_ONVERHARD = "opp_gemengd_onverhard"
STATISTICS_TABLE_FIELD_OPP_HWA_DAK = "opp_hwa_dak"
STATISTICS_TABLE_FIELD_OPP_HWA_GESL_VERH = "opp_hwa_gesl_verh"
STATISTICS_TABLE_FIELD_OPP_HWA_OPEN_VERH = "opp_hwa_open_verh"
STATISTICS_TABLE_FIELD_OPP_HWA_ONVERHARD = "opp_hwa_onverhard"
STATISTICS_TABLE_FIELD_OPP_VGS_DAK = "opp_vgs_dak"
STATISTICS_TABLE_FIELD_OPP_VGS_GESL_VERH = "opp_vgs_gesl_verh"
STATISTICS_TABLE_FIELD_OPP_VGS_OPEN_VERH = "opp_vgs_open_verh"
STATISTICS_TABLE_FIELD_OPP_VGS_ONVERHARD = "opp_vgs_onverhard"
STATISTICS_TABLE_FIELD_OPP_DWA_DAK = "opp_dwa_dak"
STATISTICS_TABLE_FIELD_OPP_DWA_GESL_VERH = "opp_dwa_gesl_verh"
STATISTICS_TABLE_FIELD_OPP_DWA_OPEN_VERH = "opp_dwa_open_verh"
STATISTICS_TABLE_FIELD_OPP_DWA_ONVERHARD = "opp_dwa_onverhard"
STATISTICS_TABLE_FIELD_OPP_INFILTRATIEVOORZIENING_DAK = "opp_infiltratievoorziening_dak"
STATISTICS_TABLE_FIELD_OPP_INFILTRATIEVOORZIENING_GESL_VERH = "opp_infiltratievoorziening_gesl_verh"
STATISTICS_TABLE_FIELD_OPP_INFILTRATIEVOORZIENING_OPEN_VERH = "opp_infiltratievoorziening_open_verh"
STATISTICS_TABLE_FIELD_OPP_INFILTRATIEVOORZIENING_ONVERHARD = "opp_infiltratievoorziening_onverhard"
STATISTICS_TABLE_FIELD_OPP_OPEN_WATER_DAK = "opp_open_water_dak"
STATISTICS_TABLE_FIELD_OPP_OPEN_WATER_GESL_VERH = "opp_open_water_gesl_verh"
STATISTICS_TABLE_FIELD_OPP_OPEN_WATER_OPEN_VERH = "opp_open_water_open_verh"
STATISTICS_TABLE_FIELD_OPP_OPEN_WATER_ONVERHARD = "opp_open_water_onverhard"
STATISTICS_TABLE_FIELD_OPP_MAAIVELD_DAK = "opp_maaiveld_dak"
STATISTICS_TABLE_FIELD_OPP_MAAIVELD_GESL_VERH = "opp_maaiveld_gesl_verh"
STATISTICS_TABLE_FIELD_OPP_MAAIVELD_OPEN_VERH = "opp_maaiveld_open_verh"
STATISTICS_TABLE_FIELD_OPP_MAAIVELD_ONVERHARD = "opp_maaiveld_onverhard"
STATISTICS_TABLE_FIELD_PERC_GEMENGD_DAK = "perc_gemengd_dak"
STATISTICS_TABLE_FIELD_PERC_GEMENGD_GESL_VERH = "perc_gemengd_gesl_verh"
STATISTICS_TABLE_FIELD_PERC_GEMENGD_OPEN_VERH = "perc_gemengd_open_verh"
STATISTICS_TABLE_FIELD_PERC_GEMENGD_ONVERHARD = "perc_gemengd_onverhard"
STATISTICS_TABLE_FIELD_PERC_HWA_DAK = "perc_hwa_dak"
STATISTICS_TABLE_FIELD_PERC_HWA_GESL_VERH = "perc_hwa_gesl_verh"
STATISTICS_TABLE_FIELD_PERC_HWA_OPEN_VERH = "perc_hwa_open_verh"
STATISTICS_TABLE_FIELD_PERC_HWA_ONVERHARD = "perc_hwa_onverhard"
STATISTICS_TABLE_FIELD_PERC_VGS_DAK = "perc_vgs_dak"
STATISTICS_TABLE_FIELD_PERC_VGS_GESL_VERH = "perc_vgs_gesl_verh"
STATISTICS_TABLE_FIELD_PERC_VGS_OPEN_VERH = "perc_vgs_open_verh"
STATISTICS_TABLE_FIELD_PERC_VGS_ONVERHARD = "perc_vgs_onverhard"
STATISTICS_TABLE_FIELD_PERC_DWA_DAK = "perc_dwa_dak"
STATISTICS_TABLE_FIELD_PERC_DWA_GESL_VERH = "perc_dwa_gesl_verh"
STATISTICS_TABLE_FIELD_PERC_DWA_OPEN_VERH = "perc_dwa_open_verh"
STATISTICS_TABLE_FIELD_PERC_DWA_ONVERHARD = "perc_dwa_onverhard"
STATISTICS_TABLE_FIELD_PERC_INFILTRATIEVOORZIENING_DAK = "perc_infiltratievoorziening_dak"
STATISTICS_TABLE_FIELD_PERC_INFILTRATIEVOORZIENING_GESL_VERH = "perc_infiltratievoorziening_gesl_verh"
STATISTICS_TABLE_FIELD_PERC_INFILTRATIEVOORZIENING_OPEN_VERH = "perc_infiltratievoorziening_open_verh"
STATISTICS_TABLE_FIELD_PERC_INFILTRATIEVOORZIENING_ONVERHARD = "perc_infiltratievoorziening_onverhard"
STATISTICS_TABLE_FIELD_PERC_OPEN_WATER_DAK = "perc_open_water_dak"
STATISTICS_TABLE_FIELD_PERC_OPEN_WATER_GESL_VERH = "perc_open_water_gesl_verh"
STATISTICS_TABLE_FIELD_PERC_OPEN_WATER_OPEN_VERH = "perc_open_water_open_verh"
STATISTICS_TABLE_FIELD_PERC_OPEN_WATER_ONVERHARD = "perc_open_water_onverhard"
STATISTICS_TABLE_FIELD_PERC_MAAIVELD_DAK = "perc_maaiveld_dak"
STATISTICS_TABLE_FIELD_PERC_MAAIVELD_GESL_VERH = "perc_maaiveld_gesl_verh"
STATISTICS_TABLE_FIELD_PERC_MAAIVELD_OPEN_VERH = "perc_maaiveld_open_verh"
STATISTICS_TABLE_FIELD_PERC_MAAIVELD_ONVERHARD = "perc_maaiveld_onverhard"
STATISTICS_TABLE_FIELD_OPP_DAK = "opp_dak"
STATISTICS_TABLE_FIELD_OPP_GESL_VERH = "opp_gesl_verh"
STATISTICS_TABLE_FIELD_OPP_OPEN_VERH = "opp_open_verh"
STATISTICS_TABLE_FIELD_OPP_ONVERHARD = "opp_onverhard"
STATISTICS_TABLE_FIELD_OPP_GROEN_DAK = "opp_groen_dak"
STATISTICS_TABLE_FIELD_OPP_WATERPAS_VERH = "opp_waterpas_verh"
STATISTICS_TABLE_FIELD_OPP_WATER = "opp_water"
STATISTICS_TABLE_FIELD_PERC_DAK = "perc_dak"
STATISTICS_TABLE_FIELD_PERC_GESL_VERH = "perc_gesl_verh"
STATISTICS_TABLE_FIELD_PERC_OPEN_VERH = "perc_open_verh"
STATISTICS_TABLE_FIELD_PERC_ONVERHARD = "perc_onverhard"
STATISTICS_TABLE_FIELD_PERC_GROEN_DAK = "perc_groen_dak"
STATISTICS_TABLE_FIELD_PERC_WATERPAS_VERH = "perc_waterpas_verh"
STATISTICS_TABLE_FIELD_PERC_WATER = "perc_water"


CHECKS_TABLE_NAME = "controles"

CHECKS_TABLE_FIELD_ID = "id"
CHECKS_TABLE_FIELD_LEVEL = "niveau"
CHECKS_TABLE_FIELD_CODE = "error_code"
CHECKS_TABLE_FIELD_TABLE = "tabel"
CHECKS_TABLE_FIELD_COLUMN = "kolom"
CHECKS_TABLE_FIELD_VALUE = "waarde"
CHECKS_TABLE_FIELD_DESCRIPTION = "omschrijving"

CHECKS_LARGE_AREA = 5000


