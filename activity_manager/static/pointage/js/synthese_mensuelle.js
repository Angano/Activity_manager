// Synthese_mensuelle
var date = new Date()
$('#TextBox1').val(("0"+(date.getMonth()+1)).slice(-2)+'-'+date.getFullYear())
var url = window.location.origin
$( "#TextBox1" ).MonthPicker({
    // https://github.com/KidSysco/jquery-ui-month-picker/wiki/Events
     MonthFormat: 'mm-yy' ,
      IsRTL: true,
    i18n: {
        year:'Année',
        months:['Jan.','Fév.','Mar.','Avr.','Mai','Juin','Juil.','Août','Sep.','Oct.','Nov.','Déc.']
        },
     OnAfterChooseMonth: function() {
            $('#TextBox1').val($(this).val())

            var datePointage = $(this).val().split('-')
            datePointage = datePointage[1]+'-'+datePointage[0]

            var activite_pk = window.location.href.split('/')[window.location.href.split('/').length - 1];

            $.ajax({
                url:url+'/pointage/synthese_mensuelle/'+activite_pk,
                type:'POST',
                dataType:'html',
                data:{
                    'csrfmiddlewaretoken':$('input[name="csrfmiddlewaretoken"]').val(),
                    'pk':activite_pk,
                    'datepointage':datePointage
                    },
                success:function(code,status){
                    var resultat = $('#table_resultat',$(code));
                    var nom_activite = $('#activite_nom',$(code));
                    $('#synthese_resultat').html(resultat);
                    $('#activite_nom').text(nom_activite.text())
                },
                complete:function(code, status){
                    //console.log($($('#activite_nom'),$(code.responseText)).text())
                    }
                });


        } ,

})


