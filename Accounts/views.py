from django.shortcuts import render

from Accounts.forms import CustomUserCreationForm


# Create your views here.
def addUser(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = CustomUserCreationForm()
    return render(request, 'tipo_registration.html', {'form': form})
