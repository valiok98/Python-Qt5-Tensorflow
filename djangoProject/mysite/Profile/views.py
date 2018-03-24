from django.shortcuts import render
from django.http import Http404
from .models import PersonalProfile


# Create your views here.
def profile(request):
    all_profiles = PersonalProfile.objects.all()
    return render(request, 'frontend.html', {'all_users' : all_profiles})

def items(request,user_id):

    try:
        curr_user = PersonalProfile.objects.get(pk=user_id)
    except PersonalProfile.DoesNotExist:
        raise Http404('This user does not exist')

    return render(request, 'display.html', {'user' : curr_user})
