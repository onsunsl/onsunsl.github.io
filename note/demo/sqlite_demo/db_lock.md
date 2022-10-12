Scheduler-UI_3 保存推送订单数据  上锁：2022-08-26 19:54:52,584 Scheduler-UI_3: peewee proxy connect 已经写入db
Thread 0x000003a4 (most recent call first):                                               
File "site-packages\peewee.py", line 3747 in close
File "db\utilities.py", line 843 in insert_data
File "db\utilities.py", line 1383 in insert_offline_order
File "logic\push_dmall_offline_order_logic.py", line 1192 in save_push_order_data
File "common\__init__.py", line 103 in inner
File "logic\payment_logic.py", line 760 in finish_payment
File "ui\kv\payment\payment_screen.py", line 1039 in finish_and_print
File "concurrent\futures\thread.py", line 56 in run
File "concurrent\futures\thread.py", line 69 in _worker
File "threading.py", line 864 in run
File "threading.py", line 916 in _bootstrap_inner
File "threading.py", line 884 in _bootstrap

Scheduler().schedule_interval(partial(cls.push_offline_order, int_pre_day), interval=3600) 1小时循环推单 2022-08-26 19:54:52,604 Scheduler_3: rdp订单推送服务端
Thread 0x00001bdc (most recent call first):                                                  
File "db\sqlite\executor.py", line 99 in connect
File "db\sqlite\peewee_proxy.py", line 55 in _connect
File "site-packages\peewee.py", line 3768 in _create_connection
File "site-packages\peewee.py", line 3738 in connect
File "db\utilities.py", line 817 in insert_data
File "db\utilities.py", line 1383 in insert_offline_order
File "logic\push_dmall_offline_order_logic.py", line 633 in record_offline_order_new
File "logic\push_dmall_offline_order_logic.py", line 731 in dmall_order_deal
File "common\__init__.py", line 103 in inner
File "logic\push_dmall_offline_order_logic.py", line 1207 in do_push_order
File "common\__init__.py", line 103 in inner
File "logic\push_dmall_offline_order_logic.py", line 171 in push_offline_order
File "schedule\scheduler.py", line 184 in wraps
File "concurrent\futures\thread.py", line 56 in run
File "concurrent\futures\thread.py", line 69 in _worker
File "threading.py", line 864 in run
File "threading.py", line 916 in _bootstrap_inner
File "threading.py", line 884 in _bootstrap

Scheduler_2 上传任务  阻塞在： 2022-08-26 19:55:01,238 Scheduler_2: SQLiteExecuteQueue:173875312 / 2022-08-26_pos.db init
Thread 0x00000dd4 (most recent call first):                                                   
File "db\sqlite\executor.py", line 82 in __enter__
File "db\sqlite\executor.py", line 171 in query_many
File "db\sqlite\executor.py", line 158 in query
File "logic\push_dmall_offline_order_logic.py", line 1150 in get_sale_into_db
File "common\__init__.py", line 103 in inner
File "logic\push_dmall_offline_order_logic.py", line 1165 in get_sale_upload_ok
File "common\__init__.py", line 103 in inner
File "interface\upload_sale_data.py", line 314 in is_upload_done
File "common\__init__.py", line 103 in inner
File "interface\upload_sale_data.py", line 238 in upload_data
File "interface\upload_sale_data.py", line 174 in upload
File "schedule\scheduler.py", line 184 in wraps
File "concurrent\futures\thread.py", line 56 in run
File "concurrent\futures\thread.py", line 69 in _worker
File "threading.py", line 864 in run
File "threading.py", line 916 in _bootstrap_inner
File "threading.py", line 884 in _bootstrap


MainThread  2022-08-26 19:55:52,717 MainThread: 任务超时：b636ccbc-e4c8-443e-993a-6a861c846811 打印等待60S超时， 返回销售扫商品时候db阻塞了
Thread 0x0000055c (most recent call first):
File "db\sqlite\executor.py", line 82 in __enter__
File "db\sqlite\executor.py", line 171 in query_many
File "db\sqlite\executor.py", line 158 in query
File "logic\sale_logic.py", line 1921 in get_item_id_from_db
File "logic\sale_logic.py", line 603 in insert_merch
File "ui\kv\sale\sale_screen.py", line 737 in logic_insert
File "ui\kv\sale\sale_screen.py", line 770 in goods_insert
File "ui\kv\sale\sale_screen.py", line 695 in add_merch
File "ui\kv\sale\sale_screen.py", line 724 in _add_goods_merge_callback
File "site-packages\kivy\clock.py", line 1095 in callback_func


peewee.py                       peewee_proxry.py          executor.py
     connect()
     _conn_lock.acquire()
                                  _connect()
                                                         __lock.acquire()
                                                              |
                                                         __conn_q.get()



close()
    _conn_lock.acquire()		
                                 _close()                      
                                                         __lock.release()      
                                                              |
                                                         __conn_q.put




Scheduler-UI_3: connect() =》 _conn_lock 上锁  =》  __lock 上锁  =》  _conn_lock 释放  =>   -----------读写db----------------  close() =》阻塞等待 _conn_lock 释放    ---死锁

Scheduler_3: --------------------其他work-----------------------------   connect() =》 _conn_lock 上锁 => 阻塞等待 __lock                                          ---死锁

Scheduler_2: --------------------------其他work---------------------------------   connect() =》 阻塞等待 __lock

MainThread: ------------------ 60 秒打印超时 进入下一单扫描db 操作 ------------------   connect() =》 阻塞等待 __lock    