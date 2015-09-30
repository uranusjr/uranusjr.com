[<img title="Xcode + Qt" src="http://lh5.ggpht.com/_U8003MaCwnM/TI-_y0mm8ZI/AAAAAAAABoY/j5NvWFgqP-s/s800/xcode-qt.png" alt="" width="616" height="233" />](http://picasaweb.google.com/lh/photo/uqTEIhq1Sodfs8CvwOqqT0LNNXm9fiZNGPgajya8deI?feat=embedwebsite)

好久沒寫文了…最近都在研究 Qt，本來都是在 Linux 上玩，不過這幾天突然想把程式放到 Mac OS X 上跑，所以就研究了一下編譯環境。

先來介紹一下 Qt 好了，如果你已經知道這是什麼就跳過這一段吧。Qt 是兩個北歐人用 C++ 寫出來的應用程式 framework，本來它們創了一家公司叫 Trolltech，後來被 Nokia 買走。Qt 在 Linux 上算是聲名赫赫，也是 KDE 的基礎，不過他們在跨平台上下了很多心力，不僅是 Linux，在 Windows 和 Mac OS X 上使用者也不少，各式嵌入式作業系統上也常常看得到。原生的開發語言是 C++，不過也有很多其他語言的介面，其中比較重要的應該是 Java（Qt Jambi）、Python（PyQt）和  Ruby on Rails（QtRuby），詳見[官網](http://qt.nokia.com/)與[維基百科](http://zh.wikipedia.org/zh-tw/Qt)相關條目。

Qt 提供了一套完整的 SDK，官方推的 IDE 叫 Qt Creator。不過我一直不喜歡這東西，不知道是我不會用還是怎樣，反正介面又醜又複雜又難用…所以一開始在 Linux 上我就只有用文字編輯器加終端機。（Windows 上好一點，用了 Code::Blocks 加上一些 tools。比較麻煩的問題是我不喜歡 Visual Studio，而 MinGW 和 Qt 4.6.x 的組合又有問題…不過這是另一個話題了。）所以在 Mac 上我也朝這個方向研究。當然直接用終端機 qmake + make 也是可以，不過在我發現 Mac 上可以用習慣的 Xcode 來寫之後，當然不試試看就說不過去了。XD

首先，當然我們要有 Xcode，或者應該說要有整套開發工具 — 雖然好像也沒有除了全裝之外的選擇。好吧不管，總之這裡假設你已經裝好整套 Apple Developer Tools。接著就是下載 Qt 的開發環境來裝。我用的是[官網提供](http://qt.nokia.com/downloads/qt-for-open-source-cpp-development-on-mac-os-x)的 LGPL 10.5/10.6 Cocoa 版 binary，不含 Qt Creator 和 debugging library。4.6.3 版裝起來也才不到 600 MB 好輕巧啊。XD

安裝只有下一步跟同意可以選，應該沒什麼好教的，跳過。

認真研究過 Qt 的大概都知道，Qt 的編譯有兩個部份，首先要用 moc 解析 signals 和 slots 產生額外的源碼（moc 檔），然後才用 Makefile 去編譯。為了處理這部份的麻煩，Qt 提供了一些編譯工具，現在的版本叫 QMake。一般的 Qt 專案要用三個步驟來編譯：

* qmake -project
* qmake
* make

首先用 QMake 產生專案檔，副檔名是 .pro，裡面描述專案名稱、包含的源檔與頭檔檔名、以及一些額外參數。接著用 QMake 解析源碼決定要產生哪些 moc 檔案，並產生對應的 Makefile 檔。最後進行編譯，首先經過 moc 產生 moc 檔，然後進 C++ 編譯器。

可是在 Xcode 上事情有點不太一樣：Xcode 沒有 Makefile 可以搞，東西都藏在 Info.plist 和專案檔（.xcodeproj）裡面。所以如果你在終端機下 qmake -project 和 qmake 之後，會變成這樣：

[<img title="QMake Three Steps on Mac OS X" src="http://lh5.ggpht.com/_U8003MaCwnM/TI-_zW3oV5I/AAAAAAAABoc/YknF87f93Y0/s800/three-steps.png" alt="" width="528" height="185" />](http://picasaweb.google.com/lh/photo/3XkDlVazwkSFJgKjAbPW5kLNNXm9fiZNGPgajya8deI?feat=embedwebsite)

最後會產生一個 Xcode 的專案檔，讓你自己打開來再按 Build 來編譯…

當然這樣也不是不行啦，只是既然如此那不如就直接用 Xcode（其實這個在 .pro 裡有參數可以設，不過我覺得比較麻煩）。可是如果都在 Xcode 專案新增檔案來寫，又會產生另一個問題：Xcode 專案檔新增的檔案不會和 .pro 同步，所以不會更新產生 moc 檔的列表，如果你新增加的檔案裡有 signals 或/和 slots 的程式碼，就會沒辦法編。

所以唯一的方法是在編譯之前重新產生 Xcode 專案檔，也就是要關掉那個專案，打開終端機，然後再 QMake 一次，然後再打開新的 Xcode 專案，然後再編譯。光想就累了，搞屁啊…

所以接著就是本篇文章唯一的重點（XD）。為了簡化這個步驟當然就是要寫 script，我寫了一個這樣的：

```applescript
-- Get project folder

set theFolder to input

tell application "Finder"
    if (theFolder as string) does not end with ":" then
        set theFolder to (container of (theFolder as alias)) as alias
    end if
end tell
```

 

```applescript
-- Run QMake in project folder
do shell script ¬
    "cd " & quoted form of (POSIX path of theFolder) & ¬
    "; qmake -project; qmake"

-- Open Xcode project
tell application "Finder"
    open (theFolder & name of (theFolder as alias) & ".xcodeproj") as string
end tell
```

用法就很多啦。最簡單的方式是放到工序指令選單（參考[這篇](http://uranusjr.twbbs.org/2009/08/itunes-and-quicktime-working-together-nicely/)），選擇 Finder 裡那個專案的檔案夾，或者專案的任何一個檔案之後，選擇那個選單就行了。不過選單有點遠選起來不太方便，所以更棒的方法是做成 Automator 服務（參考[這篇](http://uranusjr.twbbs.org/2010/02/use-7-zip-in-mac-os-x/)）：

[<img title="QMake Automator Service" src="http://lh5.ggpht.com/_U8003MaCwnM/TI-_zmxPIqI/AAAAAAAABog/JErKAHaPCrw/s800/qmake-service.png" alt="" width="482" height="356" />](http://picasaweb.google.com/lh/photo/gaYPpiFtKWJvN8x7iZOXnULNNXm9fiZNGPgajya8deI?feat=embedwebsite)

Automator 裡有提供「執行 AppleScript」的方塊可以用，只要把上面那段貼進 on run/end run 中間就行了。

選個名字儲存起來（我命名成 QMake Here），這樣當要編譯時，只要關掉原本的 Xcode 專案，然後在專案的檔案夾上按右鍵，選擇最下面的 QMake Here，就可以自動重新 qmake -project、qmake、然後打開新的專案，我們只要在 Xcode 裡再選擇編譯就行了。（沒有把編譯包在一起的原因是我有時候要 debug 之類的，直接我自己選編譯感覺比較直覺。）

就這樣，小鎮村又恢復了和平的一天，這一切都要感謝…的人太多了，就謝天吧（亂接）。

這篇真的很沒重點，根本是純心得文…