from datetime import datetime, timedelta
from src.CommonParameter import commonParameter as cpara

class timePeriod:
    def __init__(self, start, end):
        self.start = datetime.strptime(start, cpara.DATETIME_FORM)
        self.end = datetime.strptime(end, cpara.DATETIME_FORM)
        if self.start > self.end:
            raise ValueError("end time is smaller than start time")
        self.time_cost = self.end - self.start

    def __str__(self):
        return_str = "from "+ str(self.start) + " to " + str(self.end)
        return return_str

    @staticmethod
    def is_time_intersect(timeperiod1, timeperiod2):
        if timeperiod1.end <= timeperiod2.start or timeperiod2.end <= timeperiod1.start:
            return False
        else:
            return True

    def is_time_include(self, timestamp):
        if timestamp > self.start and timestamp < self.end:
            return True
        else:
            return False

    def move_ahead(self, time_gap):
        """
        positive time_gap value means move time forword
        value means the minutes we want to move.
        :param time_gap: int type, minutes, mark the gap we want to move
        :return:  None
        """
        time_gap = timedelta(minutes=time_gap)
        self.start += time_gap
        self.end += time_gap


if __name__ == '__main__':
    tp1 = timePeriod("05/05/2017 15:25", "05/06/2017 12:20")
    tp2 = timePeriod("05/04/2017 15:25", "05/05/2017 12:20")
    print(tp1)
    print(timePeriod.is_intersect(tp1, tp2))
    tp1.move_ahead(50)
    print(tp1)
