var url = window.location.origin
/*$("table .ui-datepicker-calendar").hide();*/

// modal pour pointages
$('body').on('click','.modalPointage',function(){
    $(this).preventDefault
    $('.modal-content').html('') // on efface les données dans la boite modal
    $.get(url+$(this).attr('href'),function(data){
   $('.modal-content').html(data)
    })

})

// validation du pointage
$('body').on('submit','#myForm2',function(e){
    e.preventDefault();
    var form = document.getElementById('myForm2')
    var formData = new FormData(form)
    var xml = new XMLHttpRequest()

    xml.open('POST',url+'/pointage/add_pointage/'+$('#id_activite').val(), true)
    xml.onload= function(){
        alert('Enregistrement fait')
    }

    xml.send(formData)
})






