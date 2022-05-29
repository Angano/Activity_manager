var url = window.location.origin


$('body').on('click','.testEdit', function(e){
    e.preventDefault();
    $('#buttonBack').hide()

    $.get($(this).prop('href'),function(data){
        var $data=$(data)

        $('#modal-body').html($data.find('#table'))
        $('#titreHeader').html($data.find('#tity'))
    })



})

$('body').on('click','.edit_ligne',function(){
    $('#modal-body').load(url+'/comptabilite/editLigne/'+$(this).data('id_ligne'))

    $('#buttonTransfered').hide()
    $('#buttonBack').show()
})



// maj ligne dans modal
$('body').on('submit','#saveForm',function(e){
    e.preventDefault();

    var data = document.getElementById('saveForm');
    var form = new FormData(data)

    var xml = new XMLHttpRequest()
    xml.open('POST',url+'/comptabilite/editLigne/'+$('#saveForm').data('id_ligne'))
    xml.onload=function(){
        $('#table').load(url+'/comptabilite/test/'+$('#trt').data('idbrouillon')+' #table')

    }
    xml.send(form)
})

// insertion nouvelle ligne dans brouillon
$('body').on('submit','#oloo',function(e){
    e.preventDefault();
    var mon_formulaire = new FormData(document.getElementById('bob'))
    var xml = new XMLHttpRequest()
    xml.open('POST',url+'/comptabilite/add_line_test/' )

    xml.onload=function(){
        document.getElementById('myform').reset()
        $('#modal-body').load(url+'/comptabilite/test/'+$('#trt').data('idbrouillon')+' #table')
        $('#buttonBack').toggle()
        $('#addLine').toggle()
        $('#buttonTransfered').toggle()




    }
    xml.send(mon_formulaire)



})

// Effacement d'une ligne dans un brouillon
$('body').on('click','.dd', function(){
    var pk = $(this).data('id');
    var brouillon = $(this).data('brouillon');
    console.log(pk, brouillon);
    $('#table').load(url+'/comptabilite/test/delete/'+pk+' #table')


})




