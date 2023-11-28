from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
import hashlib
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, name, employee_id, gender, age, group, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(
            username=username,
            name=name,
            employee_id=employee_id,
            gender=gender,
            age=age,
            group=group,
            #is_superuser = True,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, username, password=None, **extra_fields):
        # extra_fields.setdefault('is_staff', True)
        # extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(verbose_name='用户名', max_length=32, unique=True)
    password = models.CharField(verbose_name='密码', max_length=128)
    name = models.CharField(verbose_name="真实姓名", max_length=32)
    employee_id = models.CharField(verbose_name='工号', max_length=20, unique=True)
    gender_choices = ((1, "男"), (2, "女"),)
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)
    age = models.SmallIntegerField(verbose_name="年龄")
    group_choices = ((1, "超级管理员"), (2, "普通管理员"),)
    group = models.SmallIntegerField(verbose_name='用户组', choices=group_choices, default=2)
    
    is_staff = models.BooleanField(default=True)#是否是后台管理员
    is_active = models.BooleanField(default=True)#是否启用
    is_superuser = models.BooleanField(default=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'employee_id', 'gender', 'age', 'group']
    class Meta:
        app_label = 'book_managerment'
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.username
    
# Create your models here.
class Book(models.Model):
    isbn = models.CharField(verbose_name="ISBN", max_length=20, unique=True)
    book_name = models.CharField(verbose_name="书籍名称", max_length=64)
    publish_house = models.CharField(verbose_name="出版社", max_length=64)
    author = models.CharField(verbose_name="作者", max_length=32)
    sellprice = models.DecimalField(verbose_name="零售价格", max_digits=8, decimal_places=2, 
                                    default=0, validators=[MinValueValidator(0)])
                                    #最后validators设置该字段不能小于0
    stock_quantity = models.PositiveIntegerField(verbose_name="当前库存数量", default=0)

    def sell_book(self, quantity=0): #图书销售
        if self.stock_quantity < quantity:
            raise ValueError('库存不足，请返回修改出售数量')
        self.stock_quantity -= quantity
        self.save()


# class Adminn(models.Model):
#     username = models.CharField(verbose_name='用户名', max_length=32, unique=True)
#     password = models.CharField(verbose_name='密码', max_length=64)
#     name = models.CharField(verbose_name="真实姓名", max_length=32)
#     employee_id = models.CharField(verbose_name='工号', max_length=20, unique=True)
#     gender_choices = ( (1, "男"), (2, "女"),)
#     gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)
#     age = models.SmallIntegerField(verbose_name="年龄")
#     group_choices = ( (1, "超级管理员"), (2, "普通管理员"),)
#     group = models.SmallIntegerField(verbose_name='用户组', choices=group_choices)
    # def save(self, *args, **kwargs):
    #     md5_obj = hashlib.md5()
    #     md5_obj.update(bytes(self.password, encoding='utf-8'))
    #     self.password = md5_obj.hexdigest()
    #     super(Admin, self).save(*args, **kwargs)

class Purchase(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='purchasess')
    purchase_time = models.DateTimeField(verbose_name='进货时间', default=timezone.now)
    purchase_price = models.DecimalField(verbose_name="进货价格", max_digits=8, decimal_places=2, 
                                         default=0, validators=[MinValueValidator(0)])
    purchase_quantity = models.PositiveIntegerField(verbose_name="进货数量")
    STATUS_CHOICES = ( ('unpaid', '未付款'), ('paid', '已付款'), ('returned', '已退货'), )
    status = models.CharField(verbose_name="状态", max_length=10, choices=STATUS_CHOICES, default='unpaid')
    arrived_ornot = ( (0, '未到货'), (1, '已到货'),)
    arrived = models.SmallIntegerField(verbose_name="到货状态", choices=arrived_ornot, default=0)

    def __str__(self):
        return f"{self.book} - {self.purchase_time}"

    def mark_as_paid(self): #进货付款
        if self.status != 'unpaid':
            raise ValueError("只有未付款状态的进货记录可以标记为已付款。")
        self.status = 'paid'
        self.save()
    
    def return_book(self): #图书退货
        if self.status != 'unpaid':
            raise ValueError("只有未付款状态的进货记录可以标记为已退货。")
        self.status = 'returned'
        self.save()

    def mark_as_arrived(self): #已付款的到货
        if self.status != 'paid':
            raise ValueError("只有已付款状态的进货记录可以标记为已到货。")
        if self.arrived == 1:
            raise ValueError("只有未到货状态的进货记录可以标记为已到货。")
        self.arrived = 1
        self.book.stock_quantity += self.purchase_quantity #到货，加库存数量
        self.book.save()
        self.save()


class Bill(models.Model):
    bill_time = models.DateTimeField(verbose_name='创建时间', default=timezone.now)
    username = models.ForeignKey(verbose_name='操作用户', to='CustomUser', to_field='username', 
                                 null=True, blank=True, on_delete=models.SET_NULL)
                #ForeignKey默认使用目标模型的主键，那么会是自动生成的id，这里指定对应到用户名
    type_choices = ( (1, '收入'), (2, '支出') )
    type = models.SmallIntegerField(verbose_name='类型', choices=type_choices)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, related_name='bills')
    price = models.DecimalField(verbose_name="单价", max_digits=8, decimal_places=2, 
                                default=0, validators=[MinValueValidator(0)])
    quantity = models.PositiveIntegerField(verbose_name="数量", default=0)
    amount = models.DecimalField(verbose_name='金额', max_digits=8, decimal_places=2, default=0)
    description = models.CharField(verbose_name='备注', max_length=128, null=True, blank=True)