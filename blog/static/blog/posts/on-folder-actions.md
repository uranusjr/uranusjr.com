Mac OS X 是以優秀的權限管理（繼承 Un*x 而來）、以及領先全球的簡潔、易用使用者介面而聞名。但很多人不知道的是 Mac OS X 也有許多非常好用的「power feature」供使用者加速自己的日常工作。這部份也是因為 Mac 的 UI 設計哲學，傾向把一般人不需要的功能隱藏起來。這其中的一個就是檔案夾動作。

簡單來講，所謂檔案夾動作（folder actions），是作業系統底層提供的一種自動化機制，可以讓系統自動偵測所發生的「事件」，並根據事件對應相對功能。如名稱，這個東西可以附加在任何檔案夾上，在檔案夾產生事件時，就會被觸發。

這些事件包括：

* 檔案夾內容增加（被放入新檔案）或移除
* 檔案夾被 Finder 打開，或在 Finder 視窗中被關閉
* 檔案夾本身被移動

以這些事件為基礎，我們就可以做出一些方便的功能。例如你是老闆，正在等手下傳來某個關鍵文件。可是你可能正在寫一份重要文章，不想每五分鐘就去檢查投遞箱，那麼你就可以在投遞箱檔案夾加上一個動作，這樣當檔案夾收到這份文件時，Finder 就會自動跳出一個視窗，告訴你這個檔案被收到了。
類似的動作其實不少見，例如 Mac 上很廣泛使用的 [Growl](http://growl.info/) 就是類似的延伸。比起 Growl，檔案夾動作的功能沒有那麼多，也只能和 Finder 連動，可是它也有自己的優勢，也有只有它才做得到的自動化功能。

以一個例子來說明檔案夾動作的使用法…

## Folder Action in Action

假設我現在想在部落格的文章裡放圖片。可是我手上的圖可能是 tiff 檔，為了網頁速度，我想轉小一點。當然這個用預覽程式就可以轉，可是這樣很麻煩。那麼我就可以用檔案夾動作，把我選擇的檔案都直接轉檔：
首先建立一個資料夾，名稱隨便取。

![](/media/blog/folder-action/fa-1.png)

如果你從來沒有用過檔案夾動作，那要先從輔助選單裡啟用。

![](/media/blog/folder-action/fa-2.png)

接著附加你想要的檔案夾動作。

![](/media/blog/folder-action/fa-3.png)

我們這邊用內建的 Duplicate as JPEG。

![](/media/blog/folder-action/fa-4.png)

如果檔案選擇視窗沒有帶你到正確的位置，這個檔案在 /Library/Scripts/Folder Action Scripts/ 裡。

![](/media/blog/folder-action/fa-4-2.png)

注意是 Folder Action Scripts，不是 Folder Action 檔案夾。

設定完成之後，直接把你想轉檔的檔案丟到資料夾裡，

![](/media/blog/folder-action/fa-5.png)

就會自動幫你轉好檔，放在資料夾裡面（原始檔也留著）。

![](/media/blog/folder-action/fa-6.png)

如果你不想要一個檔案夾動作，那可以從輔助選單中同樣直接移除。或者，如果你希望比較詳細的設定，可以選擇「設定檔案夾動作」，出現類似這個視窗：

![](/media/blog/folder-action/fa-7.png)

最上面可以啟用或停用「全部」的檔案夾動作（和選單裡的選項功能一樣），左邊是你有使用檔案夾動作的所有檔案夾，右邊是上面使用的工序指令。如果你想增加、減少或編輯都可以在這裡面完成。

## Scripting a Folder Action

以上就是檔案夾動作的使用。Mac OS X 預附 13 個檔案夾動作工序指令：

<table class="table">
<tbody>
<tr><th>add - new item alert.scpt</th><td>檔案夾增加物件時，跳出提示視窗。</td></tr>
<tr><th>close - close sub-folders.scpt</th><td>關閉該檔案夾視窗時，關閉所有瀏覽子檔案夾的視窗。</td></tr>
<tr><th>convert - PostScript to PDF.scpt</th><td>cript 轉成 PDF 檔。</td></tr>
<tr><th>Image - Add Icon.scpt</th><td>修改檔案夾裡所有圖片，以圖片內容作為檔案圖示。</td></tr>
<tr><th>Image - Duplicate as JPEG.scpt</th><td>將圖片轉成 JPEG 檔。</td></tr>
<tr><th>Image - Duplicate as PNG.scpt</th><td>轉成 PNG。</td></tr>
<tr><th>Image - Duplicate as TIFF.scpt</th><td>轉成 TIFF。</td></tr>
<tr><th>Image - Flip Horizontal.scpt</th><td>把圖片水平翻轉。</td></tr>
<tr><th>Image - Flip Vertical.scpt</th><td>垂直翻轉。</td></tr>
<tr><th>Image - Info to Comment.scpt</th><td>把圖片資訊放到檔案註釋。</td></tr>
<tr><th>Image - Rotate Left.scpt</th><td>	圖片向左旋轉。</td></tr>
<tr><th>Image - Rotate Right.scpt</th><td>向右旋轉。</td></tr>
<tr><th>open - show comments in dialog.scpt</th><td>打開該檔案夾時，跳出對話框顯示註釋。</td></tr>
</tbody>
</table>

當然如果有需求，也可以用 AppleScript 自己寫。AppleScript 的寫法沒辦法在這邊講，所以這邊只提和檔案夾動作有關的寫法，詳細的 AppleScript 指令就請自己學，或等有時間再分享。

檔案夾動作工序指令是以 handler 為基礎，on - end 負責控制當什麼 event 發生時，要執行該工序指令。例如 10.5 的 stacks，因為不太好看所以[有人做了抽屜圖示](http://www.geocities.jp/chy065/)。如果要把抽屜擺在最上面，那就把抽屜的檔名以空白開頭，然後以名稱排列就行了，可是下載資料夾就很麻煩 — 通常我們會希望下載資料夾裡面是最新放入的放在最上面，這樣比較好找（原廠預設也是這個設定），可是這樣每次有新東西，抽屜就會跑到下面去。這種時候我們也可以用檔案夾動作，讓 Finder 幫我們自己移動抽屜圖示。

例如可以打開工序指令編寫程式（/Applications/AppleScript/Script Editor.app），然後這樣寫…

```applescript
on adding folder items to theFolder after receiving addedItems
    tell application "Finder"
        set allFiles to name of every file of theFolder
        repeat with theItem in allFiles
            if theItem begins with " " then
                set theIcon to theItem
                exit repeat
            end if
        end repeat  
        move file theIcon of theFolder to home
        move file theIcon of home to theFolder
    end tell
end adding folder items to
```

存成工序指令檔（.scpt），和其他檔案夾動作一起放在 /Library/Scripts/Folder Action Scripts/ 裡面。

![](/media/blog/folder-action/fa-10.png)

然後把 Downloads 檔案夾附加這個動作，然後把抽屜圖示取個以空白開頭的檔名就行了。這樣只要在檔案夾被加入新檔案（on adding folder items to theFolder）時，Finder 就會找出圖示檔的檔名（找出所有檔案，用 repeat 找到空白開頭的檔），然後把圖示移出資料夾，然後再移回來（兩行 move），這樣就可以確保圖示是最後加入的檔案，進而被放在最上面。

![](/media/blog/folder-action/fa-12.gif)

如果有興趣，也可以自己打開原廠附帶的 .scpt 檔研究一下。

## Automate an Folder Action

如果不會寫 AppleScript 怎麼辦？沒關係，自 10.4 起，Mac OS X 發佈了 Automator，讓使用者能更簡單地規劃基本的工作流程。確實對不會寫程式的人而言，Automator 是救星，而其實即使會寫 AppleScript，我自己有時候也會用…Automator 的動作雖然比較慢，可是寫起來（技術上來說，根本不用寫）快超多，而且不用檢查半天為什麼你的 syntax 就是沒辦法編譯。
Automator 怎麼和檔案夾動作連動呢？以前面那個轉檔的例子…

建立一個這樣的流程：

![](/media/blog/folder-action/fa-automator-1.png)

其中 originals 是我在 convert to JPG 資料夾裡建立的另一個資料夾。

然後在檔案選單裡選擇「儲存為外掛模組」（opt + cmd + s）：

![](/media/blog/folder-action/fa-automator-2.png)

重點是第二行，選擇外掛模組用於：檔案夾動作。第三行就附加到我們剛剛的那個檔案夾。

這樣就行了，照樣把檔案拖進去就能用，也一樣會有備份。

如果之後想刪掉，這個檔案會在 ~/Library/Workflows/Applications/Folder Actions/ 裡面，

![](/media/blog/folder-action/fa-automator-3.png)

如果我們打開「設定檔案夾動作」的視窗，我們會發現有一個 .scpt 檔被附加了：

![](/media/blog/folder-action/fa-automator-4.png)

咦，不是 .app 檔嗎？不是的，這個檔仍然在剛剛的 Folder Action Scripts 檔案夾裡，打開來看看…

![](/media/blog/folder-action/fa-automator-5.png)

其實 Mac OS X 只是寫了幾行工序指令，命令系統自己用 Droplet 方式打開剛剛那個 Automator 程式而已嘛！XD

不過用這個方法，就可以更方便地應用檔案夾動作囉。
