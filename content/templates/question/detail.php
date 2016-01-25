<!-- -------------------------------------------------------------------------
  Template for a question.
  ------------------------------------------------------------------------- -->


<!-- -------------------------------------------------------------------------
  Load files, assign variables.
  ------------------------------------------------------------------------- -->
{% load staticfiles %}
{% load content_tags %}
<link href="{% static "detail.css" %}"      type="text/css" rel="stylesheet"/>
<script src="{% static "jsvim.js" %}"       type="text/javascript"/></script>
<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4/jquery.min.js"> </script>
<script src="{% static "highlight.js" %}" type="text/javascript"/></script>

{% if user.username != "" %}
 {% answered_question user question as answered %}
{% endif %}



<!-- -------------------------------------------------------------------------
  Display the username.
  ------------------------------------------------------------------------- -->
{% if user.username != "" %}
  <div class="name-container">
    {{ user }}
  </div><br/>
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
{% if user.username != "" %}
  <form class=mc action="{% url 'content:autograde' user.id question.id %}" method="post">
  {% csrf_token %}



<!-- -------------------------------------------------------------------------
  Short answer.
  ------------------------------------------------------------------------- -->
  {% if question.form == "Short Answer" %}
  <div class="button-container">
     <input class="short-answer" type="text" name="choice" id="choice" value=""/>
       <label for="choice"></label>
  </div>
      <br />



<!-- -------------------------------------------------------------------------
  Multiple choice.
  ------------------------------------------------------------------------- -->
  {% elif question.form == "Multiple Choice" %}
    {% autoescape off %}
      {{ question.choices }}
    {% endautoescape %}



<!-- -------------------------------------------------------------------------
  Code writing.
  ------------------------------------------------------------------------- -->
  {% elif question.form == "Code Writing" %}
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
   <input class=autograde type="submit" value="Grade" />
  </div>
  </form>
{% endif %}



<!-- -------------------------------------------------------------------------
  Tell if question is correct.
  ------------------------------------------------------------------------- -->
{% if user.username != "" %}
 {% if question.correct != NULL %}
  {{ question.correct }}
  {{ user.answered }}
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
  </center>
{% endif %}

