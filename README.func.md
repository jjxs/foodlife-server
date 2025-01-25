

# Util 共通クラス

1. 現在時間文字列取得

```python
    def current_string(format="%Y/%m/%d %H:%M:%S.%f"):
        ...

    # 使用例：
    Util.current_string("%Y%m%d%H%M%S%f")
```

2. 現在時間取得

```python
    def current():
            return datetime.now()
```

    DBの利用関数
    
    ■　now()はCURRENT_TIMESTAMPと同じもので、伝統的なPostgreSQL関数です。 
    ■　transaction_timestamp()はCURRENT_TIMESTAMP同様のものですが、明確に何が返されるかを示す名前になっています。■　statement_timestamp()は現在の文の実行開始時刻を返すものです（より具体的にいうと、直前のコマンドメッセージをクライアントから受け取った時刻です）。 
    ■　statement_timestamp()およびtransaction_timestamp()はトランザクションの最初のコマンドでは同じ値を返しますが、その後に引き続くコマンドでは異なる可能性があります。 
    ■　clock_timestamp()は実際の現在時刻を返しますので、その値は単一のSQLコマンドであっても異なります。
    事务处理中登录唯一时间的情况下，优先使用transaction_timestamp()


3. 

```python
    def model_to_json(model):
        ...
    
    #使用例
    Util.model_to_json(seat_status),
```

4. 
5. 
6. 
7. 