一篇簡單的舊文，也沒什麼專業成份，不過很少看到有人提，所以還是放上來當個備份。這個 HFS 不是蘋果開發的那個磁碟格式（[Hierarchical File System](http://en.wikipedia.org/wiki/Hierarchical_File_System)），而是一種檔案共享平台，HTTP File Server 的縮寫。

概念是，把自己電腦中的檔案賦予一個公開的 HTTP 位址，這樣別人只要簡單在瀏覽器中輸入，就可以直接下載該檔案。詳細就不講了，自己去 Google 這個名詞就會有[一堆網站](http://azo-freeware.blogspot.com/2006/03/hfs-20.html)。可是目前這個小工具雖然很方便，可是只有 Windows 版。其實說真的，Mac OS X 內建 Apache，[直接架個站](http://maczealots.com/tutorials/websites/)都可以了，放個單一檔只是小兒科。不過話又說回來，殺雞焉用牛刀嘛…

不過放心吧，Mac OS X 當然也有雞刀，而且同樣是內建的！首先打開終端機。

![](/media/blog/Terminal.png)

進到你想分享的檔案夾下，使用這行指令：

    python -m SimpleHTTPServer portnumber

SimpleHTTPServer 就是我們的程式名稱。前面的 python 代表這個程式是以 python 寫的。後面的 portnumber 是一個你指定的號碼，最好大於 1024 。如果留白，預設值是 8000。

這樣會把你終端機當下的檔案夾作為根目錄，發佈在 http://IP:portnumber 這個網址。例如如果我在 ~ 下面輸入 python -m SimpleHTTPServer 5000，那麼我的家目錄裡的檔案就會在 http://114.32.81.146:5000/ 下面，因為 114.32.81.146 是我家的 IP。沒那麼直覺（主要因為沒有圖形界面），不過平常使用也夠了。

只要終端機視窗開著，檔案共享就會持續進行；如果要停止，直接關終端機視窗，或者 ctrl c 中斷執行就行了。這個小東西相當方便，有需要的可以試試。