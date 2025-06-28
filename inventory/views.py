from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from .models import Category, Item, Computer, Entity, Brand, ModelName, Supplier, Personnel, Position
from django.db.models import Count, Sum, IntegerField
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.functions import Cast
import json
from .forms import ItemForm, ComputerForm

def home(request):
    return render(request, 'home.html', {'show_navbar': False})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    # Get total counts
    total_items = Item.objects.count()  # type: ignore
    total_computers = Computer.objects.count()  # type: ignore
    
    # Get items by category
    items_by_category = list(Item.objects.values('category__name').annotate(count=Count('id')))  # type: ignore
    
    # Get computer status distribution
    computer_status = list(Computer.objects.values('status').annotate(count=Count('id')))  # type: ignore
    
    # Get items needing attention (under maintenance or disposed)
    items_needing_attention = Item.objects.filter(  # type: ignore
        status__in=['maintenance', 'disposed']
    ).select_related('category').order_by('status')[:5]
    
    # Get computers needing maintenance
    computers_needing_maintenance = Computer.objects.filter(status='maintenance')[:5]  # type: ignore
    
    # Prepare data for charts
    chart_data = {
        'items_by_category': json.dumps(items_by_category, cls=DjangoJSONEncoder),
        'computer_status': json.dumps(computer_status, cls=DjangoJSONEncoder),
    }
    
    context = {
        'total_items': total_items,
        'total_computers': total_computers,
        'chart_data': chart_data,
        'items_needing_attention': items_needing_attention,
        'computers_needing_maintenance': computers_needing_maintenance,
    }
    
    return render(request, 'inventory/dashboard.html', context)

@login_required
def item_list(request):
    items = Item.objects.all().select_related('entity', 'category', 'brand', 'model', 'supplier', 'received_by', 'received_by_position', 'receive_from', 'receive_from_position', 'fund_cluster')  # type: ignore
    edit_id = request.GET.get('edit')
    form = None
    if request.method == 'POST':
        if edit_id:
            item = get_object_or_404(Item, pk=edit_id)
            form = ItemForm(request.POST, instance=item)
        else:
            form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item saved successfully!')
            return redirect('item_list')
    else:
        if edit_id:
            item = get_object_or_404(Item, pk=edit_id)
            form = ItemForm(instance=item)
        else:
            form = ItemForm()
    return render(request, 'inventory/item_list.html', {'items': items, 'form': form, 'action': 'Edit' if edit_id else 'Add', 'edit_id': edit_id})

@login_required
def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'inventory/item_detail.html', {
        'item': item
    })

@login_required
def computer_list(request):
    # Get computers grouped by room
    rooms = ['EB204', 'EB205', 'EB206', 'EB207', 'EB208', 'EB209', 'EB210']
    computers_by_room = {}
    
    for room in rooms:
        computers_by_room[room] = Computer.objects.filter(room=room).annotate(
            unit_no_int=Cast('unit_no', IntegerField())
        ).order_by('unit_no_int')  # type: ignore
    
    return render(request, 'inventory/computer_list.html', {
        'computers_by_room': computers_by_room,
        'rooms': rooms
    })

@login_required
def computer_detail(request, pk):
    computer = get_object_or_404(Computer, pk=pk)
    return render(request, 'inventory/computer_detail.html', {
        'computer': computer
    })

def is_superuser(user):
    return user.is_superuser

@login_required
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item added successfully!')
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'inventory/item_form.html', {'form': form, 'action': 'Add'})

@login_required
def edit_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item updated successfully!')
            return redirect('item_list')
    else:
        form = ItemForm(instance=item)
    return render(request, 'inventory/item_form.html', {'form': form, 'action': 'Edit', 'item': item})

@login_required
def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item deleted successfully!')
        return redirect('item_list')
    return render(request, 'inventory/item_confirm_delete.html', {'item': item})

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
@login_required
def add_computer(request):
    if request.method == 'POST':
        form = ComputerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Computer added successfully!')
            return redirect('computer_list')
    else:
        form = ComputerForm()
    
    return render(request, 'inventory/computer_form.html', {
        'form': form
    })

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
@login_required
def edit_computer(request, pk):
    computer = get_object_or_404(Computer, pk=pk)
    if request.method == 'POST':
        form = ComputerForm(request.POST, instance=computer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Computer updated successfully!')
            return redirect('computer_list')
    else:
        form = ComputerForm(instance=computer)
    return render(request, 'inventory/computer_form.html', {'form': form, 'edit': True, 'computer': computer}) 