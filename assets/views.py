from django.shortcuts import render, get_object_or_404
from .models import Product, Category, SubCategory, Outlet, OutletStock

def home(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    subcategory_id = request.GET.get('subcategory', '')
    
    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)
    if category_id:
        products = products.filter(category_id=category_id)
    if subcategory_id:
        products = products.filter(subcategory_id=subcategory_id)

    products = products.order_by('-id')

    low_stock_count = products.filter(quantity__gt=0, quantity__lte=5).count()
    over_stock_count = products.filter(quantity__gt=200).count()
    out_of_stock_count = products.filter(quantity=0).count()

    outlets = Outlet.objects.all()

    context = {
        'products': products,
        'categories': Category.objects.all(),
        'subcategories': SubCategory.objects.all(),
        'outlets': outlets,
        'query': query,
        'category_id': category_id,
        'subcategory_id': subcategory_id,
        
        'low_stock_count': low_stock_count,
        'over_stock_count': over_stock_count,
        'out_of_stock_count': out_of_stock_count,
    }
    
    return render(request, 'home.html', context)

def outlet_inventory(request, outlet_id):
    outlet = get_object_or_404(Outlet, id=outlet_id)
    stocks = OutletStock.objects.filter(outlet=outlet)
    
    context = {
        'outlet': outlet,
        'stocks': stocks,
    }
    
    return render(request, 'outlet_inventory.html', context)