$(document).ready(function(){
	$('#addBook').click(function(){
		$('#bookModal').modal({
			backdrop: 'static',
			keyboard: false
		});		
		$("#bookModal").on("shown.bs.modal", function () {
			$('#bookForm')[0].reset();				
			$('.modal-title').html("<i class='fa fa-plus'></i> Add Book");					
			$('#action').val('addBook');
			$('#save').val('Save');
		});
	});		
});

$(document).ready(function(){
	$('#pengembalianBook').click(function(){
		$('#pemgembalianModal').modal({
			backdrop: 'static',
			keyboard: false
		});		
		$("#pemgembalianModal").on("shown.bs.modal", function () {
			$('#bookForm')[0].reset();				
			$('.modal-title').html("<i class='fa fa-plus'></i> Pengembalian");					
			$('#action').val('addBook');
			$('#save').val('Save');
		});
	});		
});

$(document).ready(function(){
	$('#pinjamBook').click(function(){
		$('#pinjamModal').modal({
			backdrop: 'static',
			keyboard: false
		});		
		$("#pinjamModal").on("shown.bs.modal", function () {
			$('#bookForm')[0].reset();				
			$('.modal-title').html("<i class='fa fa-plus'></i> Peminjaman");					
			$('#action').val('addBook');
			$('#save').val('Save');
		});
	});		
});

// $(document).ready(function(){
// 	$('#addBook').click(function(){
// 		$('#book').modal({
// 			backdrop: 'static',
// 			keyboard: false
// 		});		
// 		$("#addBook").on("shown.bs.modal", function () {
// 			$('#bookForm')[0].reset();				
// 			$('.modal-title').html("<i class='fa fa-plus'></i> Add Book ");					
// 			$('#action').val('addBook');
// 			$('#save').val('Save');
// 		});
// 	});		
// });

