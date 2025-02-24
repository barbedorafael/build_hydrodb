-- Table for Data Types (Precipitation, Level, Discharge)
CREATE TABLE IF NOT EXISTS data_types (
    type_id INT PRIMARY KEY,  
    description TEXT
);

-- Table for Measurement Methods
CREATE TABLE IF NOT EXISTS methods (
    type_id INT,
    method_id INT,
    method_name TEXT UNIQUE,
    PRIMARY KEY (type_id, method_id),
    FOREIGN KEY (type_id) REFERENCES data_types(type_id)
);

-- Table for Status Metadata
CREATE TABLE IF NOT EXISTS status_levels (
    status_id INT,
    status_name TEXT UNIQUE,
    PRIMARY KEY (status_id)
);

-- Table for Stations Metadata
CREATE TABLE IF NOT EXISTS stations (
    station_id INT PRIMARY KEY,            -- Primary Key
    name TEXT,                             -- Station Name
    station_type TEXT,                     -- Type of Station
    lon FLOAT,                             -- Longitude (Geo)
    lat FLOAT,                             -- Latitude (Geo)
    basin_id INT,                          -- Basin Code
    sub_basin_id INT,                      -- Sub-Basin Code
    river_id INT,                          -- River Code
    state_id INT,                          -- State Code
    municipality_id INT,                   -- Municipality Code
    responsible_id INT,                    -- Responsible Entity Code
    responsible_unit TEXT,                 -- Responsible Unit
    responsible_jurisdiction TEXT,         -- Responsible Jurisdiction
    operator_id INT,                       -- Operator Code
    operator_unit TEXT,                    -- Operator Unit
    operator_subunit TEXT,                 -- Operator Sub-Unit
    additional_code TEXT,                  -- Additional Station Code
    altitude FLOAT,                        -- Altitude in meters
    drainage_area FLOAT                    -- Drainage Area
);

-- Table for Time Series Data
CREATE TABLE IF NOT EXISTS timeseries (
    station_id INT,
    type_id INT,
    consistency_id INT,
    date DATE,
    value FLOAT,
    status INT,
    method_id INT,
    PRIMARY KEY (station_id, date, type_id, consistency_id),
    FOREIGN KEY (station_id) REFERENCES stations(station_id),
    FOREIGN KEY (type_id) REFERENCES data_types(type_id),
    FOREIGN KEY (consistency_id) REFERENCES consistency_levels(consistency_id),
    FOREIGN KEY (method_id) REFERENCES methods(method_id),
    FOREIGN KEY (status) REFERENCES status_levels(status_id)
);