import os
import numpy as np
import sys
import DB_Connection as dbc

# argv1 : member_no
try :
      member_no = int(sys.argv[1])
      similarity = np.load(os.getcwd()+'\\Recommend.npy')[member_no]
      similarity[member_no] = 0
      rank = list(map(int, similarity.argsort()[::-1]))

      sql = "select distinct content_type, content_id " \
            "from node " \
            "where ((content_type, content_id) not in " \
            "(select content_type, content_id from node where member_no = %s)" \
            "and member_no in (%s, %s, %s, %s));"

      dbc.cursor.execute(sql, (member_no, rank[0], rank[1], rank[2], rank[3]))
      recommend_list = dbc.cursor.fetchmany(5)

      for i in recommend_list :
            print(i)
except Exception as e :
      print(str(e))