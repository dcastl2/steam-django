{% load staticfiles %}
{% load content_tags %}
<link href="{% static "detail.css" %}" type="text/css" rel="stylesheet"/>

{% for item in lecture.get_items %}
  {% include 'item/detail.php' %}
{% endfor %}
