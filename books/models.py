from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2']

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
# Sản phẩm/Sách
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='books/', blank=True, null=True)

    def __str__(self):
        return self.title
    
    @property
    def discounted_price(self):
        """Calculate the price after discount"""
        if self.discount > 0:
            return self.price * (1 - self.discount / 100)  # Sử dụng cách tính chính xác hơn
        return self.price
    
    @property
    def average_rating(self):
        reviews = self.reviews.all()
        return reviews.aggregate(models.Avg('rating'))['rating__avg'] or 0
    
    @property
    def review_count(self):
        return self.reviews.count()
    
    @property
    def rating_1(self):
        return self.reviews.filter(rating=1).count() / self.review_count * 100 if self.review_count else 0
    
    @property
    def rating_2(self):
        return self.reviews.filter(rating=2).count() / self.review_count * 100 if self.review_count else 0
    
    @property
    def rating_3(self):
        return self.reviews.filter(rating=3).count() / self.review_count * 100 if self.review_count else 0
    
    @property
    def rating_4(self):
        return self.reviews.filter(rating=4).count() / self.review_count * 100 if self.review_count else 0
    
    @property
    def rating_5(self):
        return self.reviews.filter(rating=5).count() / self.review_count * 100 if self.review_count else 0

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.book.title}"

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.book.price * self.quantity

# Đơn hàng
class Order(models.Model):
    PAYMENT_CHOICES = [
        ('BCASH', 'Thanh toán bằng tiền mặt'),
        ('CREDIT', 'Thanh toán chuyển khoản'),
    ]
    SHIPPING_CHOICES = [
        ('standard', 'Giao hàng Tiêu Chuẩn'),
        ('express', 'Giao hàng Nhanh'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    shipping_method = models.CharField(max_length=10, choices=SHIPPING_CHOICES, default='standard')
    is_paid = models.BooleanField(default=False)
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

# Chi tiết đơn hàng
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.book.price * self.quantity