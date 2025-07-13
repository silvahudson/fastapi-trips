
CREATE TABLE IF NOT EXISTS trips (
    id SERIAL PRIMARY KEY,
    region TEXT NOT NULL,
    origin GEOMETRY(Point, 4326),
    destination GEOMETRY(Point, 4326),
    datetime TIMESTAMP,
    datasource TEXT,
    time_of_day TEXT
);

CREATE INDEX IF NOT EXISTS idx_origin_geom ON trips USING GIST(origin);
CREATE INDEX IF NOT EXISTS idx_dest_geom ON trips USING GIST(destination);
CREATE INDEX IF NOT EXISTS idx_datetime ON trips(datetime);
