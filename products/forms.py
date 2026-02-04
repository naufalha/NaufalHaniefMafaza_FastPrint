from django import forms
from .models import Produk, Kategori, Status

class ProdukForm(forms.ModelForm):
    class Meta:
        model = Produk
        fields = ['nama_produk', 'harga', 'kategori', 'status']
        widgets = {
            'nama_produk': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'harga': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'required': True}),
            'kategori': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean_nama_produk(self):
        nama = self.cleaned_data.get('nama_produk')
        if not nama or nama.strip() == '':
            raise forms.ValidationError('Nama produk harus diisi')
        return nama.strip()
    
    def clean_harga(self):
        harga = self.cleaned_data.get('harga')
        if harga is None or harga < 0:
            raise forms.ValidationError('Harga harus berupa angka positif')
        return harga