本文基於[這篇回應](https://www.ptt.cc/bbs/MacDev/M.1392287163.A.E62.html)。

## 溫故

首先我們複習一下怎麼繼承 `NSObject` 創建一個 class（以免有人 Xcode template 用太多忘了怎麼寫XD）：

```obj-c
#import <Foundation/Foundation.h>

@interface Answer : NSObject
@end

@implementation Answer
@end

int main(int argc, char const *argv[])
{
    id answer = [[Answer alloc] init];
    NSLog(@"%@", answer);
    [answer release];
    return 0;
}
```

這樣編譯：[^clang-compile-foundation]

```bash
$ clang answer.m -o answer -framework Foundation
```

執行結果類似這樣：

```bash
$ ./answer
2014-02-14 10:43:44.206 answer[76522:507] <Answer: 0x7f8fdb408200>
```

## 去除 `NSObject` 依賴

現在我們試著不繼承 `NSObject`。由於 `alloc`、`init`、`release` 的定義來自 `NSObject`（精確來說是來自 `NSObject` *protocol*，`NSObject` class 提供的只有實作），所以就不能用了。不過沒關係，我們先把定義搞出來。

```obj-c
@interface Answer
@end

@implementation Answer
@end

int main(int argc, char const *argv[])
{
    return 0;
}
```

編譯看看：[^clang-compile-objc]

```bash
$ clang answer.m -o answer -lobjc
```

可以過，但是 Clang 會吐出一個警告：

```bash
test1.m:1:12: warning: class 'Answer' defined without specifying a base class [-Wobjc-root-class]
@interface Answer
           ^
test1.m:1:18: note: add a super class to fix this problem
@interface Answer
                 ^
1 warning generated.
```

這是因為 Clang 在編譯 Objective-C 時，有幾個預設的 warning flags。`-Wobjc-root-class` 會在你沒有繼承任何 class 時觸發，因為絕大多數狀況下你都會想繼承 `NSObject` 或其子類別。

但我們這裡就是不想繼承它們啊！所以如果你確定要這麼做，當然可以 supress 這個警告。`NSObject` 本身就沒有父類別，所以 Apple 在實作的時候肯定動了什麼手腳。他們的[做法](https://code.google.com/p/cocotron/source/browse/Foundation/NSObject/NSObject.h)是用一個 `NS_ROOT_CLASS` macro 來修飾。這個 macro 的宣告在 `NSObjCRuntime.h`：[^nsobject-declaration]

```obj-c
#ifdef __clang__
#define NS_ROOT_CLASS __attribute__((objc_root_class))
#else
#define NS_ROOT_CLASS
#endif
```

所以其實只要這樣就可以讓 Clang 閉嘴：

```obj-c
__attribute__((objc_root_class))
@interface Answer
@end

@implementation Answer
@end

int main(int argc, char const *argv[])
{
    return 0;
}
```

不過（我覺得）比較好的方法是用 pragma 直接關掉這個警告：

```obj-c
#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Wobjc-root-class"

@interface Answer
@end

@implementation Answer
@end

#pragma clang diagnostic pop

int main(int argc, char const *argv[])
{
    return 0;
}
```

這樣 Clang 就會安靜了，而且也不會遇到其他編譯器（例如以前的 GCC Objective-C extension）沒有辦法識別 `__attribute__((objc_root_class))` declarative 的問題。

## Filling Out

我們加一個 method 進去，看看這個 class 是不是真的能用：

```obj-c
#import <stdio.h>

#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Wobjc-root-class"

@interface Answer
+ (int)answer;
@end

@implementation Answer
+ (int)answer
{
    return 42;
}
@end

#pragma clang diagnostic pop

int main(int argc, char const *argv[])
{
    printf("The answer is: %d\n", [Answer answer]);
    return 0;
}
```

注意因為我們沒有連結 Foundation 所以也沒有 `NSLog` 可用，所以我用 C 的 `printf`。編譯然後執行：

```bash
$ clang answer.m -o answer -lobjc
$ ./answer
The answer is: 42
```

真的能用！

不過這個 class 沒辦法實體化（instantiate），說真的算不上完整的 class，充其量只能算是…呃好像什麼都算不上，毫無反應只是個 method 放置器。

### 打地基

可以實體化的 Objective-C class 必須擁有一個 `Class isa` 成員（`isa` 代表「is a」），指向該 class 的 `Class` object。[^objc-class] 所以我們改寫一下宣告：

```obj-c
@interface Answer
{
    Class isa;
}
@end
```

### 蓋出物件

現在我們可以開始實作物件實體化的部分了。首先是宣告：[^strange-names]

```obj-c
@interface Answer
{
    Class isa;
}
+ (id)instantiate;
- (void)die;
@end
```

然後是實作：

```obj-c
+ (id)instantiate
{
    Answer *result = malloc(class_getInstanceSize(self));
    result->isa = self;
    return result;
}
```

Objective-C 物件的成員變數部分其實就是一個 C struct，直接用 `malloc` 就能建立。記得引入 `stdlib.h`。問題是要 allocate 多少記憶體？Objective-C 物件的大小因 Objective-C runtime 版本而異，不過規範上有一個內建函式 `class_getInstanceSize` 可以為你取得這個值。這個函式的定義在 `objc/runtime.h`，也要記得引入。

對了，在 Objective-C class method 裡 `self` 代表「目前的 class」，以防你在疑惑。:)

分配完記憶體後，我們就要填入正確的初始值。在這裡可以很明顯看到 Objective-C class 的成員部分真的就是一個 C struct，不要懷疑！

比較新版的 Clang 可能會對上面的程式有意見，因為直接修改 `isa` 成員不是什麼好事。你可以和上面一樣忽略它：

```obj-c
#pragma clang diagnostic ignored "-Wdeprecated-objc-isa-usage"
```

當然，記憶體用完要釋放：

```obj-c
- (void)die
{
    free(self);
}
```

### 使用

現在我們有一個可以實體化的 class 了。我們為它加上一個 property，然後實際用看看：

```obj-c
// ...

@property(assign, nonatomic) int value;

// ...

int main(int argc, char const *argv[])
{
    Answer *answer = [Answer instantiate];
    answer.value = 42;
    printf("The answer is: %d\n", answer.value);
    [answer die];
    return 0;
}
```

編譯並執行：

```bash
$ clang answer.m -o answer -lobjc
$ ./answer
The answer is: 42
```

完全可以用！完整的程式在[這裡](https://gist.github.com/uranusjr/8995334)，如果上面有不清楚的地方，可以再慢慢研究。

Happy hacking!


[^clang-compile-foundation]: 如果你看不太懂，`clang` 是編譯器名，`answer.m` 是源碼檔名，`-o answer` 代表輸出一個叫 `answer` 的程式，而 `-framework Foundation` 代表我們要連結 `Foundation` 這個 framework（以獲得 `NSObject` 的定義與實作）。

[^clang-compile-objc]: 我們現在不需要連結 Foundation Framework，不過只要是 Objective-C 程式都必須連結 libobjc 這個函式庫，所以我們要加上 `-lobjc`。

[^nsobject-declaration]: 連結是 [Cocotron](http://www.cocotron.org) 的宣告，不過 Apple 的版本也一樣，可以看你自己電腦裡的 `/System/Library/Frameworks/Foundation.framework/Headers/NSObject.h`。

[^objc-class]: 如果你不太熟 Objective-C 但是熟悉其他的物件導向語言，`Class` object 是用來儲存 Objective-C class 的 metaclass，讓 Objective-C 實體可以擁有 introspection 能力。這個形態的宣告是 `typedef struct objc_class *Class;`，其實只是一個 pointer to a struct。

[^strange-names]: 為了顯示這個 class 的特殊性，我特意用了不一樣的 method 名，不過它們的作用應該還是很明顯。
