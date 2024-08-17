INSERT INTO cities (name, province)
VALUES 
    ("Vancouver", "BC"),
    ("Toronto", "ON"),
    ("Montreal", "QC"),
    ("Edmonton", "AB"),
    ("Calgary", "AB"),
    ("Ottowa", "ON");

INSERT INTO organizations (name, website, phone, email, description)
VALUES
    ("Church A", "a.ch.com", 1234, "a@ch.com", "A chuch with two locations"),
    ("Church B", "b.ch.com", 1234, "b@ch.com", "B chuch with one locations");

INSERT INTO locations (organization_id, city_id, address, has_service) 
VALUES
    (0, 0, "1234 Street", 1),
    (0, 1, "34892 Street", 0),
    (1, 0, "40957 Street", 1);

INSERT INTO location_languages (location_id, language_id, nation_id)
VALUES
    (0, 1, 1),
    (0, 1, 2),
    (1, 2, 7),
    (2, 2, 7);