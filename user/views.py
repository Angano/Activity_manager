from django.shortcuts import render, redirect


# Create your views here.
from .forms import UserForm, ProfilForm
from django.contrib.auth.models import User
from .models import Profil, Role
from django.views.generic import CreateView, UpdateView
from .forms import RoleForm

def listuser(request):
    users = User.objects.all()
    return render(request,'user/list_user.html', {'users':users, 'titre':'Liste des utilisateurs'})


def user(request):

    if request.method == 'POST':
        roles = dict()
        userform = UserForm(request.POST)
        profilForm = ProfilForm(request.POST)
        if userform.is_valid() and profilForm.is_valid():
            try:
                roles = Role.objects.filter(pk__in=request.POST.getlist('role'))
            except:
                roles=dict()

            userform.save()
            user = User.objects.last()
            Profil.objects.create(user=user)
            profil = Profil.objects.get(user=user)
            profilform = ProfilForm(instance=profil,data=request.POST)
            data = profilform.save(commit=False)
            for role in roles:
                data.role.add(role)
            data.save()

            return redirect('/user/listuser/')
        else:
            print('error')
            render(request, 'user/user.html',{ 'form':userform})
    else:
        userform = UserForm
        roles = Role.objects.all()
        profilForm = ProfilForm()


    return render(request, 'user/user.html',{ 'form':userform, 'roles':roles, 'titre':'Ajout d\'un utilisateur', 'profilForm':profilForm})


def role(request, pk):
    roles = Role.objects.all()
    user = User.objects.get(pk=pk)
    userForm = UserForm(instance=user)
    try:
        userRole = [data.pk for data in user.profil.role.all()]
    except:
        userRole = dict()

    try:
        profil = Profil.objects.get(user=pk)
        profilform = ProfilForm(instance=profil)
    except Profil.DoesNotExist:
        Profil.objects.create(user=user)
        profil = Profil.objects.get(user=pk)
        profilform = ProfilForm()
        print('none')

    if request.method == 'POST':
        print(request.POST)
        profilform = ProfilForm(request.POST, instance=profil)
        userForm = UserForm(request.POST,instance=user)
        if profilform.is_valid() and userForm.is_valid():
            profilform.save()
            userForm.save()
            return redirect('/user/listuser/')
        else:
            print(profilform.errors ,'toto')

    return render(request,'user/profil_form.html',{'userrole':userRole, 'userForm':userForm, 'profilform':profilform,'roles':roles,'titre':'Edition utilisateur','profil':profil})


def profil(request):
    userform = UserForm(instance=request.user)
    if request.method == 'POST':
        userform = UserForm(request.POST, instance=request.user)
        if userform.is_valid():
            userform.save()
    return  render(request,'user/profil.html',{'userform':userform, 'titre':'Mon Profil' })


class RoleView(CreateView):
    form_class = RoleForm
    template_name = 'user/role_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titre'] = ' Ajout d\'un role'
        context['submit'] = 'Ajouter'
        context['edition'] = False
        return context

class RoleUpdateView(UpdateView):
    form_class = RoleForm
    template_name = 'user/role_form.html'
    queryset = Role.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titre']='Edition d\'un rôle'
        context['submit'] ='Metre à jour'
        context['edition'] = True
        return context
