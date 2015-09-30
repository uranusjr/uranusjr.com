本篇為[《輕鬆管理你的影片，如同管理你的音樂》](http://uranusjr.twbbs.org/2009/06/manage-your-vids-easily-as-your-music/)之續篇。

上次我試著利用 Perian 的功能，繞過 iTunes 的檔案格式辨認，以在 iTunes 裡整理影片。但很快我就遇到另一個問題：iTunes 的影片控制功能有夠爛，而且沒辦法一次顯示超過一個視訊視窗（即使你選擇「在獨立視窗內顯示」）；跟 Spaces 的整合也很糟，雖然視訊視窗可以跨桌面移動，但是只要一進入全螢幕就會回到和 iTunes 相同的桌面上。除此之外，我之前就習慣在 QuickTime 裡用滾輪來 navigate（不知道中文要怎麼翻），現在 iTunes 裡辦不到，一整個綁手綁腳。

iTunes 的右鍵選單裡有個功能是「顯示於 Finder」，可以顯示該 entry 的原檔案。所以我的第一個想法是更進一步，能不能多加進一個右鍵選單項目，用來執行「以 QuickTime 開啟」。不過這一下就碰壁了，因為 iTunes 並不像 Finder 本身有寫進去這種功能，而我又不會寫 iTunes 的外掛…（這建立在 iTunes 可以加外掛的前提上，而如果我沒記錯，iTunes 好像還是 Carbon 程式所以不太容易辦到…）

總之此路不通，所以我又回頭來找 AppleScript 解決方案 — Script Menu。

這東西歷史也很久了，簡單來說就是在 Menu Bar 右邊多放一個下拉選單的圖示，以快速找到工序指令來執行。我的第一台蘋果是 12" iBook，那個 Menu Bar 連應用程式選單都快放不下，何況右邊的圖示（當初我是連 Spotlight 都想盡辦法幹掉呢），所以從來沒想過要用這個選單，雖然從一開始就覺得好像有點用。

離題了。總之這年頭電腦都寬螢幕，應該不會再有我當初的問題，所以我們去打開 /Applications/AppleScript/AppleScript Utility.app

![](/media/blog/itunes-quicktime/applescript-utility-path.png)

勾選「在選單列顯示工序指令選單」，選單列右側就會出現一個黑黑彎彎的工序指令選單圖示 <span>![](/media/blog/itunes-quicktime/script-menu-icon.png)</span>。

我個人覺得內建的工序指令很雞肋，所以下面那個「顯示電腦的工序指令」是沒勾，不過你可以比較看看兩種的差別。所謂「電腦工序指令」是指放在 /Library/Scriipts/ 裡面的檔案，而「使用者工序指令」則放在 ~/Library/Scripts。下面關於應用程式工序指令的位置，我建議先放在頂部。

我個人覺得內建的工序指令很雞肋，所以下面那個「顯示電腦的工序指令」是沒勾，不過你可以比較看看兩種的差別。所謂「電腦工序指令」是指放在 /Library/Scriipts/ 裡面的檔案，而「使用者工序指令」則放在 ~/Library/Scripts。下面關於應用程式工序指令的位置，我建議先放在頂部。

我個人覺得內建的工序指令很雞肋，所以下面那個「顯示電腦的工序指令」是沒勾，不過你可以比較看看兩種的差別。所謂「電腦工序指令」是指放在 /Library/Scriipts/ 裡面的檔案，而「使用者工序指令」則放在 ~/Library/Scripts。下面關於應用程式工序指令的位置，我建議先放在頂部。

接著我寫了一個 [Open with QuickTime.scpt](/media/blog/itunes-quicktime/Open%20with%20QuickTime.scpt)：

```applescript
tell application "iTunes"
    set theLength to length of (selection as list)
    set theTrack to the location of selection
end tell

if theLength is 1 then
    tell application "QuickTime Player"
        activate
        open theTrack
    end tell
end if
```

放到 ~/Library/Scripts/Applications/iTunes/ 裡面（簡單的作法：按工序指令選單圖示 > 打開使用者 Scripts 檔案夾；創一個 Applications 檔案夾，裡面再創一個 iTunes 檔案夾，然後把這個檔案放進去）。

![](/media/blog/itunes-quicktime/itunes-script-menu.png)

這樣就完成了。去 iTunes 選取（單擊，不用打開）你想看的影片，然後點選工序指令選單，就會發現裡面多了一個分類「iTunes 工序指令」，裡面包含我們剛剛創的 Open with QuickTime（副檔名不顯示）。按下去，就會開啟一個新的 QuickTime Player 視窗，播放剛剛選取的影片。

可以看到我的選單裡除了 iTunes 工序指令，還有一些其他的東西。如果你把檔案直接放在 ~/Library/Scripts/ 底下，這些東西就會被視為「全域」項目，也就是不論現在最前端的程式為何，都會出現在選單裡。如果在 Scripts 檔案夾裡放檔案夾，那麼在選單裡也會顯示為階層形式（除了系統設定的某些特定檔案夾會被隱藏，例如 Applications）。

另外以前[提過](http://uranusjr.twbbs.org/2009/02/briefly-on-folder-actions/)，檔案夾動作的工序指令也放在這裡（/Library/Scripts/Folder Action Scripts/ 和 ~/Library/Scripts/Folder Action Scripts/ 下面），但這些檔案同樣不會出現在選單裡，相當貼心。

--------

這個技巧也有其他用途，例如剛好今天有人問怎麼兩倍速播放 iTunes 裡的檔案，這也要呼叫 QuickTime 才辦得到，所以很適合。倍速播放的 AppleScript 指令是設定 `rate of (document)`，我把上面那個程式稍微改了一下，有需要同樣可以載回去（[2x playing.scpt](/media/blog/itunes-quicktime/2x%20playing.scpt)）。打開之後倒數第三行有個 2，那個是播放速率，改成你想要的倍數即可（可以有小數點，如果你想也可以多存幾個，分別寫 1.5 倍、兩倍、三倍等等）。同樣存檔之後放到老地方就能用。

另外，雖然這個選單叫 **Scripts** Menu，不過其實也能放一些其他的東西。例如如果你有一些常用的程式，但又覺得放 Dock 很擠不想用 Stacks，或者希望有階層，那也可以把那些程式的 aliases（替身）放到這裡，一樣會顯示。在 10.4 或更早這可能會更有用就是了（尤其 10.6 之後 Stacks 也會有階層）。

如果還有興趣再更加強 iTunes，或者需要一些客製化的功能，可以參考 [Doug's AppleScripts for iTunes](http://dougscripts.com/itunes/) 網站，那邊蒐集了不少好東西。若你有興趣學習 AppleScript，這個網站作為起點也不壞（雖然我還是建議從看書開始）。

關於 iTunes 和 Scripts Menu 的話題還可以繼續，如果有空，可能還會再寫個兩篇吧。不過要多久才寫出來，這我就不能保證了…XD