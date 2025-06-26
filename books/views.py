from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Book, CartItem, Order, OrderItem, Category
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Sum




def register(request):
    form = CreateUserForm
    if request.method =="POST":
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context={'form':form}
    return render(request, 'app/register.html',context)
def login_view(request):
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Tên đăng nhập hoặc mật khẩu không đúng!')
    return render(request, 'app/login.html')
def logoutPage(request):
    logout(request)
    return redirect('login')
def home(request):
    # Đếm số lượng sản phẩm trong giỏ hàng
    cart_item_count = 0
    if request.user.is_authenticated:
        cart_item_count = CartItem.objects.filter(user=request.user).count()

    # Lấy tất cả sách (nếu cần cho section tổng hợp)
    books = Book.objects.all().order_by('id')  # Thay 'orderitem' bằng 'id' hoặc trường hợp lệ

    # Danh sách 10 danh mục cố định
    categories = [
        'Sách Kinh Tế',
        'Sách Văn Học',
        'Sách Thiếu Nhi',
        'Sách Tâm Lý',
        'Sách Lịch Sử',
        'Sách Văn Hóa',
        'Sách Tôn Giáo',
        'Sách Y Học',
        'Sách Giáo Dục',
        'Sách Nghệ Thuật',
    ]

    # Tạo dictionary chứa sách cho từng danh mục
    books_by_category = {}
    for category_name in categories:
        books_by_category[category_name] = Book.objects.filter(category__name=category_name).order_by('id')  # Thêm order_by nếu cần

    # Truyền tất cả context vào template
    context = {
        'cart_item_count': cart_item_count,
        'books': books,
        'books_by_category': books_by_category,
    }
    return render(request, 'app/main.html', context)

#chi tiết sản phẩm
@login_required
def product_detail(request, pk):
    product = get_object_or_404(Book, pk=pk)
    cart_item_count = CartItem.objects.filter(user=request.user).count()

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        review_content = request.POST.get('review_content')
        rating = request.POST.get('rating', 0)

        if name and email and review_content and 0 < int(rating) <= 5:
            Review.objects.create(
                book=product,
                user=request.user,
                name=name,
                email=email,
                content=review_content,
                rating=rating
            )
            messages.success(request, 'Đánh giá của bạn đã được gửi thành công!')
            return redirect('product_detail', pk=pk)

    context = {
        'product': product,
        'cart_item_count': cart_item_count,

    }
    return render(request, 'app/product_detail.html', context)




@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = 0
    item_totals = {}  # Sử dụng dictionary

    for item in cart_items:
        price = item.book.discounted_price
        item_total = float(price) * item.quantity
        item_totals[item.id] = item_total  # Lưu với key là item.id
        total_price += item_total

    context = {
        'cart_items': cart_items,
        'cart_item_count': cart_items.count(),
        'total_price': total_price,
        'item_totals': item_totals,  # Truyền dictionary
    }
    return render(request, 'app/cart.html', context)

@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    action = request.POST.get('action')

    if action == 'increase':
        cart_item.quantity += 1
        cart_item.save()
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    messages.success(request, 'Cập nhật giỏ hàng thành công!')
    return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    messages.success(request, 'Đã xóa sản phẩm khỏi giỏ hàng!')
    return redirect('cart')

@login_required
def place_order(request):
    if request.method == 'POST':
        cart_items = CartItem.objects.filter(user=request.user)
        if not cart_items:
            messages.error(request, 'Giỏ hàng trống, không thể đặt hàng!')
            return redirect('cart')

        # Tạo đơn hàng
        payment_method = request.POST.get('payment', 'BCASH')
        order = Order.objects.create(
            user=request.user,
        )

### Hoàn thiện view `place_order` trong `views.py`

@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    action = request.POST.get('action')

    if action == 'increase':
        cart_item.quantity += 1
        cart_item.save()
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'message': 'Cập nhật giỏ hàng thành công!',
            'cart_count': CartItem.objects.filter(user=request.user).count()
        })

    messages.success(request, 'Cập nhật giỏ hàng thành công!')
    return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'message': 'Đã xóa sản phẩm khỏi giỏ hàng!',
            'cart_count': CartItem.objects.filter(user=request.user).count()
        })

    messages.success(request, 'Đã xóa sản phẩm khỏi giỏ hàng!')
    return redirect('cart')

@login_required
def place_order(request):
    if request.method == 'POST':
        print(f"Place order request: {request.POST}")  # Debug
        cart_items = CartItem.objects.filter(user=request.user)
        if not cart_items:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': 'Giỏ hàng trống!'}, status=400)
            messages.error(request, 'Giỏ hàng trống!')
            return redirect('cart')

        # Lấy dữ liệu từ form
        full_name = request.POST.get('full_name')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        city = request.POST.get('city')
        district = request.POST.get('district')
        shipping = request.POST.get('shipping', 'standard')  # Mặc định là 'standard'
        payment_method = request.POST.get('payment')
        invoice_required = 'invoice' in request.POST

        # Kiểm tra dữ liệu bắt buộc
        if not all([full_name, phone_number, address, city, district, payment_method]):
            print("Missing required fields")  # Debug
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': 'Vui lòng điền đầy đủ thông tin!'}, status=400)
            messages.error(request, 'Vui lòng điền đầy đủ thông tin!')
            return redirect('cart')

        # Tạo đơn hàng
        order = Order.objects.create(
            user=request.user,
            payment_method=payment_method,
            is_paid=False,
            full_name=full_name,
            phone_number=phone_number,
            address=address,
            city=city,
            district=district,
            shipping_method=shipping
        )

        # Thêm các mặt hàng từ giỏ hàng vào đơn hàng qua OrderItem
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity
            )
            item.delete()  # Xóa giỏ hàng sau khi thêm vào đơn hàng

        print(f"Order created: {order.id}")  # Debug
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'message': 'Đặt hàng thành công!',
                'cart_count': 0
            })

        messages.success(request, 'Đặt hàng thành công!')
        return redirect('home')

    return redirect('cart')

def about(request):
    context={}
    return render(request,'app/gioithieu.html')
def contact(request):
    context={}
    return render(request,'app/contact.html')

def sachthieunhi(request):
    books = Book.objects.filter(category__name='Sách Thiếu Nhi')
    context = {'books': books}
    return render(request, 'app/sachthieunhi.html', context)

def sachvanhocvn(request):
    books = Book.objects.filter(category__name='Sách Văn Học Việt Nam')
    context = {'books': books}
    return render(request, 'app/sachvanhocvn.html', context)

def sachkinhte(request):
    books = Book.objects.filter(category__name='Sách Kinh Tế - Kỹ Năng')
    context = {'books': books}
    return render(request, 'app/sachkinhte.html', context)

def sachnghethuat(request):
    books = Book.objects.filter(category__name='Sách Nghệ Thuật Sống - Tâm Lý')
    context = {'books': books}
    return render(request, 'app/sachnghethuatsong.html', context)

def sachtamlinh(request):
    books = Book.objects.filter(category__name='Sách Tâm Linh Tôn Giáo')
    context = {'books': books}
    return render(request, 'app/sachtamlinh.html', context)

def sachvanhocncngoai(request):
    books = Book.objects.filter(category__name='Sách Văn Học Nước Ngoài')
    context = {'books': books}
    return render(request, 'app/sachvanhocncngoai.html', context)

def sachyhoc(request):
    books = Book.objects.filter(category__name='Sách Y học - Thực Dưỡng')
    context = {'books': books}
    return render(request, 'app/sachyhoc.html', context)

def sachvanhoa(request):
    books = Book.objects.filter(category__name='Sách Văn Hóa - Nghệ Thuật')
    context = {'books': books}
    return render(request, 'app/sachvanhoa.html', context)

def sachgiaoduc(request):
    books = Book.objects.filter(category__name='Sách Giáo Dục - Gia Đình')
    context = {'books': books}
    return render(request, 'app/sachgiaoduc.html', context)

def sachlichsu(request):
    books = Book.objects.filter(category__name='Sách Lịch Sử')
    context = {'books': books}
    return render(request, 'app/sachlichsu.html', context)
def support(request):
    context={}
    return render(request,'app/support.html')
def tusach(request):
    context={}
    return render(request,'app/tusach.html')


def sachtonghop(request):
    # Lấy tất cả sách
    books = Book.objects.all().order_by('id')  # Sắp xếp theo id để đảm bảo thứ tự
    # Khởi tạo Paginator, 20 sách mỗi trang (5 hàng x 4 sản phẩm)
    paginator = Paginator(books, 20)
    # Lấy số trang từ query parameter (ví dụ: ?page=2)
    page_number = request.GET.get('page')
    # Lấy sách cho trang hiện tại
    page_obj = paginator.get_page(page_number)
    
    context = {
        'books': page_obj,  # Truyền page_obj thay vì danh sách books
        'paginator': paginator,  # Truyền paginator để sử dụng trong template
        'page_obj': page_obj,   # Truyền page_obj để truy cập các thuộc tính như has_next, has_previous
    }
    return render(request, 'app/tonghopsach.html', context)

@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    quantity = int(request.POST.get('quantity', 1))  # Lấy số lượng từ form, mặc định là 1

    # Tạo hoặc cập nhật CartItem
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        book=book,
        defaults={'quantity': quantity}
    )
    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    messages.success(request, f'Đã thêm "{book.title}" vào giỏ hàng!')
    return redirect('home')  # Hoặc chuyển hướng đến trang giỏ hàng: 'cart'

def search(request):
    query = request.GET.get('q', '')
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        ).order_by('id')
    else:
        books = Book.objects.all().order_by('id')
    print(f"Query: {query}, Books found: {books.count()}")  # Debug
    
    paginator = Paginator(books, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'books': page_obj,
        'paginator': paginator,
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'app/search.html', context)


