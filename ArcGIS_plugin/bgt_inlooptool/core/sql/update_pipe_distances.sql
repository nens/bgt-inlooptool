-- Update distances to pipes
UPDATE bgt_surfaces
SET
      distance_hwa = (SELECT pipe_distances.distance
                            FROM pipe_distances
                            WHERE pipe_distances.gml_id = bgt_surfaces.gml_id AND pipe_distances.pipe_type = 'Hemelwaterriool'),
	  distance_dwa = (SELECT pipe_distances.distance
                            FROM pipe_distances
                            WHERE pipe_distances.gml_id = bgt_surfaces.gml_id AND pipe_distances.pipe_type = 'Vuilwaterriool'),
	  distance_gemengd = (SELECT pipe_distances.distance
                            FROM pipe_distances
                            WHERE pipe_distances.gml_id = bgt_surfaces.gml_id AND pipe_distances.pipe_type = 'Gemengd riool'),
	  distance_gi = (SELECT pipe_distances.distance
                            FROM pipe_distances
                            WHERE pipe_distances.gml_id = bgt_surfaces.gml_id AND pipe_distances.pipe_type IN ('DT-riool','Infiltratieriool'))
WHERE
    EXISTS (
        SELECT *
        FROM pipe_distances
        WHERE pipe_distances.gml_id = bgt_surfaces.gml_id
);

