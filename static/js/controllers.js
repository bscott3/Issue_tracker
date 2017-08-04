/**
 * Created by bscott3 on 12/4/15.
 */
var appContrl = angular.module('app.controllers', []);

appContrl.controller('LoginCtrl', function($scope, $timeout, $mdSidenav, $log){
    $scope.toggleRight = function(){
                $mdSidenav('right')
          .toggle()
          .then(function () {
            $log.debug("toggle is done");
          });
    };
})

 .controller('RightCtrl', function ($scope, $timeout, $mdSidenav, $log) {
    $scope.close = function () {
      // Component lookup should always be available since we are not using `ng-if`
      $mdSidenav('right').close()
        .then(function () {
          $log.debug("close RIGHT is done");
        });
    };
  })

 .controller('HomeCtrl', function ($scope, $log, ProjectService, $state) {
        $scope.projects = [];
        ProjectService.fetchAllOwnerProjects().then(function (resp) {
            console.log(resp);
            $scope.projects = resp.data;
        },function (err) {
            $log.error(err)
        });

        $scope.goToProjectDetail = function (datastore_id){
            $state.go('app.projectDetail', {id:datastore_id})
        };

  }).controller('ProjectDetailCtrl', function ($scope, $log, ProjectService, $stateParams) {
        console.log($stateParams.id)

  });;
