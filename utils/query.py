from pymysql import connect, MySQLError


# 创建数据库连接
def create_connection():
    return connect(
        host='localhost',
        user='root',
        password='root',
        database='wb',
        port=3306
    )


# 查询函数
def querys(sql, params, type='no_select'):
    try:
        # 每次执行查询时都重新创建连接和游标
        conn = create_connection()
        cursor = conn.cursor()

        # 确保连接有效
        conn.ping(reconnect=True)

        # 执行查询
        params = tuple(params)
        cursor.execute(sql, params)

        if type != 'no_select':
            # 获取查询结果
            data_list = cursor.fetchall()
            conn.commit()
            return data_list
        else:
            conn.commit()
            return '数据库语句执行成功'
    except MySQLError as e:
        print(f"执行查询时发生错误: {e}")
        return None
    finally:
        # 确保关闭游标和连接
        cursor.close()
        conn.close()


# 示例：调用查询函数
def get_all_comments_data():
    sql = "SELECT * FROM comments"
    params = []  # 可以根据需要传递参数
    result = querys(sql, params, type='select')
    return result

# 示例：在Flask视图函数中调用
# 在视图中调用 get_all_comments_data() 来获取评论数据
