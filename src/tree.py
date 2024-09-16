import uuid
TOLERANCE = 0.0001
from connection import execute_sql, count_results
from datetime import date
from logger import logger
import struct

class Tree:
    """Initialize tree with dictionary containing parsed json, validate fields. Gives tree a UUID when finished"""
    def __init__(self, json, uid=None):
        self.json = json
        self.location = self.parse_location()
        try:
            self.name = self.json['owner']
            self.species = self.json['species']

            self.images = self.json['images']
            if not isinstance(self.images, list):
                raise TypeError("Images should be an instance of the list type")

            self.plant_date = Date(self.json['plant_date'])

            try:
                self.visits = int(self.json['visits'])
            except ValueError:
                raise ValueError(f"Error converting visits ({self.json['visits']}) field into integers")

            if self.visits < 0:
                raise ValueError(f"visits ({self.visits}) field should not be negative")

        except KeyError as e:
            raise ValueError(f"One or more required fields missing {e}")

        #Everything is good, assign the tree a UUID if it exists, otherwise keep the old one
        self.uid = uid if uid else str(uuid.uuid4())

    def to_json(self):
        json =  {
                'tree_id' : self.uid,
                'owner' : self.name,
                'plant_date' : str(self.plant_date),
                'species' : self.species,
                'images' : self.images,
                'visits' : self.visits
                }
        if self.location:
            json['location'] = self.location.to_json()
        return json

    """Check for Location field in JSON, returns either None if not found or two tuple of floats if field exists. Performs verification of data"""
    def parse_location(self):
        # Check if optional location field exists
        # Style + Efficiency: return early if nothing needs to be done
        if "location" not in self.json:
            return None

        # Fetch field, confirm that there are 
        # A: two named fields (latitude and longitude) that are floats 
        # B: The values of these floats are valid longitude and latitude values

        location = self.json.get("location")
        if location is None:
            return None

        # Handle special point
        if not isinstance(location, dict):
            try:
                ewkb = location
                if isinstance(ewkb, str):
                    ewkb = bytes(ewkb, 'ascii')
                lat, lon = self.parse_ewkb(ewkb)
            except ValueError as e:
                raise e
        else:
            if not {"latitude", "longitude"}.issubset(location.keys()):
                    raise ValueError("Location data does not contain latitude and longitude keys")
            try:
                lat, lon = float(location.get("latitude")), float(location.get("longitude"))
            except ValueError:
                raise ValueError(f"Location data {location} are not floats")

        if ((abs(lat) - 90.0 > TOLERANCE) or
            (abs(lon) - 180.0 > TOLERANCE)):
            raise ValueError(f"Invalid location data {lat} {lon}")

        return Location(lat=lat, long=lon)

    def parse_ewkb(self, ewkb_data):
        # Check byte order
        byte_order = ewkb_data[0]
        if byte_order == 0x01:
            endian = '<'
        elif byte_order == 0x00:
            endian = '>'
        else:
            raise ValueError("Unknown byte order")

        typ = struct.unpack(endian + 'I', ewkb_data[1:5])[0]
        if typ != 1:
            raise ValueError("Not a 2D Point")

        start = 9

        # These are always little endian for some reason?
        long = struct.unpack('<d', ewkb_data[start: start + 8])[0]
        lat = struct.unpack('<d', ewkb_data[start + 8: start + 2 * 8])[0]

        return lat, long 
    
    def save(self):
        execute_sql("DELETE FROM tree WHERE tree_id=%(uid)s", {"uid": self.uid})
        execute_sql("DELETE FROM tree_images WHERE tree_id=%(uid)s", {"uid": self.uid})

        execute_sql(("INSERT INTO tree (tree_id, location, species, owner, plant_date, visits) " # Query
            f"VALUES (%(tree_id)s, {'POINT(%(location_x)s, %(location_y)s)' if self.location else 'NULL'}, %(species)s, %(owner)s, %(plant_date)s, %(visits)s)"), # Params
            {"tree_id": self.uid, "location_x": self.location.longitude if self.location else None, "location_y": self.location.latitude if self.location else None,
             "species": self.species, "owner": self.name, "plant_date": self.plant_date.to_date(), "visits": self.visits}) # Filled params
        
        for image in self.images:
            if execute_sql("SELECT * FROM images WHERE url=%(url)s", {"url": image}, callback=count_results, commit=False) == 0:
                execute_sql("INSERT INTO images (url) VALUES (%(url)s)", {"url": image}) 
                logger.info(f"Inserted new image: {image}")

            execute_sql("INSERT INTO tree_images (url, tree_id) VALUES (%(url)s, %(tree_id)s)", {"url": image, "tree_id": self.uid}) 

class Location:
    def __init__(self, *, lat, long):
        self.latitude = lat
        self.longitude = long

    def to_json(self):
        return {"latitude": self.latitude, "longitude": self.longitude}


class Date:
    def __init__(self, parsing):

        if isinstance(parsing, date):
            self.day = parsing.day
            self.month = parsing.month
            self.year = parsing.year

        else:
            if len(parsing) != 10:
                raise ValueError("Date received in incorrect format (invalid length). Expected `dd/mm/yyyy`")

            self.day = parsing[0:2]
            self.month = parsing[3:5]
            self.year = parsing[6:10]

            if not (self.day.isdigit() and self.month.isdigit() and self.year.isdigit()):
                raise ValueError("Date received in incorrect format. Expected `dd/mm/yyyy`")

    def __str__(self):
        return f"{self.day}/{self.month}/{self.year}"
    
    def to_date(self):
        return date(int(self.year), int(self.month), int(self.day))
