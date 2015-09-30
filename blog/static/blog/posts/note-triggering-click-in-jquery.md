## 狀況
### Works

```javascript
    $('<button>foo</button>')
      .click(function() { alert('Foo!') })
      .click();
```

### Works

```javascript
    $('<a href="bar">go to bar</a>')
      .click(function(e) {
        e.preventDefault();
        alert($(this).attr('href'));
      })
      .click();
```

### *Does not work*

```javascript
    $('<a href="bar">go to bar</a>').click();
```

### Works!!

```javascript
    $('<a href="bar">go to bar</a>')[0].click();
```

## 說明

好，其實我也不知道為什麼...。根據 [Stack Overflow](http://stackoverflow.com/questions/5867370/) 的回答，jQuery 物件**只能觸發由 jQuery 創造的 click 事件**，所以像 `a` tag 的連結導向事件就沒辦法用，因為它不是 jQuery 物件上的事件。

如果想觸發 `a` tag 的點擊事件，就必須找到正確的物件——也就是那個 `a` tag 本身。`[0]` 取出包裹器中的單一 DOM 元素，使得 `click()` 不再作用於包裹器物件，而是 DOM 元素，因而觸發了瀏覽器點擊 `a` DOM 元素的事件。

感謝 [Stevanicus 的回答](http://stackoverflow.com/questions/773639/)。順帶一題，雖然那個回答下面有人說 Safari 不能用，不過我實測（Safari 6.0.5, OS X 10.8.4）的結果是可以的。