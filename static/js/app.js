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

app.config(function($stateProvider) {
  var helloState = {
    name: 'nav',
    url: '/nav',
    templateUrl: 'static/views/nav.html'
  }

  var aboutState = {
    name: 'home',
    url: '/home',
    templateUrl: 'static/views/home.html'
  }

  $stateProvider.state(helloState);
  $stateProvider.state(aboutState);
});
