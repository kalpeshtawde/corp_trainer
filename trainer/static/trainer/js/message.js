var app = angular.module('message', [], function($interpolateProvider) {
    // {{}} interpolated with [[]]
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});

app.controller('messageController', function($scope, $http, $filter) {
    //$scope.messageList = [{msgText: 'Finish this app', done: false}];

    $http.get('/trainer/api/message/').then(function(response) {
        $scope.messageList = response.data
        $scope.messageList = []
        for (var i= 0; i < response.data.length; i++) {
            var message = {};
            message.msgId = 'collapse' + i;
            message.msgText = response.data[i].message;
            message.msgPhone = response.data[i].phone;
            message.msgEmail = response.data[i].email;
            message.msgDateTime = response.data[i].dttime;
            $scope.messageList.push(message);
        }
        $scope.byOrder = 'msgDateTime';
    })

    $scope.sortMessage = function(order) {
        if (order == 1) {
            $scope.messageList = $filter('orderBy')($scope.messageList, '-msgDateTime')
        } else {
            $scope.messageList = $filter('orderBy')($scope.messageList, 'msgDateTime')
        }
    };

    $scope.messageAdd = function() {
        $scope.messageList.push({msgText: $scope.inputMessage, done: false});
        $scope.inputMessage = '';
    };

    $scope.remove = function() {
        var oldList = $scope.messageList;
        $scope.messageList = [];
        angular.forEach(oldList, function(x){
            if (!x.done) {
            $scope.messageList.push(x);
            };
        })
    };

});