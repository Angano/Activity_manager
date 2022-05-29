var url = window.location.origin;

function get_eleves(){
    var tab=($('input[name="composition"]')).get();
    var data_eleve = [];
    for(var i=0;i<tab.length; i++){
            data_eleve.push(parseInt(tab[i].value));
            }
    return JSON.stringify(data_eleve)
}

$('#search').keyup(function(e){
    if(e.target.value.length > 2){

        $.ajax({
            url:url+'/activite/get_eleve/',
            method:'POST',
            data: {'csrfmiddlewaretoken':$('input[name="csrfmiddlewaretoken"]').val(),'data':e.target.value,'data_eleve':get_eleves()},
            success:function(code, status){
                $('#resultat').html(code)
                $('*[data-eleve]').on('click',function(e){
                    var id = e.target.id;
                    console.log(id.split('_')[2])
                    console.log(e.target)
                    ell = '<label class="badge bg-secondary text-dark m-1" for="'+id+'"><input name="composition" checked type="checkbox" value="'+id.split("_")[2]+'" id="'+id+'">'+e.target.innerText+'</label>';

                    $('#tata').append(ell)
                    e.target.remove()
                })


            }
            })
    
    
    }else{
    $('#resultat').html('')}
})

$( ".datepick" ).datepicker(
{
   onSelect:function(dateText,object){
   dateText = dateText.split('-')[1]+'-'+dateText.split('-')[0];

        var token = $('input[name="csrfmiddlewaretoken"]').val();
        var activite_pk = window.location.href.split('/')

        activite_pk = activite_pk[activite_pk.length - 1];
        $.ajax(
            {

            url:url+'/pointage/synthese_mensuelle/'+activite_pk,
            type:'POST',
            dataType:'html',
            data:{'csrfmiddlewaretoken':token,'pk':activite_pk, 'datepointage':dateText},
            success:function(code,status){

            var toti = $('#table_resultat',$(code));
            console.log(code)
            var nom_activite = $('#activite_nom',$(code));

            $('#tit').html(toti);
            $('#activite_nom').text(nom_activite.text())

            },
            complete:function(code, status){
                //console.log($($('#activite_nom'),$(code.responseText)).text())
            }});},
   dateFormat: "mm-yy",
})