var app = angular.module('message', []);

app.controller('messageController', function($scope, $http) {
    //$scope.messageList = [{msgText: 'Finish this app', done: false}];
    $http.get('/trainer/api/message/').then(function(response) {
        $scope.messageList = response.data
        $scope.messageList = []
        for (var i= 0; i < response.data.length; i++) {
            var message = {};
            message.msgId = response.data[i].id
            message.msgText = response.data[i].message
            message.msgPhone = response.data[i].phone
            message.msgEmail = response.data[i].email
            $scope.messageList.push(message)
        }
    })

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
            }
        })
    }

})