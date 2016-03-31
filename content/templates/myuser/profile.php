<!-- -------------------------------------------------------------------------
  Template for a profile.
  ------------------------------------------------------------------------- -->

<!-- -------------------------------------------------------------------------
  Load files, assign variables.
  ------------------------------------------------------------------------- -->
{% load staticfiles %}
{% load content_tags %}
<link href="{% static "detail.css" %}"    type="text/css" rel="stylesheet"/>
<script src="{% static "jsvim.js" %}"     type="text/javascript"/></script>
<script type="text/javascript" src="http://code.jquery.com/jquery-latest.min.js"> </script>
<script src="{% static "highlight.js" %}" type="text/javascript"/></script>
<script src="{% static "clickevents.js" %}" type="text/javascript"/></script>


<body>
 <div style='margin:auto; width:90%'>
  <div style='width:49%; float:left'>
    thing
  </div>
  <div style='width:49%; float:right'>
   {% autoescape off %}
     {{ user.render_profile }}
   {% endautoescape %}
  </div>
 </div>
</body>

<!-- 
  </div>
-->
