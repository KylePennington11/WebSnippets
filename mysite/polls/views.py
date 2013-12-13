from django.shortcuts import get_object_or_404, render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from polls.models import Choice, Poll, Snippet
import datetime

def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render_to_response('polls/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        }, context_instance=RequestContext(request))
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('poll_results', args=(p.id,)))

def snippet(request):
    latest_snippet_list = Snippet.objects.order_by('-date_added')[:]
    context = {'latest_snippet_list': latest_snippet_list}
    return render(request, 'polls/snippet.html', context)

def addsnippet(request):
    return render(request, 'polls/addsnippet.html')

def savesnippet(request):
    e = Snippet(title = request.POST['title'],
                url = request.POST['url'],
                text = request.POST['text'],
                image = request.POST['image'],
                date_added = datetime.datetime.now(),
                last_viewed = datetime.datetime.now())

    e.save(force_insert=True)
    latest_snippet_list = Snippet.objects.order_by('-date_added')[:]
    context = {'latest_snippet_list': latest_snippet_list}
    return render(request, 'polls/snippet.html', context)