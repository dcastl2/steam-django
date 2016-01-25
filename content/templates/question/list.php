{% load staticfiles %}
<link href="{% static "detail.css" %}" type="text/css" rel="stylesheet"/>

<style>
  td {
    margin: 20px;
  }
</style>

<div class=main-container>
 <div class=question-container>
  <div class=code-header-container style="margin:340px; background:black; color:white"> 
    Questions
  </div>
  <div class=source-code style="height: 400px">

<table style="width:600px;">
 {% for question in questions %}
 <tr>
  <td> <a href="question/{{ question.id }}">question/{{question.id}}</a> </td>
  <td> {{ question.concept }}  </td>
  <td> {{ question.stars}}     </td>
  <td> {{ question.form}}      </td>
  <td> {{ question.domain}}    </td>
 </tr>
 {% endfor %}
</table>

</div>
</div>
</div>
