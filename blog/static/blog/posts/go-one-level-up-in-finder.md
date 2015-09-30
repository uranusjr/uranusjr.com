昨天為了藍牙耳機寫了一個切換輸出設備的 AppleScript，驅動系統偏好設定的面板。

因為系統偏好設定面板沒有 AppleScript 指令可以用（這件事本身有點詭異，不過事實如此），所以只好用 System Events 來寫。程式本身是沒什麼問題，不過寫完之後我突然想起前陣子看到的這篇，所以就回去看了一下。

程式本身當然沒問題，不過有幾件事情要澄清一下。System Events 是 AppleScript 的基礎，所以其實這絕對不是 10.5 的新東西，而是從 AppleScript 剛出現時就一直存在。程式是 Leopard only 沒錯，但並非 System Events 本身，而是因為 Leopard 修改了其中的機制。

省略進一步的原理（反正不重要），其實這個作法可以很容易地改寫成 10.4 以下通用版本，只要在最前面加上一行

```applescript
tell application "Finder" to activate
```

就行了。在 10.4 以前這是所有 System Events 寫法的必要措施。

不過如果你實際測試（在 10.5 這個寫法仍然有用，不需要回到 10.4 以下執行），你會發現這個通用程式明顯較慢。當然這是 activate 指令的緣故。所以雖然理論上這個程式完全可以向下相容，不過我個人完全不建議這麼做。

關於中英文版本的問題，因為 localized name 的緣故，中英文系統（或應該說 Finder 的執行語系不同，畢竟這本來就可以分開設定）必須使用不同的工序指令。但其實有另外一個方法，可以繞過這個問題，就是這樣寫：

```applescript
tell menu bar 1
    tell menu bar item 6
        tell menu 1 to click menu item 3
    end tell
end tell
```

用數字編碼來避免命名。當然這個寫法的缺點就是，如果 10.6 把選單順序改了，那就要重新修改。

另外，如果你有仔細研究上面的程式碼，menu bar item 是這樣排列的（在現在的 Finder 上）：

1. 蘋果符號
2. Finder
3. 檔案
4. 編輯

依此類推。所以「前往」是第六個，不是第五個。



如果這樣結束似乎少了什麼？科科，其實這件事情從頭到尾就不用這麼麻煩，真的。可以看到「上層檔案夾」指令有個快捷鍵 ⌘↑（喝！盜圖！）：

[![](http://farm3.static.flickr.com/2280/3534771143_a49e57663b_o.png)](http://blog.yorkxin.org/posts/2009/05/16/finder-go-to-enclosing-folder/)

所以最 sick 的寫法其實是這樣：

```applescript
tell application "System Events"
    tell application "Finder" to activate
    keystroke up using {command down}
end tell
```

直接呼叫快捷鍵，然後就完了、結束、end、done、終わった。快捷鍵永遠比點選單要快多了啊，即使寫程式也不例外，哇哈哈哈哈～