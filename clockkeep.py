import time
import dataset

db = dataset.connect('sqlite:///record.db')

groups = db['groups']
times = db['times']
notes = db['notes']

def add_group(name, inactive=False):
    # TODO: validate conditions: group does not exist, name is valid str
    groups.insert(name=name, inactive=False, punched_in=False)

def punch_in(group_id, time=time.time()):
    # TODO: validate conditions: group is punched out,
    # no out times are None within group
    db.begin()
    times.insert(group_id=group_id, in_time=time, out_time=None)
    group = groups.find_one(group_id=group_id)
    group['punched_in'] = True
    groups.update(group)
    db.commit()

def punch_out(group_id, time=time.time()):
    # TODO: validate conditions: exactly one time in group is None,
    # group is punched in
    db.begin()
    interval = times.find_one(group_id=group_id)
    interval['out_time'] = time
    times.update(interval)
    group = groups.find_one(group_id=group_id)
    group['punched_in'] = False
    groups.update(group)
    db.commit()

def add_note(group_id, note, time=time.time()):
    # TODO: validate group exists, note is valid str
    notes.insert(group_id=group_id, time=time, note=note)
