from django.shortcuts import render, redirect
from .forms import MoveForm
from .models import Move, Stock
import math

def round_half_up(n, decimals=0):
    n = float(n)  # Convertir a número decimal
    multiplier = 10 ** decimals
    return math.floor(n * multiplier + 0.5) / multiplier

def inventory(request):
    global move_unitPrice
    if request.method == 'POST':
        form = MoveForm(request.POST)
        if form.is_valid():
            new_move = form.save(commit=False)
            move_type = form.cleaned_data['move_type']
            move_quantity = form.cleaned_data['move_quantity']

            if move_type == 'input':
                move_unitPrice = form.cleaned_data['move_unitPrice']
            elif move_type == 'output':
                move_unitPrice = new_move.stock.stock_unitPrice

            new_move.move_price = move_quantity * move_unitPrice
            new_move.save()

            if move_type == 'input':
                new_move.stock.stock_quantity += move_quantity
                new_move.stock.save()
                new_move.stock_quantity = new_move.stock.stock_quantity
                new_move.save()
                new_move.stock_unitPrice = (new_move.stock.stock_price + new_move.move_price) / new_move.stock.stock_quantity
                new_move.stock_unitPrice = round_half_up(new_move.stock_unitPrice, 2)  # Redondea a 2 decimales
                new_move.save()
                new_move.stock.stock_unitPrice = new_move.stock_unitPrice
                new_move.stock.save()
                new_move.stock.stock_price = new_move.stock.stock_price + new_move.move_price
                new_move.stock.save()
                new_move.stock_price = new_move.stock.stock_price
                new_move.save()
            elif move_type == 'output':
                print(new_move.stock.stock_quantity)
                new_move.stock.stock_quantity -= move_quantity
                new_move.stock.save()
                new_move.stock_quantity = new_move.stock.stock_quantity
                new_move.save()
                print(new_move.stock.stock_quantity)
                if new_move.stock.stock_quantity > 0:
                    new_move.stock_unitPrice = (new_move.stock.stock_price - new_move.move_price) / new_move.stock.stock_quantity
                    new_move.stock_unitPrice = round_half_up(new_move.stock_unitPrice, 2)  # Redondea a 2 decimales
                    new_move.save()
                    new_move.stock.stock_unitPrice = new_move.stock_unitPrice
                    new_move.stock.save()
                else:
                    new_move.stock.stock_unitPrice = 0
                    new_move.stock.save()
                new_move.stock.stock_price = new_move.stock.stock_price - new_move.move_price
                new_move.stock.save()
                new_move.stock_price = new_move.stock.stock_price
                new_move.save()

            new_move.stock.save()
            #new_move.stock.stock_price = new_move.stock.stock_unitPrice * new_move.stock.stock_quantity
            #new_move.stock.stock_price = round(new_move.stock.stock_price, 2)  # Redondea a 2 decimales
            #new_move.stock.save()
            #new_move.stock_price = new_move.stock.stock_price
            new_move.save()

            return redirect('inventory')
    else:
        form = MoveForm()

    moves = Move.objects.all()
    stocks = Stock.objects.all()
    return render(request, 'inventory.html', {
        'moves': moves,
        'form': form,
        'stocks': stocks
    })
