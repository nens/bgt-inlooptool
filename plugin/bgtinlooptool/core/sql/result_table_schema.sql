CREATE TABLE empty_result_table (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    geom CURVEPOLYGON, laatste_wijziging DATETIME,
    bgt_identificatie TEXT,
    type_verharding TEXT,
    graad_verharding REAL,
    hellingstype TEXT,
    hellingspercentage REAL,
    berging_dak REAL,
    putcode TEXT,
    leidingcode TEXT,
    gemengd_riool REAL,
    hemelwaterriool REAL,
    vgs_hemelwaterriool REAL,
    infiltratievoorziening REAL,
    niet_aangesloten REAL
);

SELECT CreateSpatialIndex('empty_result_table', 'geom');
