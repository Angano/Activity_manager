
// url
var url = window.location.origin
// id brouillon
var idBrouillon = $("#idbrouillon").data('idBrouillon')

// date sous formatt dd-mm-YY
function change_format_date(date){
    // retourne une date sous format iso
    var data = date.split('-');
    data = data[2]+'-'+data[1]+'-'+data[0]
    return data;
}

// modification dans la bdd de la ligne modifiée
function update_line(ligne){
    var ligne = ligne
    var id_ligne = ligne.data('idligne')
    var prix_uni = ligne.children('td[data-article="prix"]').text()
    var quantite = ligne.children('td[data-article="quantite"]').text()
    var description = ligne.children('td[data-article="description"]').text()

    var tab = {
                'id_ligne':id_ligne,
                'prix_uni':prix_uni,
                'description':description,
                'quantite':quantite
            }

     $.ajax({
            url:url+'/comptabilite/maj_ligne_brouillon/',
            type:'post',
            dataType:'json',
            data:{
                'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val(),
                'data':JSON.stringify(tab)},
            success:function(code, status){
                console.log(code)

                }

})
}

// Vide les champs input
function resetInput(){
    $('#addLigne').find('input:not(input[type=submit])').not($('#id_brouillon')).val('')
}

// Validation_pointage.html
// mise en page du tableau
function majTab(){
    $('.montant_total').html('')
    $('.montant').each(function(key,value){
        var id = $(value).attr('id')
        var html = $(value).html()
        $('#'+id+'_total').html(html)
    });
    // Raffraichissement des quantités
    $('.quantite_total').html('')
    $('.quantite').each(function(key,value){
        var id = $(value).attr('id')
        var html = $(value).html()
        $('#'+id+'_total').html(html)
        });
}


// affiche le détail dans validation_pointage.htmlElement
$('body').on('click','.categorie',function(e){
    //console.log(e.target.id+'_total')
    $('#modal-body').html($('#'+e.target.id+'_total').html())

})


// choix de la date
$( ".datepick" ).datepicker({
   onSelect:function(dateText,object){
    var date_debut =(change_format_date($('#date_debut').prop('value')));
    var date_fin = (change_format_date($('#date_fin').prop('value')));

    if(new Date(date_fin).getTime()>= new Date(date_debut).getTime()){
        $.ajax({url:url+'/comptabilite/validation_pointage/',
        type:'post',
        dataType:'html',
        data:{'date_debut':change_format_date(date_debut), 'date_fin':change_format_date(date_fin),'csrfmiddlewaretoken':$('input[name="csrfmiddlewaretoken"]').val()},
        success:function(code, status){
            $('#resultat').html($('#table',$(code)))
            $('#resultat2').html($('#resultat3',$(code)))
            majTab();
            $('#resultat').show()
        }})
    }else{
        $('#resultat').html('')
        $('#resultat').show()
        alert('Vérifier les dates');
    }
   }
   ,
   dateFormat: "dd-mm-yy"
})

// Mise à jour total facture
function calcul_total(){
    var data = $('tr[data-idligne]');
    var total = 0;
    for(i=0; i<data.length; i++){
        total = total+
                parseFloat($(data[i]).children('td[data-article=prix]').text().replace(',','.')).toFixed(2)*
                parseFloat($(data[i]).children('td[data-article=quantite]').text().replace(',','.')).toFixed(2);
    }
    $('#totalFacture').text(total.toFixed(2))
}

// Mise à jour total d'une ligne
function update_line_total(line){
    var price = parseFloat($(line).children('td[data-article=prix]').text()).toFixed(2)
    var quantity = parseFloat($(line).children('td[data-article=quantite]').text()).toFixed(2);
    var total = (price*quantity).toFixed(2);
    $(line).children('td[data-article=total]').text(total)
}

// Recherche d'une activite
function searchACtivite(){
     $("body").on('keyup','#searchActivite',function(e){
        $('#addLigne').find('input:not(input[type=submit])').not($('#id_brouillon')).not($('#searchActivite')).val('')
        var datas = $(e.target).val()
        find_activite(datas)
        })
    }

function find_activite(datas){

    if(datas.length>1){
        $.ajax({
            url:url+'/activite/articles/',
            type:'post',
            dataType:'json',
            data:{'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val(),'datas':datas},
            success:function(code, status){
                 $('.myul').remove()
                    retour ='<ul id="myul">'
                    for(key in code){
                        retour = retour+
                        '<li class="myul list-group-item list-group-item-action" data-activitepk='+code[key]["pk"]+'>'+code[key]['fields']['nom']+
                        '</li>'
                        }
                    retour = retour + '</ul>'

                    $("#resultatActivite").html(retour);
                    $(".myul").on('click',function(e){
                        var tab = (Object.values(code).find(activite => activite.pk===$(e.target).data('activitepk')))['fields']
                        $("#id_article").val($(e.target).data('activitepk')) ;
                        $("#searchActivite").val(tab["nom"]) ;
                        $("#id_description").val(tab["description"]) ;
                        $("#id_prix").val(tab["prix"]) ;
                        $("#id_quantite").val(1) ;
                        $("#id_total").val(tab["prix"]*1) ;

                        $("#resultatActivite").text('')

                        });},
            error:function(jqXHR, textStatus,  errorThrown){
                console.log(errorThrown);
                return false;},
            complete:function(code, status){

                }
            });
            }
    else{
        $('#myul').html('')
    }

}
searchACtivite()

// edit brouillon: Validation et insertion nouvelle ligne saisie
$("body").on('submit',"#myForm",function(e){
        // id factured

        e.preventDefault();

        if($('#id_article').val()!==''){
            var form = document.getElementById('myForm')
            var  formData = new FormData(form)
            var idBrouillon = $("#idbrouillon").data('idbrouillon')
            $.ajax({
                url:url+'/comptabilite/addLigneBrouillon/',
                type:'post',
                processData: false,
                contentType: false,
                data :  formData,
                success:function(code, status){
                    calcul_total()
                    resetInput();
                    $('#tableBrouillon').load('http://localhost:8000/comptabilite/brouillon_detail/'+idBrouillon+' #tableBrouillon')

                }
            }) }
        else {
            alert('Choisissez une activité valide')
        }

    })

// Suppression d'une ligne
$('body').on('click','.del',function(e){
    var ligne = $($(e.target).parent().parent()[0]).data('idligne');
    var token = $('input[name="csrfmiddlewaretoken"]').val();
    if(window.confirm('on supprime la ligne?')){
        $.ajax({
        url:url+'/comptabilite/deligne/',
        dataType:'html',
        type:'POST',
        data:{'csrfmiddlewaretoken':token,'idligne':ligne},
        success:function(code, status){
           $("tr[data-idligne='"+ligne+"']").remove();
            calcul_total()

        }})
    }
})

// Modification de la quantité
$("body").on('click','td[data-article=quantite]',function(e){
    // on récupère la ligne article
    var line = $(e.target).parent()

    // on ajoute un champ input
    var quantite = $(e.target)
    $(e.target).html('<input type="text" class="form-control modify-input" value="'+$(quantite).text()+'">')

    // sortie du focus
   var saisie_quantite = $(e.target).children('input')
   $(saisie_quantite).focus().focusout(function(){
        var qte = parseFloat($(saisie_quantite).val().replace(',','.')).toFixed(2);
        if(qte==''  || isNaN(qte)){
            qte = 0;
        }
        quantite.text(qte);
        update_line_total(line);
        calcul_total();
        update_line(line)
   })
})

// Modification du prix
$('body').on('click', "td[data-article=prix]", function(e){
    var line = $(e.target).parent();
    var prix = e.target;
    $(prix).html('<input type="text" value="'+$(prix).text()+'" class=" form-control modify-input">');
    $(prix).children().focus();
    $(prix).children().focusout(function(){
        var price = parseFloat($(prix).children().val().replace(',','.')).toFixed(2);
        if(price == "" || isNaN(price)){
            price = 0;}
        $(prix).text(price);
        update_line_total(line)
        calcul_total()
        update_line(line)
    })
})

// reset sur input
$('body').on('click','#clear',function(){
    resetInput()
})

// calcul total ligne
$('body').on('change','.calcul', function(){
    $('#id_total').val((parseFloat($('#id_quantite').val().replace(',','.'))*parseFloat($('#id_prix').val().replace(',','.')).toFixed(2)))
})

// page brouillons: chargement du détail d'un brouillon
$('body').on('click','.detail-piece',function(){
    $.get($(this).prop('href'),function(data){
        $('#modal-body').html($(data).find('#content'))
        $('#titreHeader').html($(data).find('#headerForModal'))

    });


})

//Affichage du formulaire dans détail
$('body').on('click','#btnAddLine', function(){
    $('#ligneForm').css('z-index','0')
    $('#btnAddLine').css('z-index','-1')
    $('#btnHideLine').css('z-index','0')
})

$('body').on('click','#btnHideLine', function(){
    $('#ligneForm').css('z-index','-1')
    $('#btnAddLine').css('z-index','0')
    $('#btnHideLine').css('z-index','-1')
})

// Modification brouillon: rechargement de la page lors de la fermeture de la boîte modal
$('body').on('click','.buttonClose',function(){
    $('#table').load(url+'/comptabilite/brouillons/ #table')
})

// confirmation validation_pointage
$('body').on('click', '#confirm', function(){

    if ($(this).prop('checked')===true){
        $('#valide').prop('disabled',false)
    }else{
        $('#valide').prop('disabled',true)
    }
})


// Detail facture
$('body').on('click', 'a',function(){
    $('#modal-body').html('')
    var xml = new XMLHttpRequest()
    xml.open('GET',$(this).prop('href'))
    xml.responseType = "document"
    xml.onload = function(){
        $('#modal-body').html(this.response.getElementById('main').innerHTML)
        $("#id_date_solde").datepicker({
            onSelect:function(dateText,object){
            dateText = dateText.split('-')[1]+'-'+dateText.split('-')[0];
            },
            dateFormat: "yy-mm-dd",
        });
    }
    xml.send()
})

$('body').on('submit','#factureForm',function(e){
    e.preventDefault();
    var form = document.getElementById('factureForm');
    var factureForm = new FormData(form)
    var xml = new XMLHttpRequest()
    xml.open('post',url+'/comptabilite/facture_detail/'+$('#factureForm').data('id_facture'))
    xml.onerror = function(){
        alert('Errors!')
    }
    xml.onreadystatechange = function(){
        if(this.status==200 && this.readyState==4){
            var xmlTable = new XMLHttpRequest()
            xmlTable.responseType = 'document'
            xmlTable.open('get',url+'/comptabilite/factures/')
            xmlTable.onload = function(){
                document.getElementById('table').innerHTML = xmlTable.response.getElementById('table').innerHTML ;
                delta()
                alert('Mise à jour faite');
                $('.modal').modal('hide')

                }
            xmlTable.send()


        }}
    xml.send(factureForm)
})

// traitement affichage tableau
function affiche(){
    var doc = document.getElementById('tbody').getElementsByTagName('tr')
    for(i=0;i<doc.length;i++){
        if(doc[i].children[4].textContent!=''){
           //doc[i].style.display='none'
           $(doc[i]).hide(200)
        }else{
            //doc[i].style.display='block'
            $(doc[i]).show(400)
        }
    }

}
function not_affiche(){
    var doc = document.getElementById('tbody').getElementsByTagName('tr')
    for(i=0;i<doc.length;i++){
        if(doc[i].children[4].textContent==''){
           //doc[i].hidden=true
           //doc[i].style.display='none'
           $(doc[i]).hide(200)

        }else{
            //doc[i].hidden=false
            //doc[i].style.display='block'
            $(doc[i]).show(400)
        }
    }

}
function allAffiche(){
    var doc = document.getElementById('tbody').getElementsByTagName('tr')
    for(i=0;i<doc.length;i++){
        doc[i].style.display='table-row'
    }
}

function delta(){
        var etat = $('#affichage_detail').data('etat')
        switch(etat){
        case 'not_solded':
            affiche();
            console.log('cas 1')
            break;

        case 'solded':
            not_affiche();
            break;

        case 'all':
            allAffiche();
            break;

        default:
            break
    }

}

$('body').on('click','#solded',function(){
    not_affiche();
    $('#affichage_detail').data('etat','solded');
})

$('body').on('click','#no_solded',function(){
    affiche();
    $('#affichage_detail').data('etat','not_solded')
})
$('body').on('click','#all',function(){
    allAffiche()
    $('#affichage_detail').data('etat','all')
})

$('#affichage_detail>button').on('click',function(){
    $('#affichage_detail>button').removeClass('btn-success').addClass('btn-primary')
    $(this).removeClass('btn-primary').addClass('btn-success')

})



majTab()