from bottle import get, route, request,response, run, template, static_file,TEMPLATE_PATH,post,install, hook, redirect,auth_basic
from passlib.hash import sha256_crypt
import bottle_session
#from bottle.ext.beaker.middleware import SessionMiddleware
from beaker.middleware import SessionMiddleware
from validate_email_address import validate_email
from datetime import timedelta

#firebase setting
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir + '/firebase-python')

#template setting
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH.insert(0, BASE_DIR)
print "BASE_DIR:", BASE_DIR, ", currentdir:",currentdir

import firebase
import ast,json
URL_ROOT = 'dazzling-heat-6704'

USER_ADMIN = 'admin'

API_TOKEN = 'smartroom'

def check_pass(username, password):
    hashed = ''.join(API_TOKEN)
    return sha256_crypt.verify(password, hashed)

#return format example [{'password': '', 'userid': 'wilsonzhao', 'email': 'yza215@sfu.ca', 'name': 'wilsonzhao'}]
def firebase_get_user_list():
    url = URL_ROOT + "/users"
    result = firebase.get(url)
    user_list = []
    if isinstance(result,dict):
        for key, value in result.iteritems():
           # print key, value
            user_dict = {}
            for user_key, user_value in value.iteritems():
               # print "user:", user_key, user_value
                user_dict[str(user_key)] = str(user_value)
            user_dict["userid"]= str(key)
            user_list.append(user_dict)#with remove unicode string
       # print "firebase_get_user_list:", user_list
    else:
        print "firebase-get_user_list: result is not dict:",result
    return user_list

def firebase_get_users_dict():
    url = URL_ROOT + "/users"
    print "url:", url
    result = firebase.get(url)
    users_dict = {}
    if isinstance(result,dict):
        for key, value in result.iteritems():
            print key, value
            users_dict[str(key)] = ast.literal_eval(json.dumps(value))
            print users_dict
        print "get_users_dict:", users_dict
        return users_dict
    else:
        print "firebase-get_users_dict: result is not dict:",result, bool(result),bool(None)
        return None


def firebase_delete_user(userid):
    url = URL_ROOT + "/users/%s" % userid
   # print "firebase_delete_user, url:", url
    dict_users = firebase_get_users_dict()
    result = dict_users.pop(userid, None)
   # print "--------------------- delete_user(after) userid:%s,\n dict_users:%s" %( userid, dict_users)
    firebase.put(URL_ROOT + "/users",dict_users)
        #2nd way but not stable
    #firebase.put(url,None)
    print "firebase_delete_user: done"

def firebase_get_user_dict(userid):
    url = URL_ROOT + "/users/%s" % userid
    print "url:", url
    result = firebase.get(url)
    users_dict = {}
    if isinstance(result,dict):
        for key, value in result.iteritems():
            print key, value
            users_dict[str(key)] =str(value)
            print users_dict
        print "get_user_dict:", users_dict
        return users_dict
    else:
        print "firebase-get_user_dict: result is not dict:",result, bool(result),bool(None)
        return None

def firebase_check_if_user(userid,password):
    dict_users = firebase_get_user_dict(userid)
    if dict_users is not None:
        print "check_if_user(got dict):", dict_users
        db_password = dict_users["password"]
        if db_password == password:
            return True
        else:
                return False
    else:#resut a user
        print "check_if_user(empty dict):", dict_users
        return False
        
def firebase_check_if_user_exist(userid):
    dict_users = firebase_get_user_dict(userid)
    if dict_users is not None:
        return True
    else:
        return False

def firebase_add_user(userid,name,password,email):
    url = URL_ROOT + "/users/%s" %(userid.lower())
    dict_user = {}
    dict_user["name"] = name
    dict_user["password"] = password
    dict_user["email"] = email

    firebase.patch(url,dict_user)

    print "add_user with userid:%s,username:%s, password:%s, email:%s" %(userid,name,password,email)



#Static Routes
@get('/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='/home/smartroom/web/static/js')

@get('/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='/home/smartroom/web/static/css')

@get('/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='/home/smartroom/web/static/img')

@get('/<filename:re:.*\.(eot|ttf|woff|svg)>')
def fonts(filename):
    return static_file(filename, root='/home/smartroom/web/static/fonts')


#admin URL
@route('/', methods=['GET','POST'])
def load_user_page():
    print "web user page"
    session = request.environ.get('beaker.session')
    print "your session: " , session.get("userid")
    if session.get('userid'):
        print "logined"
        username = session.get('username')
        userid = session.get('userid')
        api_token  = API_TOKEN
        return template('my.html',ang_keys="{{ key }}: {{ val }}",ang_add_devicename="{{deviceName}}",ang_tem_key="{{tem_key}}", ang_mytime = "{{myTime}}", username=username,userid=userid,api_token=api_token)
    else:
        print "no session:" , session.get("userid")
        return static_file('index.html', root='/home/smartroom/web')


@get('/<filename:re:.*\.html>')
def javascripts(filename):
    return static_file(filename, root='/home/smartroom/web')

#@route('/my')
#def index():
#        return static_file('my.html', root='/home/smartroom/web')

@route('/users/<userid>')
def get_status_all(userid):
    #dict_users = firebase_get_users_dict(userid)
    #name = dict_users["name"]
    #password =dict_users["password"]
    #email=dict_users["email"]
    #pw_check_result = firebase_check_if_user(userid,"1234")
    #firebase_add_user("test1","test1","1234","test1@sfu.ca")# this is just test, need to change

    #return template('<p> welcome {{user}}, {{result}} </p>',user=name, result=pw_check_result)
    templateDef = """
    <HTML>
    <HEAD><TITLE>$title</TITLE></HEAD>
    <BODY>
    $contents
    ## this is a single-line Cheetah comment and won't appear in the output
    #* This is a multi-line comment and won't appear in the output
        blah, blah, blah
    *#
    </BODY>
    </HTML>"""
    #nameSpace = {'title': 'Hello World Example', 'contents': 'Hello World!'}
    #t = Template(templateDef, searchList=[nameSpace])
    t = Template(file=BASE_DIR + "/index.html")
    return t

#this is not yet done os you need to check my website below

@route('/users/testsession')
def testsession():
    session = request.environ.get('beaker.session')
    if session.get('userid'):
        username = session.get('username')
        userid = session.get('userid')
        return template('<p> welcome {{username}} , {{userid}}</p>',username=username,userid=userid)
    else:
        redirect('/web/users/login')

@route('/users/login')
def index():
    session = request.environ.get('beaker.session')
    if session.get('userid') is not None:
        redirect('/web/users/logout')
    else:
        return template('login.html',error_status="  ")

@route('/users/login', method='POST')
def login():
    print "login:" , request.forms.get('save','')
    if request.forms.get('save','').strip():
        userid = request.forms.get('userid', '').strip()
        exist = firebase_check_if_user_exist(userid)
        if not exist:
           return template('login.html',error_status="The user does not exist")
            
        print "userid:", userid, " exist!!"
        password= request.forms.get('password', '').strip()
        pw_check_result = firebase_check_if_user(userid,password)
        if not pw_check_result:
           return template('login.html',error_status="Incorrect password")
        print "your userid", userid, " and password matched up!"
        dict_user = firebase_get_user_dict(userid)
        name = dict_user["name"]
        session = request.environ.get('beaker.session')
        session.cookie_expires = timedelta(minutes=3)
        session.timeout = 300  #this is the key for working also at firefox
        session['userid'] = userid
        session['username'] = name
        #session.cookie_expires = False
        session._update_cookie_out()
        session.save()


        print "logineed session:", session['userid']

        if is_admin():
            print "user is admin"
            #load_admin_page()
            redirect('/web/admin')
        else:
            redirect('/web/')

       

@route('/users/logout')
def logout():
    session = request.environ.get('beaker.session')
    if session.get('userid') is not None:
        session['userid'] = None
        session['username'] = None
        session.delete()
        redirect('/web/')
    else:
        redirect('/web/users/login')

@route('/users/register')
def register_page():
    return template('register.html',error_status="   ")

@route('/users/register',method='POST')
def register():
    if  request.forms.get('register','').strip():
        userid = request.forms.get('userid', '').strip()
        if firebase_check_if_user_exist(userid):
            return template('register.html',error_status="The user already exist")
        else:
            password= request.forms.get('password', '').strip()
            name = request.forms.get('name','').strip()
            email = request.forms.get('email','').strip()
            if validate_email(email):
            	firebase_add_user(userid,name,password,email)
            	print "userid:", userid, " has successfully registered"
            	return template('login.html',error_status="Account has been successfully created")
            else:
            	return template('register.html',error_status="please type in correct email")
    else:
        redirect('/web/users/register')

#admin URL
def is_admin():
    session = request.environ.get('beaker.session')
    print "checking admin session: " , session.get("userid")
    if session.get('userid') == USER_ADMIN:
        return True
    else:
        return False

@route('/admin')
def load_admin_page():
    redirect('/web/admin/users')
    #admin_user_list()

@route('/admin/users')
def admin_user_list():
    print "admiin user list"
    if is_admin():
        print "right admin, show list of users"
        #print firebase_get_user_list()
        #firebase_delete_user("test2")
        return template('admin_user_list.html',user_lists=firebase_get_user_list())
    else:
        redirect('/web/users/login')

@route('/admin/users/delete',method='POST')
def admin_delete_user():
    print "delete user"
    if  request.forms.get('delete','').strip():
        print "ready to delete"
        userid=request.forms.get('userid','').strip()
        firebase_delete_user(userid)
        redirect('/web/admin/users') 
@route('/admin/users/users/delete',method='POST')
def delete():
    if  request.forms.get('delete','').strip():
       # userid=request.forms.get('userid','').strip()

	firebase_delete_user('sen')
        redirect('/web/admin/users')
    else:
        print "request is wrong"
        redirect('/web/users/users')
