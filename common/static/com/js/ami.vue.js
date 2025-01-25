Ami = function () {

  var ami = this;

  ami.emptyFunc = function () {};

  ami.initData = {};


  ami.close = function (value) {
    window.close();
  };

  ami.isEmpty = function (value) {

    if (typeof value === 'undefined')
      return true;

    if (value === null)
      return true;

    if (value === '')
      return true;

    if ($.isEmptyObject(value))
      return true;

    if (value instanceof jQuery && value.length === 0)
      return true;

    if ($.isArray(value) && value.length === 0)
      return true;

    return false;
  };

  ami.isDefined = function (value) {
    return typeof value !== 'undefined';
  };

  ami.isArray = ('isArray' in Array) ? Array.isArray : function (value) {
    return toString.call(value) === '[object Array]';
  };

  ami.isDate = function (value) {
    return toString.call(value) === '[object Date]';
  };

  ami.isObject = (toString.call(null) === '[object Object]') ?
    function (value) {
      // check ownerDocument here as well to exclude DOM nodes 
      return value !== null && value !== undefined && toString.call(value) === '[object Object]' && value.ownerDocument === undefined;
    } :
    function (value) {
      return toString.call(value) === '[object Object]';
    };


  ami.isString = function (value) {
    return typeof value === 'string';
  };

  ami.isBoolean = function (value) {
    return typeof value === 'boolean';
  };

  ami.isNumber = function (value) {
    return typeof value === 'number' && isFinite(value);
  };

  ami.applyIf = function (toObj, fromObj) {
    var key;

    if (!this.isObject(toObj)) {
      return {};
    }

    for (key in fromObj) {
      if (toObj[key] === undefined) {
        toObj[key] = fromObj[key];
      }
    }

    return toObj;
  };

  ami.apply = function (toObj, fromObj) {
    var key;

    if (!this.isObject(toObj)) {
      toObj = {};
    }

    for (key in fromObj) {
      toObj[key] = fromObj[key];
    }

    return toObj;
  };


  ami.encode = function (obj) {
    return JSON.stringify(obj);
  };


  ami.decode = function (json) {
    try {
      return JSON.parse(json);
    } catch (e) {
      return null;
    }
  };

  ami.copy = function (data) {
    var str = this.encode(data),
      model = this.decode(str);
    return model;
  };

  ami.isFunction = (typeof document !== 'undefined' && typeof document.getElementsByTagName('body') === 'function') ?
    function (value) {
      return !!value && toString.call(value) === '[object Function]';
    } : function (value) {
      return !!value && typeof value === 'function';
    };

  ami.info = {
    device: (function () {
      var nav = navigator.userAgent;

      if ((nav.indexOf('iPhone') > 0 && nav.indexOf('iPad') == -1) ||
        nav.indexOf('ipad') > 0 ||
        nav.indexOf('Android') > 0) {
        return 'smart';
      }
      return 'pc';
    }())
  };

  ami.appendParameters = function (url, params) {
    var urls,
      urlParams = "",
      newUrl = url;
    if (!this.isEmpty(params)) {

      $.each(params, function (key, value) {
        key = encodeURIComponent(key);
        value = encodeURIComponent(value);
        urlParams += '&' + key + "=" + value;
      });

      urls = url.split('?');
      if (urls.length > 1) {
        newUrl = url + urlParams;
      } else {
        newUrl = url + "?" + urlParams.substr(1);
      }
    }

    return newUrl;
  }

  return ami;
};

Vue.use({
  install: function (Vue, options) {
    // 1. グローバルメソッドまたはプロパティを追加
    Vue.myGlobalMethod = function () {
      // 何らかのロジック ...
    };

    Vue.$amiGlobalObjects = {};

    // 2. グローバルアセットを追加
    Vue.directive('my-directive', {
      bind(el, binding, vnode, oldVnode) {
        // 何らかのロジック ...
      }

    });
    // 3. 1つ、または複数のコンポーネントオプションを注入
    Vue.mixin({
      beforeCreate: function () {
        // var value = $('#__init__').val();
        if (this.$ami.isDefined(__init__))
          this.$ami.initData = __init__;
        else
          this.$ami.initData = {};
      },

      created: function () {
        // 何らかのロジック ...

      }

    });
    // 4. インスタンスメソッドを追加
    Vue.prototype.$myMethod = function (methodOptions) {
      // 何らかのロジック ...
    };

    Vue.prototype.$ami = new Ami();

    Vue.prototype.amiRowClassName = function ({
      row,
      rowIndex
    }) {
      if (rowIndex % 2 === 0) {
        return 'ami-odd-table-row';
      }
      return 'ami-even-table-row';
    };


    Vue.prototype.$amiEvnetBus = new Vue();

    Vue.prototype.$jq = $;


    /*
     *  连续请求时 loading对象等变量 互相独立的目的，利用闭包特性单独封装
     */
    var doPost = function (opt) {
      var loading = this.$loading({});
      this.$http.post(opt.url, opt.params, opt.options)
        .then(function (response) {
          var me = this,
            data = response.data;
          if (me.$ami.isDefined(data) && me.$ami.isDefined(data.result)) {
            if (data.result === "__success__") {
              //業務は正常に完了しました。
              opt.success.call(me, data, response);
              if (!me.$ami.isEmpty(data.msg)) {
                this.$message({
                  message: data.msg,
                  type: 'success'
                });
              }
              //me.$message.error('错了哦，这是一条错误消息');

              // this.$alert(response.data.msg, {
              //   confirmButtonText: '确定',
              //   callback: action => {
              //     this.$message({
              //       type: 'info',
              //       message: `action: ${action}`
              //     });
              //   }
              // });
            } else if (data.result === "__faulure__") {
              //業務上に失敗しました。
              opt.failure.call(me, response);

              if (!me.$ami.isEmpty(data.msg)) {
                this.$message.error(data.msg);
              }
            } else if (data.result === "__error__") {
              //業務上に予想外のエラーを起こしました。
              opt.failure.call(me, responseresponse);

              if (!me.$ami.isEmpty(data.msg)) {
                this.$message.error(data.msg);
              }
            }


          } else {
            opt.success.call(me, response);
          }
        })
        .catch(function (response) {
          var me = this;
          //timeout

          //回線問題で、接続できない
          opt.failure.call(me, response);
        })
        .finally(function () {
          var me = this;
          setTimeout(function () {
            loading.close();

          }, 100);
        });
    };

    var doJsonp = function (opt) {
      var loading = this.$loading({});

      this.$http.jsonp(opt.requestUrl, opt.params)
        .then(function (response) {
          var me = this;
          opt.success.call(me, response);
        })
        .catch(function () {
          var me = this;

        })
        .finally(function () {
          setTimeout(function () {
            loading.close();
          }, 100);
        });

    };

    Vue.prototype.ajax = function (settings) {
      var me = this,
        urls = [],
        opt = me.$ami.applyIf(settings, {
          url: '.',
          requestUrl: '.',
          type: 'post',
          params: {},
          urlParmas: {},
          comDepend: true,
          /*個別で処理したい場合、「success」「failure」「finally」を設定せずcomplete函数を利用する*/
          complete: me.$ami.emptyFunc,
          success: me.$ami.emptyFunc,
          failure: me.$ami.emptyFunc,
          finally: me.$ami.finally
        });

      //opt.params = new FormData(opt.params);
      opt.headers = settings.headers || {};
      var csrf = $("[name=csrfmiddlewaretoken]").val()
      if (!this.$ami.isEmpty(csrf)) {
        opt.headers['X-CSRFToken'] = csrf;
      }
      opt.options = {
        headers: opt.headers
      };
      if (!(opt.params instanceof FormData)) {
        opt.options['emulateJSON'] = true;
      }

      //Url追加
      // opt.requestUrl = opt.url;
      // if (!this.$ami.isEmpty(opt.urlParmas)) {
      //   urls = opt.url.split('?');
      //   if (urls.length > 1) {
      //     opt.requestUrl += urls[1];
      //   } else {
      //     opt.requestUrl += '?ami=auto';
      //   }


      //   $.each(opt.urlParmas, function (key, value) {
      //     key = encodeURIComponent(key);
      //     value = encodeURIComponent(value);
      //     opt.requestUrl += '&' + key + "=" + value;
      //   });
      // }
      opt.requestUrl = this.$ami.appendParameters(opt.url, opt.urlParams);

      switch (opt.type.toLowerCase()) {

        case 'jsonp':
          {
            doJsonp.call(this, opt);
          }
          break;
        case 'get':
          {

          }
          break;
        case 'post':
        default:
          {
            doPost.call(this, opt);
          }
          break;

      }

    };

    //Arrayからデータモデールを作成
    Array.prototype.getModel = function () {
      var me = this,
        ami = new Ami()
      if (me.length == 0) return {}

      var arrayStr = ami.encode(me[0]),
        model = ami.decode(arrayStr);
      $.each(model, function (key, value) {
        if (ami.isNumber(value)) {
          model[key] = 0;
        } else if (ami.isDate(value)) {
          model[key] = null;
        } else if (ami.isString(value)) {
          model[key] = "";
        } else if (ami.isBoolean(value)) {
          model[key] = false;
        } else if (ami.isObject(value)) {
          model[key] = null;
        } else {
          model[key] = null;
        }
      });
      return model;
    }

  }
});


var ami = new Ami()
