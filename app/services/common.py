from dateutil import tz

def convert_utc_to_ist(utc_time):
    # Define timezones
    utc_zone = tz.tzutc()
    ist_zone = tz.gettz('Asia/Kolkata')
    
    # Convert UTC time to IST
    ist_time = utc_time.replace(tzinfo=utc_zone).astimezone(ist_zone)
    return ist_time