from ..date_parser import parser

class TestDateParser:

    def test_get_none_if_invalid(self):
        d = parser.parse('invalid')
        assert d == None

    def test_only_date(self):
        d = parser.parse('12/02/1997')
        assert d.day == 12
        assert d.month == 2
        assert d.year == 1997

    def test_only_date_without_year(self):
        d = parser.parse('15/05')
        assert d.day == 15
        assert d.month == 5

    def test_date_and_time(self):
        d = parser.parse('01/07/1997', '13:52')
        assert d.day == 1
        assert d.month == 7
        assert d.year == 1997
        assert d.hour == 13
        assert d.minute == 52

    def test_date_without_year_and_time(self):
        d = parser.parse('01/07', '13:52')
        assert d.day == 1
        assert d.month == 7
        assert d.hour == 13
        assert d.minute == 52
