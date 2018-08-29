import clockkeep

def print_info():
    groups = clockkeep.groups.find(inactive=False)
    print('in:  id:  name:')
    for row in groups:
        print('[%s] [%i]   %s' % (
                '*' if row['punched_in'] else ' ',
                row['id'],
                row['name']
              ))

def print_report(group_id):
    times = clockkeep.times.find(group_id=group_id)
    print([time for time in times])
    notes = clockkeep.notes.find(group_id=group_id)
    print([note for note in notes])

while True:
    print_info()
    command = input(':')
    if command.isdigit():
        group_id = int(command)
        clockkeep.toggle_punch(group_id)
    elif command[0] == 'n':
        group_id, note = command[1:].split(' ', 1)
        group_id = int(group_id)
        clockkeep.add_note(group_id, note)
    elif command[0] == 'a':
        name = command[1:]
        clockkeep.add_group(name)
    elif command[0] == 'r':
        group_id = command[1:]
        print_report(group_id)
    elif command[0] == 'q':
        quit()
