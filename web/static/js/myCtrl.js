app.config(['$httpProvider', function($httpProvider) {
  $httpProvider.defaults.useXDomain = true;
  // $httpProvider.defaults.withCredentials = true;
  delete $httpProvider.defaults.headers.common["X-Requested-With"];
  $httpProvider.defaults.headers.common["Accept"] = "application/json";
  $httpProvider.defaults.headers.common["Content-Type"] = "application/json";
}]);
app.config(function(ngQuickDateDefaultsProvider) {
  return ngQuickDateDefaultsProvider.set({});
});
app.controller('myCtrl', function($scope, $http, $timeout) {
  //$scope.account = localStorage.getItem("userID");
  $scope.password = localStorage.getItem("password");
  var Base64={_keyStr:"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",encode:function(e){var t="";var n,r,i,s,o,u,a;var f=0;e=Base64._utf8_encode(e);while(f<e.length){n=e.charCodeAt(f++);r=e.charCodeAt(f++);i=e.charCodeAt(f++);s=n>>2;o=(n&3)<<4|r>>4;u=(r&15)<<2|i>>6;a=i&63;if(isNaN(r)){u=a=64}else if(isNaN(i)){a=64}t=t+this._keyStr.charAt(s)+this._keyStr.charAt(o)+this._keyStr.charAt(u)+this._keyStr.charAt(a)}return t},decode:function(e){var t="";var n,r,i;var s,o,u,a;var f=0;e=e.replace(/[^A-Za-z0-9\+\/\=]/g,"");while(f<e.length){s=this._keyStr.indexOf(e.charAt(f++));o=this._keyStr.indexOf(e.charAt(f++));u=this._keyStr.indexOf(e.charAt(f++));a=this._keyStr.indexOf(e.charAt(f++));n=s<<2|o>>4;r=(o&15)<<4|u>>2;i=(u&3)<<6|a;t=t+String.fromCharCode(n);if(u!=64){t=t+String.fromCharCode(r)}if(a!=64){t=t+String.fromCharCode(i)}}t=Base64._utf8_decode(t);return t},_utf8_encode:function(e){e=e.replace(/\r\n/g,"\n");var t="";for(var n=0;n<e.length;n++){var r=e.charCodeAt(n);if(r<128){t+=String.fromCharCode(r)}else if(r>127&&r<2048){t+=String.fromCharCode(r>>6|192);t+=String.fromCharCode(r&63|128)}else{t+=String.fromCharCode(r>>12|224);t+=String.fromCharCode(r>>6&63|128);t+=String.fromCharCode(r&63|128)}}return t},_utf8_decode:function(e){var t="";var n=0;var r=c1=c2=0;while(n<e.length){r=e.charCodeAt(n);if(r<128){t+=String.fromCharCode(r);n++}else if(r>191&&r<224){c2=e.charCodeAt(n+1);t+=String.fromCharCode((r&31)<<6|c2&63);n+=2}else{c2=e.charCodeAt(n+1);c3=e.charCodeAt(n+2);t+=String.fromCharCode((r&15)<<12|(c2&63)<<6|c3&63);n+=3}}return t}}
 
  function make_base_auth(user, password) {
      var tok = user + ':' + password;
      var hash = Base64.encode(tok);
      return hash;
  }
  var token = "?token=";
  var auth = make_base_auth($scope.account, $scope.password);
  $scope.userName;
  $scope.$watch('account', function () {
      $scope.userName = $scope.account;
  });
  $http.get("http://cmpt470.csil.sfu.ca:8017/api/" + $scope.account)
    .success(function (response) {$scope.dev_status = response;});

  $scope.tem_key;
  $scope.setkey = function(data){
    $scope.tem_key = data;
  }

  $scope.addDevice = function(data){
    $http({
      url: "http://cmpt470.csil.sfu.ca:8017/api/" + $scope.account + token + auth,
      method: "PUT",
      data: {"command": "add_device", "devicename": data},
      headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, X-Requested-With',
          'Content-Type': 'application/json'
      }
    })
    .success(function (response) {$scope.dev_response = response;});
    $timeout(function() { window.location.reload(); }, 1000);
    
  }

  $scope.turnON = function(data){
    $scope.started = true;
    $http({
      url: "http://cmpt470.csil.sfu.ca:8017/api/" + $scope.account + token + auth,
      method: "PUT",
      data: {"command": "turn_on", "devicename": data},
      headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, X-Requested-With',
            'Content-Type': 'application/json'
      }
    }).success(function (response) {$scope.dev_response = response;callback(response);});
    $timeout(function() { window.location.reload(); }, 1000);
  }
  $scope.turnOFF = function(data){
    $scope.started = false;
    $http({
      url: "http://cmpt470.csil.sfu.ca:8017/api/" + $scope.account + token + auth,
      method: "PUT",
      data: {"command": "turn_off", "devicename": data},
      headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, X-Requested-With',
            'Content-Type': 'application/json'
      }
    }).success(function (response) {$scope.dev_response = response;callback(response);});
    $timeout(function() { window.location.reload(); }, 1000);
  }

  $scope.deleteDevice = function(data){
    $http({
      url: "http://cmpt470.csil.sfu.ca:8017/api/" + $scope.account + token + auth,
      method: "PUT",
      data: {"command": "delete_device", "devicename": data},
      headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, X-Requested-With',
            'Content-Type': 'application/json'
      }
    }).success(function (response) {$scope.dev_response = response;callback(response);});
    $timeout(function() { window.location.reload(); }, 1000);
    
  }

  $scope.turn_off_all = function(){
  $http({
  		url: "http://cmpt470.csil.sfu.ca:8017/api/" + $scope.account + token + auth,
  		method: "PUT",
  		data: {"command": "turn_off_all"},
  		headers: {
        	'Access-Control-Allow-Origin': '*',
        	'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
         	'Access-Control-Allow-Headers': 'Content-Type, X-Requested-With',
           	'Content-Type': 'application/json'
      }
  	})
  	.success(function (response) {$scope.dev_response = response;callback(response);});
    $timeout(function() { window.location.reload(); }, 1000);
    
  }
  $scope.turn_on_all = function(){
  $http({
      url: "http://cmpt470.csil.sfu.ca:8017/api/" + $scope.account + token + auth,
      method: "PUT",
      data: {"command": "turn_on_all"},
      headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, X-Requested-With',
            'Content-Type': 'application/json'
      }
    })
    .success(function (response) {$scope.dev_response = response;callback(response);});
    $timeout(function() { window.location.reload(); }, 1000);
    
  }



  //formate lib
  var dateFormat = function () {
    var token = /d{1,4}|m{1,4}|yy(?:yy)?|([HhMsTt])\1?|[LloSZ]|"[^"]*"|'[^']*'/g,
        timezone = /\b(?:[PMCEA][SDP]T|(?:Pacific|Mountain|Central|Eastern|Atlantic) (?:Standard|Daylight|Prevailing) Time|(?:GMT|UTC)(?:[-+]\d{4})?)\b/g,
        timezoneClip = /[^-+\dA-Z]/g,
        pad = function (val, len) {
            val = String(val);
            len = len || 2;
            while (val.length < len) val = "0" + val;
            return val;
        };

    // Regexes and supporting functions are cached through closure
    return function (date, mask, utc) {
        var dF = dateFormat;

        // You can't provide utc if you skip other args (use the "UTC:" mask prefix)
        if (arguments.length == 1 && Object.prototype.toString.call(date) == "[object String]" && !/\d/.test(date)) {
            mask = date;
            date = undefined;
        }

        // Passing date through Date applies Date.parse, if necessary
        date = date ? new Date(date) : new Date;
        if (isNaN(date)) throw SyntaxError("invalid date");

        mask = String(dF.masks[mask] || mask || dF.masks["default"]);

        // Allow setting the utc argument via the mask
        if (mask.slice(0, 4) == "UTC:") {
            mask = mask.slice(4);
            utc = true;
        }

        var _ = utc ? "getUTC" : "get",
            d = date[_ + "Date"](),
            D = date[_ + "Day"](),
            m = date[_ + "Month"](),
            y = date[_ + "FullYear"](),
            H = date[_ + "Hours"](),
            M = date[_ + "Minutes"](),
            s = date[_ + "Seconds"](),
            L = date[_ + "Milliseconds"](),
            o = utc ? 0 : date.getTimezoneOffset(),
            flags = {
                d:    d,
                dd:   pad(d),
                ddd:  dF.i18n.dayNames[D],
                dddd: dF.i18n.dayNames[D + 7],
                m:    m + 1,
                mm:   pad(m + 1),
                mmm:  dF.i18n.monthNames[m],
                mmmm: dF.i18n.monthNames[m + 12],
                yy:   String(y).slice(2),
                yyyy: y,
                h:    H % 12 || 12,
                hh:   pad(H % 12 || 12),
                H:    H,
                HH:   pad(H),
                M:    M,
                MM:   pad(M),
                s:    s,
                ss:   pad(s),
                l:    pad(L, 3),
                L:    pad(L > 99 ? Math.round(L / 10) : L),
                t:    H < 12 ? "a"  : "p",
                tt:   H < 12 ? "am" : "pm",
                T:    H < 12 ? "A"  : "P",
                TT:   H < 12 ? "AM" : "PM",
                Z:    utc ? "UTC" : (String(date).match(timezone) || [""]).pop().replace(timezoneClip, ""),
                o:    (o > 0 ? "-" : "+") + pad(Math.floor(Math.abs(o) / 60) * 100 + Math.abs(o) % 60, 4),
                S:    ["th", "st", "nd", "rd"][d % 10 > 3 ? 0 : (d % 100 - d % 10 != 10) * d % 10]
            };

        return mask.replace(token, function ($0) {
            return $0 in flags ? flags[$0] : $0.slice(1, $0.length - 1);
        });
    };
}();

// Some common format strings
dateFormat.masks = {
    "default":      "ddd mmm dd yyyy HH:MM:ss",
    shortDate:      "m/d/yy",
    mediumDate:     "mmm d, yyyy",
    longDate:       "mmmm d, yyyy",
    fullDate:       "dddd, mmmm d, yyyy",
    shortTime:      "h:MM TT",
    mediumTime:     "h:MM:ss TT",
    longTime:       "h:MM:ss TT Z",
    isoDate:        "yyyy-mm-dd",
    isoTime:        "HH:MM:ss",
    isoDateTime:    "yyyy-mm-dd'T'HH:MM:ss",
    isoUtcDateTime: "UTC:yyyy-mm-dd'T'HH:MM:ss'Z'"
};

// Internationalization strings
dateFormat.i18n = {
    dayNames: [
        "Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat",
        "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"
    ],
    monthNames: [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
        "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"
    ]
};

// For convenience...
Date.prototype.format = function (mask, utc) {
    return dateFormat(this, mask, utc);
};



  $scope.myDate = new Date();
  $scope.myTime = dateFormat($scope.myDate, "HH:MM:ss");
  $scope.fivelater = function() {
    var minInFuture = 1000*60*5;
    $scope.myDate5 = new Date();
    $scope.myDate = new Date($scope.myDate5.getTime()+minInFuture);
    $scope.myTime = dateFormat($scope.myDate, "HH:MM:ss");
  }
  $scope.thirtylater = function() {
    var minInFuture = 1000*60*30;
    $scope.myDate30 = new Date();
    $scope.myDate = new Date($scope.myDate30.getTime()+minInFuture);
    $scope.myTime = dateFormat($scope.myDate, "HH:MM:ss");
  }
  $scope.sixtylater = function() {
    var minInFuture = 1000*60*60;
    $scope.myDate5 = new Date();
    $scope.myDate = new Date($scope.myDate5.getTime()+minInFuture);
    $scope.myTime = dateFormat($scope.myDate, "HH:MM:ss");
  }
  $scope.setToToday = function() { $scope.myDate = new Date(); }
  $scope.setTimerON = function(dataName,dataTime) {
    $scope.date = dateFormat(dataTime, "yyyy-mm-dd"); 
    $scope.timer = dateFormat(dataTime, "HH:MM:ss");
    $scope.datetime = $scope.date + "T" + $scope.timer;
    console.log($scope.account);
    console.log(dataName);
    console.log($scope.datetime);
    $http({
      url: "http://cmpt470.csil.sfu.ca:8017/api/" + $scope.account + token + auth,
      method: "PUT",
      data: {"command": "turn_on", "devicename": dataName, "executedate": $scope.datetime},
      headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, X-Requested-With',
          'Content-Type': 'application/json'
      }
    })
    .success(function (response) {$scope.dev_response = response;});
    $timeout(function() { window.location.reload(); }, 1000);
  };
  $scope.setTimerOFF = function(dataName,dataTime) {
    $scope.date = dateFormat(dataTime, "yyyy-mm-dd"); 
    $scope.timer = dateFormat(dataTime, "HH:MM:ss");
    $scope.datetime = $scope.date + "T" + $scope.timer;
    console.log($scope.account);
    console.log(dataName);
    console.log($scope.datetime);
    $http({
      url: "http://cmpt470.csil.sfu.ca:8017/api/" + $scope.account + token + auth,
      method: "PUT",
      data: {"command": "turn_off", "devicename": dataName, "executedate": $scope.datetime},
      headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, X-Requested-With',
          'Content-Type': 'application/json'
      }
    })
    .success(function (response) {$scope.dev_response = response;});
    $timeout(function() { window.location.reload(); }, 1000);
  };
  
});
