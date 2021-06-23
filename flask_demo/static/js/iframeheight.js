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
