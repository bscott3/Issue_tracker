/**
 * Created by Owner on 1/25/2017.
 */
var appServices = angular.module('app.services', []);

appServices.service('ProjectService', function($http){
   var self = this;

   self.fetchAllOwnerProjects = function(){
     return $http.get("/projects")
   };
});