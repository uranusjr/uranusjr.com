在[上一篇文章](http://uranusjr.logdown.com/posts/2013/12/20/write-python-3-codes-that-run-on-the-python-2-interpreter)結束前，我列出了 Python 3 與 Python 2 不相容的主要原因，並將它們分成三類：

1. 可以藉由建立 coding style 達到語法上（syntactic）完全相容。
2. 可以藉由簡單的手段達到完全相容。
3. 沒有簡單的方法可以處理。

在這篇文章中，我會討論第一種類型，也就是可以直接藉由良好的 coding style 解決的問題。Python 3 的很多新功能其實都有被 backport 回 Python 2.6 與 2.7。只要注意使用新的寫法，就可以解決很多 Python 3 的不相容問題。事實上， **即使你完全沒有用 Python 3 的打算，新寫法還是比較好**，因為它們通常更為清晰，也被大多數人所喜愛。

<!--more-->

## `file` 型別

在 Python 2 中，當你開啟一個檔案，獲得的 handle 就會屬於 `file` 內建型別。在最原始的 Python 風格中，開啟檔案的語法就是建構一個新的 `file` instance：

```python
    f = file('/path/to/a/file')
    # Do things with the file
    f.close()
```
    
但現在的 style 推薦使用內建的 `open` 函式，而不要直接呼叫 `file`。請把第一行改成

```python
    f = open('/path/to/a/file')
```

## 回傳 iterator 或 sequence 的函式

在很多狀況下，回傳 iterator 還是 sequence（`list` 或 `tuple` 等類別的 instance）其實沒有太大差異。如果你有個迴圈

```python
fruit_counts = {'apple': 4, 'orange': 6}

for fruit, count in fruit_counts.keys():
    # Do some things...
```

那麼不論 `keys` 回傳的是 `list`, iterator, *view* 還是什麼其他鬼東西，只要它是 iterable，其實都沒有關係。只要堅持在 Python 2 使用「無印」的版本（例如 `dict` 的 `keys`、`values`、`items`，以及內建的 `range` 等等），而不要用回傳 iterator 的「加強版」（`iterkeys`、`itervalues`、`iteritems`、`xrange` 等等），就可以保證轉移到 Python 3 時不會出錯（內部實作有變，因為改回傳 iterator，不過在語法上不影響）。

這不是萬全的解。如果你必須保證得到的是 sequence，那麼就要稍微注意：

```python
# 在 Python 2 是 list, 但 Python 3 是 iterator
counts1 = fruit_counts.values()

# 保證是 list
counts2 = list(counts1)
```

當然，這會影響效能。如果你必須在 Python 2 使用回傳 iterator 的函式，就需要額外的輔助。我們之後會再處理這個問題。

## 新的保留字元

在 Python 2 中，由於歷史因素，有些看起來像系統常數的名稱其實 **不是保留字**。這代表你在 Python 2 其實可以這樣胡搞：

```python
True = 0

if True:
    # 不會被執行！
    pass
```

Python 3 打破了向後相容，所以可以趁機把這些歷史遺毒清掉，使上面的程式變得不合法。但不論在什麼版本，你都不應該寫出這種東西，所以這基本上不是問題。

## 新的例外賦名語法

新的語法

```python
values = ['a']
try:
    integer_value = int(values[0])
except ValueError as e:
    log_error(e)
```

從 Python 2.6 就存在了，如果你現在尚未採用，請立刻修正。舊的語法

```python
values = ['a']
try:
    integer_value = int(values[0])
except ValueError, e:
    log_error(e)
```

在 Python 2 與上面的新語法完全對等，但是相對起來較不明確，而且容易和同時捕捉多種例外的語法搞混：

```python
values = ['a']
try:
    integer_value = int(values[0])
except (ValueError, IndexError):
    pass
```

所以無論如何，請避免使用舊語法，採用新的 `as` 關鍵字。

## 舊式類別被移除

舊式類別指的是沒有 parent class 的自訂型別，以及繼承這類類別的 child classes。例如：

```python
class MyClass:
    pass
```

這個語法從應該是 2.2 開始就被捨棄了，存活到今天純粹只是歷史因素。不論在任何狀況，請繼承自內建型別或其他自訂型別；如果你不知道要繼承什麼，請繼承 `object`：

```python
class MyClass(object):
    pass
```

新式類別[好處多多](https://wiki.python.org/moin/NewClassVsClassicClass)，不過兩者之間的差別不在本文範疇，請自行研究。:)

## 其他新語法，以及 Python 3 移除的舊語法

比起上面的項目，其他的語法修正其實不見得有其他好處，只是習慣問題。

以八進位整數為例，舊的語法承襲 C 的準則，在整數前加 `0` 代表八進位（所以 `012` 是十進位的 10）。為了清晰起見，Python 3 只接受 `0o`（一個零，然後一個小寫 o）前綴，所以 10 要寫成 `0o12`，舊寫法會拋出 `SyntaxError`。但是新寫法已經 backport 回 2.6 以上版本了，所以只要記得使用新寫法就不會有問題！

另一個比較常見的語法是 `b''` 字面值。在 Python 3 中，`''`字面值會產生一個 Unicode 文字物件（對應到 Python 2 的 `unicode`），所以原本的 8-bit byte array 物件（對應到 Python 2 `str`）就改用前綴 `b` 的標記。這個語法同樣有 backport 回 2.6 以上，所以如果你需要表示的是 encoded byte array 而非 text（在數據傳輸等應用上需要），可以盡量改用新寫法以避免語意模糊的問題。

另一方面，原本 Python 2 用來產生 Unicode literal 的語法 `u''` 在 Python 3.0 開始被刪除。但由於反彈聲浪過大，從 Python 3.3 起這個語法重新成為合法，在 Python 3 中產生 `str` 物件。如果你已經在處理 text contents 時使用 `u''`，很好，請繼續這麼做！

感謝 Python 核心社群在 backporting 上投注的心力，你只要稍微修正一些 coding convention，就可以在簡單的程式中完全相容 Python 3 與 Python 2.6/2.7。在下一篇中，我會介紹一些 Python「內建」的工具，讓其他基本功能也能雙面相容。字串型態在 Python 中是非常重要的型別，所以 Python 3 的字串型態修正影響非常大，所以也當然有內建的工具可以協助你處理。在下一篇中，也會回過頭來進一步討論字串型態相容性問題。