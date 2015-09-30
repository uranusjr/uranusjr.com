在[上一篇文章](http://uranusjr.com/blog/post/2/write-python-3-codes-that-run-on-the-python-2-interpreter-2/)結束時，我們已經可以完全靠自己寫出部份的 Python 2 與 3 語法相容。但是如果語法使用的 tokens，例如關鍵字、符號等互相衝突，就不可能有語法上對等的折衷解。幸好，Python 提供了良好的向前相容工具，讓我們可以自由在新、舊版之間切換。

## `2to3`

[`2to3`](http://docs.python.org/2/library/2to3.html) 是 Python 官方提供的一個小程式，功能就像名稱顯示的一樣，可以將你已經寫好的 Python 2 script 自動轉換成 Python 3 script，或者在發現無法自動修正的邏輯時提示你。如果你已經有一個不相容 Python 3 的 Python 2 程式，但是不想手動改寫，可以試試看這個小工具。`2to3` 可能會產生不相容於 Python 2 的語法，所以如果你想要達到雙面相容，還是需要手動檢查（比較好的方法是利用單元測試），不過這個小工具仍然是不錯的起點。

## `future_builtins`

我們曾經提過，Python 3 把一些內建函式的 interface 換掉了。這些修改有時候可以被繞開，但其他則會有點麻煩。所以 Python 提供了 [`future_builtins`](http://docs.python.org/2/library/future_builtins.html) 讓工作簡單一些。

例如，你原本在 Python 2 會寫

```python
from itertools import izip

foo = ( ... a very long iterable ... )
bar = ( ... another very long iterable ... )
zipped = izip(foo, bar)
```

在 Python 3，因為內建的 `zip` 就是接受 iterables，`itertools.izip` 消失，所以你要寫

```python
foo = ( ... a very long iterable ... )
bar = ( ... another very long iterable ... )
zipped = zip(foo, bar)
```

如果你要同時相容兩種狀況，就會變成這種東西：

```python
import itertools

# 如果有 izip 就用, 否則 fallback 到內建 zip
zip = getattr(itertools, 'izip', zip)

foo = ( ... a very long iterable ... )
bar = ( ... another very long iterable ... )
zipped = zip(foo, bar)
```

實在不是很直觀。有了 `future_builtins`，就可以寫得比較漂亮：

```python
try:
    from future_builtins import zip
except ImportError:		# 代表已經在 Python 3
    pass

foo = ( ... a very long iterable ... )
bar = ( ... another very long iterable ... )
zipped = zip(foo, bar)
```

下面是個對照表：

<table class="table">
<thead>
  <tr><th><code>future_builtins</code></th><th>Python 2</th><th>Python 3</th></tr>
</thead>
<tbody>
  <tr><th><code>ascii</code></th><td><code>repr</code></td><td><code>ascii</code></td></tr>
  <tr><th><code>filter</code></th><td><code>itertools.ifilter</code></td><td><code>filter</code></td></tr>
  <tr><th><code>hex</code></th><td colspan="2"><strong>(註)</strong></td></tr>
  <tr><th><code>map</code></th><td><code>itertools.imap</code></td><td><code>map</code></td></tr>
  <tr><th><code>oct</code></th><td colspan="2"><strong>(註)</strong></td></tr>
  <tr><th><code>zip</code></th><td><code>itertools.izip</code></td><td><code>zip</code></td></tr>
</tbody>
</table>

其中 `hex` 和 `oct` 比較特殊一點。在 Python 2 中，當你呼叫內建的 `hex` 或 `oct` 時，Python 會呼叫 callee 的 magic methods `__hex__` 或 `__oct__`，以獲得一個**字串值**。Python 3 廢除了這兩個 magic methods，而改呼叫 `__index__` magic method 獲得一個整數，然後再用內建的整數格式化產生十六或八進位表示法。如果你用了這個 function，在建立自訂型別時，就不用費心去維護相容性：

```python
class Answer(object):
    def __oct__(self):
        return '052'
    def __hex__(self):
        return '0x2a'
    def __index__(self):
        return 42
```

而只要一個 method 就搞定！

```python
class Answer(object):
    def __index__(self):
        return 42
```

## `__future__`

[`__future__` 模組](http://docs.python.org/2/library/__future__.html)是 Python 用來處理向前相容的最主要模組。當某個功能性 PEP 被接受時，如果這個功能的語法會影響到既有的程式，則 Python 會先把它放進 `__future__` 模組，讓使用者知道新功能的存在，並逐步改寫自己的程式，以便在未來新寫法正式被納入標準庫時可以無痛轉換。會造成不相容問題的 `__future__` 成員包括：

* `division`：除法自動浮點數轉換
* `print_function`：`print` 成為函數，而非 statement
* `unicode_literals`：字串字面值產生 Unicode string 而非 byte string。

用法是 `from __future__ import <feature to import>`。

### `print`

廢話這麼久還沒講到這個，應該有人已經在不爽了吧？XD

Python 3 讓 `print` 成為 function，所以原本的 `print 'something'` 語法不再合法。這應該是很多人無法順利轉換的最大原因。事實上，即使沒有額外輔助，也可以一定程度繞過這個差異，因為在 Python 2 上

```python
>>> print('something')
something
>>>
```

也是完全可以動！對 Python 2 而言這裡的括弧有加沒加都一樣，不影響 `print` 獲得的參數。

但是有一點要注意：

```python
# Python 3
>>> print()

>>>
```

可是

```python
# Python 2
>>> print()
()
>>>
```

呃，Python 2 會把上面這行解讀成印出 `()`，也就是一個空 tuple。同樣地：

```python
# Python 3
>>> print(1, 2, 3)
1 2 3
>>>
```

但是

```python
# Python 2
>>> print(1, 2, 3)
(1, 2, 3)
>>>
```

這就是 `print_statement` feature 出場的時候了。當你 import 這個 feature 之後，Python 會把 `print` 從 statement 中剔除，讓 parser 把 `print` 視為和 Python 3 一樣的函數（`print` 函數的定義內建於 Python 2.6 以上的所有版本，只是在 Python 2 預設狀況下會被 `print` statement 屏蔽）。所以

```python
>>> from __future__ import print_function
>>> print(1, 2, 3)
1 2 3
>>> print('foo', 'bar', sep=', ')
foo, bar
>>>
```

Hooray!

這篇到現在已經有點太長了。在下一篇中，我會討論另一個很重要的 future feature：`unicode_literal`。下次見！