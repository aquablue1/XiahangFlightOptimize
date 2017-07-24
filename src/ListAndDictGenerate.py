from src.AirLine import airLine, form_airlines
from src.TyphoonInfluence import typhoonInfluence, form_typhoon_accidents
from src.TimePeriod import timePeriod
from src.PlaneJobLine import planeJobLine
from src.CommonParameter import commonParameter as cpara
from src.CommonDirectory import commonDirectory as D
from collections import defaultdict
from datetime import datetime
import csv


def generate_airline():
    return form_airlines()


def generate_accident():
    return form_typhoon_accidents()


def generate_airline_string(airline_set):
    airline_string_dict = {}
    for planeID in list(set([line.LinePlaneID for line in airline_set])):
        airline_string_dict[planeID] = planeJobLine(planeID)
    for airline in airline_set:
        planeid = airline.LinePlaneID
        airline_string_dict[planeid].insert_airline(airline)
    return airline_string_dict


def generate_directInfluenced_airline(airline_set, accident_set):
    def is_influenced(airline, accident_set):
        if timePeriod.is_time_intersect(airline.LineFlyPeriod,
                                        accident_set[0].TyphoonForbiddenLand.ForbiddenRuleTimePeriod) \
            and (airline.LineDepartureAirport in [typhoon.TyphoonAirportID for typhoon in accident_set]
                     or airline.LineLandAirport in [typhoon.TyphoonAirportID for typhoon in accident_set]):
            return True
        return False

    influenced_airline_set = []
    influenced_plane_set = []
    for airline in airline_set:
        if is_influenced(airline, accident_set):
            influenced_airline_set.append(airline)
            influenced_plane_set.append(airline.LinePlaneID)
            airline.LineIsInfluenced = 1
    influenced_plane_set = list(set(influenced_plane_set))
    return influenced_airline_set, influenced_plane_set


def generate_plane_set(airline_set):
    return list(set([line.LinePlaneID for line in airline_set]))


def generate_indirectInfluenced_airline(directInfluenced_airline_set, airline_string_dict):
    indirectInfluenced_airline_set = []
    end_append, mid_reset = 0, 0
    for planeID in airline_string_dict.keys():
        lineset = airline_string_dict[planeID].planeFlightList
        start, end = 0, len(lineset)-1
        is_influenced = False
        for i in range(len(lineset)):
            if lineset[i].LineIsInfluenced == 1:
                is_influenced = True
                start = i
                break
        for j in range(len(lineset)):
            if lineset[end - j].LineIsInfluenced == 1:
                is_influenced = True
                end = end - j
                break
        if is_influenced:
            airline_string_dict[planeID].planeInfluencedRange = [start, end]
            for index in range(start, end+1):
                if lineset[index].LineIsInfluenced != 1:
                    lineset[index].LineIsInfluenced = 2
                    mid_reset += 1
                    indirectInfluenced_airline_set.append(lineset[index])
            while True:
                if airline_string_dict[planeID].planeInfluencedRange[1] >= len(lineset)-1:
                    break
                if D.flight_timecost(D.planeID_totype(lineset[start].LinePlaneID),
                                     lineset[start].LineDepartureAirport,
                                     lineset[end].LineLandAirport) is not False:
                    # print(D.planeID_totype(lineset[start].LinePlaneID), lineset[start].LineDepartureAirport, lineset[end].LineLandAirport)
                    break
                end += 1
                airline_string_dict[planeID].planeInfluencedRange[1] = end
                lineset[end].LineIsInfluenced = 2
                end_append += 1
                indirectInfluenced_airline_set.append(lineset[end])
    # print(mid_reset, end_append)
    return indirectInfluenced_airline_set


def generate_influenced_airline_string(airline_string):
    if airline_string.planeFlightList != [] and airline_string.planeInfluencedRange is not None:
        return airline_string.planeFlightList[airline_string.planeInfluencedRange[0]: airline_string.planeInfluencedRange[1]+1]


if __name__ == '__main__':
    airline_head, airline_set = generate_airline()
    typhoon_head, typhoon_set = generate_accident()

    airline_string_dict = generate_airline_string(airline_set)


    directInfluenced_airline_set, influenced_plane_set = generate_directInfluenced_airline(airline_set, typhoon_set)

    indirectInfluenced_airline_set = generate_indirectInfluenced_airline(directInfluenced_airline_set, airline_string_dict)

    print(len(indirectInfluenced_airline_set))

    """    
    for planeid in airline_string_dict.keys():
        print(planeid, end=" : ")
        for line in airline_string_dict[planeid].planeFlightList:
            print(line.LineIsInfluenced, end=" -> ")
        print("")
    """

    for plane in airline_string_dict.keys():
        cow_count = 9001
        lineset = airline_string_dict[plane].planeFlightList
        with open(cpara.PATH_OUTPUT, 'a', newline='') as f:
            f_csv = csv.writer(f)
            for line in lineset:
                if line.LineIsInfluenced == 0:
                    row = [line.LineID,
                           line.LineDepartureAirport,
                           line.LineLandAirport,
                           line.LineFlyPeriod.start.strftime(cpara.OUTPUT_DATETIME_FORM),
                           line.LineFlyPeriod.end.strftime(cpara.OUTPUT_DATETIME_FORM),
                           line.LinePlaneID,
                           0, 0, 0]
                else:
                    row = [line.LineID,
                           line.LineDepartureAirport,
                           line.LineLandAirport,
                           line.LineFlyPeriod.start.strftime(cpara.OUTPUT_DATETIME_FORM),
                           line.LineFlyPeriod.end.strftime(cpara.OUTPUT_DATETIME_FORM),
                           line.LinePlaneID,
                           1, 0, 0]
                f_csv.writerow(row)

            if airline_string_dict[plane].planeInfluencedRange is not None:
                start = airline_string_dict[plane].planeInfluencedRange[0]
                end = airline_string_dict[plane].planeInfluencedRange[1]
                if lineset[start].LineDepartureAirport != lineset[end].LineLandAirport:
                    row = [cow_count,
                           lineset[start].LineDepartureAirport,
                           lineset[end].LineLandAirport,
                           lineset[start].LineFlyPeriod.start.strftime(
                               cpara.OUTPUT_DATETIME_FORM),
                           (lineset[start].LineFlyPeriod.start +
                            D.flight_timecost(
                                D.planeID_totype(lineset[start].LinePlaneID),
                                lineset[start].LineDepartureAirport,
                                lineset[end].LineLandAirport,
                                )).strftime(cpara.OUTPUT_DATETIME_FORM),
                           airline_string_dict[plane].planeID,
                           0, 0, 1
                           ]
                    cow_count += 1
                    f_csv.writerow(row)


