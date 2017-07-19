from src.TimePeriod import timePeriod
from src.CommonDirectory import commonDirectory as D


class typhoonForbiddenRule:
    def __init__(self, rule):
        self.ForbiddenRuleType = D.dict_InfluenceToNum[rule[2]]
        self.ForbiddenRuleTimePeriod = timePeriod(rule[0], rule[1])


class typhoonInfluence:
    def __init__(self, typhoon_info):
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