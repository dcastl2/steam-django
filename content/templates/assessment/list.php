{% load staticfiles %}
<link href="{% static "detail.css" %}" type="text/css" rel="stylesheet"/>

<style>
  td {
    margin: 20px;
  }
</style>

<div class=main-container>
 <div class=assessment-container>
  <div class=code-header-container style="margin:340px; background:black; color:white"> 
    Assessments
  </div>
  <div class=source-code style="height: 400px">

<table style="width:600px;">
 {% for assessment in assessments %}
 <tr>
  <td> <a href="assessment/{{ assessment.id }}">assessment/{{assessment.id}}</a> </td>
  <td> {{ assessment.name}}      </td>
 </tr>
 {% endfor %}
</table>

</div>
</div>
</div>
