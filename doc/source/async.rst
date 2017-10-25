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