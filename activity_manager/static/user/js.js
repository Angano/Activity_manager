$('body').on('click','a',function(){
    $('#modal-dialog').load($(this).prop('href')+ ' #modal-body')

})


var url = window.location.origin

// Modification d'un rôle
    $('#role').on('submit',$('#myRoleForm'),function(e){
    e.preventDefault();
    var myForm = document.getElementById("myRoleForm")
    var form = new FormData(myForm)
    var xml = new XMLHttpRequest()
    xml.open('POST',url+'/user/edit_role/'+$(myForm).data('role'))
    xml.onload=function(){
        alert("Modification réussie")
        $("#table").load(url+'/user/roles/'+ ' #table')
        $('#exampleModal').modal('hide');


        }
    xml.send(form)

})

// Modification d'un Utilisateur

    $('#profil').on('submit',$('#myProfilForm'),function(e){
    e.preventDefault();
    var myForm = document.getElementById("myProfilForm")
    var form = new FormData(myForm)
    var xml = new XMLHttpRequest()
    xml.open('POST',url+'/user/edit/'+$(myForm).data('profil'))
    xml.onload=function(){
        alert("Modification réussie")
        $("#table").load(url+'/user/listuser/'+ ' #table')
        $('#exampleModal').modal('hide');

        }
    xml.send(form)

})