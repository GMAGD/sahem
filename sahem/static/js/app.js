/**
 * Created by ilyes on 3/8/16.
 */
var sahemApp = angular.module('sahemApp', ['ui.router', 'ngResource', 'ngRoute']);

// url settings
var port = '8000';
var baseUrl = 'http://localhost:' + port;

sahemApp.config(['$interpolateProvider', '$httpProvider', '$routeProvider', '$resourceProvider', '$urlRouterProvider', function ($interpolateProvider, $httpProvider, $routeProvider, $resourceProvider, $urlRouterProvider) {

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
    $http.get(baseUrl + '/api/events/' + $routeParams.catSlug).then(function (responce) {
        $scope.events = responce.data;
    });

    // Get all the categories
    $http.get(baseUrl + '/api/categories/?format=json').then(function (responce) {
        $scope.categories = responce.data;
    })
});

sahemApp.controller('aboutController', function ($scope, $location) {
});

