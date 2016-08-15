{% load staticfiles %}
<link href="{% static "detail.css" %}" type="text/css" rel="stylesheet"/>
{% for question in assessment.get_questions %}
  {% include 'question/detail.php' %}
{% endfor %}

{% if user != NULL %}
  {{ user }}
{% endif %}
