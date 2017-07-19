from src.AirLine import airLine
from src.commonDirectory import *


class connectingFlight:
    def __init__(self, firLine, secLine):
        if firLine.LineNum != secLine.LineNum:
            raise ValueError("connecting flight needs same line num")
        elif firLine.LineDate != secLine.LineDate:
            raise ValueError("connecting flight needs same date")
        elif firLine.LinePlaneID != secLine.LinePlaneID:
            raise ValueError("connecting flight needs same planeID")

        self.FlightID = firLine.LineNum
        self.FlightDate = firLine.LineDate
        self.FlightPlaneID = firLine.LinePlaneID
        self.FlightDeparture = firLine.LineDepartureAirport
        self.FlightLand = secLine.LineLandAirport
        self.FlightType = firLine.LineType + secLine.LineType - firLine.LineType * secLine.LineType
        # mark 1 if one of the flight is international else 0

        self.FlightInfo = [firLine, secLine]
        self.FlightIF = firLine.LineIF + secLine.LineIF


    def flight_straighten(self):
        newLine = []
        newLine.append(newLineID)
        newLine.append(self.FlightDate.strftime('%Y/%m/%d'))
        if self.FlightType == 1:
            raise ValueError("illegal to connecting an international airline")
        newLine.append(dict_NumToNationality[self.FlightType])
        newLine.append(self.FlightID)
        newLine.append(self.FlightDeparture)
        newLine.append(self.FlightLand)
        newLine.append(self.FlightInfo[0].LineFlyPeriod.start.strftime('%Y/%m/%d %H:%M'))
        newLine.append(self.LineFlyPeriod.end.strftime('%Y/%m/%d %H:%M'))
        newLine.append(self.FlightPlaneID)
        newLine.append(dict_PlaneIDToType[self.FlightPlaneID])
        newLine.append(self.FlightIF)
        return newLine
