import uuid
TOLERANCE = 0.0001

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

            try:
                self.age = int(self.json['age'])
                self.visits = int(self.json['visits'])
            except ValueError:
                raise ValueError(f"Error converting age ({self.json['age']}) and visits ({self.json['visits']}) fields into integers")

            if ((self.age < 0) or (self.visits < 0)):
                raise ValueError(f"age ({self.age}) and visits ({self.visits}) fields should not be negative")

        except KeyError:
            raise ValueError("One or more required fields missing")

        #Everything is good, assign the tree a UUID if it exists, otherwise keep the old one
        if uid is None:
            self.uid = uuid.uuid4()
        else:
            self.uid = uid

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

class Location:
    def __init__(self, *, lat, long):
        self.latitude = lat
        self.longitude = long
