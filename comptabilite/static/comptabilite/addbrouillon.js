 var pattern = /^[0-9]*($|(\.[0-9]{0,})$)/

// url
var url = window.location.origin
// affiche le corp du brouillon si présence d'éléments
function showDraft(){
    var childs = parseInt($('#tbody').children().length);
    if(childs>0){
        $('.draft').show()
    }else{
        $('.draft').hide()
    }
}
// calcul total
function calculTotal(){
    var total = $('input[name="total"]')
    var x = 0
    for(var i =0; i<total.length; i++){

        if(!isNaN(parseFloat($(total[i]).val()).toFixed(2))){
            x = parseFloat($(total[i]).val())+x

        }
    }
    $('#totalFacture').text(parseFloat(x).toFixed(2).toString())
    showDraft();

}


// Recherche d'une activite
function searchACtivite(){
         $("#id_nom").keyup(function(e){
            var datas = $(e.target).val()
            find_activite(datas)
            })
        }


function find_activite(datas){

    $('#add-ligne').find('input').not($('#id_nom')).not($('input[reset]')).val('')
    if(datas.length>0){
        $.ajax({
            url:url+'/activite/articles/',
            type:'post',
            dataType:'json',
            data:{'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val(),'datas':datas},
            success:function(code, status){

                     $("#id_nom").keyup(function(e){
                     $('.myul').remove()

                        var retour ='<ul id="myul">'
                        for(key in code){
                            retour = retour+
                            '<li class="myul list-group-item list-group-item-action " data-activitepk='+code[key]["pk"]+'>'+code[key]['fields']['nom']+'</li>'
                            }
                        retour = retour + '</ul>'
                        $("#resultatNom").html(retour);
                        $(".myul").on('click',function(e){
                            e.preventDefault();
                            var tab = (Object.values(code).find(activite => activite.pk===$(e.target).data('activitepk')))['fields']
                            $("#id_nom").val(tab["nom"]) ;
                            $("#id_description").val(tab["description"]) ;
                            $("#id_prix").val(tab["prix"]) ;
                            $("#id_quantite").val(1) ;
                            $("#id_total").val(tab["prix"]*1) ;
                            $("#id_article").val($(e.target).data('activitepk'))
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


// Recherche d'un client
$("#client").keyup(function(e){
    var data = $(e.target).val()

    if(data.length>0){

        $.ajax({
            url:url+'/famille/searchParent/',
            type:'post',
            dataType:'text',
            data:{'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val(),'parent':data},
            success:function(code, status){
                var tab = JSON.parse(code);
                tab = Object.values(tab);
                var parents = '';
                tab.forEach(function(value,key){
                    var champ = value['fields'];
                    parents = parents +'<button class=" d-block list-group-item list-group-item-action" data-parent='+value['pk']+'>'+champ['nom']+' '+champ['prenom']+'</button>';
                    });
                ;
                $('#resultatParent').html(parents);
                $('#resultatParent>button').on('click',function(e){
                    $("#resultatParent").html('')
                    $("#resultatClient").val($(e.target).data('parent'))
                    $("#client").val($(e.target).text())
                })
                },
            error: function (xhr, ajaxOptions, thrownError) {
                console.log(xhr.responseText,thrownError);
                },
        })
    }

    })

// validation du nouveau brouillon
$('#monFormulaire').submit(function(e){
    $('#add-ligne').remove()
    e.preventDefault();
    var monFormulaire = document.getElementById('monFormulaire')
    var forma = new FormData(monFormulaire);
    $.ajax({
        url:url+'/comptabilite/addbrouillonNew/',
        type:'post',
        processData: false,
        contentType: false,
        data :  forma,
        success:function(code, status){
            window.location.href=url+'/comptabilite/brouillons/'
        }
    })
})

// utile pour ajouter un brouillon
$('#ajouter').on('click',function(){
    if($('#id_article').val()!==''){
        var ligne = $('#add-ligne').clone()
        $(ligne).find('span').remove()
        $(ligne).find('#resultatNom').remove()
        $(ligne).find('input').removeAttr('id').prop('readonly',true).prop('required',true)

    // Création d'un bouton delete
        var deleteButton = document.createElement('span')
        deleteButton.className = 'btn-secondary btn btn-sm delete '
        deleteButton.textContent = 'X'
        $(ligne).children().last('td').append(deleteButton)
        $(ligne).removeAttr('id')

        $('#tbody').append(ligne)
        $('#add-ligne').find('input').val('')
       calculTotal()
    }
    else{
        alert('Choisissez une activité valide')
    }


})
// Date picker
$( "#id_date_brouillon" ).datepicker({
   onSelect:function(dateText,object){
   dateText = dateText.split('-')[1]+'-'+dateText.split('-')[0];
   },
   dateFormat: "yy-mm-dd",
   })

// Reset de la ligne ajout article
$('body').on('click','#reset', function(){
    $('#add-ligne').find('input').val('')
    $('.myul').remove()
   calculTotal()
})

searchACtivite()

// Mise à jour des champs dans un brouillon
$('body').on('click','.editable',function(){
    $(this).prop('readonly',false)
    var quantiteStart = parseFloat($(this).parents('tr').find('input[name="quantite"]').val().replace(',','.')).toFixed(2)
    var prixStart = parseFloat($(this).parents('tr').find('input[name="prix"]').val().replace(',','.')).toFixed(2)
    $('body').on('focusout','.editable',function(){
       calculTotal()

        $(this).prop('readonly',true)
        var prix = parseFloat($(this).parents('tr').find('input[name="prix"]').val().replace(',','.')).toFixed(2)
        var quantite = parseFloat($(this).parents('tr').find('input[name="quantite"]').val().replace(',','.')).toFixed(2)

        if(prix.toString().match(pattern)){
            $(this).parents('tr').find('input[name="prix"]').val(prix)}
        else{
                $(this).val(prixStart)}
       if(quantite.toString().match(pattern)){
            $(this).parents('tr').find('input[name="quantite"]').val(quantite)}
         else{
                $(this).val(quantiteStart)}
        var totalLigne = (prix*quantite).toFixed(2)

        $(this).parents('tr').find('input[name="total"]').val(totalLigne)
        $('body').off('focusout','.editable')
       calculTotal()

    })
})



// Suppression d'une ligne dans le brouillon
$('body').on('click','.delete',function(){
    $(this).parents('tr').remove()
   calculTotal()
})
$('body').on('click','#erase',function(){
    $(this).prev().val('').focus()
    $('#resultatParent').html('')
})
