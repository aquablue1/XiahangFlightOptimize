from src.TimePeriod import timePeriod
from src.CommonDirectory import commonDirectory as D
import csv
from src.CommonParameter import commonParameter as cpara


class typhoonForbiddenRule:
    def __init__(self, rule):
        if len(rule) != 4:
            raise ValueError("length of forbidden rule is not 6")
        self.ForbiddenRuleType = D.dict_InfluenceToNum[rule[2]]
        self.ForbiddenRuleTimePeriod = timePeriod(rule[0], rule[1])

    def __str__(self):
        output = "forbidden time period: " + str(self.ForbiddenRuleTimePeriod) + ". forbidden type: " + str(self.ForbiddenRuleType)
        return output

class typhoonInfluence:
    def __init__(self, typhoonInfluenceAirportID):
        self.TyphoonAirportID = typhoonInfluenceAirportID
        self.TyphoonForbiddenLand = None
        self.TyphoonForbiddenDeparture = None
        self.TyphoonForbiddenStop = None

    def add_forbiddenrule(self, forbiddenRule):
        if forbiddenRule.ForbiddenRuleType == 0:
            self.TyphoonForbiddenLand = forbiddenRule
        elif forbiddenRule.ForbiddenRuleType == 1:
            self.TyphoonForbiddenDeparture = forbiddenRule
        elif forbiddenRule.ForbiddenRuleType == 2:
            self.TyphoonForbiddenStop = forbiddenRule


def form_typhoon_accidents():
    influencdeAirportIDSet = []
    with open(cpara.PATH_TYPHOON, encoding="gbk") as f:
        data = csv.reader(f)
        head = next(data)
        for row in data:
            if row[3] not in influencdeAirportIDSet:
                influencdeAirportIDSet.append(row[3])
    # print(influencdeAirportIDSet)
    typhoonInfluenceSet = []
    for airportID in influencdeAirportIDSet:
        typhoonInfluenceSet.append(typhoonInfluence(airportID))
    with open(cpara.PATH_TYPHOON, encoding="gbk") as f:
        data = csv.reader(f)
        head = next(data)
        for row in data:
            for situation in typhoonInfluenceSet:
                if row[3] == situation.TyphoonAirportID:
                    situation.add_forbiddenrule(typhoonForbiddenRule(row[0:4]))
                    break
    return head, typhoonInfluenceSet


if __name__ == '__main__':
    with open(cpara.PATH_TYPHOON, encoding="gbk") as f:
        data = csv.reader(f)
        head = next(data)
        typhoonInfluenceSet = []
        for row in data:
            print(row[3])
            continueFlag = False
            for situation in typhoonInfluenceSet:
                if row[3] == str(situation.TyphoonAirportID):
                    situation.add_forbiddenrule(typhoonForbiddenRule(row[0:4]))
                    continueFlag = True
                    break
            if continueFlag:
                continue
            typhoonInfluenceSet.append(typhoonInfluence(row[0:4]))
    # return head, typhoonInfluenceSet
