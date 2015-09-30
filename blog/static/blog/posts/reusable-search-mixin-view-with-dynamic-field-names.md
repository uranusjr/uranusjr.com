[本周的 Django Workshop（2013-12-24）](http://www.meetup.com/Taipei-py/events/154717332/) 講到了 [*Two Scoops of Django*](https://django.2scoops.org) 第九章： *Common Patterns of Forms*。Alfred 在最後提到書上有一個 *Reusable Search Mixin View*，但是說以他自己的狀況而言，因為跨 model 的 field names 通常不一樣，所以這個 pattern 比較派不上用場。

當時我補了一句「其實這個還是有解」，本來打算稍後討論的時候提出來，不過後來被 Andy 拱上去講 naming convention 就完全忘了這件事，直到現在。 orz

所以我現在要來彌補這個錯誤。

為了那些沒有看過 *Two Scoops of Django* 的人（如果你覺得自己算是個 Django programmer，我強烈建議你[馬上買來看](https://django.2scoops.org)），Reusable Search Mixin View 是這樣的概念：我們通常會想在網站上做某個 model 的搜尋結果頁面，而且可能會有不止一個 model 需要能搜尋。與其為每個 model 建立一個 view class 來顯示，不如寫一個這樣的 mixin：

```python
# core/views.py
class TitleSearchMixin(object):
    def get_queryset(self):
        # Fetch the queryset from the parent’s get_queryset 
        queryset = super(TitleSearchMixin, self).get_queryset()
        # Get the q GET parameter
        q = self.request.GET.get("q")
        if q:
            # return a filtered queryset 
            return queryset.filter(title__icontains=q)
        # No q is specified so we return queryset 
        return queryset
```

然後你就可以這樣建立搜尋結果頁：

```python
# add to stores/views.py 
from django.views.generic import ListView 
 
from core.views import TitleSearchMixin 
from .models import Store 
 
class IceCreamStoreListView(TitleSearchMixin, ListView): 
    model = Store
```

 

```python
# add to flavors/views.py 
from django.views.generic import ListView 
 
from core.views import TitleSearchMixin 
from .models import Flavor 
 
class IceCreamFlavorListView(TitleSearchMixin, ListView): 
    model = Flavor
```

這樣做的好處是，你根本不用寫 form！只要做兩個 templates：

```xml
{# form to go into stores/store_list.html template #} 
< form action="" method="GET"> 
    <input type="text" name="q" /> 
    <button type="submit">search</button> 
</form>
```

 

```xml
{# form to go into flavors/flavor_list.html template #} 
< form action="" method="GET"> 
    <input type="text" name="q" /> 
    <button type="submit">search</button> 
</form>
```

就搞定了！不論使用者 submit 哪一個 form，都可以被 `IceCreamStoreListView` 處理。

上面的 pattern 有一個先決條件：`Store` 和 `Flavor` 要被搜尋的欄位都必須叫做 `title`。你可能不想要，甚至不能有這個限制。所以我們要把這個欄位名變成動態的，可以讓我們自己指定。

首先我們要改寫 `TitleSearchMixin`。因為現在不一定只能搜尋 title 了，順便也改個名吧（因為[名詞需要多多重構](https://speakerdeck.com/uranusjr/naming-convention-in-python?slide=12)！）：

```python
class FieldSearchMixin(object): 
    def get_queryset(self): 
        queryset = super(TitleSearchMixin, self).get_queryset() 
        q = self.request.GET.get("q") 
        if q: 
            filters = {field_name + '__icontains': q}
            return queryset.filter(**filters) 
        return queryset
```

這樣只要換掉 `field_name`，就可以搜尋任何你想要的欄位。

下一步就是要想辦法拿到 `field_name` 的值。這有很多種方法，最無腦的是加一個 form field：


```xml
< form action="" method="GET"> 
    <input type="text" name="q" /> 
    <input type="hidden" name="field_name" />
    <button type="submit">search</button> 
</form>
```

 

```python
class FieldSearchMixin(object): 
    def get_queryset(self): 
       field_name = self.request.GET.get("field_name")
       # 後面省略
```

但是這非常不安全，因為你永遠都[不該相信 user input](https://www.owasp.org/index.php/Don%27t_trust_user_input)，更何況這邊是用 `GET`，在網址列都被看光光了。

好一點的寫法是放在 view class 裡面：

```python
class FieldSearchMixin(object): 
    def get_queryset(self): 
       field_name = self.field_name_to_search
```

 

```python
class IceCreamFlavorListView(TitleSearchMixin, ListView): 
    model = Flavor
    field_name_to_search = 'title'
```

但是仍然有點問題，因為 class attribute 有被其他人複寫的風險；這個欄位名明明就只有在 `get_queryset` 用到，這樣寫就...就少了一個 class attribute name 可以用，很不方便。不論如何，變數的 scope 本來就應該[越小越好](http://www.google.com/search?q=limit+variable_scope)。最理想的方法應該是使用 [factory method pattern](http://en.wikipedia.org/wiki/Factory_method_pattern)：

```python
def field_search_mixin_factory(field_name):
    class FieldSearchMixin(object): 
        def get_queryset(self): 
            queryset = super(TitleSearchMixin, self).get_queryset() 
            q = self.request.GET.get("q") 
            if q: 
                filters = {field_name + '__icontains': q}
                return queryset.filter(**filters) 
            return queryset
    return FieldSearchMixin
```

然後這樣用

```python
class IceCreamFlavorListView(field_search_mixin_factory('title'), ListView): 
    model = Flavor
```

很神奇嗎？Python [就是這麼神奇](http://xkcd.com/353/)！