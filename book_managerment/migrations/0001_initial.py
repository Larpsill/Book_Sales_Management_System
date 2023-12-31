# Generated by Django 4.2.1 on 2023-06-01 06:09

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=32, unique=True, verbose_name='用户名')),
                ('password', models.CharField(max_length=64, verbose_name='密码')),
                ('name', models.CharField(max_length=32, verbose_name='真实姓名')),
                ('employee_id', models.CharField(max_length=20, unique=True, verbose_name='工号')),
                ('gender', models.SmallIntegerField(choices=[(1, '男'), (2, '女')], verbose_name='性别')),
                ('age', models.SmallIntegerField(verbose_name='年龄')),
                ('group', models.SmallIntegerField(choices=[(1, '超级管理员'), (2, '普通管理员')], verbose_name='用户组')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isbn', models.CharField(max_length=20, unique=True, verbose_name='ISBN')),
                ('book_name', models.CharField(max_length=64, verbose_name='书籍名称')),
                ('publish_house', models.CharField(max_length=64, verbose_name='出版社')),
                ('author', models.CharField(max_length=32, verbose_name='作者')),
                ('sellprice', models.DecimalField(decimal_places=2, default=0, max_digits=8, validators=[django.core.validators.MinValueValidator(0)], verbose_name='零售价格')),
                ('stock_quantity', models.PositiveIntegerField(default=0, verbose_name='当前库存数量')),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='进货时间')),
                ('purchase_price', models.DecimalField(decimal_places=2, default=0, max_digits=8, validators=[django.core.validators.MinValueValidator(0)], verbose_name='进货价格')),
                ('purchase_quantity', models.PositiveIntegerField(verbose_name='进货数量')),
                ('status', models.CharField(choices=[('unpaid', '未付款'), ('paid', '已付款'), ('returned', '已退货')], default='unpaid', max_length=10, verbose_name='状态')),
                ('arrived', models.SmallIntegerField(choices=[(0, '未到货'), (1, '已到货')], default=0, verbose_name='到货状态')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchasess', to='book_managerment.book')),
            ],
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('type', models.SmallIntegerField(choices=[(1, '收入'), (2, '支出')], verbose_name='类型')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=8, validators=[django.core.validators.MinValueValidator(0)], verbose_name='单价')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='数量')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='金额')),
                ('description', models.CharField(blank=True, max_length=128, null=True, verbose_name='备注')),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bills', to='book_managerment.book')),
                ('username', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, to_field='username', verbose_name='操作用户')),
            ],
        ),
    ]
