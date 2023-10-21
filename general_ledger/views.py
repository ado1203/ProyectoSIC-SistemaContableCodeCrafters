from django.shortcuts import render, redirect
from .forms import AccountForm
from .models import Account


def account(request):
    accounts = Account.objects.all()
    return render(request, 'account.html', {
        'accounts': accounts
    })


def create_account(request):
    if request.method == 'GET':
        return render(request, 'create_account.html', {
            'form': AccountForm
        })
    else:
        try:
            form = AccountForm(request.POST)
            new_account = form.save(commit=False)
            new_account.balance = 0
            new_account.catalog_id = 1
            new_account.save()
            return redirect('account')
        except ValueError:
            return render(request, 'create_account.html', {
                'form': AccountForm,
                'error': 'Porfavor ingrese los datos correctamente'
            })
