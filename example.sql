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
    ("Church B", "b.ch.com", 1234, "b@ch.com", "B chuch with one locations"),
    ("Church C", "c.ch.com", 12345, "c@ch.com", "A church"),
    ("Church D", "d.ch.com", 12345, "d@ch.com", "A church"),
    ("Church E", "e.ch.com", 12345, "e@ch.com", "A church");

INSERT INTO locations (organization_id, city_id, address, has_service) 
VALUES
    (1, 1, "1234 Street", 1),
    (1, 2, "34892 Street", 0),
    (2, 1, "40957 Street", 1),
    (3, 6, "4890 Street", 1),
    (4, 4, "4890 Street", 0),
    (5, 5, "7438 Street", 1);

INSERT INTO location_languages (location_id, language_id, nation_id)
VALUES
    (1, 2, 2),
    (1, 3, 2),
    (2, 8, 3),
    (3, 8, 3),
    (4, 20, 7),
    (5, 20, 6),
    (6, 10, 4);