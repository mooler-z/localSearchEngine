from django.shortcuts import render
from .forms import SearchForm
import os, json


def index_view(request):
    search = request.POST.get('search_query')
    s = search
    if search:
        os.system(f"python3 /home/ultron/00workSpace/scripting/python_202/project_s/localSearchEngine/LSE_v1/lseApp/engine.py '{search}'")
        with open("/home/ultron/00workSpace/scripting/python_202/project_s/localSearchEngine/LSE_v1/results.json", 'r') as res:
            print(dir(res))
            results = json.load(res)
        search = results['results']
    else:
        search = []

    context = {
        "form": SearchForm(),
        "search": s,
        "results": search
    }
    return render(request, 'lseApp/index.html', context)
