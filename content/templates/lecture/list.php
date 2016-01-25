{% load staticfiles %}
<link href="{% static "detail.css" %}" type="text/css" rel="stylesheet"/>

<style>
  td {
    margin: 20px;
  }
</style>

<div class=main-container>
 <div class=lecture-container>
  <div class=code-header-container style="margin:340px; background:black; color:white;"> 
    Lectures
  </div>
  <div class=source-code style="height: 400px">

<table style="width:600px;">
 {% for lecture in lectures %}
 <tr>
  <td> <a href="lecture/{{ lecture.id }}">lecture/{{lecture.id}}</a> </td>
  <td> {{ lecture.name }}  </td>
 </tr>
 {% endfor %}
</table>

</div>
</div>
</div>
