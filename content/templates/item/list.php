{% load staticfiles %}
<link href="{% static "detail.css" %}" type="text/css" rel="stylesheet"/>

<style>
  td {
    margin: 20px;
  }
</style>

<div class=main-container>
 <div class=item-container>
  <div class=code-header-container style="margin:340px; background:black; color:white"> 
    Items 
  </div>
  <div class=source-code style="height: 400px">

<table style="width:600px;">
 {% for item in items %}
 <tr>
  <td> <a href="item/{{ item.id }}">item/{{item.id}}</a> </td>
  <td> {{ item.concept }}  </td>
  <td> {{ item.stars}}     </td>
  <td> {{ item.form}}      </td>
  <td> {{ item.domain}}    </td>
 </tr>
 {% endfor %}
</table>

</div>
</div>
</div>
