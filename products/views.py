from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Produk, Status
from .forms import ProdukForm

def product_list(request):
    status_filter = request.GET.get('status', 'bisa dijual')
    
    if status_filter == 'tidak bisa dijual':
        tidak_bisa_dijual_status = Status.objects.filter(nama_status='tidak bisa dijual').first()
        products = Produk.objects.filter(status=tidak_bisa_dijual_status) if tidak_bisa_dijual_status else []
    else:
        bisa_dijual_status = Status.objects.filter(nama_status='bisa dijual').first()
        products = Produk.objects.filter(status=bisa_dijual_status) if bisa_dijual_status else []
    
    return render(request, 'products/list.html', {
        'products': products, 
        'current_status': status_filter
    })

def product_add(request):
    if request.method == 'POST':
        form = ProdukForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produk berhasil ditambahkan')
            return redirect('product_list')
    else:
        form = ProdukForm()
    return render(request, 'products/form.html', {'form': form, 'title': 'Tambah Produk'})

def product_edit(request, pk):
    product = get_object_or_404(Produk, pk=pk)
    if request.method == 'POST':
        form = ProdukForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produk berhasil diupdate')
            return redirect('product_list')
    else:
        form = ProdukForm(instance=product)
    return render(request, 'products/form.html', {'form': form, 'title': 'Edit Produk'})

def product_delete(request, pk):
    product = get_object_or_404(Produk, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Produk berhasil dihapus')
        return redirect('product_list')
    return render(request, 'products/confirm_delete.html', {'product': product})