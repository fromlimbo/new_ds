.. 动态调度 documentation master file, created by
   sphinx-quickstart on Thu Sep 28 10:40:46 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Python算法模板
====================================

本项目的核心是提供了一套使得算法可以被分布式异步调用的框架，以及算法运行过程中会使用的工具类，包括日志、读写缓存、读写数据库等。

工程分为三个主要部分：算法入口、算法模块和工具类。

算法入口主要为 ``app.py`` 和 ``app_view.py`` 两个文件。其中 ``app.py`` 里生成了各工具类的实例， ``app_view.py`` 为flask的视图函数。

工具类包含在 ``util`` 文件夹下，各模块的使用方法可在各自的文档中找到。

算法模块是与本模板独立的一部分，由各个小组实现。请将算法放在 ``algorithm`` 文件夹下，并提供明确的调用入口。

文档
====================================

.. toctree::
   :maxdepth: 2

   config
   async
   example
   utils


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

