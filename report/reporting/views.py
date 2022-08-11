from xmlrpc.client import Transport
from django.shortcuts import render, redirect
from reporting.models import Transaction, Entry
from django.forms.widgets import CheckboxInput

def main(request):
    return render(request, 'reporting/index.html', {})

def transaction(request):
    if request.method == "POST":
        name = request.POST["name"]
        expense = True if request.POST.get("flag") else False

        if name:
            t1 = Transaction(name=name, expense=expense)
            t1.save()
        
        return redirect(to="/")
    
    return render(request, "reporting/transaction.html", {})

def expense(request):
    if request.method == "POST":
        amount = request.POST["amount"]
        transaction = request.POST["transaction"]      
        db_transaction = Transaction.objects.filter(name=transaction).first()

        if amount and transaction:
            e1 = Entry(amount=amount, transaction=db_transaction)
            e1.save()
        
        return redirect(to="/")
    
    return render(request, "reporting/expense.html", {"transactions": Transaction.objects.filter(expense=True)})

def income(request):
    if request.method == "POST":
        amount = request.POST["amount"]
        transaction = request.POST["transaction"]      
        db_transaction = Transaction.objects.filter(name=transaction).first()

        if amount and transaction:
            i1 = Entry(amount=amount, transaction=db_transaction)
            i1.save()
        return redirect(to="/")
    
    return render(request, "reporting/income.html", {"transactions": Transaction.objects.filter(expense=False)})


def period(request):
    if request.method == "POST":
        all = request.POST.get("flag")

        if all:
            return redirect(to="/result/all/all")
        
        else:
            start = request.POST["start"]
            end = request.POST["end"]      
            return redirect(to=f"/result/{start}/{end}")
    
    return render(request, "reporting/period.html", {})


def result(request, start, end):
    

    expenses = Entry.objects.filter(transaction__expense=True).order_by("transaction__name")
    income = Entry.objects.filter(transaction__expense=False).order_by("transaction__name")

    if start != "all" and end != "all":

        period_entries = Entry.objects.filter(created__range=(start, end))

        expenses = list(filter(lambda x: x in period_entries, expenses))
        income = list(filter(lambda x: x in period_entries, income))
  
    else:
        period_entries = Entry.objects.all()

    result = sum((-x.amount) if x.transaction.expense else x.amount for x in period_entries)
    
    return render(request, "reporting/result.html", {"result": result, "expenses": expenses, "income": income, "start": start, "end": end})

def delete_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    entry.delete()

    return redirect(to="/result/")