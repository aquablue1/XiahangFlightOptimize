from datetime import datetime, date
from src.CommonDirectory import commonDirectory as D
from src.CommonParameter import commonParameter as cpara
from src.TimePeriod import timePeriod
import csv


class airLine:
    def __init__(self, line_info):
        if len(line_info) != 11:
            raise ValueError("line_info length is not 11")
        self.LineID = int(line_info[0])
        self.LineDate = datetime.strptime(line_info[1], cpara.DATE_FORM)
        self.LineType = D.dict_NationalityToNum[line_info[2]]
        self.LineTypeDetail = [1,1]
        self.LineNum = int(line_info[3])
        self.LineDepartureAirport = str(line_info[4])
        self.LineLandAirport = str(line_info[5])
        self.LineFlyPeriod = timePeriod(line_info[6], line_info[7])  # departure and land time.
        self.LinePlaneID = str(line_info[8])
        # self.LinePlaneType = line_info[9]  #igore the plane type
        self.LineIF = float(line_info[10])  # IF: influence factor
        self.LineIsInfluenced = 0

    def __str__(self):
        output = "AirlineID: " + str(self.LineID) + ", time: " + str(self.LineFlyPeriod) + \
        ". from "+self.LineDepartureAirport+" to "+self.LineLandAirport+"."
        return output

    def reconstruct_list(self):
        """
        return a list of a flight with original information type
        :return: list
        """
        rtl = []
        rtl.append(self.LineID)
        rtl.append(self.LineDate.strftime(cpara.DATE_FORM))
        rtl.append(D.dict_NumToNationality[self.LineType])
        rtl.append(self.LineNum)
        rtl.append(self.LineDepartureAirport)
        rtl.append(self.LineLandAirport)
        rtl.append(self.LineFlyPeriod.start.strftime(cpara.DATETIME_FORM))
        rtl.append(self.LineFlyPeriod.end.strftime(cpara.DATETIME_FORM))
        rtl.append(self.LinePlaneID)
        rtl.append(D.planeID_totype(self.LinePlaneID))
        rtl.append(self.LineIF)
        return rtl

def form_airportInfoDetail(airlineSet):
    local_airport_set = []
    international_airport_set = []
    airport_set = list(set([line.LineDepartureAirport for line in airlineSet]))
    airport_set_back = list(set([line.LineLandAirport for line in airlineSet]))
    airport_set = list(set(airport_set + airport_set_back))
    for line in airlineSet:
        if line.LineType == 0:
            local_airport_set.append(line.LineDepartureAirport)
            local_airport_set.append(line.LineLandAirport)
    local_airport_set = list(set(local_airport_set))
    # international_airport_set = list(set(airport_set) - set(local_airport_set))
    for line in airlineSet:
        if line.LineDepartureAirport in local_airport_set:
            line.LineTypeDetail[0] = 0
        if line.LineLandAirport in local_airport_set:
            line.LineTypeDetail[1] = 0


def form_airlines():
    with open(cpara.PATH_AIRLINE) as f:
        data = csv.reader(f)
        head = next(data)
        airlineSet = []
        for row in data:
            airlineSet.append(airLine(row))
        form_airportInfoDetail(airlineSet)
        return head, airlineSet


if __name__ == '__main__':
    with open("../Scenario/Xiahang_Airline.csv") as f:
        data = csv.reader(f)
        head = next(data)
        airlineSet = []
        for row in data:
            airlineSet.append(airLine(row))
        print(airlineSet[1].LineDate.date())
        print(airlineSet[0].LineIF)
        form_airportInfoDetail(airlineSet)

