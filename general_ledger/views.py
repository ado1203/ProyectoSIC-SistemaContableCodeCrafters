from django.shortcuts import render, redirect
from .forms import AccountForm, TransactionForm, LedgerForm
from .models import Account, Category, Transaction, Ledger
from django.shortcuts import get_object_or_404


def get_account_order_by_category():
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

    return ordered_accounts


def account(request):
    ordered_accounts = get_account_order_by_category()

    return render(request, 'account.html', {
        'categorized_accounts': ordered_accounts
    })


def create_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            new_account = form.save(commit=False)
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
    error_message = None

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction_date = form.cleaned_data['transaction_date']
            transaction_type = form.cleaned_data['transaction_type']
            amount = request.POST.get('amount')

            try:
                ledger = Ledger.objects.get(start_date__lte=transaction_date,
                                            end_date__gte=transaction_date)
                if ledger.is_balance_sheet:
                    error_message = ('No se pueden agregar transacciones a un '
                                     'libro mayor con cierre contable.')
                else:
                    new_transaction = form.save(commit=False)

                    if transaction_type == 'debit':
                        new_transaction.transaction_debit_amount = amount
                    elif transaction_type == 'credit':
                        new_transaction.transaction_credit_amount = amount

                    new_transaction.ledger = ledger
                    new_transaction.save()

                    return redirect('transaction')
            except Ledger.DoesNotExist:
                error_message = (
                    'No se puede agregar la transacción porque no '
                    'existe un libro mayor para esa fecha.')
        else:
            error_message = ('Formulario no válido. Por favor, verifica los '
                             'campos.')

    else:
        form = TransactionForm()

    accounts = Account.objects.all()
    transactions = Transaction.objects.all().order_by('-transaction_date')

    context = {
        'form': form,
        'accounts': accounts,
        'transactions': transactions,
        'error_message': error_message,
    }

    return render(request, 'transaction.html', context)


def ledgers(request):
    if request.method == 'POST':
        form = LedgerForm(request.POST)
        if form.is_valid():
            new_ledger = form.save(commit=False)
            new_ledger.save()
            return redirect('ledgers')
    else:
        form = LedgerForm()

    return render(request, 'ledgers.html', {
        'form': form,
        'ledgers': Ledger.objects.all().order_by('-start_date'),
    })


def ledger(request, ledger_id):
    ledger = get_object_or_404(Ledger, pk=ledger_id)
    ordered_accounts = get_account_order_by_category()
    transactions = Transaction.objects.filter(ledger=ledger).order_by(
        'transaction_date')

    account_totals = {}
    for transaction in transactions:
        account_name = transaction.account.name
        if account_name not in account_totals:
            account_totals[account_name] = {
                'debit_total': transaction.transaction_debit_amount,
                'credit_total': transaction.transaction_credit_amount,
            }
        else:
            account_totals[account_name][
                'debit_total'] += transaction.transaction_debit_amount
            account_totals[account_name][
                'credit_total'] += transaction.transaction_credit_amount

    # mostrar el total de cada cuenta en terminal
    for account_name, totals in account_totals.items():
        print(f'{account_name} - {totals["debit_total"]}')

    return render(request, 'ledger.html', {
        'ledger': ledger,
        'categorized_accounts': ordered_accounts,
        'transactions': transactions,
        'account_totals': account_totals,
    })
