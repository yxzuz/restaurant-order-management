from datetime import datetime, timezone, timedelta

# Thai timezone (Asia/Bangkok) is UTC+7
THAI_TZ = timezone(timedelta(hours=7))

def now_thai():
    """Get current datetime in Thai timezone"""
    return datetime.now(THAI_TZ)

def utc_to_thai(dt):
    """Convert UTC datetime to Thai timezone"""
    if dt is None:
        return None
    if dt.tzinfo is None:
        # Assume UTC if no timezone info
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(THAI_TZ)

def thai_to_utc(dt):
    """Convert Thai datetime to UTC"""
    if dt is None:
        return None
    if dt.tzinfo is None:
        # Assume Thai timezone if no timezone info
        dt = dt.replace(tzinfo=THAI_TZ)
    return dt.astimezone(timezone.utc)
