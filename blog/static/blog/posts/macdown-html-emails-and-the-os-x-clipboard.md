我偶爾會[在 Twitter 上搜尋 MacDown](https://twitter.com/search?q=macdown) 看看有沒有什麼有趣的討論。通常搜出來的東西都是 [O-Town MacDown] 的宵夜文，但有時候還是會看到一些討論，而且不知道為什麼日本使用者比例頗高。

[O-Town MacDown]: http://support.gktw.org/site/PageNavigator/macdown.html

再講下去就要離題了。總之我前幾天看到了這個 tweet：

<blockquote class="twitter-tweet" lang="en-gb"><p lang="en" dir="ltr">Protip: compose your email in Macdown and copy/paste from the preview pane to your email.</p>&mdash; Justin Sternberg (@Jtsternberg) <a href="https://twitter.com/Jtsternberg/status/647109186799730688">September 24, 2015</a></blockquote> <script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

我個人通常是用 OS X 內建的 Mail.app 寫 email，所以不太用這個。不過似乎不少人會用 Markdown 寫 email，然後再貼到 Gmail 的編輯器裡面。

但這個功能背後其實有點故事。


## Email 文件格式

在講故事前，先來一點背景知識。一封 email 可以被分為 header 與 body 兩部分，其中 header 包含寄件者收件者之類的資訊，而 body 就是郵件內容。郵件內容通常會是純文字、[Rich Text Format]、或者 HTML。

[Rich Text Format]: https://zh.wikipedia.org/wiki/RTF

現代的 GUI email clients 通常都完全支援瀏覽這三種格式，但對後兩者的撰寫支援就比較不一致。例如 OS X 的 Mail.app 只支援 RTF，而 Gmail 網頁上的編輯器則是輸出 HTML。其實這在多數狀況下也沒什麼影響，反正寄來寄去大家都看得到。但如果你想把其他地方寫的文字格式拷貝進去，才會發現有些格式可以保存，有些卻不行。


## OS X 剪貼簿

當使用者按下 <kbd>⌘</kbd><kbd>C</kbd> 時，桌面系統會把使用者選取的東西寫入剪貼簿。但使用者究竟選取了什麼？假設使用者在網頁上選取一段文字，然後拷貝。這時當然文字需要要拷貝，但文字的**格式**（例如字體、大小、對齊方式）怎麼辦？如果不保存格式，使用者就只能貼上純文字，但如果保存，當使用者真正想貼上純文字（例如從網頁拷貝文字，貼到 MacDown 的編輯區）時，就會多出一些奇怪的格式符號。

在這個例子中，決定使用者期望行為的關鍵，其實不是由拷貝決定，而是**貼上**的目標。所以 OS X 的處理方法是「都拷貝」，等到貼上時再選擇合適的資料送出。繼續以網頁文字為例，當使用者從 Safari 拷貝一段文字時，OS X 剪貼簿會寫入高達 7 種資料格式。這些內容可以用 Clipboard Viewer 來檢視：[^1]

![Clipboard Viewer screenshot with text from Safari.](http://d.pr/i/12ZjP+)

[^1]: Clipboard Viewer 包含在 Auxiliary Tools for Xcode 裡面。有 Apple 開發者帳號的人可以從[這裡](https://developer.apple.com/downloads/)下載。

當使用者貼上剪貼簿中的內容時，接收貼上指令的 responder 會選擇最適合自己的資料格式，並向剪貼簿要求讀取。例如 MacDown 的編輯區是一個 plain text 的 `NSTextView`，所以會選擇 OS X 原生的純文字剪貼格式 `NSStringPboardType`；一個 rich text 編輯器則可以要求包含文字格式的剪貼資料，例如內建的文字編輯（TextEdit.app）在 Rich Text 模式下，就會要求 NeXT Rich Text Format，進而獲得文字格式，甚至包含表格與圖片。[^2]

[^2]: 嚴格來說 RTF 格式其實不能處理圖片，只有 RTFD 格式才行。不過這是細節。

這也是 OS X 一些「特異功能」，例如拷貝一個應用程式，然後打開預覽程式（Preview.app）貼上，會得到該程式 icon 的由來——當 OS X 剪貼簿寫入一個 app bundle 時，也會同時寫入該 app 的 icon 檔案，而該格式會被預覽程式選擇。


## HTML Emails 與 MacDown

MacDown 的預覽區基於 OS X 的 `WebView` class。這個 view 和 Safari 使用同樣的核心（WebKit），所以提供同樣的剪貼簿功能。如果你用 Safari 打開 Gmail 網頁，然後把 MacDown 預覽區的內容貼進郵件編輯框，就會得到完美的 HTML 格式。

但<del>我也是看 issue tracker 才知道</del>[貼到 Google Chrome 的結果有問題](https://github.com/uranusjr/macdown/issues/115)。在 Firefox 更慘，直接變成 plain text 啦！

![Paste results from MacDown preview to Firefox, Google Chrome, and Safari.](https://cloud.githubusercontent.com/assets/358122/3916875/3d90f088-2382-11e4-9b24-430b35be97b5.png)

我研究了一陣子才發現，這不是 MacDown 的問題——如果你在 Safari 開 Gmail 寫到一半，然後想把表格從 Safari 的 Gmail 編輯框貼到 Google Chrome 或 Firefox 的 Gmail 編輯框，也會發生一模一樣的事情。問題出在 WebKit。

仔細研究上面那個 Clipboard Viewer 可以發現，當使用者從 Safari 拷貝一段文字（不包含多媒體資料）時，只有兩筆資料屬於帶格式文字：Apple Web Archive 與 RTF。後者我們已經討論過，前者則是 Apple 專有的網頁資料交換格式。既然是 Apple 專有，其他瀏覽器也就無法使用。Google Chrome 至少看得懂 RTF，因此貼上了這個內容（只有字體資訊，無法保存 HTML heading 資訊與 stylesheets）。可憐的 Firefox 只懂純文字，就被排擠了。

這些第三方瀏覽器的拷貝行為也不太一樣。下面是 Opera 的狀況：

![Clipboard Viewer screenshot with text from Opera.](http://d.pr/i/193Ii+)

它就寫了兩種格式：純文字與 HTML。但這兩種格式才是交換性最高的呀！所有市面上的瀏覽器（包括 Safari）都可以正確貼上。

既然知道了原因，[解法](https://github.com/uranusjr/macdown/commit/265b4b04bd1715526135c304839eff73f6fec81a)就簡單了。當使用者把 focus 放在預覽區執行拷貝時，MacDown 會偷偷在剪貼簿裡多塞一筆 HTML 資料。

~~~objc
// 取出 selection 的 HTML。
NSString *html = webView.selectedDOMRange.markupString;

// 把 HTML 寫入剪貼簿。
NSPasteboard *pb = [NSPasteboard generalPasteboard];
[pb setString:html forType:@"public.html"];
~~~

這樣就可以成功貼至所有瀏覽器——絕大多數情況下會使用我的 HTML 資料，只有 Safari 會用內建的 Apple Web Archive，不過也沒關係。為了不讓系統本身的拷貝行為覆寫這段 HTML 資料，我另外加了一些小手段（用 `NSOperationQueue` 稍微延遲 HTML 資料被寫入剪貼簿的時間），不過基本的概念就是如此。MacDown 從 0.2.3 開始（天哪這版本已經是 13 個月前的事！）完整支援預覽區資料的 copy-pasting operations。

---

之前有人說想聽 MacDown 的開發故事，所以就趁這個機會寫了（雖然他好像也不會看 :p）。如果覺得這類故事還算有趣的話麻煩說一聲，以後有機會也可以寫一些類似的 tidbits。或者八卦？我知道有人想聽另一類的故事啦，不過這個可能比較有難度，笑。
