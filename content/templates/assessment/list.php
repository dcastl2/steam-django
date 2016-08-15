{% load staticfiles %}

<link href="{% static "detail.css" %}" type="text/css" rel="stylesheet"/>

<style>
  td {
    margin: 20px;
  }
</style>

<table style="width:600px;">
 {% for assessment in assessments %}
 <tr>
  <td> 
       <a href="{{ settings.BASE_URL }}/assessment/{{ assessment.id }}">
         assessment/{{assessment.id}}
       </a>
  </td>
  <td> {{ assessment.name  }} </td>
  <td> {{ assessment.scale }} </td>
 </tr>
 {% endfor %}
</table>

