var app = angular.module('trainer', [], function($interpolateProvider) {
    // {{}} interpolated with [[]]
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});

// Profile modifications controlled by modifyController
app.controller('modifyController', function($scope, $http, $filter) {

    $scope.disableAvailability = true;

    $http.get('/trainer/api/availability/').then(function(response) {
        $scope.locations_text = response.data[0].locations
        $scope.hours_per_week_text = response.data[0].hours_per_week
    })

    $scope.enableAvailability = function() {
        $scope.disableAvailability = false;
    };


    $scope.updateAvailability = function() {
        var data = {
            "locations": $scope.locations_text,
            "hours_per_week": $scope.hours_per_week_text,
            };
        console.log(data)
        $http.put('/trainer/api/availability/', data);
        $scope.disableAvailability = true;
    }
})

// All the messaging controlled by messageController
app.controller('messageController', function($scope, $http, $filter) {
    $scope.showMessageModal = true;

    $http.get('/trainer/api/message/').then(function(response) {
        $scope.messageList = response.data
        $scope.messageList = []
        for (var i= 0; i < response.data.length; i++) {
            var message = {};
            message.msgId = 'collapse' + i;
            message.rawMsgId = response.data[i].id;
            message.msgText = response.data[i].message;
            message.msgPhone = response.data[i].phone;
            message.msgEmail = response.data[i].email;
            message.msgRead = response.data[i].read;
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

    $scope.readMessage = function(message) {
        if (! message.msgRead) { // Do not change the flag is message is already read
            var data = {
                "id": message.rawMsgId,
                "message": message.msgText,
                "phone": message.msgPhone,
                "email": message.msgEmail,
                "read": true,
                "dttime": message.msgDateTime
            };
            console.log(data)
            $http.patch('/trainer/api/message/', data);
        }
    }

    $scope.sortMessage = function(order) {
        if (order == 1) {
            $scope.messageList = $filter('orderBy')($scope.messageList, '-msgDateTime')
        } else {
            $scope.messageList = $filter('orderBy')($scope.messageList, 'msgDateTime')
        }
    }

    $scope.messageAdd = function() {
        $scope.messageList.push({msgText: $scope.inputMessage, done: false});
        $scope.inputMessage = '';
    }

    $scope.remove = function() {
        var oldList = $scope.messageList;
        $scope.messageList = [];
        angular.forEach(oldList, function(x){
            if (!x.done) {
            $scope.messageList.push(x);
            };
        })
    }

});