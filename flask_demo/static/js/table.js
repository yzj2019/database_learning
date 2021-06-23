//双击编辑表格
$(document).ready(function () {
  $(document)
    //为了使新增加的元素依旧适用绑定的事件，使用on绑定事件
    .on("dblclick", "#search-table td", function () {
      if (!$(this).is(".input")) {
        $(this)
          .addClass("input")
          .html('<input type="text" value="' + $(this).text() + '" />')
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
  $(document).on("click", "#search-table tr", function () {
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

/*
$(function () {
            //鼠标悬停改变未选中行的样式
            $('tr').hover(
                function () {
                    // 找到checkbox对象
                    var chks = $("input[type='checkbox']", this);
                    if (!chks.prop("checked")) {
                        // 之前未选中，鼠标悬停时可改变样式
                        $(this).addClass("hover");    //切换样式
                    }
                },
                function () {
                    // 找到checkbox对象
                    var chks = $("input[type='checkbox']", this);
                    if (!chks.prop("checked")) {
                        // 之前未选中，鼠标悬停时可改变样式
                        $(this).removeClass("hover");    //切换样式
                    }
                }
            );
        });
 */
