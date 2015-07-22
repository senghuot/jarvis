// defining our module first
var demo = angular.module('demo', []);

var keys = ["amount", "accountType", "bookingType", "expectedRevenue", "productCount","recordType"];
    keys = keys.concat(["forecastCategory", "leadSource", "annualRevenue", "employeeCount"]);
    keys = keys.concat(["coreProduct", "locationCount", "producerCount", "oppRevenue", "oppCount"]);

demo.controller('IntroController', function ($scope, $http) {
  $scope.initBtnClicked = function(){
    // display loading screen
    $('#init').toggle();
    $('#loading').toggle();    

    // grab the music
    var audio = new Audio('intro.mp3');
    audio.play();

    // this is too request server to train the data
    $http.get('http://127.0.0.1:5000/init')
      .success(function(response){
        $('#loading').toggle();
        $('#next').toggle().addClass('bounceIn animated');
        audio.pause();
      }).error(function(error){
        console.log(error);
    });
  };

  $scope.nextBtnClicked = function() {
    $('#intro').toggle();
    $('#compute').toggle();
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
        $scope.response = response;
      }).error(function(error) {
        console.log(error);
      });
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
  };
});

$(function() {
    $.material.init();
});