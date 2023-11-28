from django.contrib import admin
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect,HttpResponse
from django.template.loader import render_to_string
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.db.models import Q
from django.contrib.admin.filters import DateFieldListFilter
from django_filters import DateFilter
from datetime import datetime
#from django.contrib.admin import DateRangeFilter
from rangefilter.filter import DateTimeRangeFilter
# Register your models here.
from .models import *
from .forms import BookForm,PurchaseForm,BillForm,CustomUserCreationForm, CustomUserChangeForm

#from django.contrib.admin import helpers
#from django.urls import path
#from django.shortcuts import render, redirect


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    book = BookForm
    list_display = ('id','isbn', 'book_name', 'publish_house', 'author', 'sellprice', 'stock_quantity')
    list_per_page = 5 #每页显示5条数据
    fields = ('isbn', 'book_name', 'publish_house', 'author', 'sellprice', 'stock_quantity')
    search_fields = ['id', 'isbn', 'book_name', 'publish_house', 'author', 'sellprice', 'stock_quantity']
    list_filter = ('id','isbn', 'book_name', 'publish_house', 'author', 'sellprice', 'stock_quantity')
    readonly_fields = ('stock_quantity',) #库存从头到尾不可编辑
    actions = ['sell_books',]

    #设置isbn在添加后不可修改
    def get_readonly_fields(self, request, obj=None):
        if obj: # obj is not None, so this is an edit view
            return self.readonly_fields + ('isbn',)
        return self.readonly_fields #adding readonly_fields to your fields
    
    def sell_books(self, request, queryset):
        if len(queryset) != 1:
            raise ValueError("书籍销售时每次只能操作一笔账单。")
        book = queryset.first()
        #     book.sell_book()
        # 创建账单并填入信息
        bill = Bill.objects.create(
            username=request.user,#
            type=1, # 收入类型
            book=book,
            price=book.sellprice,
            #quantity=purchase.purchase_quantity,
            #amount=purchase.purchase_price * purchase.purchase_quantity,
            description='出售收款'
        )
        # 更新消息提示
        self.message_user(request, '成功收款并创建了一条账单：{}'.format(bill.id))
        url = reverse('admin:book_managerment_bill_change', args=[bill.id])
        return HttpResponseRedirect(url)
    sell_books.short_description = '图书销售'
    #def author(self, obj):
    #    return [author.name for author in obj.authors.all()]

    #def publish_name(self, obj):
     #   return obj.publish.name

    #filter_horizontal = ('authors',)


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    form = PurchaseForm
    #双下划线语法在 list_display 中是不支持的！！所以要写一个get_book_id的函数
    list_display = ('get_book_id', 'purchase_time', 'purchase_price', 'purchase_quantity', 'status', 'arrived')
    list_per_page = 5 #每页显示5条数据
    list_filter = ('status', 'arrived')
    search_fields = ('book__isbn', 'book__book_name', 'book__author', 'status', 'arrived')
    readonly_fields = ('status','arrived') #从头到尾都不可编辑
    actions = ['return_selected_books', 'mark_paid', 'mark_arrived']
    
    def get_book_id(self, obj):
        return obj.book.id
    get_book_id.short_description = '书籍编号' #通过 short_description 属性设置列的显示名称为 '书籍编号'

    def return_selected_books(self, request, queryset):
        for purchase in queryset:
            purchase.return_book()
        self.message_user(request, '成功退货')
    return_selected_books.short_description = '图书退货'

    def mark_paid(self, request, queryset):
        if len(queryset) != 1:
            raise ValueError("进货付款时每次只能操作一笔账单。")
        for purchase in queryset:
            purchase.mark_as_paid()
        # 创建账单并填入信息
        bill = Bill.objects.create(
            username=request.user,#
            type=2, # 支出类型
            book=purchase.book,
            price=purchase.purchase_price,
            quantity=purchase.purchase_quantity,
            amount=purchase.purchase_price * purchase.purchase_quantity,
            description='进货付款'
        )
        # 更新消息提示
        self.message_user(request, '成功付款并创建了一条账单：{}'.format(bill.id))
        url = reverse('admin:book_managerment_bill_change', args=[bill.id])
        return HttpResponseRedirect(url)
    mark_paid.short_description = '图书付款'

    def mark_arrived(self, request, queryset):
        if len(queryset) != 1:
            raise ValueError("确认到货时每次只能确认一个。")
        for purchase in queryset:
            purchase.mark_as_arrived()
        self.message_user(request, '成功更改为已到货！请添加上书籍的零售价格：')
        #重定向到Book的修改界面
        book = queryset.first().book
        url = reverse('admin:book_managerment_book_change', args=[book.id])
        return HttpResponseRedirect(url)
    mark_arrived.short_description = '图书到货确认'


# class DateRangeForm(forms.Form):
#     start_time = forms.DateField(
#         label='起始时间',
#         widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
#         input_formats=['%Y-%m-%d']
#     )
#     end_time = forms.DateField(
#         label='终止时间',
#         widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
#         input_formats=['%Y-%m-%d']
#     )
#     # start_time = forms.DateField(label='起始时间', widget=forms.DateInput(attrs={'type': 'date','name': 'start_time'}))
#     # end_time = forms.DateField(label='终止时间', widget=forms.DateInput(attrs={'type': 'date','name': 'end_time'}))
# class DateRangeFilter(admin.SimpleListFilter):
#     title = '时间范围'
#     parameter_name = 'date_range'

#     def lookups(self, request, model_admin):
#         return (
#             ('custom', '自定义时间范围'),
#         )
#     def queryset(self, request, queryset):
#         print('queryset method called')
#         # if self.value() == 'custom':
#         #     start_time = request.GET.get('start_time')
#         #     end_time = request.GET.get('end_time')
#         #     print('start_time:', start_time)
#         #     print('end_time:', end_time)
#         #     if start_time and end_time:
#         #         start_time = timezone.datetime.strptime(start_time, '%Y-%m-%d')
#         #         end_time = timezone.datetime.strptime(end_time, '%Y-%m-%d') + timezone.timedelta(days=1)
#         #         return queryset.filter(bill_time__range=(start_time, end_time))
#         #     else:
#         #         return queryset
#         # else:
#         #     return queryset
#         start_time = request.GET.get('start_time')
#         end_time = request.GET.get('end_time')

#         if start_time and end_time:
#             try:
#                 start_datetime = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
#                 end_datetime = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
#                 return queryset.filter(bill_time__range=(start_datetime, end_datetime))
#             except ValueError:
#                 return queryset
#         return queryset
    
#     def choices(self, changelist):
#         print('anie')
#         # # 渲染自定义表单的HTML代码
#         # form_html = render_to_string('admin/date_range_filter.html', {
#         #     'form': DateRangeForm(initial={
#         #         'start_time': changelist.get_filters_params().get('bill_time__gte', ''),
#         #         'end_time': changelist.get_filters_params().get('bill_time__lt', ''),
#         #     }),
#         # })
#         # 返回包含自定义表单的生成器对象
#         # yield {
#         #     'selected': self.value() == 'custom',
#         #     'query_string': changelist.get_query_string({self.parameter_name: 'custom'}),
#         #     'display': '自定义时间范围',
#         #     'form': True,
#         #     'form_html': form_html,
#         # }
#         yield {
#             'selected': self.value() is None,
#             'query_string': changelist.get_query_string(remove=[self.parameter_name,]),
#             'display': '自定义时间范围',
#         }
# class CustomTimeRangeFilter(DateRangeFilter):
#     title = 'Custom Time Range'
#     parameter_name = 'custom_time_range'
#     template = 'admin/custom_time_range_filter.html'

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    form = BillForm
    list_display = ('bill_time', 'username', 'type', 'get_book_id', 'amount', 'description')
    search_fields = ['bill_time', 'username__username', 'type', 'book__isbn', 'amount', 'description']
    list_filter = ('type','bill_time',('bill_time',DateTimeRangeFilter))
    # list_filter = ('type',CustomTimeRangeFilter,)
    list_per_page = 5 #每页显示5条数据
    readonly_fields = ('username','type','price','amount','book','bill_time') #从头到尾不可编辑

    def get_book_id(self, obj):
        if obj.book:
            return obj.book.id
        else:
            return None
    get_book_id.short_description = '书籍编号'
    #草，居然是这里出错了

    #设置进货账单数量不可修改
    def get_readonly_fields(self, request, obj=None):
        if obj.type == 2 or obj.quantity != 0: # 进货 或者出售时订单已经确认过数量了
            return self.readonly_fields + ('quantity',)
        return self.readonly_fields #adding readonly_fields to your fields
    
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        # 获取当前账单信息
        bill = self.get_object(request, object_id)
        # 如果请求为 POST，则表示用户正在提交修改表单
        if request.method == 'POST' and bill.type == 1:
            # 获取书籍购买数量
            quantity = int(request.POST.get('quantity', 0))
            # 更新书籍库存
            book = bill.book
            #加一个try...except...
            if book:
                try:
                    book.sell_book(quantity)
                except ValueError as e:
                    # 库存不足，返回错误提示
                    return HttpResponse(str(e), status=400)
                bill.amount = bill.price * quantity #更新计算amount值
                bill.save()
            else:
                # 如果 book 为空，则返回错误提示
                msg = '该账单没有对应的书籍信息'
                return HttpResponse(msg, status=400)
        # 将当前账单信息传递给模板渲染
        context = {
            'title': '修改账单',
            'bill': bill,
        }
        return super().changeform_view(request, object_id=object_id, form_url=form_url, extra_context=context)
                    # 重定向回 Book 类
                # url = reverse('admin:book_managerment_book_change', args=[book.id])
                # return HttpResponseRedirect(url)
#admin.site.add_filter(DateRangeFilter)
# class CustomAdminSite(AdminSite):
#     site_header = 'My Book Management System Administration'
#     site_title = 'My Book Management System'
#     index_title = 'Dashboard'

#     def has_permission(self, request):
#         # 判断当前用户是否为超级管理员或普通管理员
#         return request.user.is_active #and (request.user.is_superuser or request.user.group == 2)
#     # def has_view_permission(self, request):
#     #     return True
#     # def has_change_permission(self, request, obj=None):
#     #     return True
#     # def get_model_perms(self, request):
#     #     return super().get_model_perms(request)
#     def get_app_list(self, request):
#         app_list = super().get_app_list(request)
#         if request.user.is_authenticated and request.user.group == 2:
#             app_list = [app for app in app_list if app['app_label'] != 'book_managerment' or app['name'] != 'CustomUser']
#         return app_list
#     def get_model_perms(self, request):
#         perms = super().get_model_perms(request)
#         if request.user.group == 2:
#             perms['book_managerment.book'] = perms.get('book_managerment.book', {})
#             perms['book_managerment.bill'] = perms.get('book_managerment.bill', {})
#             perms['book_managerment.purchase'] = perms.get('book_managerment.purchase', {})
#            # perms['book_managerment.customuser'] = perms.get('book_managerment.customuser', {})
#         return perms
    # def get_model_perms(self, request):
    #     perms = super().get_model_perms(request)
    #     if not request.user.is_superuser and request.user.group == 2:
    #         perms['book_managerment.book'] = perms.get('book_managerment.book', {})
    #         perms['book_managerment.bill'] = perms.get('book_managerment.bill', {})
    #         perms['book_managerment.purchase'] = perms.get('book_managerment.purchase', {})
    #     return perms
    # def index(self, request, extra_context=None):
    #     # 如果当前用户是普通管理员，则只显示部分内容
    #     if request.user.group == 2:
    #         extra_context = extra_context or {}
    #         extra_context['title'] = 'Sorry, you do not have permission to access this page'
    #         extra_context['subtitle'] = 'Please contact the superuser for assistance'
    #         return self.render_template('admin/custom_index.html', extra_context)

    #     # 如果是超级管理员，则显示完整的内容
    #     return super().index(request, extra_context=extra_context)
    
    # def render_template(self, template_name, context, request=None):
    #     # 实现自定义的模板渲染逻辑，这里只是一个示例
    #     from django.template import engines
    #     django_engine = engines['django']
    #     template = django_engine.get_template(template_name)
    #     return template.render(context, request=request)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'name', 'group')
    list_filter = ('group',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('name', 'employee_id', 'gender', 'age', 'group')}),
        ('Permissions', {'fields': ('is_active','is_staff','groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'name', 'employee_id', 
                       'gender', 'age', 'group', 'is_active','is_staff')}
        ),
    )
    search_fields = ('username', 'name', 'employee_id')
    ordering = ('username',)
    readonly_fields = ('group',)
    #找你找的好苦啊！
    # def has_module_permission(self, request):
    #     if request.user.is_authenticated and request.user.group == 2:
    #         return True
    #     return super().has_module_permission(request)
    def has_view_permission(self, request, obj=None):
        if obj is not None:
            if obj == request.user:
                # 允许普通管理员用户查看自己的信息
                return True
            elif request.user.group==2:
                # 普通管理员用户不能查看其他用户的信息
                return False
        return super().has_view_permission(request, obj)
    def has_change_permission(self, request, obj=None):
        if obj is not None:
            if obj == request.user:
                # 允许普通管理员用户修改自己的信息
                return True
            elif request.user.group==2:
                # 普通管理员用户不能修改其他用户的信息
                return False
            return super().has_change_permission(request, obj)
    def has_add_permission(self, request):#普通管理员不能添加用户
        if request.user.group==2:
            return False
        return super().has_add_permission(request)
    def has_delete_permission(self, request, obj=None):
        if request.user.group==2:# 普通管理员不能删除用户
            return False
        return super().has_delete_permission(request, obj)
admin.site.register(CustomUser, CustomUserAdmin)  # 注册自定义的CustomUser模型和CustomUserAdmin类
# admin.site.register(Book, BookAdmin)
# admin.site.register(Bill, BillAdmin)
# admin.site.register(Purchase, PurchaseAdmin)

#custom_site = CustomAdminSite(name='custom_admin')  # 创建自定义的AdminSite实例
# custom_site.register(CustomUser, CustomUserAdmin)  # 注册自定义的CustomUser模型和CustomUserAdmin类
# custom_site.register(Book, BookAdmin)
# custom_site.register(Bill, BillAdmin)
# custom_site.register(Purchase, PurchaseAdmin)

# admin.site = custom_site  # 替换默认的AdminSite为我们自定义的CustomAdminSite
#CustomUserAdmin.get_model_perms = get_model_perms

        # # 如果当前用户是普通管理员，返回空的权限字典，即完全无法访问 CustomUser 表
        # if not request.user.is_superuser and request.user.group == 2:
        #     return {}
        # return super().get_model_perms(request)
    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     if not request.user.is_superuser:
    #         qs = qs.filter(~Q(group=1))  # 排除用户组为超级管理员的用户
    #     return qs
    
# @admin.register(Adminn)
# class AdminnAdmin(admin.ModelAdmin):
#     list_display = ('username', 'name', 'employee_id', 'gender', 'age', 'group')
#     list_per_page = 5
#     fields = ('username', 'password', 'name', 'employee_id', 'gender', 'age', 'group')
#     search_fields = ['id', 'username', 'name', 'employee_id']
#     list_filter = ('gender', 'age', 'group')
#     # actions = ['reset_password']

#     def get_form(self, request, obj=None, **kwargs):
#         if request.user.is_superuser:
#             return super().get_form(request, obj, **kwargs)
#         else:
#             kwargs['form'] = AdminChangeForm
#             kwargs['exclude'] = ('password',)
#             return super().get_form(request, obj, **kwargs)

#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         if request.user.is_superuser:
#             return qs
#         else:
#             return qs.filter(id=request.user.id)

#     def save_model(self, request, obj, form, change):
#         if not request.user.is_superuser:
#             obj.id = request.user.id
#         super().save_model(request, obj, form, change)

#admin.site.register(Adminn, AdminnAdmin)
    # def reset_password(self, request, queryset):
    #     for admin in queryset:
    #         admin.password = make_password('123456')
    #         admin.save()
    #     self.message_user(request, '密码重置成功！')
    # reset_password.short_description = '重置密码'