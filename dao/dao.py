# import pymysql
import sqlite3

class DAO:
    def __init__(self,host="localhost",user="root",password="Zcx010712",database="live_analyzer") -> None:
        '''
        初始化数据库
        '''
        # self.db = pymysql.connect(host=host,user=user,password=password,database=database)
        self.db = sqlite3.connect("live_analyzer_database.db")
    
    def close(self):
        '''
        关闭数据库连接
        '''
        self.db.close()
    
    def get_字段名(self,table_name):
        '''
        获得制定表格的字段名称
        '''
        # for mysql
        # sql = '''
        # SHOW COLUMNS FROM {table_name};
        # '''.format(table_name = table_name)

        # for sqlite
        sql = '''
        PRAGMA table_info({table_name});
        '''.format(table_name = table_name)

        cursor = self.db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        # print(result)
        
        #for mysql
        # column_names = [row[0] for row in result]

        #for sqlite
        column_names = [column[1] for column in result]

        return column_names

    def get_证据视频(self):
        '''
        从数据库中获取证据视频表
        '''
        sql = '''
        select * from 证据视频;
        '''
        cursor = self.db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    def update_证据视频_线索内容_by_path(self, path:str, clue_content:str):
        '''
        按照证据视频的存放路径来更新证据视频的线索内容
        '''
        cursor = self.db.cursor()
        cursor.execute("UPDATE 证据视频 SET 线索内容=? WHERE 视频文件地址=?", (clue_content, path))
        self.db.commit()
        cursor.close()

    def update_证据视频_商品类别_by_path(self, path:str, good_kind:str):
        '''
        按照证据视频的存放路径来更新证据视频的线索内容
        '''
        cursor = self.db.cursor()
        cursor.execute("UPDATE 证据视频 SET 商品类别=? WHERE 视频文件地址=?", (good_kind, path))
        self.db.commit()
        cursor.close()

    def get_证据视频_by_name(self, name:str):
        '''
        按照证据视频地址从证据视频表中选择证据视频
        '''
        sql = '''
        select * from 证据视频
        where 视频文件地址 like "%{name}%";
        '''.format(name=name)
        cursor = self.db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    def get_证据视频_商品类别_by_直播间名称(self, 直播间名称:str):
        '''
        按照直播间名称从证据视频表中选择证据视频对应的商品类别
        '''
        sql = '''
        select 商品类别 from 证据视频
        where 直播间名称 = "{直播间名称}";
        '''.format(直播间名称=直播间名称)
        cursor = self.db.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        return result

    def insert_证据视频(self, video_addr:str, ocr_txt:str, asr_txt:str, content:str, good_category:str, time:str, live_url:str, live_name:str):
        '''
        向数据库中插入证据视频
        '''
        sql = '''
        INSERT INTO 证据视频 (视频文件地址, 视频ocr结果, 视频asr结果, 是否违规, 线索内容, 商品类别, 获取时间, 直播间链接, 直播间名称)
        VALUES ("{video_addr}","{ocr_txt}","{asr_txt}","否","{content}","{good_category}", "{time}","{live_url}","{live_name}");
        '''.format(video_addr=video_addr, ocr_txt=ocr_txt, asr_txt=asr_txt, content=content, good_category=good_category, time=time, live_url=live_url,live_name=live_name)
        cursor = self.db.cursor()
        cursor.execute(sql)
        self.db.commit()
        cursor.close()
    
    def delete_证据视频_by_线索内容(self, clue_content:str):
        '''
        删除特定证据视频记录
        '''
        sql = '''
        DELETE FROM 证据视频
        WHERE 线索内容 like '%{clue_content}%';
        '''.format(clue_content=clue_content)
        cursor = self.db.cursor()
        cursor.execute(sql)
        self.db.commit()
        cursor.close()

    def get_通用敏感词(self):
        '''
        从数据库中获取通用敏感词列表
        '''
        sql = """
        select * from 通用敏感词;
        """
        cursor = self.db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result
    
    def delete_通用敏感词(self, word:str):
        '''
        删除特定通用敏感词
        '''
        sql = '''
        DELETE FROM 通用敏感词
        WHERE 敏感词 like '%{word}%';
        '''.format(word=word)
        cursor = self.db.cursor()
        cursor.execute(sql)
        self.db.commit()
        cursor.close()
    
    def get_专项变体词(self):
        '''
        从数据库中获取专项变体词列表
        '''
        sql = """
        select * from 专项变体词;
        """
        cursor = self.db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    def insert_专项变体词(self, 变体词:str, 原词:str):
        '''
        向数据库中插入变体词
        '''
        sql = '''
        INSERT INTO 专项变体词 (变体词, 原词)
        VALUES ('{变体词}','{原词}');
        '''.format(变体词=变体词, 原词=原词)
        cursor = self.db.cursor()
        cursor.execute(sql)
        self.db.commit()
        cursor.close()

    def get_禁限售(self):
        '''
        从数据库中获取禁限售词列表
        '''
        sql = """
        select * from 禁限售;
        """
        cursor = self.db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result
    
    def get_保健品(self):
        '''
        从数据库中获取保健品列表
        '''
        sql = """
        select * from 保健品;
        """
        cursor = self.db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result
    
    def get_国产化妆品(self):
        '''
        从数据库中获取国产化妆品列表
        '''
        sql = """
        select * from 国产化妆品;
        """
        cursor = self.db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result
    
    def get_进口化妆品(self):
        '''
        从数据库中获取进口化妆品列表
        '''
        sql = """
        select * from 进口化妆品;
        """
        cursor = self.db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result
    
    def get_国产药品(self):
        '''
        从数据库中获取国产药品列表
        '''
        sql = """
        select * from 国产药品;
        """
        cursor = self.db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    def get_进口药品(self):
        '''
        从数据库中获取进口药品列表
        '''
        sql = """
        select * from 进口药品;
        """
        cursor = self.db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    def get_进口医疗器械备案(self):
        '''
        从数据库中获取进口医疗器械(备案)列表
        '''
        sql = """
        select * from 进口医疗器械备案;
        """
        cursor = self.db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result
    
    def get_进口医疗器械注册(self):
        '''
        从数据库中获取进口医疗器械(注册)列表
        '''
        sql = """
        select * from 进口医疗器械注册;
        """
        cursor = self.db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result
    
    def get_国产医疗器械备案(self):
        '''
        从数据库中获取国产医疗器械(备案)列表
        '''
        sql = """
        select * from 国产医疗器械备案;
        """
        cursor = self.db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result
    
    def get_国产医疗器械注册(self):
        '''
        从数据库中获取国产医疗器械(注册)列表
        '''
        sql = """
        select * from 国产医疗器械注册;
        """
        cursor = self.db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result
    
    def get_直播实体池(self):
        '''
        从数据库中获取直播实体池
        '''
        sql = """
        select * from 直播实体池;
        """
        cursor = self.db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result
    
    
    def get_定制直播实体(self):
        '''
        从数据库中获取定制直播实体
        '''
        sql = """
        select * from 定制直播实体;
        """
        cursor = self.db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    def get_定制直播历史(self):
        '''
        从数据库中获取定制直播历史
        '''
        sql = """
        select * from 定制直播历史;
        """
        cursor = self.db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result
    
    def get_巡检直播实体(self):
        '''
        从数据库中获取巡检直播实体
        '''
        sql = """
        select * from 巡检直播实体;
        """
        cursor = self.db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result
    
    def get_巡检直播历史(self):
        '''
        从数据库中获取巡检直播历史
        '''
        sql = """
        select * from 巡检直播历史;
        """
        cursor = self.db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result
    

    def insert(self,table_name,**kargs):
        '''
        向数据库指定表中插入数据
        '''
        values = ""
        keys = ""
        for i in list(kargs.values())[:-1]:
            values += "'" + i + "',"
        values += "'" + list(kargs.values())[-1] + "'"
        for i in list(kargs)[:-1]:
            keys += i + ","
        keys += list(kargs)[-1]
        sql = """
        insert into {table_name}({keys})
        values({values})
        """.format(table_name = table_name, keys = keys, values = values)
        cursor = self.db.cursor()
        cursor.execute(sql)
        self.db.commit()
        cursor.close()

    def delete(self,table_name,**kargs):
        '''
        在数据库指定表中删除指定数据
        要求字段属性必须全为字符形式
        '''
        values = list(kargs.values())
        keys = list(kargs)
        conditions = ""
        num = len(values)
        for i in range(num-1):
            conditions += keys[i] + "='" + values[i] + "' and "
        conditions += keys[num-1] + "='" + values[num-1] + "'"
        sql = """
        delete from {table_name}
        where {conditions};
        """.format(table_name = table_name, conditions = conditions)
        print(sql)
        cursor = self.db.cursor()
        cursor.execute(sql)
        self.db.commit()
        cursor.close()

    # def update(self, table_name, **kargs):
    #     '''
    #     在数据库指定表中更新
    #     '''

if __name__ == "__main__":
    dao = DAO()

    # video_path = 'static/video/variant/新西兰鱼油世家/新西兰鱼油世家4.mp4'
    # ocr_path = "BIO-H|新西兰鱼油世家  98.99 RTG结构 IFOS 高纯度 高吸收 五星鱼油 "
    # asr_path = "形态代表着什么吸某受率像一个产品它的含量高含量再高如果说他们吸收不好的话我吃到肚子里边他打折够大个比方打了个三折打了个五折吃跟没吃其实它的区别并不是很大像很多很多中老年人咱们在上了年纪以后小肠小胃这块动力这块他肯定是跟咱们十几二十岁啊"
    # content = {
    #     'type':2, 
    #     'content':{
    #         '变体词':'小肠小胃',
    #         '原词':'肠胃',
    #         '匹配方式':'正则表达式'
    #         }
    #     }
    # from datetime import datetime
    # current_time = datetime.now()
    # formatted_time = current_time.strftime("%Y-%m-%d_%H:%M:%S")
    # live_url = ""
    # live_name = "新西兰鱼油世家"
    # dao.insert_证据视频(video_path, ocr_path, asr_path, str(content),formatted_time,live_url,live_name)
    # print(dao.get_证据视频())

    # print(dao.get_专项变体词())
    # dao.delete_证据视频_by_线索内容("0")

    # print(list(dao.get_保健品())[0][0])
    # print([i[0] for i in dao.get_通用敏感词()])

    dao.insert("直播实体池",直播名称="name_test_2",直播链接="url_test_2")
    # dao.delete("直播实体池",直播名称="name_test_2",直播链接="url_test_2")