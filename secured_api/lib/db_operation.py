import sqlite3

class DatabaseManager(object): 
    """
    """
    def __init__(self): 
        # Connect to Sqlite3 file
        self.db_conn = sqlite3.connect('db.sqlite3',  check_same_thread=False)
        self.db_cursor = self.db_conn.cursor()
        print("SUCCESS: Connection to the database succeeded")

    def get_quotes(self, request):

        # 参数化查询
        dataname = request['dataname']  

        # 使用 Python 字符串格式化來插入欄位名稱
        sql = f"SELECT id, date, {dataname} FROM stocks"
        try:
            self.db_cursor.execute(sql)
            res = self.db_cursor.fetchall()

        except sqlite3.DatabaseError as e:
            res = {'msg':f"事务错误: {e}"}
            self.db_conn.rollback()  # 回滚事务
        
        return res