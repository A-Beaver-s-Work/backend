import random
import uuid
import requests

URL = "http://127.0.0.1:5000/api/v1/"

#latitude: -90.0 to 90.0
#longitude: -180.0 to 180.0

firstNames = [
    "Liam", "Noah", "Oliver", "Elijah", "James",
    "William", "Benjamin", "Lucas", "Henry", "Alexander",
    "Mason", "Michael", "Ethan", "Daniel", "Jacob",
    "Logan", "Jackson", "Sebastian", "Aiden", "Matthew",
    "Avery", "Sophia", "Isabella", "Charlotte", "Amelia",
    "Olivia", "Emma", "Aiden", "Mia", "Harper",
    "Evelyn", "Abigail", "Ella", "Scarlett", "Grace",
    "Chloe", "Camila", "Aria", "Aurora", "Sofia",
    "Emily", "Luna", "Madison", "Layla", "Riley",
    "Zoe", "Nora", "Hannah", "Lily", "Ellie"
]
lastNames = [
    "Smith", "Johnson", "Williams", "Jones", "Brown",
    "Davis", "Miller", "Wilson", "Moore", "Taylor",
    "Anderson", "Thomas", "Jackson", "White", "Harris",
    "Martin", "Thompson", "Garcia", "Martinez", "Robinson",
    "Clark", "Rodriguez", "Lewis", "Lee", "Walker",
    "Hall", "Allen", "Young", "King", "Wright",
    "Scott", "Torres", "Nguyen", "Hill", "Flores",
    "Green", "Adams", "Nelson", "Baker", "Carter",
    "Mitchell", "Perez", "Roberts", "Turner", "Phillips",
    "Campbell", "Parker", "Evans", "Edwards", "Collins"
]
trees = [
    "Oak", "Maple", "Pine", "Birch", "Spruce",
    "Fir", "Cedar", "Redwood", "Willow", "Elm",
    "Hickory", "Chestnut", "Poplar", "Aspen", "Cherry",
    "Walnut", "Beech", "Sycamore", "Mahogany", "Teak",
    "Douglas Fir", "Linden", "Holly", "Olive", "Gingko",
    "Cottonwood", "Magnolia", "Persimmon", "Alder", "Juniper",
    "Eucalyptus", "Ponderosa Pine", "American Holly", "Black Walnut", "Horse Chestnut"
]

def makeTree():
    #get lat.
    lat = random.randint(-90_000, 90_000) / 1000.0
    lon = random.randint(-180_000, 180_000) / 1000.0
    name = f"{random.choice(firstNames)} {random.choice(lastNames)}"
    age = random.randint(8, 100)
    species = random.choice(trees)
    visits = random.randint(0, 100)
    url = [f"example.com/api/v1/images/{uuid.uuid4()}.jpg" for _ in range(random.randint(1, 10))]
    return {
            "location": [lat, lon],
            "type": species,
            "owner": name,
            "age": age,
            "visits": visits,
            "images": url
            }

def createTree(tree = None):
    postUrl = URL + "trees"
    if tree is None:
        tree = makeTree()
    response = requests.post(postUrl, json=tree)
    print(response.status_code)
    print(response.json())

def listTrees():
    postUrl = URL + "trees"
    response = requests.get(postUrl)
    print(response.status_code)
    print(response.json())


