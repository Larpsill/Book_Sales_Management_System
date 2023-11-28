
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import AdminLoginForm

# def admin_login(request):
#     if request.method == 'POST':
#         form = AdminLoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('book_managerment')
#             else:
#                 form.add_error(None, '用户名或密码错误')
#     else:
#         form = AdminLoginForm()
#     return render(request, 'admin_login.html', {'form': form})