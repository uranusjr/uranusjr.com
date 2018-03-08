網頁的下拉式導覽列這大家都很熟了，路上隨便撿個前端 toolkit 都有，沒什麼技術。不過剛好最近又有機會做 PyCon Taiwan 新網站，就想來試試看不一樣的新玩法寫點心得。

我自己堅持的需求有兩個：

1. 沒有 JavaScript 也要能用。
2. 在觸控裝置上也要能用。

第一項應該很多人被我煩過 XD 被講過很多次這年頭沒人不開 JavaScript 看網頁，但是我覺得這一來是個原則問題，二來 JavaScript 或 CSS 下載出錯還是很可能發生（可能我家網路太爛）。PyCon Taiwan 官網從 2016 開始基本上都是用 progressive enhancement 原則下去做（更之前我沒參與）。

第二項可能比較不直觀。比較常看到的做法是根據 breakpoint 分手機平板桌面，然後在前兩者用不同的介面。根據這種想法，最大的螢幕屬於桌面系統，所以會用只有滑鼠辦得到的手勢展開選單[^desktop-only-gesture]。這是過時的想法。

[^desktop-only-gesture]: 例如 hover。

我在今年網站也第一次用了[新發現的 breakpoint 邏輯](https://medium.freecodecamp.org/the-100-correct-way-to-do-css-breakpoints-88d6a5ba1862)。不是這篇的重點，不過我還是想推薦這篇，請務必讀連結內文。總之我在找合適 breakpoint 時發現，在 2018 年根本沒辦法找到明確的 tablet-desktop 分界點。即使不論 Windows 觸控筆電，iPad Pro 直拿的寬度就已經是 1024px，更不要說橫拿高達 1366px，已經比我自己平時在筆電慣用的設定還寬[^browser-width]！在這個寬的介面使用 mobile navigation 完全不合理，而我們也不方便維護三種互動介面。我們別無選擇，只能讓這個介面同時適用於滑鼠與觸控。

[^browser-width]: 我通常把瀏覽器固定在 1235px。


## 往年的做法

JavaScript-free 下拉選單其實也不是什麼新鮮事。所有瀏覽器[^all-browsers]都支援 `:hover` pesudo class，所以很容易就能寫出這種效果：

[^all-browsers]: 所有「人類應該使用的」瀏覽器。

<div data-height="400" data-theme-id="0" data-slug-hash="zRbWyK" data-default-tab="css,result" data-user="uranusjr" data-embed-version="2" data-pen-title="Hover-based Dropdown" data-preview="true" class="codepen">See the Pen <a href="https://codepen.io/uranusjr/pen/zRbWyK/">Hover-based Dropdown</a> by Tzu-ping Chung (<a href="https://codepen.io/uranusjr">@uranusjr</a>) on <a href="https://codepen.io">CodePen</a>.</div>

但是這在觸控裝置顯然不可行。在觸控裝置唯一合理的手勢是按壓。我們需要一個用按壓切換的 pseudo class。

有這種東西？


## 只能用按的

我們需要實作的行為是 toggling：按一下打開下拉，再按一下把下拉收起來。按壓這個動作本身沒有 context，所以我們需要自己在頁面上管理開閉狀態。不用 JavaScript 存狀態，那就是 form input 了。恰好 HTML 標準就有一個完美的 toggler：

<label><input type="checkbox"> 按我切換狀態</label>

用一個隱藏的 checkbox 記錄狀態搭配 sibling combinator（`~`），效果會像這樣：

<div data-height="265" data-theme-id="0" data-slug-hash="rJRvEd" data-default-tab="css,result" data-user="uranusjr" data-embed-version="2" data-pen-title="Clicked-based Dropdown" data-preview="true" class="codepen">See the Pen <a href="https://codepen.io/uranusjr/pen/rJRvEd/">Clicked-based Dropdown</a> by Tzu-ping Chung (<a href="https://codepen.io/uranusjr">@uranusjr</a>) on <a href="https://codepen.io">CodePen</a>.</div>

順帶一提，常常看到有人忽略了 `<label>` 的 `for` 屬性。這會讓使用者可以按 `<label>` element 來 focus input，而不需要對準那個小不拉機的元件。這在 checkbox 與 radio button 特別明顯，但是其他的表單元件也都可以使用。

總之，這樣的選單就可以保證功能性，只要裝置能按東西就能用。接下來就是加強使用者體驗——總算可以用 JavaScript 啦！


## [漸進增強](https://zh.wikipedia.org/wiki/渐进增强)

這個介面最大的問題是需要按一下才能收合。所以使用者能夠同時開好幾個選單，然後一定要移回去按選單才能收起來，很不方便。這裡有兩個 enhancements 可以做：

1. 按其他項目時，把現在這個收起來
2. 按螢幕其他地方時，把所有選單收起來

PyCon Taiwan 網站用 [Stimulus] 這個 framework，不過這裡為了簡單起見，我直接用 vanilla JavaScript 寫。

[Stimulus]: https://stimulusjs.org

<div data-height="265" data-theme-id="0" data-slug-hash="PQLBZE" data-default-tab="css,result" data-user="uranusjr" data-embed-version="2" data-pen-title="Clicked-based Dropdown with Exclusive Selection" class="codepen">See the Pen <a href="https://codepen.io/uranusjr/pen/PQLBZE/">Clicked-based Dropdown with Exclusive Selection</a> by Tzu-ping Chung (<a href="https://codepen.io/uranusjr">@uranusjr</a>) on <a href="https://codepen.io">CodePen</a>.</div>

注意 label 的事件在這裡被特別濾掉了。這是因為按 label 本來就會取消勾選 `for` target（HTML 原生行為），我們不需要手動再做一次。如果我們太雞婆，反而會讓 `for` target 的狀態不符預期，而無法取消勾選狀態（你可以自己試試看）。

這就是個很棒的選單了。但它不符合使用者期望。


## 找回 Hover 功能

前面說過，觸控式裝置使用者只有一種合理的功能手勢：按壓。不過如果是桌面裝置，或許還是可以把 hover 做回來。我覺得要用 hover 還是 click 開啟是個人偏好；我個人偏好永遠只用 click——如果你去看各大內容網站，只用 click 顯示選單的佔了壓倒性多數——不過偏好 hover 也不是問題；只要記得**不要讓 hover 成為唯一手段**，保留 click 可行性即可。

在這種前提下，用 hover 開啟選單也是個嚴格漸進增強（strictly progressive enhancement）功能，所以可以用 JavaScript 來做。移入的邏輯很簡單：在接收到 mouseover 事件時，自動把 checkbox 勾起來就是了：

```javascript
el.addEventListener('mouseover', () => {
  el.querySelector('input').checked = true
})
```

移出時要自動收合就比較麻煩。直覺會想到 mouseout，但是這個事件在游標「從 parent 移到 child」時，會在 parent 被觸發。在我們的狀況中，這就代表你 hover 打開，接著把游標移到下拉選單上時，checkbox 就會被清除，讓選單被收合。完全無法使用啊畜生！

如果你只想支援 IE (!?)，可以用微軟特有的 mouseleave 事件。或者你可以用 jQuery，它可以在瀏覽器上模擬 mouseleave 行為。否則你就需要自己寫一些 hack 來達成類似效果。我採用的做法是

1. 在 mouseout 結束時，偵測目前游標下面有什麼元素。
2. 如果這些元素包含目前被選取的選單，忽略這個事件。
3. 只有在確定游標下面沒有目前被選取的選單時，才把該選單關掉。


## 完成

最後的結果大概像這樣：

<div data-height="265" data-theme-id="0" data-slug-hash="PQLBZE" data-default-tab="js,result" data-user="uranusjr" data-embed-version="2" data-pen-title="Clicked-based (but hoverable) Dropdown with Exclusive Selection" data-preview="true" class="codepen">See the Pen <a href="https://codepen.io/uranusjr/pen/PQLBZE/">Clicked-based (but hoverable) Dropdown with Exclusive Selection</a> by Tzu-ping Chung (<a href="https://codepen.io/uranusjr">@uranusjr</a>) on <a href="https://codepen.io">CodePen</a>.</div>

如果你現在去 [PyCon Taiwan 2018 網站](https://tw.pycon.org/2018/)，上面的選單除了一些花俏的效果（通通都是 CSS animation）之外，基本上就是這樣做的。所有螢幕都表現得超完美，關掉 JavaScript 也毫無死角呢 (´◉◞౪◟◉)ﾄﾞﾔ

如果你在任何狀況發現選單無法使用[就來回報啊](https://github.com/pycontw/pycontw2016/issues)。來啊，如果你真的有東西可以回報！賭你找不到辣！！


<script async src="https://static.codepen.io/assets/embed/ei.js"></script>
