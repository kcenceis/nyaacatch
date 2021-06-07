import sqlite3
import os

SQLDATABASEFILE = os.path.split(os.path.realpath(__file__))[0] + os.sep + 'bookAddress.db'  # 数据库文件名称


# 传入数据表名称检查是否存在 返回True False
# param: 数据表名称
def check_table(table_name):
    conn = sqlite3.connect(SQLDATABASEFILE)
    c = conn.cursor()
    # 查询数据
    cursor = c.execute("select count(*) from sqlite_master where name=? ", (table_name,))
    # values = cursor.fetchone()
    result = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    if result == 1:
        return True
    else:
        return False


# 初始化SQLite数据库文件
def connSQL():
    if not check_table('http_history'):
        conn = sqlite3.connect(SQLDATABASEFILE)
        c = conn.cursor()
        # 执行创建表
        c.execute('''CREATE TABLE http_history                      
       (id INTEGER PRIMARY KEY AUTOINCREMENT,
       address        CHAR(50),
       finish         INT(4),
       dDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
       );''')
        conn.commit()
        conn.close()
    if not check_table('file_history'):
        conn = sqlite3.connect(SQLDATABASEFILE)
        c = conn.cursor()
        # 执行创建表
        c.execute('''CREATE TABLE file_history                      
       (id INTEGER PRIMARY KEY AUTOINCREMENT,
       address        CHAR(50),
       title          CHAR(200),
       torrent        CHAR(2000),
       magnet         CHAR(2000),
       category       CHAR(2000),
       file_name      CHAR(2000),
       dDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
       );''')
        conn.commit()
        conn.close()


def insertSQL(mAddress):
    conn = sqlite3.connect(SQLDATABASEFILE)
    c = conn.cursor()
    c.execute("INSERT INTO http_history (address) \
      VALUES (?)", (mAddress,))
    conn.commit()
    c.close()
    conn.close()


def insertSQL_file_history(nyaa_list):
    conn = sqlite3.connect(SQLDATABASEFILE)
    c = conn.cursor()
    c.execute("INSERT INTO file_history (address,title,torrent,magnet,category,file_name) \
      VALUES (?,?,?,?,?,?)",
              (nyaa_list.address,
               nyaa_list.title,
               nyaa_list.torrent,
               nyaa_list.magnet,
               nyaa_list.category,
               nyaa_list.file_name,))
    conn.commit()
    c.close()
    conn.close()


def selectSQL():
    conn = sqlite3.connect(SQLDATABASEFILE)
    c = conn.cursor()
    conn.commit()
    # 查询数据
    cursor = c.execute("SELECT *  from http_history")
    for row in cursor:
        print("ID = ", row[0])
        print("ADDRESS = ", row[1])
    cursor.close()
    conn.close()


# 获取有多少相同的地址，返回bool
def isFinish(mAddress):
    conn = sqlite3.connect(SQLDATABASEFILE)
    c = conn.cursor()
    # 查询数据
    cursor = c.execute("SELECT count(*) as count  from http_history where address = ? and finish='1'", (mAddress,))
    # values = cursor.fetchone()
    result = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    if result == 1:
        return True
    else:
        return False


# 获取有多少相同的地址，返回bool
def isFinish_file_history(nyaa_list):
    conn = sqlite3.connect(SQLDATABASEFILE)
    c = conn.cursor()
    # 查询数据
    cursor = c.execute("SELECT count(*) as count  from file_history where file_name = ?", (nyaa_list.file_name,))
    # values = cursor.fetchone()
    result = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    if result == 1:
        return True
    else:
        return False


# 获取count，查看是否存在相同条目，返回bool
def HAS_SQL(mAddress):
    conn = sqlite3.connect(SQLDATABASEFILE)
    c = conn.cursor()
    # 查询数据
    cursor = c.execute("SELECT count(*) as count  from http_history where address = ?", (mAddress,))
    result = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    if result == 1:
        return True
    else:
        return False


# 更新数据库，标识是否下载完毕
def updateSQL_Download(mADDRESS):
    conn = sqlite3.connect(SQLDATABASEFILE)
    c = conn.cursor()
    cursor = c.execute('''update http_history set finish='1' where address= ?''', (mADDRESS,))
    conn.commit()
    cursor.close()
    conn.close()


# 删除180日前的数据
def DeleteSQL():
    if os.path.exists(SQLDATABASEFILE):
        conn = sqlite3.connect(SQLDATABASEFILE)
        c = conn.cursor()
        cursor = c.execute("delete from http_history where date('now', '-180 day') >= date(dDate)")  # 删除180日之前的数据
        conn.commit()
        cursor.close()
        conn.close()
