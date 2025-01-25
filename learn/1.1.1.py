
sql = "1111111{0}111111111"
con = "<22222222222>"
sql = sql.format(con)
print(sql)

# 序列を分解
data = ['ACME', 50, 91.1, (2012, 12, 21)]
_, shares, price, _ = data
print(shares)

#
record = ('Dave', 'dave@example.com', '773-555-1212', '847-555-1212')
name, email, *phone_numbers = record
print(type(phone_numbers))

# 忽略
record = ('ACME', 50, 123.45, (12, 18, 2012))
name, *_, (*_, year) = record
