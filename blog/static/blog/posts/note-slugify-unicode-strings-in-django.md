Django 的 `slugify` filter 不支援 Unicode（把非 ASCII 字元傳進去會直接被忽略）。可能的輔助工具：

## slugify_unicode

[Mezzanine] 從 Mozilla 的 [unicode-slugify] 改寫而來，位於 `mezzanine.utils.urls`。不需要額外函式庫。

```python
    import re
    import unicodedata
    from django.utils.encoding import smart_unicode

    def slugify_unicode(s):
        chars = []
        for char in unicode(smart_unicode(s)):
            cat = unicodedata.category(char)[0]
            if cat in "LN" or char in "-_~":
                chars.append(char)
            elif cat == "Z":
                chars.append(" ")
        return re.sub("[-\s]+", "-", "".join(chars).strip()).lower()
```

會直接把非 ASCII 字元進行 URL encoding 後送出。優點：可讀性不錯，尤其如果瀏覽器會自動解碼網址列，可以直接看到原本的標題。缺點：如果沒有自動解碼，網址列會是一團（對使用者而言）莫名其妙的東西；如果有解碼，則該字串並非真正的網址，如果拿去貼到某些地方（例如 BBS）會無法正確識別。

## unidecode

[這篇文章](http://stackoverflow.com/questions/702337/)有提到一些其他的解法。[unidecode] 這個套件可以把非 ASCII 字元以合理的邏輯轉換成 ASCII 字元（以中文而言，會用拼音與空白取代）。如果先用它處理過，再把字串送進 Django 內建的 `slugify`，就可以得到一個有意義的 slug。和一些主流網站的行為類似，Logdown 目前也是使用類似方法。優點：沒有瀏覽器自動解碼與否的問題。缺點：網址可讀性變差，尤其中文的同音異字異義問題很大，有時候出來的網址會完全不可讀。

如果要用後面的解法，還有一些其他的小工具可以讓事情更簡單。[python-slugify] 把 [unidecode] 包成一個 `slugify` 函式，還附上了一個 Unicode 可用的 `truncate` 函式（！）。[django-uuslug] 把 [python-slugify] 的功能接到 Django 上，讓它可以輸出 unicode 物件（而非 str），並且附上一個方便產生 unique slug 的 helper function。

What a time-saver!


[Mezzanine]: http://mezzanine.jupo.org
[unicode-slugify]: https://github.com/mozilla/unicode-slugify
[unidecode]: https://pypi.python.org/pypi/Unidecode
[python-slugify]: https://pypi.python.org/pypi/python-slugify
[django-uuslug]: https://pypi.python.org/pypi/django-uuslug