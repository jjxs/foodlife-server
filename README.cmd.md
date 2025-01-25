

# window 10 vs code Error場合：
1. 一時＝＞　Set-ExecutionPolicy RemoteSigned -Scope Process
2. 設定＝＞　
    Powershell 管理者で起動＝＞Set-ExecutionPolicy RemoteSigned　＝＞　Y　選択　

#### Python Manager.py
1. python manage.py makemigrations master
2. python manage.py migrate

#### DB COMMON
1. sudo service postgresql start
1. sudo service postgresql stop

#### Create requirements.txt
1. pip freeze > requirements.txt
2. pip install -r requirements.txt

#### Create superuser
1. python .\manage.py createsuperuser

#### Create backupdata(※既存を上書きしないように注意)
1. dumpdata
    python manage.py dumpdata master.MasterDataGroup  -o .\init_data\master.MasterDataGroup.json
    python manage.py dumpdata master.MasterData  -o .\init_data\master.MasterData.json
    python manage.py dumpdata auth --exclude auth.permission --exclude contenttypes -o .\init_data\auth.json

    python manage.py dumpdata master.Role  -o .\init_data\master.Role.json
    python manage.py dumpdata master.RoleDetail  -o .\init_data\master.RoleDetail.json
    python manage.py dumpdata master.RoleUser  -o .\init_data\master.RoleUser.json

    python manage.py dumpdata master.Guest  -o .\init_data\master.Guest.json
    python manage.py dumpdata master.GuestGroup  -o .\init_data\master.GuestGroup.json
    python manage.py dumpdata master.GuestGroupDetail  -o .\init_data\master.GuestGroupDetail.json
    python manage.py dumpdata master.GuestDevice  -o .\init_data\master.GuestDevice.json
    python manage.py dumpdata master.GuestUser  -o .\init_data\master.GuestUser.json

    python manage.py dumpdata master.SeatGroup  -o .\init_data\master.SeatGroup.json
    python manage.py dumpdata master.Seat  -o .\init_data\master.Seat.json

    python manage.py dumpdata master.Menu  -o .\init_data\master.Menu.json
    python manage.py dumpdata master.MenuFree  -o .\init_data\master.MenuFree.json
    python manage.py dumpdata master.MenuFreeDetail  -o .\init_data\master.MenuFreeDetail.json
    python manage.py dumpdata master.MenuCategory  -o .\init_data\master.MenuCategory.json

    python manage.py dumpdata master.Order  -o .\init_data\master.Order.json
    python manage.py dumpdata master.OrderDetail  -o .\init_data\master.OrderDetail.json
    python manage.py dumpdata master.OrderDetailStatus  -o .\init_data\master.OrderDetailStatus.json
    python manage.py dumpdata master.OrderDetailMenuFree  -o .\init_data\master.OrderDetailMenuFree.json

    python manage.py dumpdata master.OrderHistory  -o .\init_data\master.OrderHistory.json
    python manage.py dumpdata master.OrderDetailHistory  -o .\init_data\master.OrderDetailHistory.json
    python manage.py dumpdata master.OrderDetailStatusHistory  -o .\init_data\master.OrderDetailStatus.json
    python manage.py dumpdata master.OrderDetailMenuFreeHistory  -o .\init_data\master.OrderDetailMenuFreeHistory.json

    
    python manage.py dumpdata master.Counter  -o .\init_data\master.Counter.json
    python manage.py dumpdata master.CounterSeat  -o .\init_data\master.CounterSeat.json
    python manage.py dumpdata master.CounterDetail  -o .\init_data\master.CounterDetail.json
    python manage.py dumpdata master.CounterDetailOrder  -o .\init_data\master.CounterDetailOrder.json

 
2. loaddata
    <!-- 
    “”“ python manage.py loaddata .\init_data\auth.json
    python manage.py loaddata .\init_data\master.MasterDataGroup.json
    python manage.py loaddata .\init_data\master.MasterData.json

    python manage.py loaddata .\init_data\master.Role.json
    python manage.py loaddata .\init_data\master.RoleDetail.json
    python manage.py loaddata .\init_data\master.RoleUser.json
    
    python manage.py loaddata .\init_data\master.GuestGroup.json
    python manage.py loaddata .\init_data\master.Guest.json
    python manage.py loaddata .\init_data\master.GuestGroupDetail.json
    python manage.py loaddata .\init_data\master.GuestDevice.json
    python manage.py loaddata .\init_data\master.GuestUser.json

    python manage.py loaddata .\init_data\master.SeatGroup.json
    python manage.py loaddata .\init_data\master.Seat.json

    python manage.py loaddata .\init_data\master.Menu.json
    python manage.py loaddata .\init_data\master.MenuFree.json
    python manage.py loaddata .\init_data\master.MenuFreeDetail.json
    python manage.py loaddata .\init_data\master.MenuCategory.json

    python manage.py loaddata .\init_data\master.Order.json
    python manage.py loaddata .\init_data\master.OrderDetail.json
    python manage.py loaddata .\init_data\master.OrderDetailStatus.json
    python manage.py loaddata .\init_data\master.OrderDetailMenuFree.json 

    python manage.py loaddata .\init_data\master.OrderHistory.json
    python manage.py loaddata .\init_data\master.OrderDetailHistory.json
    python manage.py loaddata .\init_data\master.OrderDetailStatusHistory.json
    python manage.py loaddata .\init_data\master.OrderDetailMenuFreeHistory.json 

    python manage.py loaddata .\init_data\master.Counter.json
    python manage.py loaddata .\init_data\master.CounterSeat.json
    python manage.py loaddata .\init_data\master.CounterDetail.json
    python manage.py loaddata .\init_data\master.CounterDetailOrder.json 
    -->
#### upgrade 
    pip install django  --upgrade
    pip install djangorestframework  --upgrade
    pip install djangorestframework-jwt  --upgrade
    pip install PyJWT --upgrade
    pip install django-filter --upgrade
    pip install django-extensions --upgrade
    pip install django-cors-headers --upgrade

#### Start Websocket
    python .\mysite\manage.py runserver 127.0.0.1:8001

    Set-ExecutionPolicy RemoteSigned -Scope Process
    .\env\Scripts\activate
    python .\manage.py runserver 192.168.100.173:8000
    
    Set-ExecutionPolicy RemoteSigned -Scope Process
    ..\env\Scripts\activate
    python .\manage.py runserver 192.168.100.173:8001
    
    cd .\web\
    ng serve --host 192.168.100.173
 


### 会計　ORDERデータ関連復元

    insert into seat_status
    select id, counter_no, start, "end", security_key, seat_id from seat_status_history;
    delete from seat_status_history;

    insert into "order"
    select id, order_no, counter_no, order_time, guest_id, order_method_id, order_type_id, seat_id, user_id from order_history;
    delete from order_history;

    insert into order_detail
    select id, price, option, "count", cancelable, menu_id, order_id from order_detail_history;
    delete from order_detail_history;

    insert into order_detail_menu_free
    select id, usable, start, "end", stop, menu_free_id, order_id, order_detail_id from order_detail_menu_free_history;
    delete from order_detail_menu_free_history;

    insert into order_detail_status
    select id, start_time, current, order_detail_id, status_id, user_id from order_detail_status_history;
    delete from order_detail_status_history;
    
    delete from counter;
    delete from counter_detail;
    delete from counter_detail_order;
    delete from counter_seat;
    


### 注文、会計データクリア
    delete from counter;
    delete from counter_detail;
    delete from counter_detail_order;
    delete from counter_seat;
        

    delete from seat_status_history;
    delete from order_history;
    delete from order_detail_history;
    delete from order_detail_menu_free_history;
    delete from order_detail_status_history;

    delete from seat_status;
    delete from "order";
    delete from order_detail;
    delete from order_detail_menu_free;
    delete from order_detail_status;

### メニュー情報
        
    delete from menu;
    delete from menu_category;
    delete from menu_comment;
    delete from menu_course;
    delete from menu_course_detail;
    delete from menu_free;
    delete from menu_free_detail;
    delete from menu_option;
    delete from menu_sale;

# 更新
12 {"img":"/assets/images/group_mushroom.png"}
13 {"img":"/assets/images/group_mutton.png"}
23 {"img":"/assets/images/group_launch.png"}
24 {"img":"/assets/images/group_drink.png"}

update menu 
set tax_in = true
--select * 
--from menu 
where id in (
select menu_id  from menu_category  ctg
left join master_data mst on mst.id = ctg.category_id
where category_id = 100
)

select * from order_detail_history


select 'Count:',main.cnt,'　　Price:', main.price, '　　Name:', menu.name from
(
SELECT menu_id, sum(price*count) as price, sum(count) as cnt from order_detail_history
group by menu_id 
) main
inner join menu_category ctgr on main.menu_id = ctgr.menu_id
left join menu on main.menu_id = menu.id
where ctgr.category_id in (101,102)
order by cnt desc, main.price desc


Select 
grp.display_name,
mst.display_name,
menu.*
from menu_category ctgr
left join menu on menu.id = ctgr.menu_id
left join master_data mst on mst.id = ctgr.category_id
left join master_data_group grp on grp.id = mst.group_id
order by grp.id, ctgr.category_id, ctgr.display_order

where ctgr.category_id in (101,102)
order by main.price desc, cnt desc

select * from counter

SELECT pay - change AS total,
       pay,
       change,
       detail.create_time
FROM counter_detail detail
  INNER JOIN counter
          ON counter.id = detail.counter_id
         AND counter.delete IS NULL
          OR (NOT counter.delete)
WHERE detail.canceled IS NULL
OR    (NOT detail.canceled)

select * from counter_detail where id > 362