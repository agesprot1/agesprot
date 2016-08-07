// init $(document)
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
$(document).on("click", "#notification", function(){
	$('#content-alert').empty();
	show_loading('content-alert');
	$.ajax({
		url: "/notification/",
		success: function(data){
			$('#loading').remove();
			console.log(data)
			$.each(data, function (key, item) {
				$('#content-alert').append(
					'<li>'+
						'<div class="row">'+
							'<div style="padding: 5px 10px;">'+
								'<div class="col-md-1">'+
									'<i class="fa '+item.icon+' fa-fw circle-fa"></i>  '+
								'</div>'+
								'<div class="col-md-10">'+
									item.titulo_notificacion+
								'</div>'+
								'<div class="col-md-12">'+
									'<span class="pull-right small">'+item.fecha_notificacion+'</span>'+
								'</div>'+
							'</div>'+
						'</div>'+
					'</li>'+
					'<li class="divider"></li>'
				);
			});
			$('#content-alert').append(
				'<li>'+
					'<a href="/notification/me/" class="text-center">'+
						'<b>Ver todos</b> <i class="fa fa-angle-double-right"></i>'+
					'</a>'+
				'</li>'
			);
		}
	});
});
// end $(document)

// init function JS
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
function show_loading(id){
	$('#'+id).append(
		"<div class='text-center' id='loading'>"+
			"<img src='/static/img/loading.gif' alt='Cargando' style='width: 50px;'>"+
			"<h4>Cargando datos</h4>"+
		"</div>"
	);
}
// end function JS

// init other JS

(function(original){
	history.pushState = function(state){
		change(state);
		return original.apply(this, arguments);
	};
})(history.pushState);
setTimeout(function(){
	$('.alert').remove();
}, 5000);
// end other JS