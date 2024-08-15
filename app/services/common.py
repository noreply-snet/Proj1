import pytz




def convert_utc_to_ist(utc_time):

    # Define IST timezone
    ist = pytz.timezone('Asia/Kolkata')
    
    # Convert UTC time to IST
    ist_time = utc_time.astimezone(ist)
    return ist_time