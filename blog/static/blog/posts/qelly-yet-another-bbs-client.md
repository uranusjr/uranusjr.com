[Qelly](https://github.com/uranusjr/Qelly) 1.0 alpha 版發佈！可以從[這裡](https://github.com/uranusjr/Qelly/releases)找到 Windows binary 載點。

Qelly (發音同英文名 Kelly) 是我最近在玩的 BBS client project。本來是我等當兵的時候 (2011) 無聊寫的東西，最近因為常用 Windows 覺得 PCMan 不合用才挖出來繼續，一些功能補完之後現在基本上告一個段落了，所以拿出來分享一下<strike>順便拐測試員</strike>。

不用安裝，沒有 (Windows) registry，只會在你的個人資料夾裡放三個文字檔儲存資料 (見文末說明)。除了 Windows 外的其他平台基本上只要能編 Qt 大概都能自己編 dependency 和本體，有興趣的也可以自己編來玩，我測過用 Qt 4 或 5 都可以，只是要注意 LibQxt 用的 Qt 版本要相符。
<!--more-->
主要特點:

* 應用程式快捷鍵全部都是 Alt 導向 (Mac 除外)，例如

	- 複製 -> Alt+C
  - 貼上 -> Alt+V
  - 移到網址列 -> Alt+L
  - 加入書籤 -> Alt+D
  
  所以不用特別背一組 (很難按的) 快捷鍵，而是可以真正活用鍵盤

* 純文字與 ASCII color 複製功能做在一起，方便 copy-paste (從 Nally 抄來的)

* 在編輯文章時按住 Alt (或 Cmd) 點滑鼠左鍵可以直接跳到文章特定位置 (同樣從 Nally 抄來的)

* 中英文字型與畫面大小通通都可以分開設定，你可以調出你最喜歡的組合。再也不用盯著醜不拉基的細明體或標楷體英文字型 (仍然是抄 Nally)

* 幾何圖形是直接畫出來的，不是特殊字元，所以 ASCII art 再也不會因為字型而破得亂七八糟。讓你可以有更多的字型選擇 (還是抄的...)

* 自動開燈 (抄很大抄不用錢)

* 站台管理員與常用符號表

* 自動網址偵測

* 選取字串後右鍵: Google 搜尋，自動短網址偵測 (PTT 主流的短網址和縮碼應該都可以，有缺可以回報)。比較特別的是可以一次選很多個網址後右鍵通通開啟，雖然還是比不上好讀版不過已經差不多了。

* 設定 Plink (Windows) 或 OpenSSH (Linux/OS X) 路徑後可以使用 SSH 連線!!

附個精美 ASCII art 截圖與 PCMan 對照組比較 (Windows 8，Qelly 是用 Consolas 和微軟正黑體，PCMan 是細明體)
http://d.pr/i/yR35
http://d.pr/i/GF53   PCMan 對照組

如果有任何軟體上的問題，可以到 Issues 區塊直接提出。雖然上面都是英文不過你 issue 內容寫中文也 OK 的。

未來除了中文翻譯之外，考慮直接用 OpenSSH (在 Windows 上) 實作 SSH client。也有打算做類似好讀版的東西，不過目前還在想要怎麼排版比較好──有任何建議歡迎提出。

不過我不打算做網頁 BBS 二合一的合體獸 (像 PCMan Combo 之類的東西)。如果你真的不想 BBS 與網頁瀏覽器分開，請找別家謝謝...

Enjoy!

> 如果你真的有系統潔癖，會用到的設定檔是 (在我的 Windows 8 上)
>	主要設定：`AppData\Roaming\uranusjr.org\qelly.ini`
> 表情符號列表：`AppData\Local\Qelly\emoticons.json`
> 站台列表：`AppData\Local\Qelly\sites.json`
> Windows XP 路徑會不一樣，不過我沒有 XP 機懶得測，應該不會很難找