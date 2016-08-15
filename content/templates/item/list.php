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
 {% for item in items %}
 <tr>
  <td> <a href="{{ item.id }}">item/{{item.id}}</a> </td>
  <td> {{ item.concept }} </td>
  <td> {{ item.bloom  }} </td>
  <td> {{ item.level  }} </td>
  <td> {{ item.domain }} </td>
  <td> {{ item.subdomain }} </td>
 </tr>
 {% endfor %}
</table>

