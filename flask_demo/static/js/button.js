function get_checkeddata(tab) {
  //获取本页面中checkbox打勾的行的数据
  var a = $("#" + tab).find("input[id='checkbox']:checked"); //获取id为tab的元素的子元素中，所有选中的复选框
  var data = new Array(); //所有checked行的数据
  if (a.length == 0) {
    alert("尚未选中任何行！");
    return data;
  }
  //第一种方法：通过checked属性确定被选中的复选框的父节点，通过children[index]来取第index个子节点td的内容
  /** for(var i=0;i<a.length;i++){
      if(a[i].checked){
        var tddata=a[i].parentNode.parentNode.children[1].innerHTML;
        alert(tddata);
      }
    } **/
  //第二种方法：通过checked属性确定被选中的复选框的父节点，遍历父节点下所有的子节点td，当td的name等于某值时，获取该td下的内容
  for (var i = 0; i < a.length; i++) {
    var tr = a[i].parentNode.parentNode;
    var trdata = new Object(); //该行除了checkbox的数据
    $(tr)
      .find("td")
      .each(function () {
        if (this.getAttribute("name") != "checkbox") {
          trdata[this.getAttribute("name")] = this.innerHTML;
        }
      });
    data[data.length] = trdata;
    // alert(data[0]["客户身份证号"]);
  }
  return data;
}

function post_json_to_server(postdata, succfunc) {
  //将json数据postdata用post方法提交到server的当前页面
  //并接收server传回的回调数据并自动转成js对象，供回调函数succfunc处理
  $.ajax({
    //url: posturl, //访问地址--action地址，默认是当前页面
    type: "post", //提交方式
    dataType: "json",
    headers: {
      "Content-Type": "application/json;charset=utf-8",
    },
    contentType: "application/json; charset=utf-8",
    data: postdata,
    success: succfunc,
  });
}

function addTr(tab) {
  //向id为tab的表的最后一行后添加checkbox选中的所有行的副本
  //获取table最后一行 $("#tab tr:last")
  //获取table第一行 $("#tab tr").eq(0)
  //获取table倒数第二行 $("#tab tr").eq(-2)
  var table = $("#" + tab);
  var a = table.find("input[id='checkbox']:checked"); //获取id为tab的元素的子元素中，所有复选框
  if (a.length == 0) {
    alert("尚未选中任何行！");
    return data;
  }
  for (var i = 0; i < a.length; i++) {
    var tr = a[i].parentNode.parentNode; //checked复选框所在行
    table.append(tr.cloneNode(true)); //deepcopy复制并添加到table末尾
  }
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
  $("#updateBtn").click(function () {
    if (confirm("确认要修改已经选择的行吗？")) {
      var checkeddata = get_checkeddata("search-table");
      if (checkeddata.length == 0) return;
      post_json_to_server(
        JSON.stringify({
          //提交给服务器的数据
          inputdata: checkeddata,
          function: "update",
        }),
        reactfunction
      );
    }
  });
}

function deleteBtn_event(reactfunction) {
  //删除按钮的响应事件绑定，点击按钮删除选中的行
  $("#deleteBtn").click(function () {
    if (confirm("确认要删除已经选择的行吗？")) {
      var checkeddata = get_checkeddata("search-table");
      if (checkeddata.length == 0) return;
      post_json_to_server(
        JSON.stringify({
          //提交给服务器的数据
          inputdata: checkeddata,
          function: "delete",
        }),
        reactfunction
      );
    }
  });
}
