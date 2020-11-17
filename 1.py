# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/21 19:32
# @Author  : TangHuanqiang
# @File    : 1.py
from app import db,Tasks
# 查看数据库具体数据
if __name__ == '__main__':
    # id = 1
    # done = True
    # for i in range(1000):
    #     description = 'nothing' + str(id)
    #     task = Tasks(description=description,done=done)
    #     id+=1
    #     done = not done
    #     db.session.add(task)
    # db.session.commit()
    tasks = Tasks.query.all()
    i = 1
    data = {}
    for t in tasks:
        detail = {
            'id': t.id,
            'description': t.description,
            'done': t.done
        }
        string = 'task' + str(i)
        data[string] = detail
        i += 1
    for key,value in data.items():
        print(key,':',value)