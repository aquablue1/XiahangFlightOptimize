from src.commonDirectory import commonDirectory as D

class planeJobLine:
    def __init__(self, planeID):
        self.planeID = planeID
        self.planeType = D.planeID_totype(planeID)
        self.planeFlightList = []

    def insert_airline(self, newAirline):
        """
        Insert a new airline based on the time sequence
        :param newAirline: airLine 
        :return: None
        """
        if self.planeID != newAirline.LinePlandID:
            raise ValueError("New airline doesn't belong to target plane job line.")
        if self.planeFlightList == []:
            self.planeFlightList.append(newAirline)
            return
        for index in range(len(self.planeFlightList)):
            if self.planeFlightList[index].LineFlyPeriod.start > newAirline.LineFlyPeriod.end:
                self.planeFlightList.insert(index, newAirline)
                return
        self.planeFlightList.append(newAirline)

    def is_planejobline_illegal(self):
        """
        check if the airline is satisfied the consistency request. means the cur land airport must 
        be the next line's departure airport
        :return: boolean
        """
        if len(self.planeFlightList) <= 1:
            return True
        for cur, next in zip(self.planeFlightList[:-1], self.planeFlightList[1:]):
            if cur.LineLandAirport != next.LineDepartureAirport:
                return False
        return True
