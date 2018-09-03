from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Question
from django.template import loader
from django.urls import reverse

def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	# output = ', '.join([q.question_text for q in latest_question_list])
	template = loader.get_template('./polls/index.html')
	context = {
        'latest_question_list': latest_question_list,
    }
	return HttpResponse(template.render(context, request))

def detail(request, question_id):
	try:
		question = Question.objects.get(pk=question_id)
	except:
		raise Http404("Question not found!")
	return render(request, 'polls/details.html', {'question': question})

def results(request, question_id):
	response = "You're looking at the results of question %s."
	return HttpResponse(response % question_id)

def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	print("Vote called!")
	for x in request.POST:
		print(x+": "+request.POST[x])
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'polls/details.html', {
			'question': question,
			'error_message': "You didn't select a choice!"
			})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		print("Else called!!!")
		return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))
	# return HttpResponse("You're voting on question %s." % question_id)
