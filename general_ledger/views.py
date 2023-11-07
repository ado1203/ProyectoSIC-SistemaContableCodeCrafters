from django.db.models import F
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
            return redirect('create_account')
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
                ledger = Ledger.objects.get(start_date__lte=transaction_date, end_date__gte=transaction_date)
                if ledger.is_balance_sheet:
                    error_message = ('No se pueden agregar transacciones a un libro mayor con cierre contable.')
                else:
                    new_transaction = form.save(commit=False)

                    if transaction_type == 'debit':
                        new_transaction.transaction_debit_amount = amount
                    elif transaction_type == 'credit':
                        new_transaction.transaction_credit_amount = amount

                    # Asigna el libro mayor actual a la transacción
                    new_transaction.ledger = ledger
                    new_transaction.save()

                    # Redirige a la pagina actual
                    return redirect('transaction')
            except Ledger.DoesNotExist:
                error_message = ('No se puede agregar la transacción porque no existe un libro mayor para esa fecha.')
        else:
            error_message = ('Formulario no válido. Por favor, verifica los campos.')
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

    # Resetear los balances de las cuentas para este libro mayor
    Account.objects.update(balance=0, balance_type='debit')

    # Obtén los totales de débito y crédito para cada cuenta específicos para este libro mayor
    account_totals = get_account_totals(ledger)

    # Actualizar el balance de cada cuenta para este libro mayor
    for account_name, totals in account_totals.items():
        account = Account.objects.get(name=account_name)
        account.balance = totals['debit_total'] - totals['credit_total']
        if account.balance < 0:
            account.balance_type = 'credit'
            account.balance = -account.balance
        else:
            account.balance_type = 'debit'
        account.save()

    totals_balance_sheet = get_totals_balance_sheet()

    return render(request, 'ledger.html', {
        'ledger': ledger,
        'categorized_accounts': ordered_accounts,
        'transactions': transactions,
        'account_totals': account_totals,
        'totals_balance_sheet': totals_balance_sheet,
    })


def close_ledger(request, ledger_id):
    ledger = get_object_or_404(Ledger, pk=ledger_id)

    if request.method == 'POST':
        # Asegúrate de que is_balance_sheet esté marcado como True
        ledger.is_balance_sheet = True
        ledger.save()

        return redirect('ledger', ledger_id=ledger_id)


def get_account_totals(ledger):
    accounts = Account.objects.all()
    account_totals = {}

    for account in accounts:
        debit_total = 0
        credit_total = 0
        # Calcula los totales de débito y crédito específicos para el libro mayor actual
        transactions = Transaction.objects.filter(account=account, ledger=ledger)
        for transaction in transactions:
            debit_total += max(transaction.transaction_debit_amount, 0)  # Asegura que las cantidades sean positivas
            credit_total += max(transaction.transaction_credit_amount, 0)  # Asegura que las cantidades sean positivas

        if debit_total != credit_total:
            # Maneja el desequilibrio aquí (por ejemplo, registra un error o realiza alguna acción específica)
            pass

        # Guarda los totales en el diccionario de totales de cuentas
        account_totals[account.name] = {
            'debit_total': debit_total,
            'credit_total': credit_total,
        }

    return account_totals



def get_totals_balance_sheet():
    totals_balance_sheet = {
        'debit_total': 0,
        'credit_total': 0,
    }

    accounts = Account.objects.all()

    for account in accounts:
        if account.balance_type == 'debit':
            totals_balance_sheet['debit_total'] += account.balance
        elif account.balance_type == 'credit':
            totals_balance_sheet['credit_total'] += account.balance

    return totals_balance_sheet