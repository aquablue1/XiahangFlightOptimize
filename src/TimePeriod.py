from datetime import datetime

class timePeriod:
    def __init__(self, start, end):
        self.start = datetime.strptime(start, '%Y/%m/%d %H:%M')
        self.end = datetime.strptime(end, '%Y/%m/%d %H:%M')

    @staticmethod
    def is_intersect(timeperiod1, timeperiod2):
        if timeperiod1.end < timeperiod2.start or timeperiod2.end < timeperiod1.start:
            return False
        else:
            return True

    def move_ahead(self, time_gap):
        """
        positive time_gap value means move time forword
        :param time_gap: datetime type, mark the gap we want to move
        :return:  None
        """
        self.start += time_gap
        self.end += time_gap