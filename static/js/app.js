'use strict';

var app = angular.module('app', [
      //insert app dependencies here
    'ui.router',
    'app.controllers'
]);

app.config(function ($stateProvider, $urlRouterProvider) {
    $stateProvider
    //Default angular route that all other routes are stemmed from
    .state('app', {
    url: "/app",
    abstract: true,
    templateUrl: "static/views/nav.html",
    controller: 'LoginCtrl'
    })
    //This is a dynamic Angular route it creates a angular route for all html partials in the static/partials dir
    .state({
     name: 'partials',
     url:"/app/:name",
     templateUrl: function($stateParams){
         return 'static/views/' + $stateParams.name + '.html'
     }
    });

    // if none of the above states are matched, use this as the fallback
    $urlRouterProvider.otherwise('/app/home');
});
