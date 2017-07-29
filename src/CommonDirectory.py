import csv
from datetime import datetime
from datetime import timedelta
from collections import defaultdict

from src.TimePeriod import timePeriod
from src.CommonParameter import commonParameter as cpara



class commonDirectory:

    dict_NationalityToNum = {'国内':0, '国际':1}

    # dict_PlaneIDToType = {}

    dict_NumToNationality = {0:'国内', 1:'国际'}

    dict_InfluenceToNum = {'降落':0, '起飞':1, '停机':2}

    newLineID = 9001

    # dict_FlightTimeCost = {}

    @staticmethod
    def planeID_totype(planeID):
        with open("../Scenario/Xiahang_Airline.csv", encoding="gbk") as f:
            data = csv.reader(f)
            head = next(data)
            for row in data:
                if row[8] == str(planeID):
                    return row[9]
        raise ValueError("plane ID connot be found in Xiahang_Airline.csv")

    @staticmethod
    def flight_timecost(PlaneType, DepartureAirport, LandAirport):
        """
        get the timecost of a flight based on planetype, start and end airport
        all data could be found in Xiahang_FlightTime.csv
        :param PlaneType: int
        :param DepartureAirport: int
        :param LandAirport: int
        :return: int
        """
        with open("../Scenario/Xiahang_FlightTime.csv", encoding="gbk") as f:
            data = csv.reader(f)
            head = next(data)
            for row in data:
                if row[0:3] == [str(PlaneType), str(DepartureAirport), str(LandAirport)]:
                    return timedelta(minutes = int(row[3]))
            return False

    @staticmethod
    def midairport_search(PlaneType, DepartureAirport, LandAirport, exclude_set = ["49", "50", "61"]):
        reservedLand_set = []
        reservedDeparture_set = []
        timecost_dict = defaultdict(int)
        with open("../Scenario/Xiahang_FlightTime.csv", encoding="gbk") as f:
            data = csv.reader(f)
            head = next(data)
            for row in data:
                if row[0] == PlaneType:
                    if row[1] == DepartureAirport:
                        reservedLand_set.append(row[2])
                        timecost_dict[row[1] + row[2]] = int(row[3])
                    if row[2] == LandAirport:
                        reservedDeparture_set.append(row[1])
                        timecost_dict[row[1] + row[2]] = int(row[3])
            print(reservedLand_set, reservedDeparture_set)
            possibleAirport_set = list((set(reservedLand_set).union(set(reservedDeparture_set))) \
                            ^(set(reservedLand_set)^set(reservedDeparture_set)))
            min_timecost = 9999
            best_airportID = None
            real_possibleAirport_set = [i for i in possibleAirport_set if i not in exclude_set]
            for airportID in real_possibleAirport_set:
                if timecost_dict[DepartureAirport+airportID] + timecost_dict[airportID+LandAirport] < min_timecost:
                    min_timecost = timecost_dict[DepartureAirport+airportID] + timecost_dict[airportID+LandAirport]
                    best_airportID = airportID
        return best_airportID, min_timecost

    @staticmethod
    def get_cur_newlineID():
        """
        get the current new airline ID and increase it after used.
        :return: 
        """
        commonDirectory.newLineID  = commonDirectory.newLineID + 1
        return commonDirectory.newLineID - 1


if __name__ == '__main__':
    print(commonDirectory.flight_timecost(3, 49, 5))
    start = datetime.strptime("05/05/2017 15:25", cpara.DATETIME_FORM)
    end = start + timedelta(minutes= 70)
    print((end - start).__class__)
    print(timePeriod(start.strftime(cpara.DATETIME_FORM), (end+timedelta(minutes=50)).strftime(cpara.DATETIME_FORM)))

    print(commonDirectory.midairport_search("4", "36", "25"))




