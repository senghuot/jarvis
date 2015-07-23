// defining our module first
var demo = angular.module('demo', []);

var keys = ["amount", "accountType", "bookingType", "expectedRevenue", "productCount","recordType"];
    keys = keys.concat(["forecastCategory", "leadSource", "annualRevenue", "employeeCount"]);
    keys = keys.concat(["coreProduct", "locationCount", "producerCount", "oppRevenue", "oppCount"]);

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
    var data = {customers:[$scope.customer]};
    $http.post('http://127.0.0.1:5000/compute', data)
      .success(function(response) {
        if(response.label > 1)
          $scope.win = false;
        else
          $scope.win = true;
        $scope.response = response;
        $scope.buildResult();
      }).error(function(error) {
        console.log(error);
      });
  };

  $scope.buildResult = function()
  {
    $scope.result = {};
    var temp;
    var name;
    var val1;
    var val2;
    for (key in $scope.keys)
    {
      temp = [];
      name = keys[key];
      val1 = $scope.customer[name];
      val2 = $scope.response.recommend[name];
      temp.push(val1);
      temp.push(val2);
      $scope.result[name] = temp;
    }
  };

  // convert sandbox string to useful JSON
  $scope.change = function() {
    var vals = $scope.sandbox.split("\t");
    var tmp = {};
    for (var i=0; i<keys.length; i++) {
      key = keys[i];
      tmp[key] = vals[i]
    }
    $scope.customer = tmp;
    $scope.keys = keys;
  };
});


// initializing material ripple effect
$(function() {
    $.material.init();
});

// initializing wow js
new WOW().init();