var app = angular.module('message', [], function($interpolateProvider) {
    // {{}} interpolated with [[]]
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});

app.controller('messageController', function($scope, $http, $filter) {
    //$scope.messageList = [{msgText: 'Finish this app', done: false}];
    $scope.disableAvailability = true;
    $scope.showMessageModal = true;

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

    $scope.validEmail = function(email) {
        var filter = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
        if (!filter.test(email)) {
            return false;
        }
    return true;
    }

    $scope.sendMsg = function() {
        $scope.blankMessage = false;
        $scope.blankPhone = false;
        $scope.blankEmail = false;


        if (!$scope.message_text) {
            $scope.blankMessage = true;
        };
        if (!$scope.message_phone) {
            $scope.blankPhone = true;
        };
        if (!$scope.message_email || !$scope.validEmail($scope.message_email)) {
            $scope.blankEmail = true;
        };

        if (! $scope.blankMessage && !$scope.blankPhone && !$scope.blankEmail) {
            var data = {
            "profile": 1,
            "message": $scope.message_text,
            "phone": $scope.message_phone,
            "email": $scope.message_email,
            "read": false,
            "dttime": "2019-01-10T15:03:50.683434Z"
            };
            $http.put('/trainer/api/message/', data);

            //This is to close modal and backdrop of modal.
            $scope.showMessageModal = false;
            $('body').removeClass('modal-open');
            $('.modal-backdrop').remove();
        }

    }

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

    $scope.enableAvailability = function() {
        $scope.disableAvailability = false;
    };


});