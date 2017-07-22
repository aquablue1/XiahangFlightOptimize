from src.AirLine import airLine, form_airlines
from src.TyphoonInfluence import typhoonInfluence, form_typhoon_accidents
from src.TimePeriod import timePeriod
from src.PlaneJobLine import planeJobLine
from src.CommonParameter import commonParameter as cpara
from src.CommonDirectory import commonDirectory as D
from collections import defaultdict
from datetime import datetime
import csv



if __name__ == '__main__':
    airline_head, airline_set = form_airlines()
    typhoon_head, typhoon_set = form_typhoon_accidents()

    influenced_airline_set = []
    influenced_flight_set = []
    print(typhoon_set[1].TyphoonForbiddenStop)
    for airline in airline_set:
        if timePeriod.is_time_intersect(airline.LineFlyPeriod,
                                        typhoon_set[0].TyphoonForbiddenLand.ForbiddenRuleTimePeriod) \
                and (airline.LineDepartureAirport in [typhoon.TyphoonAirportID for typhoon in typhoon_set]
                     or airline.LineLandAirport in [typhoon.TyphoonAirportID for typhoon in typhoon_set]):
            influenced_airline_set.append(airline)
            airline.LineIsInfluenced=1
            influenced_flight_set.append(airline.LinePlaneID)
    influenced_flight_set = list(set(influenced_flight_set))
    print(len([line for line in airline_set if line.LineIsInfluenced==1]), '\n ----')

    plane_jobline_dict = {}
    for planeID in list(set([line.LinePlaneID for line in airline_set])):
        plane_jobline_dict[planeID] = planeJobLine(planeID)

    for line in influenced_airline_set:
        plane_jobline_dict[line.LinePlaneID].insert_airline(line)

    for line in plane_jobline_dict["3"].planeFlightList:
        print(line)

    with open(cpara.PATH_OUTPUT, 'w', newline='') as f:
        f_csv = csv.writer(f)
        for line in airline_set:
            if line.LineIsInfluenced ==0:
                row = [line.LineID,
                       line.LineDepartureAirport,
                       line.LineLandAirport,
                       line.LineFlyPeriod.start.strftime(cpara.OUTPUT_DATETIME_FORM),
                       line.LineFlyPeriod.end.strftime(cpara.OUTPUT_DATETIME_FORM),
                       line.LinePlaneID,
                       0,0,0
                       ]
            else:
                row = [line.LineID,
                       line.LineDepartureAirport,
                       line.LineLandAirport,
                       line.LineFlyPeriod.start.strftime(cpara.OUTPUT_DATETIME_FORM),
                       line.LineFlyPeriod.end.strftime(cpara.OUTPUT_DATETIME_FORM),
                       line.LinePlaneID,
                       1,0,0
                       ]
            f_csv.writerow(row)

    print("len of plane_jobline_dict.keys() is ", len(plane_jobline_dict.keys()))
    with open(cpara.PATH_OUTPUT, 'a', newline='') as f:
        f_csv = csv.writer(f)
        start = 9001
        for plane in plane_jobline_dict.keys():
            if len(plane_jobline_dict[plane].planeFlightList) == 0:
                continue
            if plane_jobline_dict[plane].planeFlightList[0].LineDepartureAirport == \
                plane_jobline_dict[plane].planeFlightList[-1].LineLandAirport:
                continue
            if D.flight_timecost(D.planeID_totype(plane_jobline_dict[plane].planeFlightList[0].LinePlaneID),
                                      plane_jobline_dict[plane].planeFlightList[0].LineDepartureAirport,
                                      plane_jobline_dict[plane].planeFlightList[-1].LineLandAirport) is False:
                continue
            print(D.planeID_totype(plane_jobline_dict[plane].planeFlightList[0].LinePlaneID))
            print(plane_jobline_dict[plane].planeFlightList[0].LineDepartureAirport)
            print(plane_jobline_dict[plane].planeFlightList[-1].LineLandAirport, '\n---')
            row = [start,
                   plane_jobline_dict[plane].planeFlightList[0].LineDepartureAirport,
                   plane_jobline_dict[plane].planeFlightList[-1].LineLandAirport,
                   plane_jobline_dict[plane].planeFlightList[0].LineFlyPeriod.start.strftime(cpara.OUTPUT_DATETIME_FORM),
                   (plane_jobline_dict[plane].planeFlightList[0].LineFlyPeriod.start+
                    D.flight_timecost(D.planeID_totype(plane_jobline_dict[plane].planeFlightList[0].LinePlaneID),
                                      plane_jobline_dict[plane].planeFlightList[0].LineDepartureAirport,
                                      plane_jobline_dict[plane].planeFlightList[-1].LineLandAirport,
                    )).strftime(cpara.OUTPUT_DATETIME_FORM),
                   plane_jobline_dict[plane].planeID,
                   0,0,1
            ]
            start += 1
            f_csv.writerow(row)

