
### django中如果启用django.middleware.csrf.CsrfViewMiddleware，所有的post请求都需要添加csrftoken才可以正常发送

1. 获取cookie中的token

```angular2html
// 获取csrftoken，解决403跨域问题
        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                let cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    let cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        let csrftoken = getCookie('csrftoken');
        console.log("csrftoken is:"+csrftoken)
```

2. ajax请求头中，添加X-CSRFToken
```angular2html
$.ajax({
                  type: "POST",
                  url: "/interface/debug/",
                  data: {name: name, url: url, method: method, type: type, header: header, parameter: parameter},
                  async: true,
                  beforeSend: function (xhr, settings) {
                    xhr.setRequestHeader('X-CSRFToken', csrftoken)
                    },
                  success: function (data) {
                      $("#result").val(data);
                  },
                  //=================== error============
                  error: function (jqXHR, textStatus, err) {
                        // jqXHR: jQuery增强的xhr
                        // textStatus: 请求完成状态
                        // err: 底层通过throw抛出的异常对象，值与错误类型有关
                        console.log(arguments);
                  }

              });
```