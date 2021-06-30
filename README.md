# 数据库lab3

[TOC]

## 大致思路

- 完成实验时，使用flask+python基于静态页面和动态数据，生成动态页面；静态页面使用jinjia模板库做模板渲染，模板在bootstrap示例的基础上修改而成；
- 后续考虑将架构修改为前后端分离式的架构，详见收藏夹几个网站。

## 食用方法

- 大致目录结构如下：

  ```zsh
  /root/database_learning/lab3
  ├── data
  │   ├── backup.sql		数据库全备份
  │   ├── bank.sql		初始数据库文件
  │   └── testdata.sql	初始测试数据
  ├── figs
  │   ├── 存放README.md的图片
  ├── flask_demo
  │   ├── util.py			用到的小函数，如自动获取日期区间中每年、每月、每季度
  │   ├── db.py			数据库处理函数
  │   ├── main.py			flask生成app的python脚本
  │   ├── static
  │   │   ├── css
  │   │   │   ├── 样式文件
  │   │   ├── figs
  │   │   │   └── 404.png
  │   │   ├── fonts		暂时没用
  │   │   └── js
  │   │       ├── 脚本文件
  │   ├── templates
  │   │   ├── 网页模板
  ├── LICENSE			可忽略
  ├── db_lab3.yaml	conda虚拟环境的配置文件
  └── README.md		实验报告/说明文档
  ```

- 创建数据库，导入测试数据

  - 创建数据库和访问用户

    <img src="./figs/install1.png" alt="1" style="zoom: 50%;" />

  - 测试用户和授予权限：

    <img src="./figs/install2.png" alt="1" style="zoom: 50%;" />

  - 导入数据库和测试数据：

    登录进MySQL终端，使用db_lab3数据库，`source backup.sql的路径`

- 配置依赖的环境：

  使用了conda创建虚拟环境：`conda env create -f db_lab3.yaml的路径`

- 启动后端，测试登录：

  ```zsh
  conda activate db_lab3	# 进入虚拟环境
  cd main.py所在文件夹
  python main.py
  ```

  打开浏览器，输入url：http://127.0.0.1:5000，进入登陆页面，相应输入信息后登录

  我这里遇到了一个小bug，解决方案如下：

  <img src="./figs/install3.png" alt="1" style="zoom:50%;" />

  <img src="./figs/install4.png" alt="1" style="zoom: 50%;" />

## 概述实验过程和效果展示

### 登陆页面

- 扒了一个觉得还不错的bootstrap登陆页面，效果如下

  <img src="./figs/login.png" alt="1" style="zoom: 33%;" />

- 登录失败时，会根据失败后返回错误的两种类型，提示对应消息

  - 数据库名称错误

    <img src="./figs/login_fail1.png" alt="1" style="zoom: 33%;" />

  - 用户名或密码错误

    <img src="./figs/login_fail2.png" alt="1" style="zoom:33%;" />

- 待实现checkbox打勾使用cookies“记住”

### 主页面

- 写了一个导航栏主页面，其中导航栏链接通过替换页面中的iframe内联框架实现页面之间的跳转；

- 主页面是数据库中所有表的count视图，同助教给的模板。

  <img src="./figs/home1.png" alt="1" style="zoom:33%;" />
  
- 在每个子页面引入脚本，使得子页面在加载时，能动态改变iframe的高度；同时子页面需要动态增加元素时，调用该函数以保证父页面iframe随时动态变化，脚本如下：

  <img src="./figs/home2.png" alt="1" style="zoom: 50%;" />

### 表格的附加功能

表单和按钮的样式也是从bootstrap的示例上扒下来的。

1. 实现了search得到的表单前面加上checkbox，使用checkbox来选择待操作的行，效果如下：

   <img src="./figs/additional_1-1.png" alt="1" style="zoom:33%;" />

   选中后会变样式

   <img src="./figs/additional_1-2.png" alt="1" style="zoom:33%;" />

   再次点击会取消选中。

2. 实现了双击使表单变成input块，用户可以修改表单内容，在此基础上进行增删改操作

   <img src="./figs/additional_2-1.png" alt="1" style="zoom: 33%;" />

3. 实现了点击按钮，为表单添加已选中的所有行的副本，用户可以基于已有数据快速编造(bushi)新数据；

   副本是只显示在前端的，并不改变后端数据，只有使用相应的增删改功能按钮后，才会相应改变后端数据；

   点击按钮前：

   <img src="./figs/additional_3-1.png" alt="1" style="zoom:33%;" />

   点击按钮后：

   <img src="./figs/additional_3-2.png" alt="1" style="zoom:33%;" />

### 客户管理

1. 删除

   - 点击删除后会提示确认信息：

     <img src="./figs/customer_del1.png" alt="1" style="zoom:33%;" />

     点击确认后，若删除成功，会提示消息

     <img src="./figs/customer_del2.png" alt="1" style="zoom:33%;" />

     点击确认后刷新页面，发现成功删除

     <img src="./figs/customer_del3.png" alt="1" style="zoom:33%;" />
     
     错误处理在最后统一展示

2. 插入

   原始页面：

   <img src="./figs/customer_insert1.png" alt="1" style="zoom:33%;" />

   增加副本并编辑，得到内容如下图：

   <img src="./figs/customer_insert2.png" alt="1" style="zoom:33%;" />

   点击插入，提示信息和插入后页面如下：

   <img src="./figs/customer_insert3.png" alt="1" style="zoom:33%;" />

   <img src="./figs/customer_insert4.png" alt="1" style="zoom:33%;" />

   <img src="./figs/customer_insert5.png" alt="1" style="zoom:33%;" />

   能看到插入成功。

3. 修改：

   先查询，将查询到的数据直接双击修改：

   <img src="./figs/customer_update1.png" alt="1" style="zoom: 33%;" />

   再点击修改选中行按钮提交修改后的数据。后端收到数据后与数据库交互，刷新界面显示修改成功：

   <img src="./figs/customer_update2.png" alt="1" style="zoom: 33%;" />

4. 查询：

   使用form进行post向后端传递数据，后端预处理后传递给数据库连接模块，再进行数据库交互。
   
   在input块中输入数据：
   
   <img src="./figs/customer_search1.png" alt="1" style="zoom: 33%;" />
   
   单击查询按钮后，成功查询：
   
   <img src="./figs/customer_search2.png" alt="1" style="zoom: 33%;" />

下面的账户管理页面和贷款管理页面与客户管理页面类似，不做过多展示。

### 账户管理

为了方便后端编写，对物理模型导出的sql语句稍作修改：

- 将关系“持有”删除，将其中的内容移至“账户”，相应设置外键；
- 删除支票账户和储蓄账户中的冗余内容；

将账户管理拆分成储蓄账户和支票账户两个页面，分开处理；

1. 开户

   数据一致性：判断初始余额是不是0，若不是0则需要相应更新支行资产

2. 销户

   数据一致性：判断销户前余额是否为0，若非0则需要在销户时结清

3. 修改：账户号、账户所在支行、账户类型、客户身份证号不允许修改

   数据一致性：判断是否修改了账户的余额，若修改了，则相应更新支行资产

4. 查询：

   认为查询不会影响“最近访问日期”。

### 贷款管理

同样为了方便后端编写，对物理模型导出的sql语句稍作修改：

- 删除了关系“借贷”表，将其中的数据“每项贷款对应的客户身份证号”加入“贷款”表，相应设置外键；
- 贷款的发放状态在查询时判断，这样就不需要在数据库内部处理数据一致性了。

下面为具体内容：

1. 增加贷款信息：

   通过贷款付款中相应元组个数与逐次支付信息比对，判断贷款当前状态。

2. 删除贷款信息：

   需要一并删除贷款的发放信息；通过贷款付款中相应元组个数与逐次支付信息比对，判断是否为“发放中状态”，若是则不允许删除并返回异常信息。

3. 查询贷款信息

4. 发放贷款：

   默认是平均发放贷款，即将贷款总额除以逐次支付信息，作为每次发放的额度；后续可能会改进这一点。

   贷款发放时相应修改银行资产，若银行剩余资产不足以支持此次发放，则不发放并返回异常信息。

### 支行业务统计

将统计页面分成三个子页面：按月、按季度、按年统计；

每个页面使用一个table展示统计的结果，以按月统计为例，统计表格如下：

<img src="./figs/statistic3.png" alt="1" style="zoom: 50%;" />

如图，最左侧是支行名称，右边列出该支行相应的按月统计数据；

统计使用的时间区间是能追溯到最早的时间到CURTDATE，后续可能会考虑增加一个可以拖动的进度条，用于选择进行展示的时间区间。

### 异常处理

最后实现的是每个页面的异常处理部分；

将按钮的事件绑定改成函数形式，在html页面中调用；传入回调函数作为绑定按钮事件的函数的参数，方便使用个性化的回调函数。

1. 查询和修改数据时，若输入有单引号，则替换为*，通过给input框绑定onkeyup事件实现

2. 能检测插入重复主键、待删除元组有外键约束，作为数据库交互时的异常进行处理

   <img src="./figs/exception1.png" alt="1" style="zoom:33%;" />

   <img src="./figs/exception2.png" alt="1" style="zoom:33%;" />

3. 需求中的特殊异常处理，如处于发放中状态的贷款记录不允许删除，在后端与数据库交互时，由自己实现的程序判断而不是由数据库捕获

   <img src="./figs/exception3.png" alt="1" style="zoom:33%;" />

4. 为了保持数据的一致性，自己手动设置并捕获一些异常：

   比如与支行资产相关的，在修改账户余额、发放贷款时，都涉及支行资产的修改；此时若支行当前资产不足以完成操作，则不会进行操作，返回异常

   <img src="./figs/exception4.png" alt="1" style="zoom:33%;" />

5. 尚不能检测“修改不存在的元组”、“删除不存在的元组”

## 系统总体设计

### 模块结构

1. 前端：

   - css：

     套了个bootstrap框架，自己写or扒了少许样式如导航栏、登陆界面、表格样式。

   - js：

     主要采用bootstrap框架的bootstrap.min.js和jQuery的jquery.min.js，自己也写了几个脚本方便使用和数据交互：

     - autohidenavbar.js：用着玩的，主要是尝试一下侧边单击显示/隐藏的侧边栏

     - button.js：自己写的按钮事件绑定，包括添加选中行副本按钮、插入按钮、更新按钮、删除按钮；贷款发放按钮我是单独放在HTML内部，没有作为外部脚本引入。

       ```javascript
       function get_checkeddata(tab) {
         //获取本页面id为tab的表格中checkbox打勾的行的数据
       }
       function post_json_to_server(postdata, succfunc) {
         //将json数据postdata用post方法提交到server的当前页面
         //并接收server传回的回调数据并自动转成js对象，供回调函数succfunc处理
       }
       function addTr(tab) {
         //向id为tab的表的最后一行后添加checkbox选中的所有行的副本
       }
       $(document).ready(function () {
         //添加行按钮的响应时间绑定，点击按钮为指定表添加选中的所有行的副本
         $("#newlineBtn").click(function () {
           addTr("search-table");
           IFrameResize();
         });
       });
       //按钮事件绑定函数
       function insertBtn_event(reactfunction) {
         //插入按钮的响应事件绑定，点击按钮插入选中的行
         $("#insertBtn").click(function () {
           if (confirm("确认要插入已经选择的行吗？")) {
             var checkeddata = get_checkeddata("search-table");
             if (checkeddata.length == 0) return;
             post_json_to_server(
               JSON.stringify({
                 //提交给服务器的数据
                 //JSON.stringify()自动将中文转译为unicode编码，注意！！！
                 inputdata: checkeddata,
                 function: "insert",
               }),
               reactfunction
             );
           }
         });
       }
       function updateBtn_event(reactfunction) {
         //修改按钮的响应事件绑定，点击按钮修改选中的行
       }
       function deleteBtn_event(reactfunction) {
         //删除按钮的响应事件绑定，点击按钮删除选中的行
       }
       ```

     - iframeheight.js：根据子页面（框架）的高度，动态调整父页面iframe高度的函数

       ```javascript
       //动态修改父页面iframe高度的函数
       function IFrameResize() {
         // alert(this.document.body.scrollHeight); //弹出当前页面的高度
         var obj = parent.document.getElementById("iframe");
         //取得父页面IFrame对象
         //alert(obj.height); //弹出父页面中IFrame中设置的高度
         obj.height = this.document.body.scrollHeight; //调整父页面中IFrame的高度为此页面的高度
       }
       // 绑定子页面窗口大小改变事件？
       // $('.table').resize(IFrameResize());
       // 尝试了各种事件，都无法监听页面高度变化。故每次涉及到高度变化的事件，就调用上面的函数
       ```

     - sidebar.js：侧边栏脚本

     - table.js：自己写的表格事件绑定，有一些方便用户操作的设计，如单击选中表格行数据、双击将表格元素变成input块

       ```javascript
       //双击编辑表格
       $(document).ready(function () {
         $(document)
           //为了使新增加的元素依旧适用绑定的事件，使用on绑定事件
           .on("dblclick", "table td", function () {
             if (!$(this).is(".input")) {
               $(this)
                 .addClass("input")
                 .html('<input type="text" value="' + $(this).text() + '" onkeyup="' + "value=value.replace(/[\']/,'*')" + '" />')
                 .find("input")
                 .focus()
                 .blur(function () {
                   $(this).parent().removeClass("input").html($(this).val());
                 });
             }
           });
         //后续可以考虑增加focus时全选、CTRL+ENTER时blur
       });
       //单击选择表格一行checkbox，鼠标悬停改变未选中行的样式
       //除了表头（第一行）以外所有的行添加click事件.
       $(document).ready(function () {
         $(document).on("click", "table tr", function () {
           // 找到checkbox对象
           var chks = $("input[type='checkbox']", this);
           if (chks.length == 0)
             //如果没有，则代表是表头
             return;
           if (chks.prop("checked")) {
             // 之前已选中，设置为未选中
             $(this).removeClass("selected"); //切换样式
             chks.prop("checked", false);
           } else {
             // 之前未选中，设置为选中
             $(this).addClass("selected");
             chks.prop("checked", true);
           }
         });
       });
       ```

   - html：

     - 一个home.heml主页面，包含导航栏和iframe；

     - 6个子页面account_checking.html、account_saving.html、customer.html、loan.html、statistic.html、table.html

       子页面中主要包含按钮、表单、表格，用户通过表单输入数据进行查询，前端将返回的数据显示在表格中，用户基于已有数据，进行增删改；

     - 登陆页面login.html、login_fail.heml。

2. 后端：

   - util.py：有用的小函数

     ```python
     def GetBetweenMonth(start, end):
         '''获取从start开始到end之间的所有的年份-月份；start传入的是datetime类型，返回的是datetime的list'''
     def GetBetweenQuarter(start, end):
         '''获取从start开始到end之间的所有的年份-季度；start传入的是datetime类型，返回的是datetime的list'''
     def GetBetweenYear(start, end):
         '''获取从start开始到end之间的所有的年份；start传入的是datetime类型，返回的是datetime的list'''
     ```

   - db.py：数据库交互类

     ```python
     class MyDefSQL:
         '''自定义python-MySQL连接类'''
         def __init__(self, user, passwd, server_addr, dbname):
             '''初始化'''
             self.user = user
             self.passwd = passwd
             self.server_addr = server_addr
             self.dbname = dbname
         def login(self):
             '''打开数据库连接'''
         def execute(self, sql):
             '''执行一条语句sql'''
         def execute_all(self, sqls):
             '''执行一组语句sql'''
         def call_proc(self, *args):
             '''执行创建好的存储过程'''
     
         # 业务逻辑部分
         # table
         def showtablecnt(self):
             '''主页面展示各table的rowcount'''
     
         # customer
         def showcustomer(self):
             '''用户管理'''
         def customer_insert(self, data):
             '''单条用户相关信息插入，data是dict型的'''
         def customer_update(self, data):
             '''单条用户相关信息修改，data是dict型的'''
         def customer_del(self, data):
             '''单条用户相关信息删除，data是dict型的'''
         def customer_search(self, searchinfo):
     
         # account，涉及多个表，故采用组合语句的方式
         def showaccount(self, issaving):
             '''账户管理，issaving为True表明是储蓄账户'''
         def account_insert(self, data, issaving):
             '''单账户开户，data是dict型的；涉及多个表操作互相影响，故需要组合查询'''
         def account_update(self, data, issaving):
             '''单账户相关信息修改，data是dict型的；涉及多个表操作互相影响，故需要组合执行'''
         def account_del(self, data, issaving):
             '''单账户相关信息删除，data是dict型的；涉及多个表操作互相影响，故需要组合执行'''
         def account_search(self, searchinfo, issaving):
     
         # 贷款管理
         def showloan(self):
             '''贷款管理'''
         def loan_insert(self, data):
             '''单条贷款相关信息插入，data是dict型的'''
         def loan_release(self, data):
             '''单条贷款发放'''
         def loan_del(self, data):
             '''单条贷款相关信息删除，data是dict型的'''
         def loan_search(self, searchinfo):
     
         # 业务统计
         def statistic_month(self):
             '''返回业务的统计信息，返回dict型，基本全是后端处理；按月'''
         def statistic_quarter(self):
             '''返回业务的统计信息，返回dict型，基本全是后端处理；按季度'''
         def statistic_year(self):
             '''返回业务的统计信息，返回dict型，基本全是后端处理；按年'''
         def __reduce__(self):
             '''关闭连接'''
     ```

   - main.py：flask app构建