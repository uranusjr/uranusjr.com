最近工作上最主要的 project 是一個大量使用 `asyncio` 的 Python service。這個 project 從前年就有規劃（真正開始執行是去年起），我是從那時候開始認真研究 Python 上的 async programming，去年也用相關的研究內容發了幾場演講。

過了一年多，雖然也是有在做其他事情，但這個專案還是佔去我工作上很多時間，也學到很多東西。最主要的心得會放在下個月 PyCon Taiwan 2016 的演講裡，可以期待一下。不過今天遇到了一個特別的問題，研究了一下終於找到解法，就先簡單紀錄。

## 遇到的問題

我的 service 需要每隔一段時間（例如一小時）執行一個 coroutine。大概是這樣：

~~~python3
import asyncio
import functools

from .somewhere import do_thing


async def do_periodical_thing():
    await do_thing()

def schedule_periodical_thing(loop):
    loop.call_later(60 * 60, do_periodical_thing)

def start_doing_thing_periodically(loop):
    task = loop.create_task(do_periodical_thing())  # Do this once.
    task.add_done_callback(functools.partial(schedule_periodical_thing, loop))


# Program entry point looks like this. I'm not going to discuss this part
# because it is basically boilerplate, and not related to my problem.
loop = asyncio.get_event_loop()
start_doing_thing_periodically(loop)
loop.run_forever()
~~~

我想要為這段程式寫個 unit test。我想知道它能不能確實

1. 在執行時立刻做一次事情；
1. 在正確的 delay 後觸發下一次事情。

第一個部分很簡單，只要用 `pytest-asyncio` 搭配 `unittest.mock`（我通常會用 `pytest-mock`，不過為了簡單起見，這裡就拿掉了）即可：

~~~python3
import unittest.mock
import pytest
import myapp


@pytest.mark.asyncio
def test_start_doing_thing(event_loop):
    with unittest.mock.patch('myapp.somewhere') as mock_somewhere:
        myapp.start_doing_thing_periodically(loop=event_loop)
        await asyncio.sleep(0)  # Let the event loop process our task.

        mock_somewhere.assert_called_once_with()    # This is called!
~~~

第二部分要測試很簡單啦，加個 `await asyncio.sleep(60 * 60 + 1)` 然後看有沒有執行第二次就好了。唯一的問題是你的測試會跑一小時。


## 思路

首先我們必須了解 `asyncio` 的 delay 原理（其實所有的 async framework 應該都差不多）。在寫 synchronous 程式時，如果我們想要「等待一段時間，然後執行一個工作」，只要簡單用一個等待指令（Python 通常是 `time.sleep()`），然後再跑下一個指令；但在 asynchronous 程式中，你的等待指令會阻塞 event loop，使原本異步的其他工作無法執行。

在 `asyncio` 中，解決方法是 `asyncio.call_later()`： 當你用它新增一個 task 時，event loop 會紀錄目前的時間 \\(t_0\\)， 並根據你需要的 delay \\(\Delta t\\)，知道它應該在時鐘走到 \\(t_0 + \Delta t\\) 之後執行 task。當 event loop 處理事件時，會不斷檢查時鐘，在發現 scheduled task 的時間已到時執行它。

> 敏銳的人可能已經發現：我不是說「當」走到 \\(t_0 + \Delta t\\)，而是走到「之後」。對，異步程式並無法保證 task 何時執行，而只能保證之後會執行——如果時間到的時候 event loop 正忙著做其他事情，則 task 必須先等它完成。這和例如硬體的 interrupt 不太一樣。在絕大多數狀況下這個差異很小，但還是需要記得。


## 解法

知道這個原理之後，我們就可以實作時光機。好啦，說時光機有點誇張了，不過我們至少可以修改 event loop 的時鐘，達到「快轉」的效果。

我的解法是這樣：

~~~python3
import asyncio

class FastForwardableEventLoop(type(asyncio.new_event_loop())):

    def __init__(self):
        super().__init__()
        self._fast_foward = 0.0

    def time(self):
        return super().time() + self._fast_foward

    def fast_forward(self, secs):
        self._fast_foward += secs
~~~

`asyncio` 的 event loop 是用一個 public API `asyncio.BaseEventloop.time()` 取得目前的時間（實作使用 `time.monotonic()`，不過這不重要）。我們新增了一個快轉 method，並加上一個 attribute 來記錄。當任何元件向我們詢問時鐘的時間時，我們就把這個快轉秒數加上去。

有了這個，我們就可以在測試中跳過一段時間：

~~~python3
@pytest.fixture
def event_loop():
    """Shadow pytest-asyncio's fixture to use our own event loop.
    """
    policy = asyncio.get_event_loop_policy()
    policy.get_event_loop().close()
    event_loop = FastForwardableEventLoop()
    policy.set_event_loop(event_loop)
    request.addfinalizer(event_loop.close)
    return event_loop


@pytest.mark.asyncio
def test_start_doing_thing_periodically(event_loop):
    with unittest.mock.patch('myapp.somewhere') as mock_somewhere:
        myapp.start_doing_thing_periodically(loop=event_loop)
        await asyncio.sleep(0)
        mock_somewhere.assert_called_once_with()

        # Wait for an hour. We yield before dialing the clock to make sure
        # the call_later task is really scheduled.
        await asyncio.sleep(0)
        event_loop.fast_forward(60 * 60)

        await asyncio.sleep(0.1)    # Delay a little to avoid resolution error.
        assert mock_somewhere.method_calls == [
            unittest.mock.call(),
            unittest.mock.call(),
        ]

        # Wait again.
        await asyncio.sleep(0)
        event_loop.fast_forward(60 * 60)

        await asyncio.sleep(0.1)
        assert mock_somewhere.method_calls == [
            unittest.mock.call(),
            unittest.mock.call(),
            unittest.mock.call(),
        ]
~~~

保險起見，我們在一小時後多等了一下下，因為 `asyncio` 因為 timer 可能有一點誤差。確實 `mock_somewhere` 會在一小時過後被呼叫一次。完成！繼續下一個 feature 吧。

---

Asynchronous programming 確實可能和你習慣的 Python 程式寫法不太一樣，也需要一些更特定的 domain knowledge。而且這不只是在寫程式本身時如此——在測試時，也同樣要考量這個問題，而且由於單元測試要求你 isolate 程式的各個元件，也就更考驗你對 framework 本身的了解。

雖然 async programming 真的非常方便，可以解決很多問題，但它也同時為你帶來新的考驗。當你遇到問題，而思考它是否能作為 solution 時，也就務必需要考慮除了它本身的功能外，對你的程式會帶來什麼連帶影響。至於你該注意哪些 check points 才能做決定，或者當你確定要寫 async 程式時，又該注意哪些事情，就請下個月參加 PyCon Taiwan 吧，我到時候會告訴你。:p
