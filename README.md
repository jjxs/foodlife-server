

# 
1. file、フォルダ小文字　
2. 変数,メソッド　xxx_xxx で名付け
3. 

# model
  model/フォルダ下

# serializer
  serializer/フォルダ下

# sql 
  sql/フォルダ下



1,
OrderDetail 
menufree => price 注文時の金額を記入

2, 为了管理，查询方便
OrderMenuFree 追加，
=> 

isUsable    是否可以开始 
usable_time 可利用時間
start_time  开始时间
end_time  结束时间(開始時間确定后计算结果直接写入，方便读取)
stop_time （中途结帐，或者别的原因结束时）

※为了写便捷，order 和 orderdetail都进行关联
order = models.ForeignKey(Order, related_name='order_detail', db_constraint=False, on_delete=models.DO_NOTHING)
order_detail = models.ForeignKey(OrderDetail, related_name='order_detail_status', db_constraint=False, on_delete=models.DO_NOTHING)

※OrderMenuFree登录的数据，不再做成OrderDetailStatus明细

※ 方针
OrderDetail 主要用于结算（所以放题和宴会本身的注文也插入该表，方便结算），厨房状态管理
OrderMenuFree 主要为了方便 关于放题注文SQL查询，和对注文进行细致话管理，
以后宴会也应该用自己对应的 OrderMenuCourse来进行管理，而不是和OrderDetail混为一潭

所有会引起理解混乱的业务，都应该考虑新建表来维持清晰的逻辑结构，


■ git　
    Site:
    https://gitee.com/amistrong
    
    教程：
    https://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000

    深入学习必要性 ★★

■ python(3.6)
  
    Site:
    https://www.python.org/

    教程：
    https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000

    深入学习必要性 ★★★

■ Django(2.1)
  
    Site:
    https://www.djangoproject.com/

    教程：
    https://docs.djangoproject.com/en/2.1/
    https://code.ziqiangxuetang.com/django/django-tutorial.html

    深入学习必要性 ★★★

■ Django django-rest-framework
 
    Site:
    https://www.django-rest-framework.org/

    教程：
    https://www.django-rest-framework.org/tutorial/quickstart/
    (英语以外未找到好的学习资料)

    深入学习必要性 ★★★★★
    

■ Django websocket package

    Site:
    https://channels.readthedocs.io/en/latest/introduction.html

    教程：
    https://channels.readthedocs.io/en/latest/tutorial/index.html

    深入学习必要性 ★★

■ Angular(6.1)
 
    Site:
    https://angular.io/

    教程：
    https://angular.cn/docs

    深入学习必要性 ★★★★★

■ Angular Material （ui for pc, pad）

    Site:
    https://material.angular.io/

    教程：
    https://material.angular.io/components/categories

    深入学习必要性 ★★★

■ angular/flex-layout （layout 調整）

    Site:
    https://github.com/angular/flex-layout

    教程：
    https://github.com/angular/flex-layout/wiki/API-Documentation
    https://tburleson-layouts-demos.firebaseapp.com/#/docs

    深入学习必要性 ★★

■ Onsen UI （ui for phone）

    Site:
    https://ja.onsen.io/angular2/

    教程：
    https://ja.onsen.io/v2/guide/angular2/

    深入学习必要性 ★★★
    

■　その他

    キャッシュウサーバ：redis
    DBサーバ：postgresql
    検証：Django rest_framework_jwt
    検索：Django django_filters
    IDE: VS Code
    公開：AWS

    深入学习必要性 ★
　
