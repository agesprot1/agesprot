$(document).on("click", ".open-modal", function(e){
	$('#Modal').load($(this).attr('href'),function(){
		$('#Modal').modal({
			show:true
		});
	});
	return false;
});
function show_message(type, message){
	Lobibox.notify(type, {
		size: 'mini',
		rounded: true,
		delayIndicator: true,
		msg: message,
		sound: false
	});
}
$(document).ready(function() {
	$('.table').DataTable();
});