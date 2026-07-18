from datetime import datetime

def get_ctime_cdate(date=None,time=None,splitter=False):
    if not splitter:
        ctd = datetime.now()
        cdate,ctime = str(ctd.date()),str(ctd.strftime('%I:%M:%S'))
    else:
        cdate,ctime = str(date),str(time)
    return {
        'date':cdate,
        'time':ctime,
        'sep_date':{
            'day':cdate.split('-')[-1],
            'mon':cdate.split('-')[1],
            'year':cdate.split('-')[0]
        },
        'sep_time':{
            'H':ctime.split(':')[0],
            'M':ctime.split(':')[1],
            'S':ctime.split(':')[-1]
        }
    }

def data_time_validator(date, time):
    get_ctd = get_ctime_cdate(splitter=False)
    get_o_ctd = get_ctime_cdate(date, time, splitter=True)

    current = datetime(
        int(get_ctd['sep_date']['year']),
        int(get_ctd['sep_date']['mon']),
        int(get_ctd['sep_date']['day']),
        int(get_ctd['sep_time']['H']),
        int(get_ctd['sep_time']['M']),
        int(get_ctd['sep_time']['S'])
    )

    expiry = datetime(
        int(get_o_ctd['sep_date']['year']),
        int(get_o_ctd['sep_date']['mon']),
        int(get_o_ctd['sep_date']['day']),
        int(get_o_ctd['sep_time']['H']),
        int(get_o_ctd['sep_time']['M']),
        int(get_o_ctd['sep_time']['S'])
    )

    return expiry > current