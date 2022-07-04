from datetime import date, datetime


class missing:
    def __str__(self):
        return '<missing>'

    def __repr__(self):
        return '<missing>'


missing = missing()
PRIMITIVE_TYPES = str, int, float, bool, date, datetime, dict
