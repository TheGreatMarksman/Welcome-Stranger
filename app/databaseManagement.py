import sqlite3
from flask import g

DATABASE = 'organizations.db'

def init_app(app):
    app.teardown_appcontext(close_db)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    result = cur.fetchall()
    cur.close()
    return (result[0] if result else None) if one else result

def filter(province=None, cities=None, languages=None, nations=None, has_church_service=None):
    query = """
    SELECT 
        o.name AS organization_name, 
        o.website AS website_name,
        o.phone AS phone,
        o.email AS email,
        o.description AS description,
        l.address AS location_address, 
        l.has_service AS has_service,
        c.name AS city_name, 
        c.province AS province_name,
        GROUP_CONCAT(DISTINCT lang.name) AS languages,
        GROUP_CONCAT(DISTINCT n.name) AS nations
    FROM locations l
    JOIN organizations o ON l.organization_id = o.id
    JOIN cities c ON l.city_id = c.id
    JOIN location_languages ll ON l.id = ll.location_id
    JOIN languages lang ON ll.language_id = lang.id
    JOIN nations n ON ll.nation_id = n.id
    WHERE 1=1
    """
    
    params = []

    if province:
        query += " AND c.province = ?"
        params.append(province)
    
    if cities:
        query += " AND c.name IN ({})".format(','.join('?' for _ in cities))
        params.extend(cities)
    
    if nations:
        query += " AND n.name IN ({})".format(','.join('?' for _ in nations))
        params.extend(nations)
    
    if languages:
        query += " AND lang.name IN ({})".format(','.join('?' for _ in languages))
        params.extend(languages)
    
    if has_church_service is not None:
        query += " AND l.has_service = ?"
        params.append(1 if has_church_service else 0)
        
    # Group by location and organization to aggregate languages and nations
    query += """
    GROUP BY l.id, o.name, l.address, l.has_service, c.name, c.province
    """

    print(query, params)
    return query_db(query, params)

def rowToDictionary(row):
    return {
        'organization_name': row[0], 
        'website_name': row[1],
        'phone': row[2],
        'email': row[3],
        'description': row[4],
        'location_address': row[5], 
        'has_service': row[6],
        'city_name': row[7], 
        'province_name': row[8],
        'languages': row[9].split(',') if row[9] else [],
        'nations': row[10].split(',') if row[10] else [],
    }

def close_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()