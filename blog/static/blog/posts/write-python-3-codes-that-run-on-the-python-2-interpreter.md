我前陣子在 Facebook 發了一個動態

![Six is good.](http://user-image.logdown.io/user/3184/blog/3218/post/168318/CXI0YAsnSqqdUM7SjxAJ_six_is_good.png)

然後 [Tim Hsu](https://www.facebook.com/wenchang.hsu) 就在下面留言表示想聽 [six](http://pythonhosted.org/six/) 的東西。six 是個好東西（很重要所以再說一遍），我不排斥分享一些心得，不過一來 six 很短，二來要準備 talk 很麻煩，三來沒什麼機會可以講，四來可能也沒有太多人想聽我講話，所以最後決定不如更新一下好久沒動的 blog。

可是還有一個問題：six 很短。如果光講它，這篇文章會沒什麼內容。所以不如就把主題定得廣一點，也會對比較多人有用。:)

<!-- more -->

## Python 3 Is Brilliant

Python 3 很棒。Python 3 是 [Guido 的真愛](https://www.dropbox.com/s/83ppa5iykqmr14z/Py2v3Hackers2013.pptx)。可是大家還是死守 Python 2.7，[最後的 Python 2](http://zh.wikipedia.org/wiki/Python#Python_3.0) 堡壘——為了第三方套件。「第三方套件無法支援」應該是絕大多數人無法順利轉移至 Python 3 的原因；直到現在，仍然有很多受歡迎的套件不支援 Python 3，包括：

* [wxPython](http://wxpython.org/)
* [py2exe](http://www.py2exe.org/)
* [Twisted](http://twistedmatrix.com/trac/)
* [PyGTK](http://www.pygtk.org/)
* [web2py](http://web2py.com/init/default/index)

可是 Python 3 真的很棒！它終於解決了惱人的 [Unicode 問題](http://pythonhosted.org/kitchen/unicode-frustrations.html)，大幅度修正命名慣例不一致的問題，更去除了一些原本因為向後相容性而存在的[潛在問題](http://python-history.blogspot.tw/2013/11/the-history-of-bool-true-and-false.html)。而且，雖然 Python 2.7 擁有[「延長維護期」特權](http://www.python.org/dev/peps/pep-0373/)，總有一天官方還是會放棄支援。與其到時候再大幅改寫我們的程式，不如及早開始「[向前相容](http://en.wikipedia.org/wiki/Forward_compatibility)」。

這篇文章的目的，就是要讓你可以寫出同時能在 Python 2 與 Python 3 順利執行的程式。你還是可以使用 Python 2 直譯器，所以不會有第三方套件不支援的煩惱；可是你會寫出完全合法的 Python 3 程式碼，所以也不必煩惱未來會不會需要額外維護！

## What's New in Python 3

首先，我們得先整理一下 Python 3 究竟有什麼與 Python 2 不相容的地方。Guido 在 2009 的[文章](http://docs.python.org/3.0/whatsnew/3.0.html)中有詳盡的整理。我把主要的項目列在下面：

1. `file` 內建型別被移至 `io` module 內（並改名）。
2. 許多原本回傳 `list` 的內建函式/方法改成回傳 iterator（官方的名稱是 *view*）。
3. `True`、`False` 與 `None` 成為保留字元。
4. 在捕捉 exception 時若想為該其賦名，必須使用 `as` 關鍵字（例如 `except TypeError as e`；舊寫法是 `except TypeError e`）。
5. 舊式類別被移除。所有自訂型別都必須繼承自一個型別。
6. 八進位字面值必須寫成 `0o10` 而非 `010`（語法錯誤）。
7. 整數除法必須使用 `//`，原本的 `/` 運算子會自動轉型至浮點數。
8. `print` 成為函式，而非 statement。
9. `str` 等同 Python 2 的 `unicode`；原本的 `str` 改名 `bytes`。`basestring` 被移除。
10. `long` 內建型別消失，統一為 `int` 且無上限值（與原本 `long` 的行為相同）。`sys.maxint` 常數移除。
11. Metaclass 語法修改。
12. 許多內建模組與型別被改名、合併、或者移除。

大概可以把這些項目分成三類：

1. 第 1. 至 6. 項。這些項目可以藉由建立良好的 coding style 達到語法上（syntactic）完全相容。某些狀況（例如 2.）其實在兩者間仍然有語意上（semantic）的差異，但可以用其他方式解決。
2. 第 7. 至 10. 項。這些項目可以藉由一些簡單的手段達到完全相容。
3. 其他。這些項目沒有簡單的方法可以處理——可是還是有方法。

所以以上所有的項目其實都有解！在下一篇文章中，我會把上面的項目走過一遍，說明要怎麼寫，才能同時符合 Python 2 與 Python 3 的語法。

## 更新

* [(2) 良好的 Coding Style](http://uranusjr.logdown.com/posts/2013/12/20/write-python-3-codes-that-run-on-the-python-2-interpreter-2)