{% load staticfiles %}
{% load content_tags %}
<link href="{% static "detail.css" %}" type="text/css" rel="stylesheet"/>

<div class=main-container>
  <div class=code-container>
    <div class=code-header-container>
     {{ code.name }}:
     {{ code.concept }} 
     ({{ code.lang }}).
    </div>
    <div class=source-code>
        {% include_code code %}
    </div>
  </div>
</div>

