import json
import time
import StringIO
import requests
from bottle import request
from common import queue
from boto.sqs.message import RawMessage
from requests.exceptions import ConnectionError

def send_push(device_id, body):
    print "device_id:%, body:%s" %(device_id, body)

def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError, e:
        return False
    return True

import datetime
def validate(date_text):
    if date_text is None:
        return False
    
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        #raise ValueError("Incorrect data format, should be YYYY-MM-DD HH:MM:SS")
        print "validate:Incorrect data format, should be YYYY-MM-DDTHH:MM:SS"
        return False
    return True

def is_right_time_to_execute(executedate):
    
    is_valid = validate(executedate)
    if not is_valid:
        print "Execute Now since it is not valid date:", executedate
        return True

    dt = datetime.datetime.strptime(executedate, '%Y-%m-%dT%H:%M:%S')
    today = datetime.datetime.now()
    if today >= dt: # already passe up
        print "is rihgt? YES: ", today, ",", dt
        return True
    else:
        print "is right? NO: ",today, ",", dt
        return False
    
    return True

# Request Device Emulator to do task(Switching on/off the device)
def request_to_emulator(userid,command,devicename):
    print "task(%s, %s, %s) requested" % (userid, command, devicename)
    #url = 'http://cmpt470.csil.sfu.ca:8017/emulator/peace' #  http://cmpt470.csil.sfu.ca:8017/api/" + userid
    url = 'http://52.24.231.104:7070/emulator/' + userid
    #url = 'http://cmpt470.csil.sfu.ca:8017/api/wilson'

    res = requests.put(url, data=json.dumps({'command': command,'devicename':devicename}),
            headers={'content-type': 'application/json'})  #params = {'consistency':'weak'}
    #except ConnectionError:
    #    time.sleep(1)
    #    print "try to request again!"
    #    response = requests.put(url, data=json.dumps({'command': command,'devicename':devicename}),headers={'content-type': 'application/json'})
    print "request res: %s" % res
    #if is_json(res):
    return res.json()['Result']
    #else:
    #    return "ERROR: Json result from emulator is not valid, result:%s" % str(res)

try:
    
    # Loop forever.
    MAX_DEL_DICT = 7
    while 1:
        #processing the queue messages and asking device emulator to do the task
        queue.set_message_class(RawMessage)
        results = queue.get_messages(num_messages=10, visibility_timeout=30,wait_time_seconds=10)
        dict_deleted ={}
        del_history = []
        print "received queue result : %d" % len(results)
        for msg in results:
            body = msg.get_body()
            jbody = json.loads(body)
            requestdate =jbody["requestdate"] if jbody["requestdate"] == None else jbody["requestdate"].strip()
            executedate =jbody["executedate"] if jbody["executedate"] == None else jbody["executedate"].strip()
            userid = jbody["userid"].strip()
            command = jbody["command"].strip()
            devicename = jbody["devicename"] if jbody["devicename"] == None else jbody["devicename"].strip()
            key = "%s:%s:%s:%s" %(requestdate,executedate,userid,command)

            print "userid:%s\n command:%s \n devicename:%s \n execute date:%s \n" % ( userid,command,devicename,executedate)
            if key not in dict_deleted:
                if is_right_time_to_execute(executedate):
                    print "now is the time to execute:",executedate,",",  userid,command,devicename
                    request_result = request_to_emulator(userid,command,devicename)
                    if request_result == "OK":
                        dict_deleted[key]=True
                        del_history.append(key)
                        msg.delete()
                        print "  --> queue message(key:%s) is proccessed! and deleted! len of dict_deleted:%d, len of history:%d " % (key, len(dict_deleted), len(del_history))
                    else:
                        print " failed with result message: %s" % request_result
                else:
                    print "now it is not yet to execute:", executedate, ",", userid, command, devicename
            else:
                # already key is deleted so it doesnot need to request to emulator again
                print " -- already key(%s) is deleted!" % key

            #only keep dict_deleted for MAX_DEL_DICT=7
            if len(dict_deleted)> MAX_DEL_DICT:
                old = del_history.pop(0)
                del dict_deleted[old]
                print "deleleted old key(%s)" % old

# When someone tries to break the program just quit gracefully
# instead of raising some nasty exception.
except KeyboardInterrupt:
    pass

