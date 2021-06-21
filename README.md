# 数据库lab3

## 大致思路

- 完成实验时，使用flask+python基于静态页面和动态数据，生成动态页面；静态页面使用jinjia模板库做模板渲染，模板在bootstrap示例的基础上修改而成；
- 后续考虑将架构修改为前后端分离式的架构，详见收藏夹几个网站。

## 实验过程

### 登陆页面

- 扒了一个觉得还不错的bootstrap登陆页面，效果如下

  ![1](./figs/login.png)

- 登录失败时，会根据失败后返回错误的两种类型，提示对应消息

  - 数据库名称错误

    ![1](./figs/login_fail1.png)

  - 用户名或密码错误

    ![1](./figs/login_fail2.png)

- 待实现checkbox打勾使用cookies“记住”

### 主页面

- 写了一个导航栏主页面，其中导航栏链接通过替换页面中的iframe内联框架实现页面之间的跳转；

- 主页面是数据库中所有表的count视图，同助教给的模板。

  ![1](./figs/home1.png)

### 客户管理

