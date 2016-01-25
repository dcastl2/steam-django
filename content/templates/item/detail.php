{% load staticfiles %}
<link href="{% static "detail.css" %}" type="text/css" rel="stylesheet"/>

<div class=main-container>
 <div class=item-container>
  <div class=item-header-container>
    {{ item.concept }}: 
    {{ item.stars   }},
    {{ item.form    }}
   ({{ item.domain  }}).
  </div>
  &nbsp;
  {% autoescape off %}
    {{ item.textformat }}
  {% endautoescape %}
</div>
  {% if item.code != NULL %}
    {% include 'code/question-code.php' %}
  {% endif %}
</div>

