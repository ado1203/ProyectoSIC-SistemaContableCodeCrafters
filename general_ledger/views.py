from django.shortcuts import render, redirect
from .forms import AccountForm
from .models import Account, Category


def account(request):
    accounts = Account.objects.all().order_by('category__name', 'code')

    categorized_accounts = {}
    for account in accounts:
        category_name = account.category.name
        if category_name not in categorized_accounts:
            categorized_accounts[category_name] = []
        categorized_accounts[category_name].append(account)

    # Define el orden específico de las categorías
    category_order = ["Activo", "Pasivo", "Patrimonio", "Gastos y Costos",
                      "Ingresos"]

    ordered_accounts = {
        category_name: categorized_accounts.get(category_name, []) for
        category_name in category_order}

    return render(request, 'account.html', {
        'categorized_accounts': ordered_accounts
    })


def create_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            new_account = form.save(commit=False)
            new_account.balance = 0
            new_account.catalog_id = 1
            new_account.save()
            return redirect('account')
    else:
        form = AccountForm()

    categories = Category.objects.all()
    return render(request, 'create_account.html', {
        'form': form,
        'categories': categories,
    })
