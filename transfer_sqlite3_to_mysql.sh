# 该脚本用来将sqlite3数据库转化为mysql数据库
# 需要使用pip安装sqlite3-to-mysql
# 参考：https://pypi.org/project/sqlite3-to-mysql/

mysqlHost=localhost
mysqlPort=3306
mysqlDatabase=live_analyzer
mysqlUserame=Example
mysqlPwd=Example

sqliteFilePath=./live_analyzer_database.db

sqlite3-to-mysql  -f $sqliteFilePath -h $mysqlHost -P $mysqlPort -d $mysqlDatabase -u $mysqlUsername --mysql-password $mysqlPwd
