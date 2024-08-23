CREATE TABLE cities (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    province TEXT NOT NULL
);

CREATE TABLE languages (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL
);

CREATE TABLE nations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE organizations (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  website TEXT,
  phone TEXT,
  email TEXT,
  description TEXT
);

CREATE TABLE locations (
  id INTEGER PRIMARY KEY,
  organization_id INTEGER NOT NULL,
  city_id INTEGER NOT NULL,
  address TEXT NOT NULL,
  has_service INTEGER,
  FOREIGN KEY (organization_id)
  REFERENCES organizations (id)
    ON DELETE CASCADE
    On UPDATE CASCADE,
  FOREIGN KEY (city_id)
  REFERENCES cities (id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
);

CREATE TABLE location_languages (
  location_id INTEGER NOT NULL,
  language_id INTEGER NOT NULL,
  nation_id INTEGER NOT NULL,
  PRIMARY KEY (location_id , language_id, nation_id),
  FOREIGN KEY (location_id) REFERENCES locations (id) 
    ON DELETE CASCADE 
    ON UPDATE CASCADE,
  FOREIGN KEY (language_id) REFERENCES languages (id) 
    ON DELETE RESTRICT 
    ON UPDATE CASCADE,
  FOREIGN KEY (nation_id) REFERENCES nations (id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
);
