

# 

1. Serializer的ReadOnlyField属性如果想作为filter的检索条件 必须额外定义，只用'__all__'的话，是无效的
    

```python
    
    # 外键的关联Key不在model中的情况 Filter定义
    class MenuCategoryFilter(filters.FilterSet):
        category_group = filters.CharFilter(field_name="category__group__id", lookup_expr='exact')
        class Meta:
        model = MenuCategory
        fields = ['id', 'category', 'menu', 'category_group']

    # Serializer定义
    class MenuCategorySerializer(ModelSerializer):
        '''
        マスタ関連データのすべて
        '''
        category_group = ReadOnlyField(source='category.group.id', read_only=True)
        category_name = ReadOnlyField(source='category.display_name', read_only=True)
        menu_no = ReadOnlyField(source='menu.no', read_only=True)
        menu_name = ReadOnlyField(source='menu.name', read_only=True)

        class Meta:
            model = MenuCategory
            fields = (
                'id',
                'category',
                'menu',
                'display_order',
                'category_group',
                'category_name',
                'menu_no',
                'menu_name',
            )
```

2. SampleAPIView DEMO

```python
class TestController(SampleAPIView):
    
    permission_classes = (permissions.AllowAny,)
    
    def init(self, request, *args, **kwargs):
        pass

    def index(self, request, *args, **kwargs):

        print("####################### test #########################")

        result = JsonResult(result=True, message="ok")

        return Response(result)

# URL
url(r'^test/(?P<fun>.*)/', TestController.as_view()),

# JsonService
this.jsonSrv.get('xxx/test/index/' ... ...
this.jsonSrv.get('xxx/test/init/' ... ...


```


3. Get serializer from model

```python
@api_view(['GET', 'POST'])
@cache_page(60 * 15)
def list(request):
    """
    ...
    
    """
    if request.method == 'GET':
        guest = Guest.objects.get(id=1)
        serializer = GuestSerializer(instance=guest)

        return Response(serializer.data)

```

4. Catch All Exception

```python
        try:

            # 放題メニューリストを取得
            menu_details = MenuFreeDetail.objects.filter(menu_free__menu__id=order_detail.menu.id)
            freemenu_list = [detail.menu.id for detail in menu_details]
            
            # ...(省略)...
        except:
            logger.error("Unexpected error: {0}".format(sys.exc_info()[0]))
```

5. Check GET,POST 存在 ＆　取得

```python
    # GET
    if 'seat_id' in request.GET:
        seat_id = request.GET['seat_id']
```

```python
    # POST
    if "select_ids" in request.data:
        self.select_ids = request.data["select_ids"]

    # Check POST DATA TYPE
    if isinstance(request.data, list):
        pks = [ data["id"] for data in request.data]
```