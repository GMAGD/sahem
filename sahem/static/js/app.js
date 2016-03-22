/**
 * Created by ilyes on 3/8/16.
 */
var sahemApp = angular.module('sahemApp', ['ui.router', 'ngResource', 'ngRoute']);

// url settings
var port = '8000';
var baseUrl = 'http://localhost:' + port;

sahemApp.config(['$interpolateProvider', '$httpProvider', '$routeProvider', '$resourceProvider', '$urlRouterProvider', '$locationProvider', function ($interpolateProvider, $httpProvider, $routeProvider, $resourceProvider, $urlRouterProvider, $locationProvider) {

    // Force angular to use square brackets for template tag
    // The alternative is using {% verbatim %}
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
    // CSRF Support
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

    ////// This only works in angular 3!
    ////// It makes dealing with Django slashes at the end of everything easier.
    //$resourceProvider.defaults.stripTrailingSlashes = false;
    //
    //$urlRouterProvider.otherwise('/');

    $routeProvider
        .when('/', {
            templateUrl: 'static/partials/pages/home.html',
            controller: 'mainController'
        })
        .when('/home', {
            templateUrl: 'static/partials/pages/home.html',
            controller: 'mainController'
        })
        .when('/events', {
            templateUrl: 'static/partials/events/list.html',
            controller: 'eventController'
        })
        .when('/events/:catSlug', {
            templateUrl: 'static/partials/events/list.html',
            controller: 'eventCategoryController'
        })
        .when('/event/:id', {
            templateUrl: 'static/partials/events/detail.html',
            controller: 'eventDetailController'
        })
        .when('/about', {
            templateUrl: 'static/partials/pages/about.html',
            controller: 'aboutController'
        })
        .otherwise('/');


}]);


sahemApp.controller('mainController', function ($scope, $http) {

});

sahemApp.controller('eventController', function ($scope, $http) {
    $scope.message = 'hello my nigga from the event list';

    // Get all the events
    $http.get(baseUrl + '/api/events/?format=json').then(function (responce) {
        $scope.events = responce.data;
    });

    // Get all the categories
    $http.get(baseUrl + '/api/categories/?format=json').then(function (responce) {
        $scope.categories = responce.data;
    })
});


sahemApp.controller('eventCategoryController', function ($scope, $http, $routeParams) {

    // Get events by category
    $http.get(baseUrl + '/api/events/category/' + $routeParams.catSlug).then(function (responce) {
        $scope.events = responce.data;
    });

    // Get all the categories
    $http.get(baseUrl + '/api/categories/?format=json').then(function (responce) {
        $scope.categories = responce.data;
    })
});

sahemApp.controller('aboutController', function ($scope, $location) {
});

sahemApp.controller('eventDetailController', function ($scope, $http, $routeParams) {

    $scope.event = {};

    $http.get(baseUrl + '/api/events/' + $routeParams.id + '/?format=json').then(function (responce) {
        $scope.event = responce.data;

        // split the start date an time
        var startDateTime = $scope.event.start.split('T');
        // split the end date and time
        var endDateTime = $scope.event.end.split('T');

        $scope.event.start = {
            date: startDateTime[0],
            time: startDateTime[1]
        };

        $scope.event.end = {
            date: endDateTime[0],
            time: endDateTime[1]
        };
        console.log($scope.event);

        // check if the acctual is user is the owner of the event
        if ($scope.event.owner.username == username) {
            $scope.isUser = true;
        }

        // Display the event into a Google maps using Google maps api
        // setup the map options zoom default position
        var mapOptions = {
            zoom: 12,
            center: new google.maps.LatLng($scope.event.latitude, $scope.event.longitude),
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };

        // get an instance of the google map
        $scope.map = new google.maps.Map(document.getElementById('map'), mapOptions);

        // set a marker with the event lat and long
        var marker = new google.maps.Marker({
            map: $scope.map,
            position: new google.maps.LatLng($scope.event.latitude, $scope.event.longitude),
            title: $scope.event.address
        });


        // Join event as a staff
        $scope.joinEventAsStaff = function () {
            $http.post(baseUrl + '/api/events/join/event/' + $scope.event.id + '/staff/' + userId + '/').then(function (responce) {
                $scope.isStaff = true;
                console.log(responce);
            })
        };
        $scope.isStaff = isUserStaff(userId, $scope.event.staff);
        console.log($scope.isStaff);

        // Join event as a participant
        $scope.joinEventAsParticipant = function () {
            $http.post(baseUrl + '/api/events/join/event/' + $scope.event.id + '/participant/' + userId + '/').then(function (responce) {
                $scope.isParticipant = true;
                console.log(responce);
            })
        };
        $scope.isParticipant = isUserParticipant(userId, $scope.event.participant);
        console.log($scope.isParticipant);

        // Leave Event
        $scope.leaveEvent = function () {
            var baseUrlApi = baseUrl + '/api/events/leave/event/' + $scope.event.id;

            // if the acctual user is a staff a this event
            if ($scope.isStaff) {

                $http.post(baseUrlApi + '/staff/' + userId + '/').then(function (responce) {
                    console.log(responce.data);
                    $scope.isStaff = false;
                    console.log('leaved the event');
                });

            } else if ($scope.isParticipant) {

                $http.post(baseUrlApi + '/participant/' + userId + '/').then(function (responce) {
                    console.log(responce.data);
                    $scope.isParticipant = false;
                    console.log('leaved the event');
                });

            }


        };


        // Save comment
        $scope.saveComment = function () {

            var data = {
                user_id: userId,
                event_id: $scope.event.id,
                comment: $scope.comment
            };

            $http.post('/api/comments/add/', data).then(function (responce) {
                $scope.event.comments.push({
                    user: $scope.event.owner,
                    content : $scope.comment
                });
                console.log(responce);
            });
        }
    });
});


function isUserStaff(staffId, staffs) {
    for (var i = 0; i < staffs.length; i++) {
        if (staffId == staffs[i].id) {
            return true;
        }
    }
    return false;
}


function isUserParticipant(participantId, participants) {
    for (var i = 0; i < participants.length; i++) {
        if (participantId == participants[i].id) {
            return true;
        }
    }
    return false;
}
