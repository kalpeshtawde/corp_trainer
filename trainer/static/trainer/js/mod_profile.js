var app = angular.module('modprofile', [], function($interpolateProvider) {
    // {{}} interpolated with [[]]
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});

app.controller('modProfileController', function($scope, $http, $filter) {

    console.log("Here");

    $scope.model = {
        isDisabled: true
    };

    $scope.enableAvailability = function() {
        alert("Here");
    };
});