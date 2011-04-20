buzz2weibo - 同步Google Buzz到新浪微博
======================================

将您自己Google Buzz上的public消息转发到新浪微博，可包括文字、图片、链接和地理坐标

特性
----

* 同步文字，这个自然
* 将buzz中的第一个图片上传
* 同步地理坐标，如果有的话
* 如果buzz附有链接，或者是发自Google Reader，链接也被同步
* 每次运行缺省只同步3条，防止被新浪微博暂时封禁
* 只同步public的buzz，保护private的私密
* 在新浪微博显示到buzz的链接
* 如果会编程，activity/下从BuzzActivity派生一个类，可以个性化处理特定的源（比如你的博客）

运行条件
--------

这是一个在你自己的机器运行的程序，它不是一个网络服务，至少目前不是。

要运行buzz2weibo，必须满足如下条件

* python 2.6 及以上版本
* 能周期定时执行本程序，否则只能每次手工运行
* 畅通的网络，非一般的畅通，你懂的

安装
----

下载、解压，完毕

当然用git clone会更舒服

配置
----

在解压目录下，运行

python setup.py

跟随屏幕操作

使用
----

python buzz2weibo.py


建议
----

建议在Linux下使用，cron里设为每分钟执行一次


链接
----

主页： https://github.com/sunner/buzz2weibo
Bugs： https://github.com/sunner/buzz2weibo/issues
作者Buzz： https://profiles.google.com/u/0/sunner/buzz
作者微博： http://weibo.com/sunnersun
