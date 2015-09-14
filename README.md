PLEASE READ BY RAW VIEW(It is more clear)
#cmpt470 smartroom system - group 17
##GIT : git@csil-git1.cs.surrey.sfu.ca:group17/group_smartroom.git
##SERVER API ROOT : http://cmpt470.csil.sfu.ca:8017/api
##EB ROOT : http://cmpt470.csil.sfu.ca:8017/web

Admin Account: admin
Admin Password: 470iot
Admin can manage users.

You can create any account by register.
Or use some existed accounts, such as test (password: 1234)

We use base64 encription before sending all put API.

We have performance testing using Jmeter, which locates in performance_test_results folder. There are some screenshots and a JMX in it. If you have Jmeter installed, you can run that JMX file.

APACHE SETTING
	LOCATION: /ETC/APACHE2/SITES-ENABLED
	smartroom.conf

##Folder Structure
        .vimrc : vi custom configuration setting
        /api : Rest API for http://cmpt470.csil.sfu.ca:8017/api
                app.wsgi : wsgi setting for rest api
                api.py : interface for user & device control
                common.py : setting & interface functions for Amazon SQS
                rootkey.csv : key to access Amazon SQS
                robot.py : for Robot to process message from SQS
        /emulator : Emulator(copied version running at Amazon EC2)
                URL: http://52.24.231.104:7070/emulator/
        /firebase-python : Firebase API(Python) to access our DB
-               DB url: https://dazzling-heat-6704.firebaseio.com

        /plugins/beaker : breaker session API to manage session in web
        /web : front-end for http://cmpt470.csil.sfu.ca:8017/web
                app.wsgi : wsgi setting for front-end
                admin_user_list.html : admin template
                login.html : login template
                register.html : user register template
                setting.html : user setting template
                index.html : first page(guest) template
                my.html : first page or my page (logined user) template
                /static : static files such as css, font,img, js

##API EXAMPLE
 for switching on/off devices for a given userid:
 curl -XPUT -H'Content-type: application/json' -d'{"command": "turn_on_all"}' http://cmpt470.csil.sfu.ca:80$
 Response is a JSON object specifying status of the devices in peace’s room:
 {"DeskLight": 1, "Heater": 0}

##API Command LIST
|command |  devicename | Result|
|turn_on_all |           |         “OK”|
|turn_off_all|           |         “OK”|
|turn_on |        “DeskLight”|     “OK”|
|turn_off |       “Heater”   |     “OK”|
|add_device |     “BedLight” |     “OK”|
|delete_device |  “BedLight” |     “OK”|

##API Command USAGE
Turn on DeskLight {"command": "turn_on", "devicename": "DeskLight"}
Add device: {"command": "add_device", "devicename": "WallLight"}
Delete device: {"command": "delete_device", "devicename": "WallLight"}


##JSON
{
  "users": {
    "peace": {
      "name": "Hwapyeong(Peace) Cho",
      "password": "1234",
      "email": "peacec@sfu.ca"
    },
    "wilson": {
      "name": "Yunfeng(Wilson) Zhao",
      "password": "1234",
      "email": "yza215@sfu.ca"
    },
    "sen": {
      "user": "Sen Luo",
      "password": "1234",
      "email": "luosenl@sfu.ca"
    },
    "edward": {
      "user": "Hongquan(Edward) Zhao",
      "password": "1234",
      "email": "hza52@sfu.ca"
    }
  },
  "devices": {
    "peace": {
      "Desk Light": 1,
      "Heater": 0
    },
    "wilson": {
      "Desk Light": 1,
      "Heater": 0,
      "Wall Light": 0
    },
    "sen": {
      "Desk Light": 1,
      "Heater": 0,
      "Wall Light": 1
    },
    "edward": {
      "Desk Light": 0,
      "Heater": 1,
      "Wall Light": 0
    }
  }
}


##System Setting Linux Command(this command has to executed at least once(very important)
a2ensite smartroom
sudo -s
sites-enabled
sudo /etc/init.d/apache2 restart
sudo /etc/init.d/apache2 stop
set ts=4

deletes all files and folders contained in the web directory : rm -rf web rm -rf web
:wqdirectory : rm -rf web chopeace

copy all fires and folders contained in the api to web: cp -r api web

to kill apache2 process : kill -9 $(ps -e | grep apache2 | awk '{print $1}')

change file or folder permission for write: sudo chmod +x /var
sudo apt-get update
sudo apt-get install apache2
clear ls
netstat -an | more
sudo apt-get install python-mimeparse
pip install git-pre-commit-hook
tail -n 15 -F access.log
json unicode : sudo apt-get install python-yaml
sudo pip install redis
pip install bottle-redis
sudo /etc/init.d/apache2 stop
set ts=4

deletes all files and folders contained in the web directory : rm -rf web rm -rf web
:wqdirectory : rm -rf web chopeace
copy all fires and folders contained in the api to web: cp -r api web
to kill apache2 process : kill -9 $(ps -e | grep apache2 | awk '{print $1}')
change file or folder permission for write: sudo chmod +x /var
sudo apt-get update
sudo apt-get install apache2
clear ls
netstat -an | more
sudo apt-get install python-mimeparse
pip install git-pre-commit-hook
tail -n 15 -F access.log

json unicode : 
sudo apt-get install python-yaml
sudo pip install redis
pip install bottle-redis
easy_install bottle-redis
apt-get install nmap
iptables -A INPUT -i eth0 -p tcp --dport 8017 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -o eth0 -p tcp --sport 8017 -m state --state ESTABLISHED -j ACCEPT
iptables -A INPUT -i eth0 -p tcp --dport 8017 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -o eth0 -p tcp --sport 8017 -m state --state ESTABLISHED -j ACCEPT
iptables -A INPUT -p udp --sport 8017 -j ACCEPT
iptables -A INPUT -p tcp --sport 8 -j ACCEPT
iptables -A RH-Firewall-1-INPUT -m state --state NEW -p tcp --dport 8017 -j ACCEPT
-A RH-Firewall-1-INPUT -m state --state NEW -p tcp --dport 443 -j ACCEPT
iptables -A INPUT -m state --state NEW -p tcp --dport 8017 -j ACCEPT
sudo nmap -T Aggressive -A -v 127.0.0.1 -p 1-65000

It will scan for all the open ports on your system. Any port that is open can be accessed from outside.
Access to file for web user: sudo chown chopeace. .
chmod 777 contact.유
pip install passlib
pip install validate_email
need to run setup.py in /home/smartroom/plugins/beaker
apt-get install nmap
iptables -A INPUT -i eth0 -p tcp --dport 8017 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -o eth0 -p tcp --sport 8017 -m state --state ESTABLISHED -j ACCEPT
iptables -A INPUT -i eth0 -p tcp --dport 8017 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -o eth0 -p tcp --sport 8017 -m state --state ESTABLISHED -j ACCEPT
iptables -A INPUT -p udp --sport 8017 -j ACCEPT
iptables -A INPUT -p tcp --sport 8 -j ACCEPT
iptables -A RH-Firewall-1-INPUT -m state --state NEW -p tcp --dport 8017 -j ACCEPT
-A RH-Firewall-1-INPUT -m state --state NEW -p tcp --dport 443 -j ACCEPT
iptables -A INPUT -m state --state NEW -p tcp --dport 8017 -j ACCEPT
sudo nmap -T Aggressive -A -v 127.0.0.1 -p 1-65000
It will scan for all the open ports on your system. Any port that is open can be accessed from outside.
Access to file for web user: sudo chown chopeace. .
chmod 777 contact.유
pip install passlib
pip install validate_email
need to run setup.py in /home/smartroom/plugins/beaker
