請大家幫忙頂這篇，Dev-C++ 真的該被時代淘汰了… orz

-------

[<img class="alignright" style="margin:17px 3px;" title="No Dev-C++" src="http://lh6.ggpht.com/_U8003MaCwnM/TJXxBxCRtUI/AAAAAAAABp0/Z077jF9HfHo/s800/no-dev-cpp.png" alt="" width="170" height="170" />](http://picasaweb.google.com/lh/photo/ZMMJTOp5DxXVhWQuGtimx0LNNXm9fiZNGPgajya8deI?feat=embedwebsite)

Dev-C++ 是 [Bloodshed Software](http://www.bloodshed.net/devcpp.html) 開發的 C/C++ IDE，其中包含完整的開發介面、專案模板、以及開源的編譯器（MinGW GCC），是對使用 Windows 的程式初學者而言，相當方便又容易上手的開發環境。因為這個原因，很多[教學文](http://azo-freeware.blogspot.com/2006/03/dev-c-50-beta-92-4992.html)都會教使用者用這套軟體，取代要錢的微軟官方開發環境 Visual C++。雖然後來微軟也有了免費的 [Visual Studio Express](http://msdn.microsoft.com/zh-tw/express/default.aspx)，但因為 Dev-C++ 有中文版，還是被[很多人](http://sofree.cc/dev-c/)繼續推薦。

所以這似乎是一套很優秀的免費軟體，那麼為什麼這篇文章閒著沒事要說服你離開這套軟體呢？答案是，對初學者而言這個軟體當然沒什麼問題，但其實它有一些潛藏的問題，如果你不是學學就算了，想繼續走程式設計，以後勢必會遇到一些麻煩。與其到時候再想一堆辦法解決，甚至中途轉換到其他 IDE 上，不如從一開始就避開這套軟體，省得繞彎路。

當然口說無憑，下面就舉出不該使用 Dev-C++ 具體的理由：（[參考內容](http://www.jasonbadams.net/20081218/why-you-shouldnt-use-dev-c/)）

1. **Dev-C++ 上次版本更新是 2005 年，而且已經完全沒有繼續活動的跡象**。這代表如果哪一天你在使用時遇到問題，得到軟體開發者答案得機會趨近於零。不論再好的軟體總是必然有 bug，Dev-C++ 目前根據 [SourceForge](http://sourceforge.net/tracker/?group_id=10639&amp;atid=110639) 使用者的回報共有 1345 個，而且只會增加不會減少。

2. 承上，由於版本已經沒有更新，**Dev-C++ 附帶的編譯器版本也過時非常非常久**。最新的 Dev-C++ 5.o Beta 9.2 附帶 MinGW 3.4.2，而目前最新的 MinGW 版本是，呃，4.5.0…。編譯器也同樣會有 bug，而更重要的是，程式語言標準會更新，因此舊的編譯器與新的程式標準不見得相容，這會讓你的程式出現問題。雖然其實編譯器與 IDE 本身有一定程度獨立，所以你還是可以在 Dev-C++ 上正常使用較新的編譯器，但這只是自找麻煩，而且不是每個人都知道應該這麼做，更別說知道應該怎麼做。

3. **Dev-C++ 的功能比起更新的 IDE 而言較弱**。五年是很長的時間，現在的 IDE 功能，不論是自動完成、自動縮排、以及格式檢查等等，都已經進步非常多。對於初學者而言這可能不太明顯，但使用功能較佳的編輯器，在建立良好程式設計習慣上有很大幫助，也可以在撰寫較複雜程式時省掉很多時間。當然另一方面來講，Dev-C++ 的環境是很簡單（因為功能少），但為了這個理由在初學時選擇它根本沒有意義，只是把問題放到以後煩惱而已。

4. 承上，**Dev-C++ 的 debugger 和現在的 IDE 根本是 LP 比雞腿…**。這可能對初學者更不明顯，但選擇好的 debugger 對程式設計會有重要影響。

大概就這樣了。如果這樣還不能說服你，嗯，事實上這四點已經完全充分構成理由，如果你完全不關心，那麼你的程式設計學習大概也不是很認真，所以或許繼續用 Dev-C++ 也沒差吧。

那麼，既然不該用，我們要用什麼取代它呢？

* [Microsoft Visual C++ Express](http://www.microsoft.com/express/Downloads/#2010-Visual-CPP)。這是微軟的免費 IDE 軟體 Microsoft Visual Studio Express 的一部份，目前最新是 2010 版。雖然官方頁面目前只有 2008 板有中文下載，但其實 2010 也有中文版可以用。詳情可參考[這篇文章](http://www.freegroup.org/2010/06/visual-studio-2010-express/)。

* [Code::Blocks](http://www.codeblocks.org/downloads)。這是從 2005 年左右開始開發的新軟體，也是目前開源社群中最活躍的 IDE。如果你已經有很多使用 Dev-C++ 開發的專案不想放棄，Code::Blocks 會是不錯的選擇，因為它帶有轉移工具，可以把 Visual C++ 或 Dev-C++（以及其他）專案匯入。這個軟體也和 Dev-C++ 一樣使用 GCC，而且是跨平台的，不只在 Windows 上可使用。缺點是，Code::Blocks 目前[繁體中文翻譯](https://translations.launchpad.net/codeblocks/trunk/+pots/codeblocks/zh_TW/+translate?start=0&amp;batch=10&amp;show=untranslated&amp;field.alternative_language=&amp;field.alternative_language-empty-marker=1&amp;old_show=untranslated)尚未完成，安裝起來也比較麻煩。詳情可見[這篇](http://lagunawang.pixnet.net/blog/post/9114139)和[這篇](http://www.ubuntu-tw.org/modules/newbb/viewtopic.php?post_id=137838)文章。

* [Eclipse](http://www.eclipse.org/home/categories/index.php?category=ide)。這個其實主要是 Java 的 IDE，不過經過加裝 CDT 與 MinGW，調整後開發 C/C++ 也很好用。詳情可見[這篇](http://nknush.kh.edu.tw/~johnsirhp/Eclipse%2BCDT%2BMinGW.htm)文章。

* [NetBeans](http://netbeans.org/downloads/)。另一個主要是 Java 的 IDE，同樣可以搭配 CDT 和 MinGW。Eclipse 和 NetBeans 孰優孰劣是千古戰題，這裡就不講了，請自行感受。詳情可見[這篇](http://hi.baidu.com/cyberniuniu/blog/item/2cc953ec39ff292d63d09f6a.html)文章。

替代方案當然還有，不過就講到這裡為止吧，我主要的目的只是想讓任何因為舊文章或舊書籍的推薦，而想上網搜尋如何下載 Dev-C++ 的人能看到這篇文章，而轉而使用其他更好的 IDE。至於你想用什麼方法來取代，以及各種方案的比較，就不是我想討論的。

反正，不管你用什麼，**請不要用 Dev-C++**。