from src.CommonDirectory import commonDirectory as D
from src.AirLine import airLine
import csv

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
        if self.planeID != newAirline.LinePlaneID:
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


if __name__ == '__main__':
    with open("../Scenario/Xiahang_Airline.csv") as f:
        data = csv.reader(f)
        head = next(data)
        airlineSet = []
        plane1Set = planeJobLine(90)
        for row in data:
            if row[8] == '90':
                plane1Set.insert_airline(airLine(row))
        for line in plane1Set.planeFlightList:
            print(line.LineFlyPeriod)