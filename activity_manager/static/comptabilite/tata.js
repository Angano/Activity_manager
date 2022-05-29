var url = window.location.origin
// Delete ligne
$('body').on('click','.dd', function(){
    var pk = $(this).data('id');
    var brouillon = $(this).data('brouillon');
    console.log(pk, brouillon);
    $('#table').load(url+'/comptabilite/test/delete/'+pk+' #table')


})

$('body').on('submit','#myform',function(e){
    e.preventDefault();
    var mon_formulaire = new FormData(document.getElementById('myform'))
    var xml = new XMLHttpRequest()
    xml.open('POST',url+'/comptabilite/add_line_test/' )

    xml.onload=function(){
        $('#table').load(window.location +' #table')
        document.getElementById('myform').reset()

    }
    xml.send(mon_formulaire)
})

 var div = document.createElement('div')
 div.id = "resultatNom"
// Recherche d'une activite
function searchACtivite(){

        $("#id_nom").after(div)
         $("body").on('keyup','#id_nom',function(e){
            var datas = $(e.target).val()
            find_activite(datas)
            })
        }

 function find_activite(datas){

    $("#id_nom").after(div)
    if(datas.length>0){
        $.ajax({
            url:url+'/activite/articles/',
            type:'post',
            dataType:'json',
            data:{'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val(),'datas':datas},
            success:function(code, status){

                     $("#id_nom").keyup(function(e){
                     $('.maurice').remove()

                        var retour ='<ul id="myul">'
                        for(key in code){
                            retour = retour+
                            '<li class="maurice" data-activitepk='+code[key]["pk"]+'>'+code[key]['fields']['nom']+
                            '</li>'
                            }
                        retour = retour + '</ul>'

                        $("#resultatNom").html(retour);
                        $(".maurice").on('click',function(e){
                            var tab = (Object.values(code).find(activite => activite.pk===$(e.target).data('activitepk')))['fields']
                            $("#id_article").val($(e.target).data('activitepk')) ;
                            $("#id_nom").val(tab["nom"]) ;
                            $("#id_description").val(tab["description"]) ;
                            $("#id_prix").val(tab["prix"]) ;
                            $("#id_quantite").val(1) ;
                            $("#id_total").val(tab["prix"]*1) ;

                            $("#myul").remove();

                            })
                        })

                ;},
            error:function(jqXHR, textStatus,  errorThrown){
                console.log(errorThrown);
                return false;
                }
            })}
    else{
        return false;
    }

}
searchACtivite()

// calcul total ligne
$('body').on('change','.calcul', function(){
    $('#id_total').val((parseFloat($('#id_quantite').val().replace(',','.'))*parseFloat($('#id_prix').val().replace(',','.')).toFixed(2)))
})

$('body').on('click','.edit_ligne',function(){
    $('#form_modal').load(url+'/comptabilite/editLigne/'+$(this).data('id_ligne'))
})

$('body').on('click','#addLine',function(){
    $('#form_modal').load(url+'/comptabilite/test2/'+$('#trt').data('idbrouillon'))
})

// maj ligne dans modal
$('body').on('click','#saveForm',function(e){
    e.preventDefault();

    var data = document.getElementById('tutu');
    var form = new FormData(data)

    var xml = new XMLHttpRequest()
    xml.open('POST',url+'/comptabilite/editLigne/'+$('#tutu').data('id_ligne'))
    xml.onload=function(){
        $('#table').load(url+'/comptabilite/test/'+116+' #table')

    }
    xml.send(form)
})


