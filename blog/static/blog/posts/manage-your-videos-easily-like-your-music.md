iTunes 是優秀的音樂管理軟體，尤其在 Mac 上。但身為一位阿宅，擁有一卡車影片也是相當合理，所以我一直想找到一個能像 iTunes 一樣，分門別類管理我的影片，而且方便搜尋、又能輕鬆收看的軟體。可是這還真是不簡單，我找了好久，免費的找了，要錢的找了（當然我只用了試用版，沒有真的砸錢下去），就是沒有一個軟體合用…

但最近我終於找到了符合我需求的對象。這個軟體的功能和 iTunes 一模一樣，也能做到我所有希望的功能：它能把影片依分類排列、依專輯以格狀顯示（重點）、編輯各種 tags、也能直接雙擊播放。

這個軟體免費，容易下載，方便使用，而且持續更新。

它就叫做 iTunes。

![](/media/blog/itunes-video/ivideo.png)

上面是廢話。不過找了一堆軟體的那段是真的，我找過好多地方，看到好多人和我有一樣的問題，最後還是發現答案其實一直都在我的電腦裡。

所以如果你曾經厭煩用檔案夾管理音樂，而愛上 iTunes 的整理法，那麼現在你也可以拋開檔案夾管理影片，用同樣的方法管理它們。

需求：

* 一台 Mac
* 新版本的 iTunes（我不確定要多高, 不過越高功能越適合管理影片是確定的）
* [Perian](http://perian.org/)

首先，iTunes 本來就能看影片，這應該沒問題。但 iTunes 可以播放的檔案相當少，主要是因為使用 QuickTime 核心，而 QuickTime 能播放的格式就那麼一點點。當然 Perian 可以大幅度擴充 QuickTime 的能力，但 iTunes 可能是為了避免錯誤，仍然限定如果影片格式不符合 QuickTime 內建的播放需求，就根本無法加入資料庫。

所以我們需要想個辦法矇騙 iTunes，讓它以為我們的影片是內建格式其中一種 — MOV 封裝。如果能唬過 iTunes 把影片加入資料庫，那麼 iTunes 就可以呼叫 QuickTime，然後由 QuickTime 呼叫 Perian 解碼，我們的影片就能在 iTunes 裡出現了。

MOV 封裝有個功能叫「參考影片」。一般的封裝都要把影像和音軌包在檔案裡面，但參考功能厲害的地方是，可以允許檔案的軌道非實體，而只是一個指向，有點像 alias（替身、捷徑…看你喜歡怎麼稱呼）的效果。不需把原本的軌道包進去，就可以讓指向檔變得很小（通常小於 2 MB），裡面包含的資訊也很少，大部分是標籤內容（影片名稱演出者之類的），但在播放時，只要呼叫原本的檔案（裡面的特定軌道）要求內容，這樣就可以播放出和原本一樣的資訊。

當然，這個東西 iTunes 會吃。所以我們只要把舊有的影片另存成參考影片，就可以餵進去了。

首先打開你的影片。

<p><a href="https://picasaweb.google.com/lh/photo/ATCOGT3-Nju4CXZX9Da9KkLNNXm9fiZNGPgajya8deI?feat=embedwebsite"><img src="https://lh6.googleusercontent.com/-5UHVvwXwgKU/SjT2TwKKL1I/AAAAAAAABow/hX7VdLWz0k4/s640/avi.png" height="427" width="640" /></a></p>

選擇「檔案 > 儲存為…」，另存為參考影片，

<p><a href="https://picasaweb.google.com/lh/photo/_0EYEjbXbsKds80eSTWlsELNNXm9fiZNGPgajya8deI?feat=embedwebsite"><img src="https://lh4.googleusercontent.com/-i7tU_XwcevQ/SjT2lhqBotI/AAAAAAAABpI/wwetcW7V8n8/s640/save-as.png" height="434" width="640" /></a></p>

就會看到多了一個小巧的 MOV 檔案。

播放起來也和原來一模一樣（注意副檔名是 .mov）：

<p><a href="https://picasaweb.google.com/lh/photo/3xrTA6qzh_TYu49QrL7DWkLNNXm9fiZNGPgajya8deI?feat=embedwebsite"><img src="https://lh3.googleusercontent.com/-Oo91dDOR6tY/SjT2YzSPubI/AAAAAAAABo0/bHP7YIbOI94/s640/mov.png" height="427" width="640" /></a></p>

這樣就完成一個檔案了！

當然很不錯，不過我的影片超過 300 GB（只計算可以大白天開著房門看的），這樣一個一個轉會升天，行不通。所以我寫了個 AppleScript 來加速作業，放在[這裡](http://uranusjr.com/media/blog/itunes-video/save-as-ref.zip)。解壓縮之後雙擊開啟，然後基本上直接按 Run（執行）就可以了。從跳出的視窗裡選擇檔案夾之後，會把所有檔案夾裡的 .avi 檔全部存成參考影片。

檔案裡還有一些細節，請參閱程式註解。另外，如果你想轉其他格式的影片，把有一段

    set theExt to ".avi"

的 .avi 改成你想要的，例如 .mkv 或之類就行了...切記前面要加「點」。轉換完的檔案會被放在 ~/Movies/iTunes Movies/ 底下。

順帶一題（因為有人在 PTT 推文提到我才想起來），必須要有 QuickTime 專業版才能把影片另存。但其實即使是標準版那些功能也還是在，只是選單按鈕被鎖住而已，所以用 AppleScript 就可以偷吃步繞過限制，誰都可以存檔。這事實上是個超級大密技，而且早在 QuickTime 出來的時候就已經存在（我是看 Adam Goldstein 的書知道的），蘋果根本從來沒打算堵起來，算是半公開的秘密。XD

言歸正傳。接著去 iTunes，把所有存好的檔丟進資料庫。嗯，不過結果似乎不太妙…

<p><a href="https://picasaweb.google.com/lh/photo/CWz5uCKeYfv3VmaXMg_NhELNNXm9fiZNGPgajya8deI?feat=embedwebsite"><img src="https://lh5.googleusercontent.com/-Aq7CuLlIM2U/SjT2bVxntYI/AAAAAAAABo4/1Jrr08bgA4w/s640/video.png" /></a></p>

每個檔案都獨立出來了，這樣一團亂的無法整理啊！難道不能像音樂一樣，以專輯為單位整理成一個圖示嗎？

嗯，答案是，影片真的沒有辦法那樣顯示。不過幸好，也不是只有音樂可以，所以改一下設定就行了。把剛剛丟進去的影片全選，打開簡介視窗，把「選項」裡的「媒體種類」改成「電視節目」：

<p><a href="https://picasaweb.google.com/lh/photo/MI9sa-EW3PIsajrQpOGy20LNNXm9fiZNGPgajya8deI?feat=embedwebsite"><img src="https://lh6.googleusercontent.com/-fbvFPywqRCg/SjT3OO31NKI/AAAAAAAABpM/m5fpCi1DYhI/s640/to-tv-shows.png" /></a></p>

等 iTunes 處理完，所有影片就會全部跑到「電視節目」下面。注意左上角，現在已經不是「影片」資料庫的畫面了。

<p><a href="https://picasaweb.google.com/lh/photo/3nvivx-hXNwXDt3c2jF5NkLNNXm9fiZNGPgajya8deI?feat=embedwebsite"><img src="https://lh4.googleusercontent.com/-wOtcGp-5tnA/SjT2egGFMXI/AAAAAAAABo8/aYiZCfKbyhU/s640/tv-shows.png" /></a></p>

不是一樣嗎？不不不，還沒完，同樣全選打開簡介視窗，輸入「專輯」名稱。（這是我的習慣，比較正確的方法應該是輸入「視訊」標籤裡的「節目」名稱。這兩種作法有微妙的不同，有興趣自己玩玩。）

<p><a href="https://picasaweb.google.com/lh/photo/CifhdfJ_4nji5WMMH-u4CkLNNXm9fiZNGPgajya8deI?feat=embedwebsite"><img src="https://lh4.googleusercontent.com/-6JxwVcbZBN8/SjT2fBRzdkI/AAAAAAAABpA/jHDqmZV0HGw/s640/album.png" /></a></p>

再等 iTunes 處理一下，所有影片就會被整理到一起了。

<p><a href="https://picasaweb.google.com/lh/photo/8qnZi2rQeGiAwRYsoz4CA0LNNXm9fiZNGPgajya8deI?feat=embedwebsite"><img src="https://lh5.googleusercontent.com/-0oQ-8T13mmY/SjVuKldlpkI/AAAAAAAABpY/ScswCr9q71E/s640/tv-shows2.png" /></a></p>

大功告成！喔當然，既然要用 iTunes，不編輯一下 tags 順便放個專輯圖片怎麼行呢？雙擊進去節目裡面，針對每一首和整體編輯一下吧。

<p><a href="https://picasaweb.google.com/lh/photo/mkSM6kmfCxRK8Qj47bjY_ELNNXm9fiZNGPgajya8deI?feat=embedwebsite"><img src="https://lh5.googleusercontent.com/-JkHmDqsm8Bs/SjVuJulNzJI/AAAAAAAABpU/ZyukWWm4Ik8/s640/kamichu.png" /></a></p>

-----

就這樣，又整理完一部影片了，不只可以在 iTunes 管理、收看、連外嵌字幕都有呢（歸功於 Perian）！

<p><a href="https://picasaweb.google.com/lh/photo/WFgweeO5icPRqKokXStDiULNNXm9fiZNGPgajya8deI?feat=embedwebsite"><img src="https://lh4.googleusercontent.com/-fz7RlCc_37E/SjT2k4x8DpI/AAAAAAAABpE/vWavdU63_3U/s640/subtitle.png" /></a></p>

更方便的是如果要轉成 iPod/iPhone 格式，直接右鍵轉換同樣能用！字幕也會一起轉進去喔！（當然會變成內嵌就是了。）「電視節目」功能裡也有很多特殊的欄位（例如「季」）可以用，超方便的啦～

已知問題：

1. RMVB 無理。這是 Perian 的限制，沒辦法。VLC 都已經支援了，希望他們能早日跟進…
2. MKV 在 QuickTime 的要讀取一段時間，而如果要存成參考影片，必須要等 QuickTime 完全讀完（時間條完全變成深色）才行。需要的時間長短依電腦等級而定，不過更重要的是因為這樣我的 script 就不能用了，要手動轉。如果是不包含字幕檔的 MKV 封裝，現在字幕組流行的影像編碼是 H.264，所以我建議把 MKV 封裝打開直接重壓成 H.264 AAC 的 MP4 封裝，這樣 iTunes 就可以直接吃，連參考影片都不用轉。*(*)*
3. 同樣是我寫的 script 的問題，目前無法讀取最上層資料夾以下的檔案（這在註解裡面有寫）。主要原因是我懶得寫，而且我自己用不太到，暫時也沒有放進去的打算。好吧，約定一下，如果 Perian 出可以播 RMVB 的版本我就更新！XD
4. 要換收看字幕或不想看字幕的話，要去原本檔案那邊調字幕檔位置才行。
5. 如果檔案很多的話。還是會有點佔空間。XD

> * 至於這要怎麼做，有空再分享吧。不過另一方面，由於 Perian 的一個限制，如果影片檔是 QuickTime 內建支援的格式，則 Perian 無法讀入外部字幕檔，所以如果你的 MKV 是連字幕檔一起包的，那暫時除了手動轉之外無解…