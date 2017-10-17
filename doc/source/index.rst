.. 动态调度 documentation master file, created by
   sphinx-quickstart on Thu Sep 28 10:40:46 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

算法模板文档
====================================

本项目的核心是提供了一套使得算法可以被分布式异步调用的框架，以及算法运行过程中会使用的工具类，包括日志、读写缓存、读写数据库等。

工程分为三个主要部分：算法入口、算法模块和工具类。

算法入口主要为 ``app.py`` 和 ``app_view.py`` 两个文件。其中 ``app.py`` 里生成了各工具类的实例， ``app_view.py`` 为flask的视图函数。

工具类包含在 ``util`` 文件夹下，各模块的使用方法可在各自的文档中找到。

算法模块是与本模板独立的一部分，由各个小组实现。

异步调用样例
===================================

分布式异步调用是通过开源框架Celery实现的。将算法修改为异步调用的版本是非常容易的，我们在 ``app_view.py`` 中提供了一个例子::

   @celery.task
   def add(x,y):
      return x+y

``add``为一个普通的python函数，只需要在函数定义上增加 ``@celery.task`` 装饰器，即可将其变为一个celery任务。
这里的 ``celery`` 是一个Celery类实例，我们在 ``app.py`` 中生成了这个实例，所以算法同学需要在你们的算法入口函数所在脚本文件中引用它::

   from app import celery

这里有个需要注意的地方，celery默认的序列化器是 ``json`` 所以没办法在参数中传递python类对象，若算法的参数中有类对象请使用 ``pickle`` 作为序列化器。
指定序列化器也很简单，将修饰器改成如下形式即可::

   @celery.task(serializer='pickle')

当将函数转为celery任务之后，我们在 ``app_view.py`` 中即可根据请求进行异步调用。例如新建一个 ``add`` 任务::

   res = add.delay(1, 2)
   task_id = res.id

之后便可使用获得的 ``task_id`` 获取计算结果及进行任务管理。

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



工具类文档
==================

.. toctree::
   :maxdepth: 2

   utils




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

