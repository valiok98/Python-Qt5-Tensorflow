from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect
from .models import PersonalProfile
from .forms import Form

# Create your views here.
def profile(request):
    all_profiles = PersonalProfile.objects.all()
    return render(request, 'Profile/frontend.html', {'all_users' : all_profiles})

def items(request,user_id):

    try:
        curr_user = PersonalProfile.objects.get(pk=user_id)
    except PersonalProfile.DoesNotExist:
        raise Http404('This user does not exist')

    return render(request, 'Profile/display.html', {'user' : curr_user})

def signin(request):


    return render(request, 'Profile/signin.html')

def signup(request):

    form = Form(request.POST or None)
    context = {
        "form":form,
    }


    if form.is_valid():
        print(form.cleaned_data.get('f_name'))
        instance = form.save(commit=False)
        instance.save()

    return render(request, 'Profile/signup.html',context)

def edit(request):

    all_to_edit = PersonalProfile.objects.all()

    context = {
        'profiles' : all_to_edit,
    }

    return render(request, 'Profile/edit.html' ,context)

def edit_form(request,id):

    instance = get_object_or_404(PersonalProfile, id=id)

    form = Form(request.POST or None, instance=instance)


    if form.is_valid():

        instance = form.save(commit=False)
        instance.save()

    context = {

        "instance":instance,
        "form":form

    }

    return render(request, 'Profile/signup.html',context)

def delete(request,id):

    instance = get_object_or_404(PersonalProfile,id=id)
    instance.delete()
    return profile(request)

