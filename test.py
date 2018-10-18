from flask import Flask
from queue import Queue
import threading
import time
import MitbProp as prop

ROUTINES = {'1':prop.trigger1, '2':prop.trigger2, '3':prop.trigger3}
app = Flask(__name__)

lock = threading.Lock()

def do_work(routine_id):
    global lock
    lock.acquire()
    ROUTINES[str(routine_id)]()
    time.sleep(5)
    print("working" + str(routine_id))
    lock.release()

@app.route('/')
def main():
    return "Hello World"

@app.route('/routine/<int:routine_id>')
def run_routine(routine_id):
    global lock
    if lock.locked():
        msg= "Busy"
    else:
        msg = "Running Routine " + str(routine_id)
        busy = True
        t = threading.Thread(target=do_work, args=(routine_id,))
        t.start()
    return msg

