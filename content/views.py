from django.conf         import settings       
from django.contrib.auth import authenticate, login
from django.core.files   import File
from django.db           import models
from django.http         import HttpResponse
from django.shortcuts    import get_object_or_404, render, render_to_response
from django.template     import RequestContext
from .forms              import UploadFileForm
from .models             import *
from django.utils.datastructures import MultiValueDictKeyError



################################################################################
# Hello, world
################################################################################
def index(request):
  return render( request, 
                       'index.html', 
               )



################################################################################
# Running autograder on a question
################################################################################
# TODO: account for assessment
def autograde(request, assessment_id, question_id):

    # Only grade if POST
    if request.method=='POST':

        # Get student and question objects
        user          = request.user;
        user_id       = user.id;
        student       = get_object_or_404(MyUser,     pk=user_id);
        question      = get_object_or_404(Question,   pk=question_id);
        assessment    = get_object_or_404(Assessment, pk=assessment_id);

        # Write response to file
        path          = settings.MEDIA_URL+student.email+"/"+str(question.id);
        responsefile  = open(path, 'w');
        djangofile    = File(responsefile);
        if   'choice'  in request.POST: djangofile.write(request.POST['choice']);
        elif 'answer'  in request.POST: djangofile.write(request.POST['answer']);
        elif 'sandbox' in request.POST: djangofile.write(request.POST['sandbox']);
        djangofile.close();

        # Open for reading
        responsefile  = open(path, 'r');
        djangofile    = File(responsefile);
        response = Response(question=question, student=student, formfile=djangofile); 
        response.save();
        djangofile.close();

        # Log that question was answered
        student.push_answered_question(question.id)
        index            = 0;
        lines            = question.solution.splitlines();
        question.correct = False;

        # In the case of multiple choice, determine correctness
        if 'choice' in request.POST:
           for line in lines:
               if (line[0]=='*'):
                  if (request.POST['choice']==("choice"+str(index))):
                     question.correct  = True
               index+=1

        # In the case of short answer, determine if solution is response
        elif 'answer' in request.POST:
             if request.POST['answer'] == question.solution:
                   question.correct =  True;
             else: question.correct = False;

        # In the case of short answer, determine if solution is response
        elif 'sandbox' in request.POST:
             question.correct = False;


        # Add to the lattice
        if (question.correct == True):
           student.increment(question_id, assessment_id);


        # Return request
        return render( request, 
                         'question/detail.php', 
                         {
                          'question': question,
                          'assessment': assessment
                         }
                     )

    # Print request if not POST
    else: print request
    return render( 
                   request, 
                   'assessment/list.php' 
                 )



################################################################################
# For rendering a profile
################################################################################
def profile(request): 
  return render(
                  request, 
                  'myuser/profile.php'
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
def question_detail(request, assessment_id, question_id):
  # TODO: check that q in a
  a = get_object_or_404(Assessment, pk=assessment_id)
  q = get_object_or_404(Question,   pk=question_id)
  return render(  request, 
                  'question/detail.php',
                      {
                        'question'  : q, 
                        'assessment': a
                      }
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
    #print user
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
                    settings.BASE_URL+'/login/login.html', 
                   {'request': request}
                 )

