$(document).on("click", ".open-modal", function(e){
	$('#Modal').load($(this).attr('href'),function(){
		$('#Modal').modal({
			show:true
		});
	});
	return false;
});
$(document).on("click", ".delete", function(){
	var id = $(this).attr('id');
	var href = $(this).attr('href');
	Lobibox.alert('info', {
		title: "Alerta",
		msg: "¿Desea eliminar el objecto seleccionado?",
		buttons:{
			yes: {
				'class': 'btn btn-warning'
			},
			no: {
				'class': 'btn btn-primary'
			}
		},
		callback: function(lobibox, type){
			if(type == 'yes'){
				$.get(href, function(data){
					show_message(data.type, data.msg);
					if(data.type == 'success'){
						$('#object-'+id).remove();
					}
				});
			}
			else{
				show_message('success', 'Cancelado por el usuario');
			}
		}
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
function change(state){
	if(state === null){
		$(document).text("Original");
	}else{
		$(document).text(state.url);
	}
}
$(document).on("click", ".url", function(){
	history.pushState({url: $(this).attr('href')}, $(this).attr('href'), '');
});
$(window).on("popstate", function(e) {
	console.log(e.originalEvent.state);
});
(function(original){
	history.pushState = function(state){
		change(state);
		return original.apply(this, arguments);
	};
})(history.pushState);
setTimeout(function(){
	$('.alert').remove();
}, 5000);