from django.db import models
from django.core.exceptions import ValidationError

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        verbose_name_plural = "Categories" 
        
    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = "Sub Categories" 
        
    def __str__(self):
        return f"{self.name} ({self.category.name})"

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0) 
    added_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Products"

    @property
    def stock_status(self):
        if self.quantity == 0:
            return "Stock Out"
        elif 0 < self.quantity <= 5:
            return "Low Stock"
        elif self.quantity > 200:
            return "Over Stock"
        else:
            return "Available"
        
    def __str__(self):
        return f"{self.name} (Warehouse: {self.quantity})"

class Outlet(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=255)
    
    class Meta:
        verbose_name_plural = "Outlets"
        
    def __str__(self):
        return self.name

class OutletStock(models.Model):
    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('outlet', 'product')
        verbose_name_plural = "Outlet Stocks"

    def __str__(self):
        return f"{self.product.name} at {self.outlet.name} (Qty: {self.quantity})"

class Transfer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    from_outlet = models.ForeignKey(Outlet, on_delete=models.SET_NULL, null=True, blank=True, related_name='transfers_out')
    to_outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE, related_name='transfers_in')
    quantity_transferred = models.PositiveIntegerField(default=1)
    challan_number = models.CharField(max_length=50, unique=True)
    transferred_by = models.CharField(max_length=100)
    received_by = models.CharField(max_length=100)
    courier_name = models.CharField(max_length=100, blank=True, null=True)
    transfer_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Transfers" 

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.from_outlet is None:
                if self.product.quantity >= self.quantity_transferred:
                    self.product.quantity -= self.quantity_transferred
                    self.product.save()
                else:
                    raise ValueError("Insufficient Warehouse Stock")
            else:
                source_stock, created = OutletStock.objects.get_or_create(
                    outlet=self.from_outlet, 
                    product=self.product
                )
                if source_stock.quantity >= self.quantity_transferred:
                    source_stock.quantity -= self.quantity_transferred
                    source_stock.save()
                else:
                    raise ValueError("Insufficient Outlet Stock")

            destination_stock, created = OutletStock.objects.get_or_create(
                outlet=self.to_outlet, 
                product=self.product
            )
            destination_stock.quantity += self.quantity_transferred
            destination_stock.save()

        super().save(*args, **kwargs)

class TransferHistory(Transfer):
    class Meta:
        proxy = True 
        verbose_name_plural = "Transfer History"