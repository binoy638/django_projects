from django.shortcuts import render
from accounts.models import User_Account, TutorialCategory

# Create your views here.
#

def home(request):

    context ={}
    cat = TutorialCategory.objects.all()
    context['cat'] = cat
    if request.GET:
        query = request.GET['q']
        context['query'] = str(query)




    return render(request, 'home.html', context)
