{% load staticfiles %}
{% load content_tags %}
<!-- <link href="{% static "detail.css" %}" type="text/css" rel="stylesheet"/> -->

  <div class=code-container>
    <div class=code-header-container>
     {{ question.code.name }}:
     {{ question.code.concept }} 
     ({{ question.code.lang }}).
    </div>
    <div class=source-code>
        {% include_code question.code %}
    </div>
</div>

