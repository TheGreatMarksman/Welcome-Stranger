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
    (1, 1, "1234 Street", 1),
    (1, 2, "34892 Street", 0),
    (2, 1, "40957 Street", 1);

INSERT INTO location_languages (location_id, language_id, nation_id)
VALUES
    (1, 2, 2),
    (1, 3, 2),
    (2, 8, 3),
    (3, 8, 3);