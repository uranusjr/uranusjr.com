## Why 7-Zip?

引述[重灌狂人](http://briian.com/)的[文章](http://briian.com/?p=5218)：

> 當我們要壓縮、解壓縮時都用什麼軟體？大家還在花錢買 WinZIP 軟體嗎？以下介紹這套全中文介面的 7-Zip 壓縮軟體，不但操作簡單、速度快，而且還**支援常見的 ZIP、RAR 壓縮格式**，**重點是 7-Zip 是免費軟體**，不用錢、不用破解。如果公司 MIS 還在幫你灌沒註冊的 WinZIP 給你用，趕快把他換掉改裝 7-Zip 吧！

而對於我們 Mac 使用者而言，好處還多了一些。首先，即使你有受權，WinRAR 是 Windows 軟體，雖然可以用 [Darwine](http://darwine.sourceforge.net/) 或 [CrossOver Mac](www.codeweavers.com/products/cxmac/) 來跑，不過總是不太方便。雖然系統內建就有壓縮工具，但不但會包進一些莫名其妙的東西，還使用老舊的 ZIP 格式，不支援萬國碼，不支援分割壓縮，也不支援文件加密。Mac 上也是有原生的 RAR 壓縮軟體，但使用的 RAR 程序有版權疑慮（RAR 官方有 Mac OS X 命令列程式，但正式版仍須付費），加上使用者介面不太好，所以我一直不喜歡用。

因為以上種種原因，我已經完全轉向 7z 壓縮格式，並建議所有 Mac 使用者這麼做。我推薦的程式是 [7zX](http://sixtyfive.xmghosting.com/products/7zx)。這是一個拖拉放程式，直接把要壓縮的檔案或檔案夾拖到圖示上，填完跳出來的選項，就會壓好。

可是這樣不夠好。內建的壓縮工具只要在檔案上開輔助選單裡面就有，比起拖拉放還是快一點。幸好 Finder 本身就內建可修改輔助選單的工具，接下來要講的就是，如何把這個功能放到選單裡。

## 以輔助選單壓縮為 7-Zip

需要的東西有兩個，一個當然是你要下載並裝好 7zX，這就不教了，下載網址文末也會附。另一個是內建的 Automator。

![](/media/blog/7-zip-os-x/Automator.png)

Automator 是什麼這應該很多文章有，官網也有[介紹](http://support.apple.com/kb/HT2488?viewlocale=zh_TW)，所以就跳過了。打開之後選擇「服務」樣板。（如果你不是用 Snow Leopard，可能名稱會不太一樣，這我不太清楚，有問題請提出。）

![](/media/blog/7-zip-os-x/Automator-1.png)

接著把流程修改成下面這樣：

![](/media/blog/7-zip-os-x/Automator-2.png)

從左邊找到「打開 Finder 項目」拖到右邊，就會得到第三步的泡泡。把裡面的應用程式改成 7zX.app。

![](/media/blog/7-zip-os-x/Automator-3.png)

這樣就行了。按儲存，名稱取例如「以 7-Zip 壓縮…」之類的沒差。現在到 Finder 上任一個項目 control-點選（或右鍵）叫出輔助選單，就會看到最下面多一個「以 7-Zip 壓縮…」，選擇之後填上想要的選項，按 Return，就會得到 7z 檔，和內建的基本一樣。

目前發現的問題是，因為 7zX 會把每個檔案分別壓縮，所以如果你一次選很多檔案壓縮，出來的不會是一個檔裡面壓了所有檔案，是很多個裡面只包含一個項目的壓縮檔，ouch。這個可以解，不過就超過 Automator 的能力，要用 AppleScript，難度就不一樣。反正只要記得如果要壓超過一個檔案，就建檔案夾丟進去再壓，也還好，所以就算了，等到哪天真的有必要再說吧。XD

有問題請在下面提出，謝謝收看。

[7zX 官網](http://sixtyfive.xmghosting.com/products/7zx/)，軟體載點在最下面。