-- Insert Data Types
INSERT OR IGNORE INTO data_types (type_id, description) VALUES
(1, 'Level'),
(2, 'Precipitation'),
(3, 'Discharge');

-- Insert Measurement Methods
INSERT OR IGNORE INTO methods (type_id, method_id, method_name) VALUES
(1, 1, 'Scale'),
(1, 2, 'Linigraph'),
(1, 3, 'Data Logger'),
(1, 5, 'Scale SMS'),
(2, 1, 'Rain Gauge'),
(2, 2, 'Rain Graph'),
(2, 3, 'Data Logger'),
(3, 1, 'Rating Curve'),
(3, 2, 'Flow Transfer'),
(3, 3, 'Flow Sum'),
(3, 4, 'ADCP');

-- Insert Status Levels
INSERT OR IGNORE INTO status_levels (status_id, status_name) VALUES
(0, 'Blank'),
(1, 'Real'),
(2, 'Estimated'),
(3, 'Doubtful'),
(4, 'Dry Scale (Level/Discharge) OR Accumulated (Precipitation)');
