import dateparser


class DateParser:
    def __init__(self):
        self.date_formats=['%d/%m/%Y', '%d/%m']
        self.time_formats=['%H:%M:%s', '%H:%M']
        pass

    def parse(self, date, time=''):
        d = dateparser.parse(date, date_formats=self.date_formats)
        t = dateparser.parse(time, date_formats=self.time_formats)

        if d == None:
            return None

        if not t == None:
            t = t.time()
            d = d.replace(hour=t.hour, minute=t.minute, second=t.second)

        return d


parser = DateParser()
