# 该脚本用来将mysql数据库转化为sqlite3数据库
# 需要使用pip安装mysql-to-sqlite3
# 参考：https://pypi.org/project/mysql-to-sqlite3/

mysqlHost=localhost
mysqlPort=3306
mysqlDatabase=live_analyzer
mysqlUserame=Example
mysqlPwd=Example

sqliteFilePath=./live_analyzer_database.db

mysql-to-sqlite3 -h $mysqlHost -P $mysqlPort -d $mysqlDatabase -u $mysqlUsername --mysql-password $mysqlPwd -f $sqliteFilePath
