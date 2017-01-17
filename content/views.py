from django.conf         import settings       
from django.contrib.auth import authenticate, login
from django.core.files   import File
from django.db           import models
from django.http         import HttpResponse
from django.shortcuts    import get_object_or_404, render, render_to_response
from django.template     import RequestContext, loader
from .forms              import UploadFileForm
from .models             import *
from django.utils.datastructures import MultiValueDictKeyError

import os
import re




################################################################################
# Hello, world
################################################################################
def index(request):
  return render( request, 
                       'index.html', 
               )



################################################################################
# For rendering a profile
################################################################################
def profile(request): 
  return render(
                  request, 
                  'profile.php'
               )



################################################################################
# For rendering a item
################################################################################
def item(request, item_id):
  # TODO: check that q in a
  i = get_object_or_404(Item, pk=item_id)
  return render(  request, 
                  'item.php',
                      {
                        'item'  : i, 
                      }
               )


################################################################################
# For rendering a item
################################################################################
def setitem(request, set_id, item_id):
  # TODO: check that q in a
  i = get_object_or_404(Item,    pk=item_id)
  s = get_object_or_404(ItemSet, pk=set_id)
  return render(  request, 
                  'item.php',
                      {
                        'item' : i, 
                        'set'  : s, 
                      }
               )



################################################################################
# For rendering items
################################################################################
def items(request):
  items = Item.objects.all()
  return render( request,
                 'items.php', 
                 {'items': items}
                 #context_instance=RequestContext(request)
               )



################################################################################
# For rendering an set
################################################################################
def set(request, set_id):
  set = get_object_or_404(ItemSet, pk=set_id)
  return render( request,
                 'set.php', 
                 {'set': set }  
                 #context_instance=RequestContext(request)
               )


################################################################################
# For printing an set
################################################################################
def printout(request, set_id):
  set = get_object_or_404(ItemSet, pk=set_id)
  return render( request,
                 'print.php', 
                 {'set': set }  
                 #context_instance=RequestContext(request)
               )



################################################################################
# For rendering an set
################################################################################
def sets(request):
  sets = ItemSet.objects.all()
  return render( request,
                 'sets.php', 
                 {'sets': sets} 
                 #context_instance=RequestContext(request)
               )


# Obtained from Wikipedia
# Levenshtein distance is number of edits required to transform s1
# to s2.
def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]



################################################################################
# Running autograder on a item
################################################################################
# TODO: account for set
def autograde(request, set_id, item_id):

    # Only grade if POST
    if request.method=='POST':

        # Get user and item objects
        user        = request.user;
        user_id     = user.id;
        myuser      = get_object_or_404(MyUser,  pk=user_id);
        item        = get_object_or_404(Item,    pk=item_id);
        set         = get_object_or_404(ItemSet, pk=set_id);

        # Save response to file
        response = Response(item=item, user=myuser, set=set, response=request.POST['response']);
        response.save();


        # Proceed to grade
        item.correct = False;
        item.answered = True;

        if item.form == "Multiple Choice":
          if request.POST['response'].strip() == item.solution.strip():
              item.correct  = True

        # In the case of short answer, determine if solution is response
        elif item.form == "Short Answer":
             r = request.POST['response'].lower();
             s = item.solution.lower();
             r = re.sub(r'\s+', '', r);
             s = re.sub(r'\s+', '', s);
             item.misspelled = False;
             if s == r:
                item.correct = True;
             elif levenshtein(s, r) < 3:
                item.correct = True;
                item.misspelled = True;
             else:
                item.correct = False;
   
        elif item.form == "Multiple Selection":
          if request.POST['response'].strip() == item.solution.strip():
              item.correct  = True

        else: item.correct = False;

        # Return request
        return render( request, 
                         'item.php', 
                         {
                          'item': item,
                          'set':  set
                         }
                     )

    # Print request if not POST
    else: print request
    return render( 
                   request, 
                   'index.html' 
                 )



################################################################################
# For rendering a login page
################################################################################
def loginpage(request):
  return render( request, 'login.html', None)



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
            sets = ItemSet.objects.all()
            return render_to_response(
                              'sets.php', 
                              {'sets': sets}
                              #context_instance=RequestContext(request)
                   )

    return render(  request, 
                    'login.html', 
                   {'request': request}
                 )




################################################################################
# Pie chart example
################################################################################
def pie(request): 
	xdata = ["Apple", "Apricot", "Avocado", "Banana", "Boysenberries", "Blueberries", "Dates", "Grapefruit", "Kiwi", "Lemon"]
	ydata = [52, 48, 160, 94, 75, 71, 490, 82, 46, 17]
	chartdata = {'x': xdata, 'y': ydata}
	charttype = "pieChart"
	chartcontainer = 'piechart_container'
	data = {
	    'charttype': charttype,
	    'chartdata': chartdata,
	    'chartcontainer': chartcontainer,
	    'extra': {
		'x_is_date': False,
		'x_axis_format': '',
		'tag_script_js': True,
		'jquery_on_ready': False,
	    }
	}
	return render_to_response('piechart.html', data)




import random
import datetime
import time
################################################################################
# Line chart example
################################################################################
def demo_linechart(request):
    """
    lineChart page
    """
    start_time = int(time.mktime(datetime.datetime(2012, 6, 1).timetuple()) * 1000)
    nb_element = 100
    xdata = range(nb_element)
    xdata = map(lambda x: start_time + x * 1000000000, xdata)
    ydata = [i + random.randint(1, 10) for i in range(nb_element)]
    ydata2 = map(lambda x: x * 2, ydata)

    tooltip_date = "%d %b %Y"
    extra_serie = {"tooltip": {"y_start": "", "y_end": " cal"},
                   "date_format": tooltip_date}
    chartdata = {'x': xdata,
                 'name1': 'series 1', 'y1': ydata, 'extra1': extra_serie,
                 'name2': 'series 2', 'y2': ydata2, 'extra2': extra_serie}
    charttype = "lineWithFocusChart"
    data = {
        'charttype': charttype,
        'chartdata': chartdata
    }
    return render_to_response('linechart.html', data)




################################################################################
# Scatter chart example
################################################################################
def demo_scatterchart(request):
    """
    scatterchart page
    """
    nb_element = 50
    xdata = [i + random.randint(1, 10) for i in range(nb_element)]
    ydata1 = [i * random.randint(1, 10) for i in range(nb_element)]
    ydata2 = map(lambda x: x * 2, ydata1)
    ydata3 = map(lambda x: x * 5, ydata1)

    kwargs1 = {'shape': 'circle'}
    kwargs2 = {'shape': 'cross'}
    kwargs3 = {'shape': 'triangle-up'}

    extra_serie1 = {"tooltip": {"y_start": "", "y_end": " balls"}}

    chartdata = {
        'x': xdata,
        'name1': 'series 1', 'y1': ydata1, 'kwargs1': kwargs1, 'extra1': extra_serie1,
        'name2': 'series 2', 'y2': ydata2, 'kwargs2': kwargs2, 'extra2': extra_serie1,
        'name3': 'series 3', 'y3': ydata3, 'kwargs3': kwargs3, 'extra3': extra_serie1
    }
    charttype = "scatterChart"
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
    }
    return render_to_response('scatterchart.html', data)

