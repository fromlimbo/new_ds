工具类使用样例
====================================

Logging
------------------------------------

以下代码展示了如何使用我们的日志模块。::

   from utils import MQLoggingHandler
   import logging

   loger = logging.getLogger(__name__)

   # 初始化MQLoggingHandler对象（logging Handler的一个子类对象）
   handler = MQLoggingHandler(MQLogConfig)

   loger.addHandler(handler)

   # 设置日志等级，Consumer需要通过这个等级确定要接收的信息
   loger.setLevel(logging.DEBUG)

   # 获得执行日志模块的 电脑名称和进程号
   computer_name=platform.node()
   pid=os.getpid()

   # 以下为不同级别的logging
   loger.debug(json.dumps({'computer_name':computer_name,
                          'pid':pid,
                          'msg':'hello world'}))
   loger.error('hello')
   loger.critical("critical world")