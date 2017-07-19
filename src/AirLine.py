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
        self.LineNum = int(line_info[3])
        self.LineDepartureAirport = int(line_info[4])
        self.LineLandAirport = int(line_info[5])
        self.LineFlyPeriod = timePeriod(line_info[6], line_info[7])  # departure and land time.
        self.LinePlaneID = int(line_info[8])
        # self.LinePlaneType = line_info[9]  #igore the plane type
        self.LineIF = float(line_info[10])  # IF: influence factor


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


if __name__ == '__main__':
    with open("../Scenario/Xiahang_Airline.csv") as f:
        data = csv.reader(f)
        head = next(data)
        airlineSet = []
        for row in data:
            airlineSet.append(airLine(row))
        print(airlineSet[1].LineDate.date())

