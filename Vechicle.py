from typing import Any
# import numpy as pynum

class Vehicle:
    # car details
    carModel = "Sedan"
    carMake = "Honda"
    carYear = 2022
    carID = 1234

    # car trunk dimensions
    trunkLength = 0
    trunkWidth = 0
    trunkHeight = 0

    # weight limit in cubic feet
    carThreshold = 0

    def __init__(self, carModel, carMake, carYear, carID, trunkLength, trunkWidth, trunkHeight, carThreshold):
        self.carID = carID
        self.carMake = carMake
        self.carModel = carModel
        self.carYear = carYear
        self.boxes = []
        if (trunkHeight > 0 and trunkLength > 0 and trunkWidth > 0 and carThreshold > 0):
            self.trunkHeight = trunkHeight
            self.trunkLength = trunkLength
            self.trunkWidth = trunkWidth
            self.carThreshold = carThreshold

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

class box:
        # measurements are in inches
    def __init__(self,length, width,height,weight, deliveryID):
        self.deliveryID = deliveryID
        self.length = length
        self.width = width
        self.height = height
        self.weight = weight    

class Delivery:
    def __init__(location, ) -> None:
        pass
v1 = Vehicle("Sedan", "Honda", 2022, 5678, 60, 40, 20, 2000)

box1 = box(10, 20, 15, 500, 1)
box2 = box(15, 30, 20, 800, 2)
box3 = box(12, 25, 18, 700, 3)
v1.add_box(box1)
v1.add_box(box2)
v1.add_box(box3)
print(f"Total weight in the trunk: {v1.calculate_total_weight()} lbs")
print(f"Number of boxes in the trunk: {len(v1.boxes)}")
