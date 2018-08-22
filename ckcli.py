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

while True:
    print_info()
    command = input(':')
    if command.isdigit():
        group_id = int(command)
        clockkeep.toggle_punch(group_id)
    elif command.split(' ')[0].isdigit():
        group_id, note = int(command.split(' ', 1))
        clockkeep.add_note(group_id, note)
    elif command[0] == 'a':
        name = command[1:]
        clockkeep.add_group(name)

