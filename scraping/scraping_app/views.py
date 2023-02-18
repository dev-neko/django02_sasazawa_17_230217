from django.shortcuts import render
from .forms import ScrapingForm, SiteForm
from .scraping import green, recruit, geekly

def frontpage(request):
    # POSTされていたらそのデータを表示
    conclusion = ""
    count = ""
    if request.method == "POST":
        form = ScrapingForm(request.POST)
        siteform = SiteForm(request.POST)
        if form.is_valid() & siteform.is_valid():
            count = form.cleaned_data['count']
            occupation = form.cleaned_data['occupation']
            site = siteform.cleaned_data['site']
            if site == "green":
                item_info = green(occupation, count)
                conclusion = f"成功しました。件数は{len(item_info)}です。"
            elif site == "recnavi":
                item_info = recruit(occupation, count)
                conclusion = f"成功しました。件数は{len(item_info)}です。"
            elif site == "geekly":
                item_info = geekly(occupation, count)
                conclusion = f"成功しました。件数は{len(item_info)}です。"
            else:
                conclusion = "エラーです。"
            
    else:
        form = ScrapingForm()
        siteform = SiteForm()
        count = ""
        conclusion = ""
        item_info=""
    return render(request, "frontpage.html", {"conclusion": conclusion,
                                              "form": form,
                                              "siteform": siteform,
                                              "count": count,
                                              "item_info":item_info,
                                              })
