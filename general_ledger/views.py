from django.shortcuts import render, redirect
from .forms import AccountForm, TransactionForm
from .models import Account, Category, Transaction


def account(request):
    # Recupera todas las cuentas de la base de datos
    accounts = Account.objects.all().order_by('category__name', 'code')

    # Organiza las cuentas en un diccionario categorizado
    categorized_accounts = {}
    for account in accounts:
        category_name = account.category.name
        if category_name not in categorized_accounts:
            categorized_accounts[category_name] = {
                'category': account.category,
                'accounts': [],
            }
        categorized_accounts[category_name]['accounts'].append(account)

    # Define el orden específico de las categorías
    category_order = ["Activo", "Pasivo", "Patrimonio", "Gastos y Costos", "Ingresos"]

    # Calcula el rowspan y agrega la información a categorized_accounts
    for category_name, data in categorized_accounts.items():
        category = data['category']
        accounts = data['accounts']
        rowspan = len(accounts) + 1
        category.rowspan = rowspan

    # Organiza las categorías en el orden deseado
    ordered_categories = [categorized_accounts.get(category_name) for category_name in category_order]

    return render(request, 'account.html', {
        'categorized_accounts': ordered_categories
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


def transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            new_transaction = form.save(commit=False)
            transaction_type = form.cleaned_data['transaction_type']
            amount = request.POST.get('amount')

            if transaction_type == 'debit':
                new_transaction.transaction_debit_amount = amount
            elif transaction_type == 'credit':
                new_transaction.transaction_credit_amount = amount

            new_transaction.ledger_id = 1
            new_transaction.save()
            return redirect('transaction')
    else:
        form = TransactionForm()

    accounts = Account.objects.all()
    transactions = Transaction.objects.all().order_by('-transaction_date')
    return render(request, 'transaction.html', {
        'form': form,
        'accounts': accounts,
        'transactions': transactions,
    })
