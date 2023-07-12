from typing import Any
# import numpy as pynum

class Vehicle:
    # car details
    carModel = "Sedan"
    carMake = "Honda"
    carYear = 2022
    vehicleID = 1234

    # car trunk dimensions
    trunkLength = 0
    trunkWidth = 0
    trunkHeight = 0

    # weight limit in cubic feet
    carThreshold = 0

    def __init__(self, carModel, carMake, carYear, vehicleID, trunkLength, trunkWidth, trunkHeight, carThreshold):
        self.vehicleID = vehicleID
        self.carMake = carMake
        self.carModel = carModel
        self.carYear = carYear
        self.boxes = []
        if (trunkHeight > 0 and trunkLength > 0 and trunkWidth > 0 and carThreshold > 0):
            self.trunkHeight = trunkHeight
            self.trunkLength = trunkLength
            self.trunkWidth = trunkWidth
            self.carThreshold = carThreshold

    def getMaxCarThreshold(self):
        return self.carThreshold
    
    def getBoxes(self):
        return len(self.boxes)
    
    # returns cubic volueme feet
    def calculateTrunkSpace(self, trunkL, trunkW, trunkH):
        return trunkL*trunkW*trunkH
    
    def calculate_total_weight(self):
        total_weight = 0
        for box in self.boxes:
            total_weight += box.weight
        return total_weight
    
    def add_box(self, box):
        # self.boxes.append(box)
        if self.calculate_total_weight() + box.weight <= self.carThreshold:
            self.boxes.append(box)
            return True
        return False

class Driver:
    def __init__(self, userID, firstName, lastName, individualWeight, vehicleID, packageLocale, personalBelongingWeight):
        self.userID = userID
        self.firstName = firstName
        self.lastName = lastName
        self.individualWeight = individualWeight
        self.vehicleID = vehicleID
        self.packageLocale = packageLocale
        self.personalBelongingWeight = personalBelongingWeight

    def getIndividualWeight(self):
        return self.individualWeight

class box:
        # measurements should be in inches
    def __init__(self, length, width, height, weight, deliveryID):
        self.deliveryID = deliveryID
        self.length = length
        self.width = width
        self.height = height
        self.weight = weight  

    def getWeight(self):
        return self.weight

class Delivery:
    def __init__(self, location, driverID, vehicleID):
        self.location = location
        self.driverID = driverID
        self.vehicleID = vehicleID
        self.boxes = []

    def calculateTotalWeight(self, driverWeight, personalPackageWeight):
        totalWeight = 0
        for box in self.boxes:
            totalWeight += box.weight
        return totalWeight + driverWeight + personalPackageWeight
    

        
#data flow:
#app --> algo --> database --> algo --> app
#warehouse --> driver(job) --> select car --> algo generate ideal layout 

v1 = Vehicle("Sedan", "Honda", 2022, 5678, 60, 40, 20, 2000)

box1 = box(10, 20, 15, 500, 1)
box2 = box(15, 30, 20, 800, 2)
box3 = box(12, 25, 18, 700, 3)
v1.add_box(box1)
v1.add_box(box2)
v1.add_box(box3)
print(f"Total weight in the trunk: {v1.calculate_total_weight()} lbs")
print(f"Number of boxes in the trunk: {len(v1.boxes)}")

def assign_packages(vehicles, packages):
    assigned_packages = []
    for vehicle in vehicles:
        assigned_packages.append({
            'vehicle': vehicle,
            'packages': []
        })

    for package in packages:
        added_to_vehicle = False
        for assigned_vehicle in assigned_packages:
            if assigned_vehicle['vehicle'].add_package(package):
                assigned_vehicle['packages'].append(package.package_id)
                added_to_vehicle = True
                break
        if not added_to_vehicle:
            print(f"Package with ID {package.package_id} cannot fit in any vehicle.")

    return assigned_packages


# Example usage
vehicles = [
    Vehicle(1, 'New York', 101, 60, 40, 20, 1, 2000),
    Vehicle(2, 'Los Angeles', 102, 70, 50, 25, 3, 2500)
]
class Package:
    def __init__(self, package_id, dimensions, weight):
        self.package_id = package_id
        self.dimensions = dimensions
        self.weight = weight

packages = [
    Package(package_id=1, dimensions=(10, 20, 15), weight=500),
    Package(package_id=2, dimensions=(15, 30, 20), weight=800),
    Package(package_id=3, dimensions=(12, 25, 18), weight=700),
    Package(package_id=4, dimensions=(20, 30, 25), weight=1200),
    Package(package_id=5, dimensions=(18, 28, 22), weight=1000)
]
assigned_packages = assign_packages(vehicles, packages)
