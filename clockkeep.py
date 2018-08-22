import time
import dataset

db = dataset.connect('sqlite:///record.db')

groups = db['groups']
times = db['times']
notes = db['notes']

def add_group(name, inactive=False):
    pass

def punch_in(group, time=time.time()):
    pass

def punch_out(group, time=time.time()):
    pass

def add_note(group, note):
    pass
