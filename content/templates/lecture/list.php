{% load staticfiles %}
{% load content_tags %}
<link href="{% static "detail.css" %}" type="text/css" rel="stylesheet"/>

<style>
  td {
    margin: 20px;
  }
</style>


<table style="width:600px;">
 {% for lecture in lectures %}
 <tr>
  <td> <a href="{{ settings.BASE_URL}}/lecture/{{ lecture.id }}">lecture/{{lecture.id}}</a> </td>
  <td> {{ lecture.name }}  </td>
 </tr>
 {% endfor %}
</table>

