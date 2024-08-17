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
  address TEXT NOT NULL,
  organization_id INTEGER NOT NULL,
  FOREIGN KEY (organization_id)
  REFERENCES organizations (id)
    ON DELETE CASCADE
    On UPDATE CASCADE
);

CREATE TABLE languages (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL
);

CREATE TABLE location_languages (
  location_id INTEGER NOT NULL,
  language_id INTEGER NOT NULL,
  PRIMARY KEY (location_id , language_id),
  FOREIGN KEY (location_id) REFERENCES locations (id) 
    ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (language_id) REFERENCES languages (id) 
    ON DELETE RESTRICT ON UPDATE CASCADE
);
