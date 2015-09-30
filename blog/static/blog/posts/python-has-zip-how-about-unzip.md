我們都知道 Pyhton 內建的 `zip` 函式可以將多個 lists 合成，這在需要同時 iterate 多個 lists 時很好用：

```python
    foo = (1, 2, 3, 4)
    bar = (5, 6, 7, 8)
    for f, b in zip(foo, bar):
        print f, b
```
        
會得到

    1, 5
    2, 6
    3, 7
    4, 8
    
可是如果我們今天想做的事情相反，是要把一個 list 裡的每個項目拆開，要怎麼辦？也就是說，如果

```python
   baz = ((1, 2), (3, 4), (5, 6), (7, 8))
```

有沒有 `unzip` 使得

```python
    rex, blah = unzip(baz)
    print rex
    print blah
```

能得到

    (1, 3, 5, 7)
    (2, 4, 6, 8)
   
的結果？

答案是有，而且很容易就能找到，如果你 [RTFM]。

> zip() in conjunction with the * operator can be used to unzip a list

所以只要這樣就能搞定了！

```python
    baz = ((1, 2), (3, 4), (5, 6), (7, 8))
    rex, blah = zip(*baz)
```
    
如果仔細想想，這其實很合理。官方文件對 `zip` 的解釋如下：

> zip([iterable, ...])
> This function returns a list of tuples, where **the i-th tuple contains the i-th element from each of the argument sequences or iterables**.

(Emphasize mine.)

所以我們可以導出下面的規則：令 `a` 與 `b` 各為一 tuple，且 `b = zip(*a)`，則 `a[i][j] == b[j][i]`，其中 `i` 與 `j` 為整數， `i <= len(a)`，且對於 `0 <= i < len(a)`，`j <= len(a[i])`。

如果你把 `a` 與 `b` 想成矩陣，事實上這個運算就等同於轉置（transpose）的效果。在一開始的那個例子（一般的使用狀況）中，`a` 即為 `((1, 2, 3, 4), (5, 6, 7, 8))`，其轉置為 `((1, 5), (2, 6), (3, 7), (4, 8))`，拿來 iterate 後就會得到上面的結果。回憶高中數學，若 *A* 為矩陣，則

\\[
    (A^T)^T = A
\\]


所以當然 `zip` 會是自己的 inverse！

註：參數展開運算子（[* operator]）需要將傳入的 sequence/tuple 完全展開，才能進行運算，因此如果傳入值體積太大，可能會造成效能瓶頸。如果有這種大量運算需求，請考慮使用其他 iterator-based 的方案，甚至直接使用 numpy 的矩陣運算為佳。


[RTFM]: http://docs.python.org/2/library/functions.html#zip
[* operator]: http://docs.python.org/2/tutorial/controlflow.html#unpacking-argument-lists
