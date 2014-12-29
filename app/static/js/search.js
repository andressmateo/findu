angular.module('ui.bootstrap.search', ['ui.bootstrap']);
        angular.module('ui.bootstrap.search').controller('TypeaheadCtrl', function($scope, $http) {

  $scope.getLocation = function(val) {
    return $http.get('/buscar_json', {
      params: {
        method : 'GET',
        search: val,
      }
    }).then(function(response){
    return response.data.names.map(function(item){
        return item.name;
      });
    });
  };
  });