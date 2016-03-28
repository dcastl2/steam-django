<!-- -------------------------------------------------------------------------
  Template for a question.
  ------------------------------------------------------------------------- -->

<!-- TODO: 
       check authentication
       response logging for code
       assessment awareness
  -->


<!-- -------------------------------------------------------------------------
  Load files, assign variables.
  ------------------------------------------------------------------------- -->
{% load staticfiles %}
{% load content_tags %}
<link href="{% static "detail.css" %}"    type="text/css" rel="stylesheet"/>
<script src="{% static "jsvim.js" %}"     type="text/javascript"/></script>
<script type="text/javascript" src="http://code.jquery.com/jquery-latest.min.js"> </script>
<script src="{% static "highlight.js" %}" type="text/javascript"/></script>
<script src="{% static "clickevents.js" %}" type="text/javascript"/></script>

{% if user.username != "" %}
 {% answered_question user question as answered %}
{% endif %}


<body>
<div class="panels-container">

{% if user.username != "" %}
  <div class="left-panel">
    <div class="name-container">
      {{ user }}
    </div>
    <br/>
  </div>
  <div class="right-panel">
    <div class="next-button">
          <span style="display:inline-block; vertical-align:middle; position:relative; top:45%">
            {% next_question user assessment question %}
          </span>
    </div>
  </div>
{% endif %}



<!-- -------------------------------------------------------------------------
  Show question details.
  ------------------------------------------------------------------------- -->
<div class=main-container>
 <div class=question-container>
  <div class=question-header-container>
    {{ question.concept }}: {{ question.stars }} {{ question.bloom }}, {{ question.form }}
     ({{ question.domain  }}{% if question.subdomain != "" %}: {{ question.subdomain }}{% endif %}).
  </div>
  &nbsp;
  {% autoescape off %}
    {{ question.textformat }}
  {% endautoescape %}
</div>



<!-- -------------------------------------------------------------------------
  Accommodate a code or image.
  ------------------------------------------------------------------------- -->
  {% if question.code != NULL and question.image != "" %}
    <style>
      div.main-container {
        height: 992px;
      }
    </style>
  {% endif %}



<!-- -------------------------------------------------------------------------
  Code for a question, if such code exists.
  ------------------------------------------------------------------------- -->
  {% if question.code != NULL %}
    {% include 'code/question-code.php' %}
  {% endif %}
  {% if question.image %}
    <div class=image-container>
      {% include_image question.image %}
    </div>
  {% endif %}



<!-- -------------------------------------------------------------------------
  Form for a question response.
  ------------------------------------------------------------------------- -->
{% if user.username != "" and question.solution != "" %}
  <form class="multiple-choice" action="{% url 'content:autograde' assessment.id question.id %}" method="post">
  {% csrf_token %}


  {% if question.form == "Likert Scale" %}
<!-- -------------------------------------------------------------------------
  Liker Scale.
  ------------------------------------------------------------------------- -->
  <div class="button-container">
     <input class="likert-scale" type="range" min="1" max="9" name="answer" id="answer" onchange="showSliderValue()"/>
       <label for="answer"></label>
  </div>
  <br />


  {% elif question.form == "Short Answer" %}
<!-- -------------------------------------------------------------------------
  Short answer.
  ------------------------------------------------------------------------- -->
  <div class="button-container">
     <input class="short-answer" type="text" name="answer" id="answer" value=""/>
       <label for="answer"></label>
  </div>
  <br />



  {% elif question.form == "Multiple Choice" %}
<!-- -------------------------------------------------------------------------
  Multiple choice.
  ------------------------------------------------------------------------- -->
    {% if answered %}
    <!-- answered -->
     {% autoescape off %}
      {% mc_choices question True %}
     {% endautoescape %}
    {% else %}
    <!-- not answered -->
     {% autoescape off %}
      {% mc_choices question False %}
     {% endautoescape %}
    {% endif %}



  {% elif question.form == "Code Writing" %}
<!-- -------------------------------------------------------------------------
  Code writing.
  ------------------------------------------------------------------------- -->
  <textarea id=sandbox>
  #include <iostream>
  
  int main() {
    
  }</textarea>
  {% endif %}



<!-- -------------------------------------------------------------------------
  Within-textbox syntax highlighting.
  ------------------------------------------------------------------------- -->
  <!--
  <div id=container0>
     <div id=highlighterContainer0>
       <div id="highlighter0">
       </div>
     </div>
     <div id=inputContainer0>
       <textarea id='text1'>
        This is awesome.
       </textarea>
     </div>
  </div>
  -->



<!-- -------------------------------------------------------------------------
  Submit button
  ------------------------------------------------------------------------- -->
  <div class="button-container">
<!--
   {% if not answered %}
     <input class=autograde type="submit" value="Grade" />
   {% endif %}
-->
     <input class=autograde type="submit" value="Grade" />
  </div>
  </form>
{% endif %}



<!-- -------------------------------------------------------------------------
  Tell if question is correct.
  ------------------------------------------------------------------------- -->
{% if user.username != "" %}
 {% if question.correct != NULL %}
   <div class="solution-container">
     {{ question.correct  }}, the answer is <tt>{{ question.get_solution }}</tt>.
   </div>
 {% endif %}
{% endif %}



<!-- -------------------------------------------------------------------------
  Script for vim textarea functionality.
  ------------------------------------------------------------------------- -->
<script>
  window.onload = function(){
    var vim = new VIM()
    vim.on_log = function(m) {
      var LENGTH = 10
      /*
      var p = $('<div></div>').text( m )
      $('#log').prepend( p )
      if ( $('#log').children().length > LENGTH ) {
        $('#log').children(':last').remove()
      }
      */
    }
    var target = document.getElementById('sandbox')
    if (target !== null) {
      vim.attach_to( target )
      target.focus()
    } else {
    }
  }
</script>
</div>



<!-- -------------------------------------------------------------------------
  Tell if question was answered.
  ------------------------------------------------------------------------- -->
{% if answered  %}
  <center>
  You answered this question already.
  {% next_question user assessment question %}
  </center>
{% endif %}

</div>
</body>

<!-- 
  </div>
-->
