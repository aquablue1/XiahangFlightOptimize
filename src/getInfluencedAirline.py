from src.AirLine import airLine, form_airlines
from src.TyphoonInfluence import typhoonInfluence, form_typhoon_accidents
from src.TimePeriod import timePeriod


if __name__ == '__main__':
    airline_head, airline_set = form_airlines()
    typhoon_head, typhoon_set = form_typhoon_accidents()

    influenced_airline_set = []
    print(typhoon_set[2].TyphoonForbiddenLand)
    for airline in airline_set:
        for typhoon in typhoon_set:
            if timePeriod.is_time_intersect(airline.LineFlyPeriod,
                                            typhoon.TyphoonForbiddenDeparture.ForbiddenRuleTimePeriod):
                influenced_airline_set.append(airline)
                break
    print(len(influenced_airline_set))
    for line in influenced_airline_set:
        print(line)