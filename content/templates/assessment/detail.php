{% load staticfiles %}

<link href="{% static "detail.css" %}" type="text/css" rel="stylesheet"/>
<style>
  td { margin: 20px; }
</style>

<table style="width:600px;">
 <tr style="background:black; color:white;">
  <td> ID         </td>
  <td> Concept    </td>
  <td> Bloom      </td>
  <td> Difficulty </td>
  <td> Domain     </td>
  <td> Subdomain  </td>
 </tr>
{% for question in assessment.get_questions %}
 <tr>
  <td> <a href="{{ settings.BASE_URL }}/question/{{ assessment.id }}/{{ question.id }}">question/{{question.id}}</a> </td>
  <td> {{ question.concept }}   </td>
  <td> {{ question.bloom  }}    </td>
  <td> {{ question.level  }}    </td>
  <td> {{ question.domain }}    </td>
  <td> {{ question.subdomain }} </td>
 </tr>
{% endfor %}
</table>

