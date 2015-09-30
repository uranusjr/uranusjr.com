這是我從 Yorkxin（duckseven @ ptt.cc）那邊偷來的。他用 AppleScript 和兩個命令列程式[寫了一個繁簡轉換程式](http://chitsaou.wordpress.com/2008/12/30/scpt-to-convert-zh-hans-and-hant-for-itunes/#comment-6183)，但他認為還需要改善。

我本來推薦他試試 [AppleScript Studio](http://developer.apple.com/documentation/applescript/conceptual/studiobuildingapps/chapter02/chapter_2_section_2.html#//apple_ref/doc/uid/20001249-TPXREF134) 作為拖拉放的解決方案，但後來我想想發現不太對勁，他這裡想達成的功能並不需要用到這個，只要用 droplet 就能有類似的效果。當初他在開發這個程式（因為 ptt Mac 板有人問）的時候我也有找過相關資料，不過因為那陣子沒空所以沒有完全做出來，所以趁這次機會，我嘗試改寫了一下他的程式。

既然只是改成 droplet，改寫是簡單的，而為了以比較簡短的程式碼保留原本的直接執行功能，我用了兩個 subroutine 取代原本的程式。但我發現他用的是 Unix 套件 autoconvert，而我當初並沒有編譯這個套件。這個差別的原因是，我當初是從[這裡](http://www.oikos.com.tw/v4/viewtopic.php?id=3402)找到資料，所以使用了另外修改過的 [autoconvertx](http://homepage.mac.com/ulyssesric/warehouse/FileSharing5.html)。為了程式可攜性，既然我已經把腳本包成 droplet，乾脆一不做二不休把 autoconvertx 套件也一併包進去做成 droplet bundle，這樣使用者就不需要另外安裝套件，直接執行這個程式就行。

這部份的改寫比較複雜，因為 autoconvertx 的語法和原本略有不同，所以我更動了一些設定部份，順便乾脆把一些參數一起拿出來另外設定。讀程式碼比起自己寫痛苦得多，而且每個人的寫法都不太一樣，為了新舊程式碼相容反而花了我好多時間 — 不過最後成果是值得的。

基本機能還是繼承本來的程式，而我手上幾乎沒有中文歌可以測試，所以不確定現在的程式會不會有原本轉錯字的問題，不過我想八成仍然有。雙引號的問題當然也存在，這個我暫時不太想去解決就是了。

最後的程式可以從[這邊](/media/blog/iTunes%20Song%20Name%20Converter%20between%20Chinese%20Varients.app.7z)下載。如果要直接執行，請在 iTunes 選擇你想轉換的曲目，再雙擊執行這個程式。若要以 droplet 方式執行，請直接將 Finder 檔案或 iTunes 曲目拖到程式圖示上放開，程式會直接執行。

要注意的是，因為只有 iTunes 有 ID3 tag 的讀取套件，所以即使你拖曳 Finder 檔案執行 droplet，**歌曲仍然會被加入 iTunes 資料庫**。你可以在轉換完畢後手動移除，但若你的 iTunes 設定為在輸入時複製檔案至 iTunes Library，名稱被轉換的將是資料庫裡的檔案，而非原本的檔案，請注意。

下載點：[iTunes Song Name Converter between Chinese Varients](/media/blog/iTunes%20Song%20Name%20Converter%20between%20Chinese%20Varients.app.7z) (7z, 492.4 KB)