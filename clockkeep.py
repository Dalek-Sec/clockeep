import time
import dataset

db = dataset.connect('sqlite:///record.db')

groups = db['groups']
times = db['times']
notes = db['notes']

def add_group(name, inactive=False):
    # TODO: validate conditions: group does not exist, name is valid str
    groups.insert(dict(name=name, inactive=False, punched_in=False))

def punch_in(group_id, in_time=time.time()):
    # TODO: validate conditions: group is punched out,
    # no out times are None within group
    db.begin()

    times.insert(dict(group_id=group_id, in_time=in_time))
    group = groups.find_one(id=group_id)
    group['punched_in'] = True
    groups.update(group, ['id'])

    db.commit()

def punch_out(group_id, out_time=time.time()):
    # TODO: validate conditions: exactly one time in group is None,
    # group is punched in
    if not 'out_time' in times.columns:
        times.create_column('out_time', db.types.float)

    db.begin()

    interval = times.find_one(group_id=group_id, out_time=None)
    interval['out_time'] = out_time
    times.update(interval, ['id'])

    group = groups.find_one(id=group_id)
    group['punched_in'] = False
    groups.update(group, ['id'])

    db.commit()

def toggle_punch(group_id, time=time.time()):
    # TODO: validate conditions: group exists
    punched_in = groups.find_one(id=group_id)['punched_in']
    if punched_in:
        punch_out(group_id, time)
    else:
        punch_in(group_id, time)

def add_note(group_id, note, note_time=time.time()):
    # TODO: validate group exists, note is valid str
    notes.insert(dict(group_id=group_id, time=note_time, note=note))
