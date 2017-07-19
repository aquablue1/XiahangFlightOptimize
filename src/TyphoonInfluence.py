from src.TimePeriod import timePeriod
from src.CommonDirectory import commonDirectory as D
import csv


class typhoonForbiddenRule:
    def __init__(self, rule):
        if len(rule) != 4:
            raise ValueError("length of forbidden rule is not 6")
        self.ForbiddenRuleType = D.dict_InfluenceToNum[rule[2]]
        self.ForbiddenRuleTimePeriod = timePeriod(rule[0], rule[1])


class typhoonInfluence:
    def __init__(self, typhoon_info):
        if len(typhoon_info) != 4:
            raise ValueError("length of typhoon_info is not 4")
        self.TyphoonAirportID = typhoon_info[3]
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


if __name__ == '__main__':
    with open("../Scenario/Xiahang_TyphoonSituation.csv", encoding="gbk") as f:
        data = csv.reader(f)
        head = next(data)
        typhoonInfluenceSet = []
        for row in data:
            for situation in typhoonInfluenceSet:
                if row[3] == situation.TyphoonAirportID:
                    situation.add_forbiddenrule(typhoonForbiddenRule(row[0:4]))
                    continue
            typhoonInfluenceSet.append(typhoonInfluence(row[0:4]))
    print(typhoonInfluenceSet)