var url = window.location.origin

// champ saisie parent
$('#saisie').on('input',function(e){
       if (e.target.value.length > 2){
            $.ajax({
            url:url+'/famille/add_enfant_ajax/',
            type:'post',
            data:'eleve='+e.target.value+'&csrfmiddlewaretoken='+$('input[name=csrfmiddlewaretoken]').val(),
            dataType:'html',
            success:function(resultat, status){
                $('#resultat').html(resultat)

                },
            error:function(resultat, status, err){
                console.log(resultat, status, err);
            }
            })
       }else{
            $('#resultat').html('')
       }

})
// Ajout élève, saisie parent
function get_parent(id_saisie,id_parent,id_resultat){
    $('body').on('input',id_saisie,function(e){
        if(e.target.value.length>1){
            $.ajax({
                url:url+'/famille/parent/',
                dataType:'text',
                type:'post',
                data:'&csrfmiddlewaretoken='+$('input[name=csrfmiddlewaretoken]').val()+'&parent='+e.target.value,
                success:function(response, status){

                    $(id_resultat).html(response)
                },
                error:function(code, error, status){
                    console.log(code, error, status);
                }, })
        }else{
            $(id_resultat).html('');
        }
    })
     $('body').on('click',id_resultat,function(e){

        $(id_parent).prop('value',(e.target.id).split('_')[1])
        $(id_saisie).prop('value',e.target.textContent)
        $(id_resultat).html('')
     })
}

get_parent('#saisieParent1','#parent1','#resultat1')
get_parent('#saisieParent2','#parent2','#resultat2')


// modification d'un parent
$('#parent').on('click','a',function(){
    $('#modal-parent').load($(this).prop('href') +' #parentForm')
})
$('#exampleModal').on('submit','#parentForm',function(e){
    e.preventDefault()
    var form = document.getElementById('parentForm')
    var parentForm = new FormData(form)
    var xml = new XMLHttpRequest()
    xml.open('POST',url+'/famille/edit_parent/'+ $(form).data('parent'))
    xml.onreadystatechange=function(){
        if(xml.readyState == 4){
            alert('Modification réussie')
            $('#exampleModal').modal('hide')
            $('#parent').load(url+'/famille/parents/ #parent')

        }
    }
    xml.send(parentForm)
})

// modification d'un enfant
$('#eleveTable').on('click','a',function(){
    $('#modalEleve').load($(this).prop('href') + ' #eleve')
})

$('#modalEleve').on('submit','#eleveForm',function(e){
    e.preventDefault()
    var form = document.getElementById('eleveForm')
    var formEleve = new FormData(form)
    var xml = new XMLHttpRequest()
    xml.open('POST',url+'/famille/update_eleve/'+ $(form).data('eleve'))
    xml.onreadystatechange=function(){
        if(xml.readyState==4){
            $('#eleveTable').load(url+'/famille/enfants/ #eleveTable');
            $('#exampleModal').modal('hide')
            alert('Modification réussie');

        }

    }
    xml.send(formEleve)
})

// effacement champs de recherche
$('body').on('click','.reset',function(){
    $(this).prev().prop('value','').focus()
})