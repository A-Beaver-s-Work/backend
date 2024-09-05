import uuid
TOLERANCE = 0.0001

class Tree():
    """Initialize tree with dictionary containing parsed json, validate fields. Gives tree a UUID when finished"""
    def __init__(self, json, treeID=None):
        self.json = json
        self.location = self.parseLocation()
        try:
            self.name = self.json['owner']
            self.type = self.json['type']
            #skip validation on this for now
            self.images = self.json['images']
            try:
                self.age = int(self.json['age'])
                self.visits = int(self.json['visits'])
            except ValueError:
                raise ValueError("Error converting age ({age}) and visits ({visists}) fields into integers")

            if ((self.age < 0) or (self.visits < 0)):
                raise ValueError("age ({age}) and visits ({visits}) fields should not be negative")

        except KeyError:
            raise ValueError("One or more required fields missing")

        #Everything is good, assign the tree a UUID if it exists, otherwise keep the old one
        if treeID is None:
            self.treeID = uuid.uuid4()
        else:
            self.treeID = treeID

    """Check for Location field in JSON, returns either None if not found or two tuple of floats if field exists. Performs verification of data"""
    def parseLocation(self):
        # Check if optional location field exists
        if "location" in self.json:
            # Fetch field, confirm that there are 
            # A: Two floats inside this field
            # B: The values of these floats are valid longitude and latitude values
            toCheck = self.json["location"]
            if len(toCheck) != 2:
                raise ValueError("Location data {toCheck} is not two floats or unspecified")
            try:
                lat, lon = float(toCheck[0]), float(toCheck[1])
            except ValueError:
                raise ValueError("Location data {toCheck} are not floats")

            if ((abs(lat) - 90.0 > TOLERANCE) or
                (abs(lon) - 180.0 > TOLERANCE)):
                raise ValueError(f"Invalid location data {lat} {lon}")

            location = (lat, lon)
        # Go the easy way if user does not report location
        else:
            location = None

        return location


