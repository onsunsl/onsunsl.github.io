# -*- coding: utf-8 -*-
# @Project : onsunsl_github_io
# @Author  : GuangLin
# @File    : pool_q_demo.py
# @Time    : 2023/1/9 16:28
# @Email   : Guanglin.Liang@DMall.com
# @Version : 0.01
# @Desc    : 
#
# @History
# -------------------------------------------
#     Time         Author          Desc
# -------------------------------------------
import collections
import queue


class LifoQueue(queue.Queue):
    def _init(self, _):
        self.queue = collections.deque()

    def _qsize(self, len=len):
        return len(self.queue)

    def _put(self, item):
        self.queue.append(item)

    def _get(self):
        return self.queue.pop()
