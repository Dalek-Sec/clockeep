import time
from datetime import date, datetime, timedelta
import clockkeep

def print_info():
    groups = clockkeep.groups.find(inactive=False)
    print('\nin:  id:  name:')
    for row in groups:
        print('[%s] [%i]   %s' % (
                '*' if row['punched_in'] else ' ',
                row['id'],
                row['name']
              ))

def print_report(group_id, weeks_back=0):
    times = list(clockkeep.times.find(group_id=group_id, order_by='in_time'))
    #print([time for time in times])

    time_matrix = get_time_matrix(times, 7, weeks_back)
    #print(time_matrix)

    notes = list(clockkeep.notes.find(group_id=group_id, order_by='time'))
    #print([note for note in notes])

    print('       Mon Tue Wed Thu Fri Sat Sun')
    for row in range(24):
        time_row = ['_' if time_matrix[day][row] == 0 else '#' for day in range(7)]
        time_row = ' | '.join(time_row)
        print(str(row).rjust(3) + ':00  ' + time_row)

    for note in notes:
        print(time.ctime(note['time'])+': ' + note['note'])

def get_time_matrix(times, days, weeks_back):
    for row in times:
        if row['out_time'] == None:
            row['out_time'] = time.time()
    time_matrix = []
    last_day = date.today() - timedelta(weeks=weeks_back)
    last_day = last_day + timedelta(days=(6 - last_day.weekday()))
    #print(last_day.ctime())
    for days_back in range(days):
        hours_list = []
        for hour in range(24): # This got complicated to account for DST, but there are still odd edge cases
            hour_start = datetime(last_day.year, last_day.month, last_day.day, hour) - timedelta(days=days_back)
            hour_end = hour_start + timedelta(hours=1)
            interval = [time.mktime(x.timetuple()) for x in [hour_start, hour_end]]
            number = 1 if are_times_in_interval(interval, times) else 0
            hours_list.append(number)
        time_matrix.insert(0, hours_list)
    return time_matrix

def are_times_in_interval(interval, times):
    for row in times:
        if row['in_time'] < interval[1] and (row['out_time'] is None or row['out_time'] > interval[0]):
            return True
    return False

while True:
    print_info()
    command = input(':')
    if command == '':
        pass
    elif command.isdigit():
        group_id = int(command)
        clockkeep.toggle_punch(group_id)
    elif command[0] == 'n':
        group_id, note = command[1:].split(' ', 1)
        group_id = int(group_id)
        clockkeep.add_note(group_id, note)
    elif command[0] == 'a':
        name = command[1:]
        if ' ' in command:
            weeks_back = command.split(' ', 1)
        else:
            weeks_back = 0
        clockkeep.add_group(name)
    elif command[0] == 'r':
        group_id = command[1:]
        print_report(group_id)
    elif command[0] == 'q':
        quit()
