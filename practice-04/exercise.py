from datetime import datetime, timedelta

# 1.  Subtract five days from current date
today = datetime.now()
five_days_ago = today - timedelta(days=5)
print("1. Five days ago:", five_days_ago)

# 2. Print yesterday, today, tomorrow
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print("2. Yesterday:", yesterday.date())
print("   Today:", today.date())
print("   Tomorrow:", tomorrow.date())

# 3. Drop microseconds from datetime
without_microseconds = today.replace(microsecond=0)
print("3. Datetime without microseconds:", without_microseconds)

# 4. Calculate difference between two dates in seconds
date1 = datetime(2026, 3, 20, 10, 0, 0)
date2 = datetime(2026, 3, 21, 12, 30, 0)

difference = date2 - date1
seconds = difference.total_seconds()

print("4. Difference in seconds:", seconds)