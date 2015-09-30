Qelly 1.0 alpha 2 發佈！感謝大家提供的問題回報和其他建議，很多東西如果沒有大家提出來我應該很難自己想到。

Windows binary 與原碼同樣由 GitHub 發佈，請至[發佈區](https://github.com/uranusjr/Qelly/releases)下載。新的功能已經著手進行中，目標是完成自動字型調整（[#45](https://github.com/uranusjr/Qelly/issues/45)），當然如果本版發佈後出現新的問題也會一併修正。

這個版本最重要修改是新增了許多人想要的「[可攜版](https://github.com/uranusjr/Qelly/issues/44)」功能。實作方法採用了 [@Wcw5504](https://github.com/Wcw5504) 的建議，當 Qelly 執行檔的相同目錄下存在一個名稱為 `PORTABLE` 的檔案（注意不可有副檔名）時，便會進入可攜模式。在可攜模式下，Qelly 的設定（含站台與表情符號）會存放於一個叫 `data` 的子目錄，而不是使用者的個人目錄。
<!--more-->
為了保持程式運行時的整體性，可攜模式的切換必須重新啟動 Qelly 才會生效。另外，由於可攜版在多使用者使用同一電腦時有資料共用的問題，於可攜和一般模式之間切換時，請自行將 Qelly 所需之資料檔移至對應位置；如果公在用電腦上使用，請多注意個人資訊安全。

**注意：**為了保持可攜模式與一般模式之間的相對路徑，我在新版本中把 `qelly.ini` 設定檔在一般模式下的位置移至與 `sites.json` 和 `emoticons.json` 相同的目錄。以 Windows 為例（詳見 [1.0a 的發佈文](http://uranusjr.logdown.com/posts/2013/10/04/qelly-yet-another-bbs-client)），原本放在 `AppData\Roaming\uranusjr.org\qelly.ini` 的檔案現在必須移至 `AppData\Local\Qelly\qelly.ini`。原本的使用者 **必須自行將 `qelly.ini` 檔移過去**。若造成不便，敬請見諒。

我這兩天主要在研究在 Qelly 本身直接實作 SSH 連線的功能，已經在概念上完成了。目前主要的問題是遇到經上游函式庫（LibQxt）的一些問題，目前[洽詢中](https://bitbucket.org/libqxt/libqxt/issue/55/qxtsshclient-stucks-if-the-ssh-host-does)，如果有解的話說不定在 1.0 正式版就可以改用新的實作。以後 Windows 就可以和大家一樣連 ssh://bbs@ptt.cc 不用繼續用弱弱的 telnet 了。新版 SSH 實作在 [ssh\_libqxt](https://github.com/uranusjr/Qelly/tree/ssh_libqxt) 這個 branch 上，不過需要不少苦工才能編出能用的版本，如果有人有興趣合作再另外討論。

以下是 1.0 alpha 2 的修改列表：

* 問題修正
	- 重新連線造成當機。
  - 勾選儲存連線時，重新啟動後無法重新連線。
  - 繪圖問題造成某些底色無法正確顯示。
  
* 新功能
	- 繁體中文翻譯。
  - goo.gl 短網址偵測。
  - 儲存工具列隱藏狀態。
  - 「可攜」模式。
  - 右鍵選單新增「貼上」項目。
  
* 改良
	- 新版本中 UI 相關的設定（字型、顏色等）可以立即看到畫面重繪，而不用重新連線。
	- 設定視窗新增了「套用」鍵，可以在不關閉視窗的情況下啟用新設定。配合前項修正十分方便。
  - 新增將 SSH 完全關閉的選項（預設為關閉）。如果不想要 SSH 功能，關閉後就不會看到警告視窗。
  
Enjoy!