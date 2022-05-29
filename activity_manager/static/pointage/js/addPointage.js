// Données pointées pour une activité
function getPointageActivite(dateText){
    var datePointage = dateText.split('-')
    datePointage = datePointage[2]+'-'+datePointage[1]+'-'+datePointage[0]

    $.ajax({
        url:url+'/pointage/add_pointage/'+ $('#id_activite').val(),
        type:'POST',
        dataType:'json',
        data:{"csrfmiddlewaretoken":$('input[name="csrfmiddlewaretoken"]').val(), "datepointage":dateText},
        success:function(code, status){
            var releve = $('input[name="releve"]');

            if(code['transfered'] == true){
                $("input[name='releve']").prop("hidden","hidden")
                $("input[name='fake']").prop("hidden","")
                $('#valid').removeClass("d-block").addClass("d-none")
                $('#alert_pointage').removeClass("d-none").addClass("d-block")
                $("#sous").prop('disabled','disabled')
                $('#lop').addClass("d-none").removeClass("d-flex")


            }else
            {
                $("input[name='releve']").prop("hidden","")
                $("input[name='fake']").prop("hidden","hidden")
                $('#valid').removeClass("d-none").addClass("d-block")
                $('#alert_pointage').removeClass("d-block").addClass("d-none")
                $("#sous").prop('disabled','')
                $('#lop').addClass('d-flex').removeClass("d-none")


            }
            // Boucle pour checker les élèves pointés
            for(var i=0; i<releve.length; i++){
                if(code['donnee'].includes($(releve[i]).val().toString())){
                    $(releve[i]).prop('checked','checked');}
                else{
                      $(releve[i]).prop('checked',false);}
                }
            },
        error:function(resultat,status, errors){
            console.log(errors);
            }
        })
    }

// Date picker pour date de pointage
    $('#id_datepointage').datepicker({
    onSelect:function(dateText,object){
       getPointageActivite(dateText)},
       dateFormat: "yy-mm-dd"
})

