from datetime import datetime
from src.commonDirectory import *
from src.TimePeriod import timePeriod


class airLine:
    def __init__(self, line_info):
        if len(line_info) != 11:
            raise ValueError("line_info length is not 11")
        self.LineID = line_info[0]
        self.LineDate = datetime.strptime(line_info[1], '%Y/%m/%d')
        self.LineType = dict_NationalityToNum[line_info[2]]
        self.LineNum = line_info[3]
        self.LineDepartureAirport = line_info[4]
        self.LineLandAirport = line_info[5]
        self.LineFlyPeriod = timePeriod(line_info[6], line_info[7])  # departure and land time.
        self.LinePlaneID = line_info[8]
        # self.LinePlaneType = line_info[9]  #igore the plane type
        self.LineIF = line_info[10]  # IF: influence factor


    def reconstruct_list(self):
        """
        return a list of a flight with original information type
        :return: list
        """
        rtl = []
        rtl.append(self.LineID)
        rtl.append(self.LineDate.strftime('%Y/%m/%d'))
        rtl.append(dict_NumToNationality[self.LineType])
        rtl.append(self.LineNum)
        rtl.append(self.LineDepartureAirport)
        rtl.append(self.LineLandAirport)
        rtl.append(self.LineFlyPeriod.start.strftime('%Y/%m/%d %H:%M'))
        rtl.append(self.LineFlyPeriod.end.strftime('%Y/%m/%d %H:%M'))
        rtl.append(self.LinePlaneID)
        rtl.append(dict_PlaneIDToType[self.LinePlaneID])
        rtl.append(self.LineIF)
        return rtl


