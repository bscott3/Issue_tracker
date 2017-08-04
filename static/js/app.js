'use strict';

var app = angular.module('app', [
    //insert app dependencies here
    'ui.router',
    'app.controllers',
    'app.services',
    'ngMaterial',
    'ngAria',
    'ngAnimate'
]);
app.config(["$locationProvider", function ($locationProvider) {
    $locationProvider.html5Mode(true);
}]);
app.config(function ($stateProvider, $urlRouterProvider) {
    $stateProvider

    //Default angular route that all other routes are stemmed from

        .state('app', {

            url: "/app",

            abstract: true,

            templateUrl: "static/views/nav.html"

        })

        .state('app.home', {

            url: "/home",

            abstract: false,

            templateUrl: "static/views/home.html"

        })
            .state('app.projectDetail', {

            url: "/projectDetail",

            abstract: false,

            templateUrl: "static/views/project_detail.html",
                params:{
                    id:null
                }

        })

    // if none of the above states are matched, use this as the fallback

    $urlRouterProvider.otherwise('/app/home');
});
