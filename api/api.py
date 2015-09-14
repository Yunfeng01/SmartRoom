import string,uuid,time,json,boto,boto.exception
import mimeparse, os, sys, hashlib, random
from bottle import hook, Bottle, route, request, run, template, response, abort,auth_basic,parse_auth
from passlib.hash import sha256_crypt
from common import queue
from boto.sqs.message import RawMessage
import ast
import os,sys,inspect
import base64

#firebase setting
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir + '/firebase-python')
import firebase
URL_ROOT = 'dazzling-heat-6704'

API_TOKEN = 'smartroom'

def check_pass(username, password):
    print "check_pass->" + username + ", " + password
    hashed = ''.join(API_TOKEN)
    return True
    #return sha256_crypt.verify(password, hashed)

@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    response.headers['Access-Control-Allow-Credentials'] = True

def allow_cors(fn):
    def _enable_cors(*args, **kwargs):
        # set CORS headers
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:9000'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token, Authorization'
        response.headers['Access-Control-Allow-Credentials'] = True

        if request.method != 'OPTIONS':
            # actual request; reply with the actual response
                return fn(*args, **kwargs)

    return _enable_cors


#write a message to SQS containing information about task for emulator to
def notify_robot(userid, command,devicename,executedate):
    data = {
                'requestdate' : time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()),
                'executedate' : executedate,
                'userid' : userid,
                'command' :command,
                'devicename' : devicename
           }
    m = RawMessage()
    m.set_body(json.dumps(data))
    status = queue.write(m)
    print 'your message sent : %s , status : %s, executedate:%s ' % ( m,status, executedate)

def result(r):
    #print "jsondumps:" , json.dumps(r)
    return json.dumps(r)

@route('/')
def index():
       return 'Hello World This is SmartHome API'

@route('/<userid>', method ='GET')
def get_status_all(userid):
    url = URL_ROOT + "/devices/%s" % userid
    print url
    result = firebase.get(url)
    print "result:" , result
    if result == None:
        return {}
    else:
        result_removed_uni = ast.literal_eval(json.dumps(result))
        print "result after eval:" , result_removed_uni
    #print "yaml:", yaml.safe_load(result)
    return result_removed_uni


#DEVICE API
@route('/<userid>', method ='GET')
def get_status_all(userid):
    url = URL_ROOT + "/devices/%s" % userid
    print url
    result = firebase.get(url)
    print "result:" , result
    if result == None:
        return {}
    else:
        result_removed_uni = ast.literal_eval(json.dumps(result))
        print "result after eval:" , result_removed_uni
    #print "yaml:", yaml.safe_load(result)
    return result_removed_uni

@route('/<userid>/get/device_list', method ='GET')
def get_devide_list(userid):    
    print "get_device_list:%s" % userid
    list_devices= firebase_get_device_list(userid)
    json_devices= list2json(list_devices)
    print json_devices
    return eval(json_devices)

def list2json(list_object):
    return "{\"Result\":[%s]}" % ", ".join("\"%s\"" % ( key ) for key in list_object)

def dict2json(dict_object):
    return "{%s}" % ", ".join("\"%s\":\"%s\"" % ( key,value) for key,value in dict_object.iteritems())


@route('/<userid>', method ='OPTIONS')
def put_task(userid):
    return {"OPTIONS_REQUEST" : 1}

# Requesting tiask to api
# curl -XPUT -H'Content-type: application/json' -d'{"command": "turn_on_all"}' http://52.24.231.104:7070/api/ peace
@route('/<userid>', method ='PUT')
def put_task(userid):

    if not verify_user(userid,request.query['token']): return {"RESULT":"YOU ARE NOT AUTHORIZED USER"}

    # Check to make sure JSON is ok
    type = mimeparse.best_match(['application/json'], request.headers.get('Accept'))
    if not type: return abort(406)

    print "Content-Type: %s" % request.headers.get('Content-Type')

    # Check to make sure the data we're getting is JSON
    #if request.headers.get('Content-Type') != 'application/json': return abort(415)

    response.headers.append('Content-Type', type)

    # Read in the data
    data = json.load(request.body)
    command = data.get('command')
    devicename = data.get('devicename')
    executedate = data.get('executedate')

    print "requested command:%s, devicename:%s, executedate:%s" % (command,devicename,executedate)
    
    # Basic sanity checks on the task
    if iscommand(command): command = command
    if not iscommand(command): return {"Result": "ERROR: your comamnd doesnot allowed in our api"}   #   abort(400)
    
    # Send a message to a robot to begin processing actual switching on/off
    notify_robot(userid,command,devicename,executedate)

    # Return the new rating for the entity
    return {
        "Result": "OK"
    }


# get instance to use from [0 to about n] instances for the tea
def iscommand(command):
    if command == "turn_on_all" or command == "turn_off_all" or command == "get_status_all" or command == "add_device" or command == "turn_on" or command == "turn_off"  or command == "delete_device":
        return True
    else:
        return False


#USER API
#@route('/users/<userid>', method ='GET')
#def test(userid):
#    dict_users = firebase_get_users_dict(userid)
#    name = dict_users["name"]
#    password =dict_users["password"]
#    email=dict_users["email"]
#    pw_check_result = firebase_check_if_user(userid,"1234")
#    #firebase_add_user("test1","test1","1234","test1@sfu.ca")# this is just test, need to change
#    return template('<p> welcome {{user}}, {{result}} </p>',user=name, result=pw_check_result)

#, method ='GET'
#get user info
@route('/users/<userid>')
def get_user_info(userid):
    
    #is_verified = verify_user(userid,request.query['token'])
    if not verify_user(userid,request.query['token']): return {"RESULT":"YOU ARE NOT AUTHORIZED USER"}
    
    print "you are authorized,auth:", request.auth
    dict_user = firebase_get_users_dict(userid)
    print "dict_user:",dict_user  # string is ' style not "
    json_user= dict2json(dict_user) # string is changed from ' to "
    print json_user
    return eval(json_user)

def verify_user(userid,requested_token):
    
    if requested_token is None or requested_token == '':
        print "verify_user: requested_token is not requested!", requested_token
        return False

    password = API_TOKEN
    token_format = '%s:%s' % (userid, password)    #'.join(API_TOKEN)
    print "token_format:" , token_format
    
    #hash = sha256_crypt.encrypt(token_format)
    hash64 = base64.b64encode(token_format)

    #print "token encrypt256:", hash
    #print "token encrypt64:", hash_64
    print "token hash64 b64encode:" , hash64
    print "requested_token:" , requested_token
    is_verified = (requested_token==hash64)
    print "is_verified:" , is_verified
    return is_verified




def check_basic_auth():
    auth = request.headers.get('Authorization')
    print "auth--> ", auth
    username, password = parse_auth(auth)
    print "basic auth:", username, "," , password
    hashed = ''.join(API_TOKEN)
    print "hashed:" ,hashed
    return sha256_crypt.verify(password, hashed)

# edit user info api
# curl -XPUT -H'Content-type: application/json' -d'{"name": "new name"}' http://52.24.231.104:7070/api/ peace
@route('/users/<userid>', method ='PUT')
def put_task(userid):

    if not verify_user(userid,request.query['token']): return {"RESULT":"YOU ARE NOT AUTHORIZED USER"}

    # Check to make sure JSON is ok
    type = mimeparse.best_match(['application/json'], request.headers.get('Accept'))
    if not type: return abort(406)

    print "Content-Type: %s" % request.headers.get('Content-Type')

    # Check to make sure the data we're getting is JSON
    #if request.headers.get('Content-Type') != 'application/json': return abort(415)

    response.headers.append('Content-Type', type)

    # Read in the data
    data = json.load(request.body)
    name = data.get('name')
    password = data.get('password')
    email = data.get('email')

    print "updating user info(new): userid:%s, name:%s, password:%s, email:%s" % (userid,name,password,email)
    firebase_edit_user(userid,name,password,email)
    # Return the new rating for the entity
    return {
        "Result": "OK"
    }


def firebase_get_device_list(userid):
    url = URL_ROOT + "/devices/%s" % userid
    result = firebase.get(url)
    device_list = []
    if isinstance(result,dict):
        for key, value in result.iteritems():
            print key, value
            device_list.append(str(key))#with remove unicode string
        print device_list
    else:
        print "firebase-get_device_list: result is not dict:",result
    return device_list



#user retrival using firebase
def firebase_get_users_dict(userid):
    url = URL_ROOT + "/users/%s" % userid
    result = firebase.get(url)
    users_dict = {}
    if isinstance(result,dict):
        for key, value in result.iteritems():
            print key, value
            users_dict[str(key)] =str(value)
            print users_dict
    else:
        print "firebase-get_users_dict: result is not dict:",result
    return users_dict
def firebase_check_if_user(userid,password):
    dict_users = firebase_get_users_dict(userid)
    db_password = dict_users["password"]
    if db_password == password:
        return True
    else:
        return False

def firebase_edit_user(userid,name,password,email):
    url = URL_ROOT + "/users/%s" %(userid)
    dict_user = {}
    dict_user["name"] = name
    dict_user["password"] = password
    dict_user["email"] = email

    firebase.put(url,dict_user)
    print "edit_user with userid:%s,username:%s, password:%s, email:%s" %(userid,name,password,email)


def firebase_add_user(userid,name,password,email):
    url = URL_ROOT + "/users/%s" %(userid)
    dict_user = {}
    dict_user["name"] = name
    dict_user["password"] = password
    dict_user["email"] = email

    firebase.patch(url,dict_user)
    print "add_user with userid:%s,username:%s, password:%s, email:%s" %(userid,name,password,email)

def test(userid):
    dict_users = firebase_get_users_dict(userid)
    name = dict_users["name"]
    password =dict_users["password"]
    email=dict_users["email"]
    pw_check_result = firebase_check_if_user(userid,"1234")
    firebase_add_user("test1","test1","1234","test1@sfu.ca")# this is just test, need to change












#@route('/<userid>',emethod='DELETE')
#def delete_user(userid):
#>.......print "------------------------------------- deleted user"
#>.......return { "Result": "OK" }


# Fire the engines
#if __name__ == '__main__':
#>.......run(host='0.0.0.0', port=os.getenv('PORT', 7070), quiet=True)



