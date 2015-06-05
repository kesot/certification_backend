;
$(function(){

	path = $(location).attr('pathname');


	$('.tab').removeClass('active'),

	$('.tab').each(function(){

		if( ($(this).attr('data-href') == $(location).attr('pathname')) && ($(location).attr('pathname') !== '/'))
			$(this).addClass('active');

	});


	$('.tab').on('click',function(){

		location.href = $(this).attr('data-href');

	});

	$('.cert').on('click',function(){

		location.href = $(this).attr('data-id');

	});	

});