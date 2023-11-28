# Book_Sales_Management_System
复旦大学数据库引论 中期实验



本项目主要是在book_managerment的`models.py`、`forms.py`、`admin.py`文件中进行编写；

booktest中`settings.py`和`urls.py`主要简单进行了模板的部署和原始设置；

templates中存一些html文件，最后只用到了`base_site.html`文件，该文件调用了Django中的模板html文件。

运行项目时需要在终端运行：

```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

