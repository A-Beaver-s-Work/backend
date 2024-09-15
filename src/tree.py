import uuid
TOLERANCE = 0.0001
from connection import execute_sql, count_results
from datetime import date
from logger import logger

class Tree:
    """Initialize tree with dictionary containing parsed json, validate fields. Gives tree a UUID when finished"""
    def __init__(self, json, uid=None):
        self.json = json
        self.location = self.parseLocation()
        try:
            self.name = self.json['owner']
            self.type = self.json['type']

            self.images = self.json['images']
            if not isinstance(self.images, list):
                raise TypeError("Images should be an instance of the list type")

            self.date = Date(self.json['date'])

            try:
                self.visits = int(self.json['visits'])
            except ValueError:
                raise ValueError(f"Error converting visits ({self.json['visits']}) field into integers")

            if self.visits < 0:
                raise ValueError(f"visits ({self.visits}) field should not be negative")

        except KeyError:
            raise ValueError("One or more required fields missing")

        #Everything is good, assign the tree a UUID if it exists, otherwise keep the old one
        self.uid = uid if uid else str(uuid.uuid4())

    """Check for Location field in JSON, returns either None if not found or two tuple of floats if field exists. Performs verification of data"""
    def parseLocation(self):
        # Check if optional location field exists
        # Style + Efficiency: return early if nothing needs to be done
        if "location" not in self.json:
            return None

        # Fetch field, confirm that there are 
        # A: two named fields (latitude and longitude) that are floats 
        # B: The values of these floats are valid longitude and latitude values

        location = self.json.get("location")
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
    
    def save(self):
        execute_sql("DELETE FROM tree WHERE tree_id=%(uid)s", {"uid": self.uid})
        execute_sql("DELETE FROM tree_images WHERE tree_id=%(uid)s", {"uid": self.uid})

        execute_sql(("INSERT INTO tree (tree_id, location, breed, owner, date_planted, visits) " # Query
            f"VALUES (%(tree_id)s, {'POINT(%(location_x)s, %(location_y)s)' if self.location else 'NULL'}, %(breed)s, %(owner)s, %(date)s, %(visits)s)"), # Params
            {"tree_id": self.uid, "location_x": self.location.longitude if self.location else None, "location_y": self.location.latitude if self.location else None,
             "breed": self.type, "owner": self.name, "date": date(int(self.date.year), int(self.date.month), int(self.date.day)), "visits": self.visits}) # Filled params
        
        for image in self.images:
            if execute_sql("SELECT * FROM images WHERE url=%(url)s", {"url": image}, callback=count_results, commit=False) == 0:
                execute_sql("INSERT INTO images (url) VALUES (%(url)s)", {"url": image}) 
                logger.info(f"Inserted new image: {image}")

            execute_sql("INSERT INTO tree_images (url, tree_id) VALUES (%(url)s, %(tree_id)s)", {"url": image, "tree_id": self.uid}) 

class Location:
    def __init__(self, *, lat, long):
        self.latitude = lat
        self.longitude = long

class Date:
    def __init__(self, parsing):
        if len(parsing) != 10:
            raise ValueError("Date received in incorrect format (invalid length). Expected `dd/mm/yyyy`")

        self.day = parsing[0:2]
        self.month = parsing[3:5]
        self.year = parsing[6:10]

        if not (self.day.isdigit() and self.month.isdigit() and self.year.isdigit()):
            raise ValueError("Date received in incorrect format. Expected `dd/mm/yyyy`")
