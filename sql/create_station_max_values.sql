-- Create table for station maximum values summary
-- This table contains the maximum level and discharge values for each station

CREATE TABLE IF NOT EXISTS station_max_values AS
SELECT
    s.station_id,
    s.name as station_name,
    s.lat,
    s.lon,
    s.sub_basin_id,
    s.river_id,
    s.altitude,
    s.drainage_area,
    level_max.max_level,
    level_max.max_level_date,
    discharge_max.max_discharge,
    discharge_max.max_discharge_date
FROM (SELECT * FROM stations
        WHERE station_type=1
        AND basin_id in (7,8)
        AND state_id in (23,24)
) s
LEFT JOIN (
    SELECT
        station_id,
        MAX(value) as max_level,
        date as max_level_date
    FROM timeseries
    WHERE type_id = 1  -- Level data
    AND (station_id, value) IN (
        SELECT station_id, MAX(value)
        FROM timeseries
        WHERE type_id = 1
        GROUP BY station_id
    )
    GROUP BY station_id
) level_max ON s.station_id = level_max.station_id
LEFT JOIN (
    SELECT
        station_id,
        MAX(value) as max_discharge,
        date as max_discharge_date
    FROM timeseries
    WHERE type_id = 3  -- Discharge data
    AND (station_id, value) IN (
        SELECT station_id, MAX(value)
        FROM timeseries
        WHERE type_id = 3
        GROUP BY station_id
    )
    GROUP BY station_id
) discharge_max ON s.station_id = discharge_max.station_id
WHERE max_discharge IS NOT NULL;