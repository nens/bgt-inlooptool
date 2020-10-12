-- Update distance to water
UPDATE bgt_surfaces
SET
      distance_water = (SELECT water_distances.distance
                        FROM water_distances
                         WHERE water_distances.gml_id = bgt_surfaces.gml_id)
WHERE
    EXISTS (
        SELECT *
        FROM water_distances
        WHERE water_distances.gml_id = bgt_surfaces.gml_id
);
