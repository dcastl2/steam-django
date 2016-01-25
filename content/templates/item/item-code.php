
{% load staticfiles %}
{% load content_tags %}
<!-- <link href="{% static "detail.css" %}" type="text/css" rel="stylesheet"/> -->

  <div class=code-container>
    <div class=code-header-container>
     {{ item.code.name }}:
     {{ item.code.concept }} 
     ({{ item.code.lang }}).
    </div>
    <div class=source-code>
        {% include_code item.code %}
    </div>
</div>

