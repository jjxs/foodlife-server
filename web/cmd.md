# 启动Shell
python .\manage.py shell

# 清空注文数据
from master.models.order import *
OrderDetailStatus.objects.all().delete()
OrderDetail.objects.all().delete()
Order.objects.all().delete()

from learn.tool.import_data import *