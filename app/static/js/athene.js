var athene = angular.module('ui.bootstrap.athene', ['ui.bootstrap']);

athene.controller('TypeaheadCtrl', function($scope, $http) {

  $scope.getPossibilities = function(val) {
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

athene.controller('ModalDemoCtrl', function ($scope, $modal) {

  $scope.openConfirmationModal = function (size) {
    var modalInstance = $modal.open({
      templateUrl: 'confirmation.html',
      controller: 'ModalInstanceCtrl',
      size: size,
      resolve: {}
    });
  };

});

athene.controller('ModalInstanceCtrl', function ($scope, $modal, $modalInstance, $http) {

  $scope.deleteUniversity = function (id) {
    $http.get('/panel/delete_university', {
      params: {
        method : 'POST',
        id: id,
      }
    }).then(function(response){
          $scope.openStatusModal(response.data)
          $modalInstance.close();
    });
  };

  $scope.deleteCareer = function (id) {
    $http.get('/panel/delete_career', {
      params: {
        method : 'POST',
        id: id,
      }
    }).then(function(response){
          $scope.openStatusModal(response.data)
          $modalInstance.close();
    });
  };

  $scope.deleteName = function (name) {
    $http.get('/panel/delete_name', {
      params: {
        method : 'POST',
        name: name,
      }
    }).then(function(response){
          $scope.openStatusModal(response.data)
          $modalInstance.close();
    });
  };

  $scope.deleteCampus = function (id) {
    $http.get('/panel/delete_campus', {
      params: {
        method : 'POST',
        id: id,
      }
    }).then(function(response){
          $scope.openStatusModal(response.data)
          $modalInstance.close();
    });
  };

   $scope.deleteCatUniversity = function (id) {
    $http.get('/panel/delete_cat_university', {
      params: {
        method : 'POST',
        id: id,
      }
    }).then(function(response){
          $scope.openStatusModal(response.data)
          $modalInstance.close();
    });
  };

$scope.deleteKnowledgeArea = function (id) {
    $http.get('/panel/delete_knowledge_area', {
      params: {
        method : 'POST',
        id: id,
      }
    }).then(function(response){
          $scope.openStatusModal(response.data)
          $modalInstance.close();
    });
};


  $scope.openStatusModal = function (status) {
    if(status=='0'){
      template = 'fail.html'
    }else if(status=='1'){
      template = 'ok.html'
    }
    var modalInstance = $modal.open({
      templateUrl: template,
      controller: 'OkModalCtrl',
      resolve: {
      }
    });
  };

  $scope.cancel = function () {
    $modalInstance.close();
  };
});

athene.controller('OkModalCtrl', function ($scope, $modalInstance, $http, $window) {

  $scope.close = function (ref) {
    if(ref=='university'){
      $window.location.href = "/panel/list_university";
    }else if(ref=='career'){
      $window.location.href = "/panel/list_career";
    }if(ref=='name'){
      $window.location.href = "/panel/list_name";
    }if(ref=='campus'){
      $window.location.href = "/panel/list_campus";
    }if(ref=='cat'){
      $window.location.href = "/panel/list_cat_university";
    }if(ref=='know'){
      $window.location.href = "/panel/list_knowledge_area";
    }
    $modalInstance.close();
  };

});

athene.filter('searchForKnowledges', function(){

	return function(arr, knowledge_question){
		if(!knowledge_question){
			return arr;
		}

		var result = [];
		knowledge_question = knowledge_question.toLowerCase();

		angular.forEach(arr, function(item){
			if(item.toLowerCase().indexOf(knowledge_question) !== -1){
				result.push(item);
			}
		});
		return result;
	};
});