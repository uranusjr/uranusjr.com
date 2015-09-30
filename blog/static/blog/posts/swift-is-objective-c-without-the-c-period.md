蘋果在美國時間週一發表了新的程式語言 Swift，然後 Internet 就高潮了，突然冒出一堆鍵盤語言專家（包括我自己）爭先恐後發表自己的看法。或許因為每個人都有自己不同的背景，而且 Objective-C 本身也不是很多人特別熟悉的語言，所以看法似乎頗為分歧，甚至連原以已經在 OS X/iOS 界的工程師似乎也不是完全理解。這裡是一些我自己的想法，其中不少是針對我覺得大家對於 Swift、Objective-C、甚至蘋果本身的誤解。

該從哪裡開始呢？嗯…

## Swift 是編譯語言，但這不代表他不如你最喜歡的腳本語言

沒錯，Swift 有獨立的編譯器，而且需要被編譯才能執行。但這不代表他比不上那個腳本語言（請自行對號入座）。畢竟不管怎麼說，絕大多數腳本語言的主流實作都會在 runtime 時及時將源碼編譯為 bytecode 才交由直譯器執行，而 Swift 的編譯器基於 LLVM（如同近期大多數的語言），與一般腳本語言在實務上的差異其實只有編譯是否自動而已。

不論你打算將 Swift 用於 iOS 或 OS X apps（目前除了這些大概 Swift 也沒什麼其他用途），都需要對你的最終成品進行額外處理，例如打包、key signing（除非你不上 App Store）等等。蘋果在這部分的手續超級繁雜，一般而言都需要 IDE 輔助。既然有 IDE 存在，編譯這件事情造成的 overhead 其實很小。如果你看了 WWDC 展示的 Swift Playground，它及時反應源碼修改的能力其實和直譯器的差距沒那麼大。既然這個步驟本身對開發流程影響不大，它就是加分了。編譯還是能帶來很多好處；以 Swift 而言，除了可以進行語法檢查之外，還可以帶來許多最佳化（尤其 Swift 使用靜態型別）。以蘋果的定位，Swift 必須被用在效能吃重的場合，所以這很重要。

編譯本身不是罪，蘋果只是選擇了適合 Swift 用途的路。但這只是實作。當然 Swift 目前看來似乎是 proprietary language，所以這個實作就是一切；不過就語言本身而言，編譯與否仍然不是很重要。但語言本身嘛…

## Swift 應該沒有大量借鑑你想的那個語言

Swift 本身有不少有趣的特點，讓許多人開始討論它究竟從什麼語言<ruby>借<rt>ㄔㄠ</rt>鑑<rt>ㄒㄧˊ</rt></ruby>了什麼概念。包括 Rust 的原設計者都有些想法。但這些想法還是有點偏差，甚至一部份根本是錯的。

很明顯因為對程式語言歷史毫無概念產生的錯誤（Generics 源自 C#？別鬧了吧。）就跳過，多數誤解似乎還是源自於很多人（即使 Objective-C programmers）其實不特別熟 Objective-C。可能是一廂情願，不過我認為如果想理解 Swift 風格背後的理由，必須先理解 Objective-C。

### 從 Objective-C 物件到 Swift 物件

在 Swift 中，幾乎所有的 object instances 都是以 reference 參照。沒有指標。這其實應該就是延續 Objective-C 的做法而已。所有的 Objective-C 物件都必須在heap 上被 allocated，在程式碼中永遠是以指標參照：

~~~obj-c
// aString 指向一個在 heap 上被建立，形態是 NSString 的物件實例。
NSString *aString = [[NSString alloc] init];
~~~

這在 Swift 裡就直接對應到物件參考：

~~~obj-c
// aString 指向一個（應該也是）在 heap 上被建立的 String 物件實例。
let aString = String()
~~~

當然，Objective-C 本身偶爾也會用到 pointer to a pointer。但通常是用來回傳多個值，或者作為 error-handling 的手段。Swift 可以把變數組成 tuple 輕鬆回傳多個值，所以這種需求其實不大。在真的有必要時，也有 inout 參數可以用。

由於 Objective-C 物件永遠是用指標參照，所以 nil（空指標）就被用來代表物件不存在。推到 Swift 上就是 optionals 了。當然語法本身肯定是有<ruby>借<rt>ㄔㄠ</rt>鑑<rt>ㄒㄧˊ</rt></ruby>別人，不過概念上還是很必然。

前面說「幾乎」所有的 Swift 變數都是物件參考。例外就是 struct。這或許受到 C# 的用法影響，不過無論如何都很明顯源自 C 的 structure。Objective-C 在很多地方使用 struct 描述 POD，所以它有專屬的 type 或許也很合理。

順帶一提，雖然文件好像都沒有特別提，不過我個人猜測 Swift 的 error-handling 應該還是和 Objective-C 一樣基於 return codes 和 error messages。由於使用同樣的 runtime（據蘋果說），Swift 的 exceptions 應該也和 Objective-C 類似，可能得避免使用。

### 參數冠名（Argument Names）延續了 Objective-C 的 Method 語法

Objective-C 的 method 語法非常特殊，喜歡的人很愛，討厭的人也很多。在 Objective-C 中，method 被呼叫時，signature 本身和傳入參數會互相交織。例如如果有個發送 email 的 method，可能就會長成這樣：

~~~obj-c
// 送出一封標題為 "Hello"，內容為 "This is a test message." 的信件。
// 寄件人為 me，收件人為 user1 與 user2。
[mailSender sendMailWithTitle:@"Hello"
                      content:@"This is a test message."
                         from:me
                           to:@[user1, user2]];
~~~

第一眼看上去可能很怪，但可讀性卻非常高。在 Swift 中，同樣作用的 method 可能會這樣宣告：

~~~swift
func sendMail(title: String, content: String, from: User, to: User[]) {
    // 實作…
}
~~~

然後這樣用：

~~~swift
sendMail("Hello", "This is a test message.", me, [user1, user2])
~~~

這和大多數程式語言的語法相符，但 Objective-C programmers 應該會覺得可讀性變差了。如果使用 parameter names，就可以這樣寫：

~~~swift
func sendMailWithTitle(
        title: String, content: String, from: User, to: User[]) {
    // 實作…
}
~~~

然後

~~~swift
sendMailWithTitle("Hello",
          content:"This is a test message.",
                           from:me,
               to:[user1, user2])
~~~

有沒有比較開心！至少我有。:D 當然這個 syntax 本身還是有可能是參考其他語言而來，不過精神上肯定是從 Objective-C 傳承來的。

## Swift 在概念上就是 Objective-C

Swift 的很多概念根本是從 Objective-C 照抄的。這在很多地方都看得出來。我在 PTT 講過記憶體管理，另外單繼承與 protocols 的概念也是如此（而不是來自 C#）。當然這有好有不好，不過至少對於已經熟悉 Objective-C 的人而言，這應該非常親切。

蘋果在設計 Swift 時，完全沒有改變它背後的理念，只是為了這些理念創造了全新的語言，而不再繼續使用基於 C，而需要背負許多包袱的 Objective-C。你從 Objective-C 學到的東西還是能夠繼續使用，只是因為它們現在不再基於 C，而會有些語法上的變化（通常是簡化）。

Tim Cook 在 keynote 講的話不是效果而已，其實 Swift 真的就是 Objective-C without the C 啊。

![Objective-C without the C](http://www.blogcdn.com/www.engadget.com/media/2014/06/wwdc2086.jpg)
