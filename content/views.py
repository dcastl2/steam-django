from django.http         import HttpResponse
from django.shortcuts    import get_object_or_404, render, render_to_response
from django.template     import RequestContext
from django.contrib.auth import authenticate, login
from .models             import Question, Item, Code, Assessment, Lecture, MyUser


################################################################################
# Hello, world
################################################################################
def index(request):
  return HttpResponse("Hello, world!")


################################################################################
# Running autograder on a question
################################################################################
# Todo: check data
def autograde(request, user_id, question_id):
    # Check that user_id is id of user logged in
    i = 0
    u = get_object_or_404(MyUser,   pk=user_id)
    q = get_object_or_404(Question, pk=question_id)
    u.push_answered_question(q.id)
    lines = q.solution.splitlines()
    print request.POST['choice']
    q.correct = False
    for line in lines:
      print line[0]
      print "choice"+str(i)
      if (request.POST['choice']==("choice"+str(i)) and line[0]=='*'):
        q.correct = True
      i+=1
    return render( request, 
                   'question/detail.php', 
                   {'question': q}
                 )


################################################################################
# For rendering a question
################################################################################
def assessment_detail(request, assessment_id):
  q = get_object_or_404(Assessment, pk=assessment_id)
  return render(
                  request, 
                  'assessment/detail.php', 
                  {'assessment': q}
               )


################################################################################
# For rendering a question
################################################################################
def question_detail(request, question_id):
  q = get_object_or_404(Question, pk=question_id)
  return render(  request, 
                  'question/detail.php',
                  {'question': q}
               )


################################################################################
# For rendering a lecture
################################################################################
def lecture_detail(request, lecture_id):
  q = get_object_or_404(Lecture, pk=lecture_id)
  return render(
                  request, 
                  'lecture/detail.php', 
                  {'lecture': q}
               )


################################################################################
# For rendering code
################################################################################
def code_detail(request, code_id):
  q = get_object_or_404(Code, pk=code_id)
  return render_to_response(
                              'code/detail.php', 
                              {'code': q}, 
                              context_instance=RequestContext(request)
                           )


################################################################################
# For rendering an item
################################################################################
def item_detail(request, code_id):
  q = get_object_or_404(Item, pk=code_id)
  return render_to_response(
                              'item/detail.php', 
                              {'item': q}, 
                              context_instance=RequestContext(request)
                           )


################################################################################
# For rendering an item
################################################################################
def items(request):
  its = Item.objects.all()
  return render_to_response(
                              'item/list.php', 
                              {'items': its}, 
                              context_instance=RequestContext(request)
                           )


################################################################################
# For rendering a question
################################################################################
def questions(request):
  its = Question.objects.all()
  return render_to_response(
                              'question/list.php', 
                              {'questions': its}, 
                              context_instance=RequestContext(request)
                           )


################################################################################
# For rendering an assessment
################################################################################
def assessments(request):
  its = Assessment.objects.all()
  return render_to_response(
                              'assessment/list.php', 
                              {'assessments': its}, 
                              context_instance=RequestContext(request)
                           )


################################################################################
# For rendering a lecture
################################################################################
def lectures(request):
  its = Lecture.objects.all()
  return render_to_response(
                              'lecture/list.php', 
                              {'lectures': its}, 
                              context_instance=requestcontext(request)
                           )


################################################################################
# For rendering a login page
################################################################################
def login_page(request):
  return render( request, 'login/login.html', None)


################################################################################
# For logging a user in
################################################################################
def auth(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    print user
    if user is not None:
        if user.is_active:
            login(request, user)
            its = Assessment.objects.all()
            return render_to_response(
                              'assessment/list.php', 
                              {'assessments': its},
                              context_instance=RequestContext(request)
                   )
    return render(  request, 
                    'login/login.html', 
                   {'request': request}
                 )

