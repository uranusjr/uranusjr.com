昨天在 PTT 遇到了一個問題，有人想知道為什麼下面的程式碼：

```objective-c
NSString *aString = @"a";
NSString *bString = @"b";
bString = aString;
NSLog(@"bString = %@", bString);
aString = @"c";
NSLog(@"aString = %@", aString);
NSLog(@"bString = %@", bString);
```

出來的結果是

    bString = a
    aString = c
    bString = a

主要的問題是，把 `bString` 的指標指向 `aString` 的物件後，當修改 `aString` 指向物件的值時，不是就等於修改 `bString` 指向物件的值嗎？為什麼感覺 `bString = aString` 這行只有把 `aString` 的值傳遞給 `bString`，而不是改變指向的物件？

事實上這是語言行為的問題。會這樣問，是因為把 Objective-C 中指定字串常量給變數的寫法，與 C++、或者 Java 等語言的寫法搞混了。Objective-C 承襲自 [Smalltalk](http://zh.wikipedia.org/zh-tw/Smalltalk) 的一個基本概念是「everything is an object」，包括字面常量在內。一個最簡單的例子可以從上面連結維基百科中的例子看出來。由於常量本身也是一個物件（的指標），如

```objective-c
NSString *aString = @"a";
```

這樣的程式碼，代表**宣告一個 `aString` 變數，其型態為 `NSString *`，並將其初始化，指向一個值為 `a` 的字面常量物件**。注意這和（例如）C++ 的類似程式碼完全不同。在 C++ 中，如

```c++
string aString = "a";
```

這樣的程式碼，代表**建立一個 `aString` 變數，其型態為 `string`，並將其字串值初始化為 a**。這樣或許看不出來有什麼不同，但如果我們接著寫下去：

```objective-c
aString = @"c";
```

在 Objective-C 中代表**將 `aString` 的值改變為指向一值為 `c` 的字面常量物件**。而

```c++
aString = "c";
```

在 C++ 中則是**將 `aString` 的字串值修改為 `c`**。這樣就會造成完全不一樣的行為。

從下面的兩個例子，就可以很明顯看出差異。首先是 Objective-C：

```objective-c
#import <Foundation/Foundation.h>

int main (int argc, const char *argv[])
{
    NSAutoreleasePool *pool = [[NSAutoreleasePool alloc] init];
    NSString *aString;
    NSLog(@"0x%llx", aString);
    aString = @"a";
    NSLog(@"0x%llx", aString);
    aString = @"b";
    NSLog(@"0x%llx", aString);
    [pool drain];
    return 0;
}
```

結果將類似：

    0x7fff5fbff7f8
    0x100001088
    0x1000010a8

我們每次指定新的字面常量時，都會改變 `aString` 指向的物件。而 C++：

```c++
#include <iostream>
#include <string>

int main(int argc, const char *argv[])
{
    using namespace std;
    string aString;
    cout << &aString << endl;
    aString = "a";
    cout << &aString << endl;
    aString = "b";
    cout << &aString << endl;
    return 0;
}
```

的結果則會類似

    0x7fff5fbff640
    0x7fff5fbff640
    0x7fff5fbff640

我們只是不斷改變同一個物件的字串值。

回到前面的程式碼。當 `aString = @"c"` 時，我們並不是修改 `aString` 指向之物件的值，而是把 `aString` 這個指標指向另一個物件。這時，因為 `bString` 仍然指向本來的物件（`@"a"`），所以當我們把這兩個變數指向物件之值印出時，結果就會不一樣。

那麼，如果我們想同時改變 `aString` 和 `bString`，要怎麼改寫這段程式呢？既然知道了原理，我們只要用對應的寫法，寫出這個行為就行了。也就是說，我們必須使用 `NSMutableString` 的 `-setString:` 方法，寫成這樣：

```objective-c
NSMutableString *aString = [NSMutableString stringWithString:@"a"];
NSMutableString *bString = [NSMutableString stringWithString:@"b"];
bString = aString;
NSLog(@"bString = %@", bString);
[aString setString:@"c"];
NSLog(@"aString = %@", aString);
NSLog(@"bString = %@", bString);
```

就可以得到我們想要的結果：

    bString = a
    aString = c
    bString = c

所以，今天的格言是，東西看起來很像，並不代表它們一樣。或者應該說，這世界上沒有一模一樣的東西，當我們想用歸納法類比時，請特別注意。
