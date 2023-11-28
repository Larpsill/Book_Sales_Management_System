from django import forms
from .models import *
import hashlib
from django.contrib import admin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class BookForm(forms.ModelForm):
    #isbn = forms.CharField()
    class Meta:
        model = Book
        fields = '__all__'
        # widgets = { 
        #         'stock_quantity': forms.HiddenInput(attrs={'value': 0}),
        #         'sellprice': forms.HiddenInput(attrs={'value': 0}),
        #     }
 #一开始就只读，反正book里的元素要付款后才能添加进去，所以也无所谓了
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['sellprice'].disabled = True
    #     self.fields['stock_quantity'].disabled = True
        # self.initial['stock_quantity'] = 0
        # self.initial['sellprice'] = 0

class PurchaseForm(forms.ModelForm): #让book和status是添加后只读
    class Meta:
        model = Purchase
        fields = '__all__'

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = '__all__'

# # 创建新的认证表单
# class CustomAuthenticationForm(AuthenticationForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['username'].label = '用户名'

#     def clean(self):
#         username = self.cleaned_data.get('username')
#         password = self.cleaned_data.get('password')

#         if username is not None and password:
#             try:
#                 user = CustomUser.objects.get(username=username)
#             except CustomUser.DoesNotExist:
#                 pass
#             else:
#                 if user.check_password(password):
#                     self.user_cache = user
            
# 创建新的用户表单
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('name', 'employee_id', 'gender', 'age', 'group',)

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        #fields = [field for field in UserChangeForm.Meta.fields if field not in ['first_name', 'last_name', 'email']] + ['name', 'employee_id', 'gender', 'age', 'group']
        fields = ['username','password','name', 'employee_id', 'gender', 'age', 'group']
        #print(fields)
        #fields = list(UserChangeForm.Meta.fields) - ['first_name','last_name','email']+ ['name', 'employee_id', 'gender', 'age', 'group',]
# class AdminCreationForm(forms.ModelForm):
#     password1 = forms.CharField(label='密码', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='确认密码', widget=forms.PasswordInput)

#     confirm_password = forms.CharField(
#         label='确认密码',
#         widget=forms.PasswordInput(render_value=True)  # 加入这个属性使得密码不会被清空
#     )
#     class Meta:
#         model = Adminn
#         fields = ['username', 'password', 'confirm_password',
#                   'employee_id', 'name', 'age', 'gender', 'group']
#         # widgets = {
#         #     'password': forms.PasswordInput(render_value=True)  # 这种类型设置使得生成的标签对于输入不可见
#         # }

#     def clean(self):
#         cleaned_data = super().clean()
#         pwd1 = cleaned_data.get("password")
#         pwd2 = cleaned_data.get("confirm_password")

#         # 判断两次输入的密码是否一致
#         if pwd1 and pwd2 and pwd1 != pwd2:
#             raise forms.ValidationError("两次输入的密码不一致，请重新输入")

#         # 对输入的密码进行MD5加密处理
#         md5_obj = hashlib.md5()
#         md5_obj.update(bytes(pwd1, encoding='utf-8'))
#         cleaned_data['password'] = md5_obj.hexdigest()

#         return cleaned_data
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user
    
# class AdminChangeForm(forms.ModelForm):
#     password = ReadOnlyPasswordHashField()

#     class Meta:
#         model = Adminn
#         fields = ('username', 'employee_id', 'name', 'gender', 'age', 'group', 'password')

#     def clean_password(self):
#         return self.initial["password"]
    
# class AdminLoginForm(forms.Form):
#     username = forms.CharField(label='用户名', max_length=30)
#     password = forms.CharField(label='密码', widget=forms.PasswordInput)
    
    '''def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance and instance.pk:
            #self.fields['book'].widget.attrs['readonly'] = True
            #self.fields['status'].widget.attrs['readonly'] = True
        #    self.fields['book'].disabled = True
        #    self.fields['status'].disabled = True 
            #self.fields['purchase_price'].widget.attrs['readonly'] = True
            # 编辑进货记录
        #    self.fields['stock_quantity'].widget.attrs['readonly'] = True
        #    self.fields['stock_quantity'].disabled = True
        #else:
            # 添加进货记录
        #    self.fields['stock_quantity'].initial = 0

    """   def clean(self):
            cleaned_data = super().clean()
            book = cleaned_data.get('book')
            stock_quantity = book.stock_quantity if book else 0

            if stock_quantity != 0:
                raise forms.ValidationError("书籍库存必须为0。")

            return cleaned_data """
'''