from src.AirLine import airLine
import csv

class influncedAirLine(airLine):
    def __init__(self, line_info):
        super(influncedAirLine, self).__init__(line_info)


    def printTestInfo(self):
        print(self.LineIF)


if __name__ == '__main__':
    with open("../Scenario/Xiahang_Airline.csv") as f:
        data = csv.reader(f)
        head = next(data)
        airlineSet = []
        airlineSet.append(airLine(next(data)))
        test_airline = airLine(next(data))
    infair = influncedAirLine(airlineSet[0].reconstruct_list())
    infair.printTestInfo()
    print(test_airline.__class__)
    test_airline.__class__ = influncedAirLine
    print(test_airline.__class__)
    test_airline.printTestInfo()
