from datetime import date, datetime

from sqlalchemy import String, Integer, JSON, Float, Boolean, Date, DateTime


SA_TYPES_MAPPING = {
    str: String,
    int: Integer,
    float: Float,
    bool: Boolean,
    date: Date,
    datetime: DateTime,
    dict: JSON,
}
