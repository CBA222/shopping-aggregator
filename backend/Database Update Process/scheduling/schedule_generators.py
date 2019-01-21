
def daily_generator(self, calendar, time=0):
    for k, v in calendar:
        calendar[k] = time
    return calendar