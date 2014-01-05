from django.shortcuts import get_object_or_404, render_to_response, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from snippets.models import Snippet
import datetime
import re

# def vote(request, poll_id):
#     p = get_object_or_404(Poll, pk=poll_id)
#     try:
#         selected_choice = p.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the poll voting form.
#         return render_to_response('polls/detail.html', {
#             'poll': p,
#             'error_message': "You didn't select a choice.",
#         }, context_instance=RequestContext(request))
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse('poll_results', args=(p.id,)))

def snippet(request, page):
    i = int(page)
    nPerPage = 15
    startpage = (i-1)*nPerPage
    endpage = i*nPerPage
    latest_snippet_list = Snippet.objects.order_by('-date_added')[startpage:endpage]
    context = {'latest_snippet_list': latest_snippet_list, 'nextpage': i+1}
    return render(request, 'snippets/index.html', context)

def addsnippet(request):
    return render(request, 'snippets/add.html')

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
    
    return redirect('/snippets/')

def deletesnippet(request):

    s = get_object_or_404(Snippet, pk = request.POST['id'])
    s.delete()

    return redirect('/snippets/')



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