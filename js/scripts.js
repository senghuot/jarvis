// here we would like to define how to converter, an array is necessary to keep the order because a map wont preserve order
var keys = ["amount", "accountType", "bookingType", "expectedRevenue", "productCount","recordType"];
    keys = keys.concat(["forecastCategory", "leadSource", "annualRevenue", "employeeCount"]);
    keys = keys.concat(["coreProduct", "locationCount", "producerCount", "oppRevenue", "oppCount"]);

var map = {'accountType': {'-1':'Unknown', 1:'Customer', 2:'Former Customer', 3:'Government', 4:'Midwest', 5:'Online Customer', 6:'Partner', 7:'Prospect'}};
    map['bookingType']      = {'-1':'Unknown', 1:'Addon', 2:'Cross-Sell', 3:'New Business'};
    map['recordType']       = {'-1':'Unknown', 1:'Add-on', 2:'Administrative', 3:'Migration', 4:'Standard'};
    map['forecastCategory'] = {'-1':'Unknown', 1:'Best Case', 2:'Commit', 3:'Pipeline', 4:'Ommited', 5:'Closed'};
    map['coreProduct']      = {'-1':'Unknown', 0:'No', 1:'Yes'};
    map['leadSource']       = {'-1':'Unknown', 1:'Agency Success Program', 2:'Ambest-List', 3:'Call-In', 4:'Client-Referall', 5:'Cold-Call', 6:'Contact List', 7:'Current Customer', 
                        8:'Email', 9:'Demo', 10:'Employee Referal', 11:'Event', 12:'Web', 13:'Tradeshow', 14:'Seminar', 15:'External Referral', 16:'Jigsaw', 17:'Lead Pass', 
                        18:'Marketing Campaign', 19:'Public Relations', 20:'Other'};
    map['label'] = {1:'Won', 2:'Approved', 3:'Propose', 4:'Prospect', 5:'Qualify', 6:'Solution Developement', 7:'Whitespace', 8:'Closed'};

// this is where we define our module. 
var demo = angular.module('demo', []);
demo.controller('IntroController', function ($scope, $http) {
  $scope.initBtnClicked = function(){
    // display loading screen
    $('#init').addClass('disabled');
    $('#loading').css('opacity', '1');    

    // grab the music
    var audio = new Audio('intro.mp3');
    audio.play();

    // this is too request server to train the data
    $http.get('http://127.0.0.1:5000/init')
      .success(function(response){
        $('#loading').css('opacity', '0');
        $('#go-down').toggle();
        audio.pause();
      }).error(function(error){
        console.log(error);
    });
  };
});

demo.controller('ComputeController', function($scope, $http) {
  $scope.master = {};
  
  // compute the result without encodig the result first
  $scope.computeBtnClicked = function() {
    // construct an array to be computed
    var data = {customers: $scope.customers};
    $http.post('http://127.0.0.1:5000/compute', data)
      .success(function(response) {
        $scope.response = response;
        $scope.buildResult();
      }).error(function(error) {
        console.log(error);
      });
  };

  // display result by converting encoded int back to string
  $scope.buildResult = function() {
    $scope.results = [];
    for (var i = 0; i < $scope.response.labels.length; i++) {
      var label = map['label'][$scope.response.labels[i]]; 
      var recommend = {};
      for (var key in keys) {
        var name            = keys[key];
        var cus_val         = $scope.customers[i][name];
        var rec_val         = $scope.response.recommends[i][name];
        if (map[name] !== undefined) {
          cus_val = map[name][cus_val];
          rec_val = map[name][rec_val];
        }
        recommend[name] = [cus_val, rec_val];
      }
      $scope.results.push({'label': label, 'recommend': recommend});
    }
    console.log($scope.results);
  };

  // convert sandbox string to useful JSON
  $scope.change = function() {
    var tmp;
    var tmps = [];
    var vals = $scope.sandbox.split("\n");
    for (var i in vals) {
      var val = vals[i];
      var val = val.split("\t");
      tmp = {};
      for (var i = 0; i < keys.length; i++) {
        key       = keys[i];
        tmp[key]  = val[i];
      }
      tmps.push(tmp);
    }
    $scope.customer = tmp;
    $scope.customers = tmps;
  };
});

// initializing material ripple effect
$(function() {
    $.material.init();
});

// initializing wow.js
new WOW().init();