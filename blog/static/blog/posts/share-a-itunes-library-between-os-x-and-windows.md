網友 cooleric323 在 Ptt 上問了個有趣的問題：

![](/media/blog/itunes-windows-os-x/cooleric3234.png)

確實是有趣。雖然我個人沒有在用 Boot Camp，不過如何共享 Mac OS 與 Windows 的 iTunes 資料庫確實值得研究。

這個技巧適用於幾個類似的狀況：

* 你希望，如同原 po，共享 Mac OS 和 Boot Camp 中 Windows 的 iTunes 資料庫。
* 你會在兩台以上電腦更動 iTunes 資料庫（典型的狀況是想增加新曲目），iTunes 提供的共享功能不夠用。
* 你想把整個資料庫放在外接硬碟，這樣你的 MacBook、公司的 Dell PC、以及家裡的 Mac Pro (!) 都可以用同一個資源庫，用同一個歌單，省得把歌曲複製來複製去，或是要把某台電腦一直開著做共享。

總之，只要你想在兩台以上電腦管理、或離線收聽同一個 iTunes 資料庫，這篇教學應該都對你很有用！

## Ready to Go

在這個教學裡，我們要用到：

* 可執行 Mac OS 的電腦。
* 可執行 Windows 的電腦（可以和上面是同一台）。
* 如果上面兩台是不同的電腦，那麼你當然需要可在兩台電腦間傳輸資料的媒介 — 例如上面第三個例子中的隨身硬碟。隨身硬碟必須格式化為兩個系統都能讀寫的格式，例如 FAT32（Mac OS 的磁碟工具程式稱作 MS-DOS (FAT)）。如果你是第一例，也就是希望 Boot Camp 共享，則你需要安裝 [MacDrive](http://www.mediafour.com/products/macdrive) 或類似軟體，讓你的 Windows 能讀取 Mac OS 磁區（或反之）。

## 認識 iTunes 資料庫

根據[蘋果官網的文件](http://docs.info.apple.com/article.html?artnum=93732-de)，iTunes 資料庫分成四大部份：

* iTunes Library，或 iTunes Library.itl（在 Windows 上）。這是資料庫的主要檔案，所有的歌曲資訊（寫在 ID3 標籤的當然是另一回事）基本上都在這裡面。
* iTunes Music 資料夾。這是你的資料庫來源，所有音樂、影片等檔案都在裡面。
* iTunes Library.xml。這是連結上面兩個部份的橋樑。.xml 檔可以用一般瀏覽緝獲文字編輯軟體打開，而如果你打開來看，你會發現裡面包含了 iTunes 資料庫所有檔案的「絕對路徑」，也就是檔案在你電腦裡的位置。
* 其他。包含專輯封面（Album Artwork 資料夾）、一些先前版本的資料庫（備份）、還有 8.0 開始有的 Genius 等等資料。

根據官網， iTunes Library 和 iTunes Library.itl 有相同的內容，只是檔名不同。

## 實作

「好吧，」你說，「既然內容一樣，那應該可以通用。」的確是這樣，但這會衍生出大問題。iTunes Library.xml 使用絕對路徑來認定檔案位址，例如：

```xml
<key>3418</key>
<dict>
    <key>Track ID</key><integer>3418</integer>
    <key>Name</key><string>Mr. Bartender (It's So Easy)</string>
    <key>Artist</key><string>Sugar Ray</string>
    <key>Album Artist</key><string>Sugar Ray</string>
    <key>Composer</key><string>Sugar Ray</string>
    <key>Album</key><string>In the Pursuit of Leisure</string>
    <key>Genre</key><string>Punk</string>
    <key>Kind</key><string>AAC 音訊檔</string>
    <key>Size</key><integer>6678014</integer>
    <key>Total Time</key><integer>210266</integer>
    <key>Disc Number</key><integer>1</integer>
    <key>Disc Count</key><integer>1</integer>
    <key>Track Number</key><integer>5</integer>
    <key>Track Count</key><integer>12</integer>
    <key>Year</key><integer>2003</integer>
    <key>Date Modified</key><date>2008-09-28T01:37:41Z</date>
    <key>Date Added</key><date>2008-09-28T01:34:50Z</date>
    <key>Bit Rate</key><integer>256</integer>
    <key>Sample Rate</key><integer>44100</integer>
    <key>Persistent ID</key><string>DF73F5D054D55D6D</string>
    <key>Track Type</key><string>File</string>
    <key>File Type</key><integer>1295270176</integer>
    <key>File Creator</key><integer>1752133483</integer>
    <key>Location</key><string>file://localhost/Users/uranusjr/Music/iTunes/iTunes%20Music/Sugar%20Ray/In%20the%20
Pursuit%20of%20Leisure/05%20Mr.%20Bartender%20(It's%20So%20Easy).m4a</string>
    <key>File Folder Count</key><integer>4</integer>
    <key>Library Folder Count</key><integer>1</integer>
</dict>
```

這是我資料庫裡的片段，顯示 Sugar Ray 的 Mr. Bartender (It’s So Easy)。最長的那一行（還換行）就是歌曲的路徑。但是由於 Mac OS 和 Windows 的檔案路徑格式完全不一樣，如果你把這個東西直接丟給 Windows 吃，即使你告訴它裡面的資料夾在哪裡，這個檔案仍然不能用。如果你直接在 Windows 下以開啟資料庫的方式開啟 iTunes（按住 shift），並指向 Mac OS 的 iTunes Library，iTunes for Windows 會讓你選擇那個資料庫，也會看到歌，但是會找不到檔案。

解決方法有，就是在 Windows 下重新製作另一個 iTunes Library.xml。但是這樣也有問題 — 因為 iTunes 規定 iTunes Library.xml 和 iTunes Library(.itl) 要放在一起，所以如果你直接指向原本的那個資料庫，iTunes for Windows 會就地重新製作 .xml 檔，然後你本來在 Mac OS 下製作的 .xml 就被覆蓋了 ⇒ G. G.。

## Getting It Done

那怎麼辦？幸好還是有辦法，感謝 [Crazor 在 macosxhints 分享的秘訣](http://www.macosxhints.com/article.php?story=20070424081346722)。（喔，他是屬於上面第二種例子。）

我們要做的其實也很簡單：把步驟顛倒過來（把思緒逆轉過來！[成步堂](http://zh.wikipedia.org/w/index.php?title=逆转裁判&amp;variant=zh-tw)是對的！）。

![](/media/blog/itunes-windows-os-x/5.png)

首先我們必須移走 Mac OS 下的（紅框）iTunes Library.xml （改名也可以，反正要避開原本的檔名，避免被覆蓋）。 接著把 iTunes Library 更名成 iTunes Library.itl。

![](/media/blog/itunes-windows-os-x/6.png)

## Fly It to the WINDOWS…

進入 Windows，按住 shift 開啟 iTunes 以指定資料庫。

![](/media/blog/itunes-windows-os-x/7.png)

按下「選擇資料庫」，然後把位置指向你在 Mac OS 下的資料庫，也就是剛剛修改的 iTunes Libraby.itl。

![](/media/blog/itunes-windows-os-x/1.png)

## …And Back

回到 Mac OS。我們可以看到 iTunes 資料夾裡面多了一個檔案。

![](/media/blog/itunes-windows-os-x/3.png)

現在找到你之前移走的 iTunes Library.xml 檔。先別移回去！首先，你現在已經有了 Windows 的 xml 檔，移回去就覆蓋掉了，之前豈不是做白工。而且你現在（對 Mac OS 而言）的資料庫叫做 iTunes Library.itl，直接放回去 iTunes for Mac OS 也認不得。所以我們把這個（一開始移走的）檔案改名成 **iTunes Library.itl.xml**，然後再放回去。

![](/media/blog/itunes-windows-os-x/2.png)

然後打開 iTunes for Mac OS。因為我們剛剛把資料庫檔名改了（本來是 iTunes Library，我們改成 iTunes Library***.itl***，所以 iTunes 認不得，會跳出一個視窗（跟前面 Windows 版本類似）問你要新建資料庫還是開啟。當然我們要開啟，找到修改的 iTunes Library.itl，按下確定。

## And It'll Be My Baby!!

![](/media/blog/itunes-windows-os-x/4.png)

是的，結束了。享受雙系統共享一個資源庫的便利吧！Now listen the rhe music! =P

-----------

就這樣，iTunes 從此腳跨兩條船，過著幸福快樂的生活。

其實沒有。在轉換途中其實還是有一些問題，只是我先跳過了。

其中比較重要的是，我在試聽 iTunes for Windows 時發現有一首歌不能播放。我的猜測是因為歌名中有個 % 符號在作怪，因為 Unicode 編碼也要用到這個符號，可能兩個系統在這邊的解讀有差異。我不了解編碼技術，就請懂的人來推測了。不過說來說去，有 % 符號的歌曲應該不會很多吧，暫時放一邊。

另外我確認了一下，在任何一邊做出資料庫更改後，另一邊的 iTunes 第一次開啟時確實要讀取比較久，不過至少仍然會更新，不需要把 .xml 檔砍掉重練。就耐心等一下吧，也沒有幾秒的，值得。

對了，前面提到的 .xml 檔路徑不同現象，我把兩個檔案拿來讓大家比對一下，就可以看出來不同。

首先是 Mac OS 版（第一篇用過的 Mr. Bartender (It’s So Easy)）：

```xml
<key>3418</key>
<dict>
    <key>Track ID</key><integer>3418</integer>
    <key>Name</key><string>Mr. Bartender (It's So Easy)</string>
    <key>Artist</key><string>Sugar Ray</string>
    <key>Album Artist</key><string>Sugar Ray</string>
    <key>Composer</key><string>Sugar Ray</string>
    <key>Album</key><string>In the Pursuit of Leisure</string>
    <key>Genre</key><string>Punk</string>
    <key>Kind</key><string>AAC 音訊檔</string>
    <key>Size</key><integer>6678014</integer>
    <key>Total Time</key><integer>210266</integer>
    <key>Disc Number</key><integer>1</integer>
    <key>Disc Count</key><integer>1</integer>
    <key>Track Number</key><integer>5</integer>
    <key>Track Count</key><integer>12</integer>
    <key>Year</key><integer>2003</integer>
    <key>Date Modified</key><date>2008-09-28T01:37:41Z</date>
    <key>Date Added</key><date>2008-09-28T01:34:50Z</date>
    <key>Bit Rate</key><integer>256</integer>
    <key>Sample Rate</key><integer>44100</integer>
    <key>Persistent ID</key><string>DF73F5D054D55D6D</string>
    <key>Track Type</key><string>File</string>
    <key>File Type</key><integer>1295270176</integer>
    <key>File Creator</key><integer>1752133483</integer>
    <key>Location</key><string>file://localhost/Users/uranusjr/Music/iTunes/iTunes%20Music/Sugar%20Ray/In%20the
%20Pursuit%20of%20Leisure/05%20Mr.%20Bartender%20(It's%20So%20Easy).m4a</string>
    <key>File Folder Count</key><integer>4</integer>
    <key>Library Folder Count</key><integer>1</integer>
</dict>
```

一樣，注意最長的那行。

接著是 Windows 版：

```xml
<key>3412</key>
<dict>
    <key>Track ID</key><integer>3412</integer>
    <key>Name</key><string>Mr. Bartender (It's So Easy)</string>
    <key>Artist</key><string>Sugar Ray</string>
    <key>Album Artist</key><string>Sugar Ray</string>
    <key>Composer</key><string>Sugar Ray</string>
    <key>Album</key><string>In the Pursuit of Leisure</string>
    <key>Genre</key><string>Punk</string>
    <key>Kind</key><string>AAC 音訊檔</string>
    <key>Size</key><integer>6678014</integer>
    <key>Total Time</key><integer>210266</integer>
    <key>Disc Number</key><integer>1</integer>
    <key>Disc Count</key><integer>1</integer>
    <key>Track Number</key><integer>5</integer>
    <key>Track Count</key><integer>12</integer>
    <key>Year</key><integer>2003</integer>
    <key>Date Modified</key><date>2008-09-28T01:37:41Z</date>
    <key>Date Added</key><date>2008-09-28T01:34:50Z</date>
    <key>Bit Rate</key><integer>256</integer>
    <key>Sample Rate</key><integer>44100</integer>
    <key>Persistent ID</key><string>DF73F5D054D55D6D</string>
    <key>Track Type</key><string>File</string>
    <key>Location</key><string>file://localhost/Y:/Music/iTunes/iTunes%20Music/Sugar%20Ray/In%20the%20Pursuit%20
of%20Leisure/05%20Mr.%20Bartender%20(It's%20So%20Easy).m4a</string>
    <key>File Folder Count</key><integer>4</integer>
    <key>Library Folder Count</key><integer>1</integer>
</dict>
```

看到不同點了嗎？Windows 版本在 localhost 之後接的是磁碟代號（我用遠端磁碟功能把 Y: 槽設成 Mac OS 底下 uranusjr 這個帳號的家目錄）。Mac OS 下沒有磁碟代號，所以這份檔案 iTunes 看不懂。反之，沒有磁碟代號的 Mac OS 路徑 Windows 版 iTunes 也看不懂。

如果你把資料庫放在外接裝置，則 Mac OS 的路徑會以 file://localhost/Volumes/(外接裝置代號) 開頭。另一方面，Windows 會用另一個磁碟代號表示。無論如何，這兩個路徑的確無法通用。

另外可以看到，除了路徑和 Track ID 不同之外，這兩份內容完全一模一樣。這兩份資料會在你於更動某一邊後，在開啟另一邊時根據 iTunes Library.itl 更新一次，所以就不會有兩邊資料庫不同步的問題。How nice!

以上就是全部的教學了，祝各位 iTunes 使用者武運昌隆！