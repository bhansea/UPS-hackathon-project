class Package:
    deliveryID = 1234
    packHeight = 0
    packWidth = 0
    packLength = 0


    def __init__(self, deliveryID, packHeight, packWidth, packLength):
        self.deliveryID = deliveryID
        self.packHeight = packHeight
        self.packLength = packLength
        self.packWidth = packWidth
    
    def __getPacketHeight__(self):
        return self.packHeight