from django.shortcuts import get_object_or_404, render_to_response, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from snippets.models import Snippet, Keyword
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
import datetime
import re
import json

def snippet(request, page):
    keywords = getKeywords() 
    i = int(page)
    nPerPage = 15
    startpage = (i-1)*nPerPage
    endpage = i*nPerPage
    snippet_list = Snippet.objects.order_by('last_viewed')[startpage:endpage]
    context = {'keywords': keywords, 'snippet_list': snippet_list, 'nextpage': i+1}
    return render(request, 'snippets/index.html', context)

def addsnippet(request):
    allkeywords = getAllKeywords() 
    keywords = getKeywords() 
    context = {'keywords': keywords, 'allkeywords': allkeywords}
    return render(request, 'snippets/add.html', context)

def viewsnippet(request, pk):
    s = get_object_or_404(Snippet, pk=pk)

    s.last_viewed = datetime.datetime.now()
    s.save()

    keywords = getKeywords() 
    context = {'snippet': s, 'keywords': keywords}
    return render(request, 'snippets/details.html', context)

def editsnippet(request, pk):
    s = get_object_or_404(Snippet, pk=pk)
    allkeywords = getAllKeywords() 
    keywords = getKeywords()
    print(allkeywords)
                                                 
          #        
          #        .order_by('-keywords_count')
    ikeywords = s.keywords.all()
    context = {'snippet': s, 'keywords': keywords, 'allkeywords': allkeywords, 'ikeywords':ikeywords}
    return render(request, 'snippets/add.html', context)

def savesnippet(request, pk=0):

    mediaDict = determineMediaType(request.POST['media'])

    e = Snippet(title = request.POST['title'],
                url = request.POST['url'],
                text = request.POST['text'],
                media = mediaDict['media'],
                mediaType = mediaDict['mediaType'],
                date_added = datetime.datetime.now(),
                last_viewed = datetime.datetime.now(),
                width = 'w1',
                height = 100)

    if request.POST['title'] == '' and request.POST['text'] == '' and request.POST['media'] != '':
        e.width = 'w0'

    if pk != 0:
        s = get_object_or_404(Snippet, pk=pk)
        s.delete()

    e.save(force_insert=True)

    tags = request.POST['tags']
    if tags != '':
        tagslist = tags.split(',')

        for tag in tagslist:
            try:
                k = Keyword.objects.get(keyword=tag)
            except ObjectDoesNotExist:
                k = Keyword(keyword=tag)
                k.save()

            e.keywords.add(k)
    

    e.save()

    return redirect('/snippets/')

def deletesnippet(request):

    s = get_object_or_404(Snippet, pk = request.POST['id'])
    s.delete()

    return redirect('/snippets/')

def query(request, query):

    snippet_list = Snippet.objects.filter(keywords__keyword__exact=query)
    keywords = getKeywords() 
    context = {'keywords': keywords, 'snippet_list': snippet_list}
    return render(request, 'snippets/index.html', context)

# Functions

def determineMediaType(media):

    matchObj = re.match( r'.*\.gif', media, re.I)
    if matchObj:
        return {'media': media, 'mediaType': '1'}

    matchObj = re.match( r'(?:https?://)?(?:www.)?youtube.com/watch\?(?:.*)v=(\w+)(?:#t=(.*))?', media, re.I)
    if matchObj:     
        return {'media': matchObj.group(1), 'mediaType': '2'}

    matchObj = re.match( r'(?:https?://)?(?:www.)?youtu.be/(.*)(?:#t=(.*))?', media, re.I)
    if matchObj:
        return {'media': matchObj.group(1), 'mediaType': '2'}

    return {'media': media, 'mediaType': '0'}

def getAllKeywords():
    return Keyword.objects.all().annotate(count=Count('snippet')).order_by('-count')

def getKeywords(limit=20):
    allkeywords = getAllKeywords()
    return allkeywords[:limit]