$(document).ready(function(){		
	$('#addUser').click(function(){
		$('#userModal').modal({
			backdrop: 'static',
			keyboard: false
		});		
		$("#userModal").on("shown.bs.modal", function () {
			$('#userForm')[0].reset();				
			$('.modal-title').html("<i class='fa fa-plus'></i> Add user");					
			$('#action').val('addUser');
			$('#save').val('Save');
		});
	});		
});

$(document).ready(function(){		
	$('#addpetugas').click(function(){
		$('#petugasModal').modal({
			backdrop: 'static',
			keyboard: false
		});		
		$("#petugasModal").on("shown.bs.modal", function () {
			$('#userForm')[0].reset();				
			$('.modal-title').html("<i class='fa fa-plus'></i> Add Petugas");					
			$('#action').val('addUser');
			$('#save').val('Save');
		});
	});		
});