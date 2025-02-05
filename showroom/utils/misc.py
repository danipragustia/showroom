import os
import datetime
from showroom.constants import HHMM_FMT, FULL_DATE_FMT

CENTURY_OFFSET = 2000


# TODO: take a datetime object instead of a time_str
def format_name(root_dir, time_str, room, ext):
    """
    Get file and folder names for a live stream.

    Takes a root directory, a time string, and a room and returns a temp directory,
    a destination directory, and a file name for the associated stream.

    Args:
        root_dir: path the top of the output directory, generally taken from settings.
            Must be a string, Path objects are not handled.
        time_str: date and time in YYYY-MM-DD HHmmss format
        room: A Room object containing information about the room

    Returns:
        A tuple of three strings, representing the temp directory, the destination
        directory, and the filename, as follows:

            (temp ("active") directory, destination directory, filename)

    TODO:
        Eliminate double spaces more cleanly.
        Is there ever a situation where outfile could already exist?
    """
    rootdir = root_dir
    dir_format = '{root}/{group}'
    tempdir = '{root}/active'.format(root=rootdir)
    name_format = 'Showroom {name} {group} {date} Jam {time} WIB.{ext}'

    # count = 0
    # count_str = '_{:02d}'

    destdir = dir_format.format(root=rootdir, date=time_str[:10], group=room.group)

    os.makedirs('{}/logs'.format(destdir), exist_ok=True)

    _date, _time = time_str.split(' ')
    hours, minutes, secs = map(str, _time.split(':'))
    if len(hours) == 1:
        hours = '0' + hours
    if len(minutes) == 1:
        hours = '0' + hours        
        
    short_date = bulan_def_indo(_date)

    outfile = name_format.format(date=short_date, time='{h} {m}'.format(h=hours, m=minutes),
                                 count='', ext=ext, group=room.group, name=room.name)

    print(outfile)

    return tempdir, destdir, outfile


def iso_date_to_six_char(date):
    y, m, d = date.split('-')
    return '{:02d}{}{}'.format(int(y)-CENTURY_OFFSET, m, d)


def bulan_def_indo(date):
    y, m, d = date.split('-')
    m = int(m)
    if m == 1:
        m = "Januari"
    elif m == 2:
        m = "Februari"
    elif m == 3:
        m = "Maret"
    elif m == 4:
        m = "April"
    elif m == 5:
        m = "Mei"
    elif m == 6:
        m = "Juni"
    elif m == 7:
        m = "Juli"
    elif m == 8:
        m = "Agustus"
    elif m == 9:
        m = "September"
    elif m == 10:
        m = "Oktober"
    elif m == 11:
        m = "November"
    elif m == 12:
        m = "Desember"
    else:
        m = m

    return '{} {} {}'.format(d, m, y)
            
                

def strftime(dt: datetime.datetime, format_str: str):
    """
    Custom strftime.

    Checks for most frequently used format strings and handles those manually,
    hands any others off to dt.strftime()

    Args:
        dt: A datetime object.
        format_str: A valid strftime format string.
            '%H:%M' and '%Y-%m-%d %H%M%S' are handled specially.

    Returns:
        A string representation of dt as described by format_str

    TODO:
        Test if this is any faster than calling dt.strftime.
        Since dt.strftime is a C function, it's PROBABLY NOT.
        Also check that dt is a valid datetime object?
    """
    if format_str == HHMM_FMT:
        return "{:02d}:{:02d}".format(dt.hour, dt.minute)
    elif format_str == FULL_DATE_FMT:
        return "{year:04d}-{mon:02d}-{day:02d} " \
               "{hour:02d}:{min:02d}:{sec:02d}".format(
            year=dt.year, mon=dt.month, day=dt.day,
            hour=dt.hour, min=dt.minute, sec=dt.second)
    else:
        return dt.strftime(format_str)
