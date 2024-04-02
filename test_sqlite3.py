import sqlite3

# 连接到SQLite数据库
conn = sqlite3.connect('example.db')
c = conn.cursor()

# 创建表
c.execute('''CREATE TABLE IF NOT EXISTS my_table (my_column TEXT)''')

# 插入None值
value = None

def func(value:str):
    c.execute("INSERT INTO my_table (my_column) VALUES (?)", (value,))

func(value)
# 提交更改并关闭连接
conn.commit()
conn.close()