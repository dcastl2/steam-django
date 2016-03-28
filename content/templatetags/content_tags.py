from django  import template
from content.models import Question, MyUser
from django.conf    import settings

register = template.Library()

# ############################################################################
# For highlighting code
# ############################################################################
@register.simple_tag(takes_context=True)
def include_code(context, code):
    if not code:
      return "NULL";
    import urllib2
    code = urllib2.urlopen("file://"+code.codefile.path).read()
    from pygments            import highlight
    from pygments.lexers     import CppLexer,JavaLexer,HaskellLexer
    from pygments.formatters import HtmlFormatter
    return highlight(code, 
                     CppLexer(), 
                     HtmlFormatter( style='vimlight', 
                                    full=True, 
                                    linenos='table', 
                                    lineanchors='Line',
                                    anchorlinenos=True,
                                    noclobber_cssfile=True,
                                    nobackground=False,
                                  )
                    )


# ############################################################################
# Including an image
# ############################################################################
@register.simple_tag(takes_context=True)
def include_image(context, image):
    if not image:
      return "NULL";
    return "<img src="+image.url+">";

# ############################################################################
# Tell if question was answered
# ############################################################################
@register.assignment_tag(takes_context=True)
def answered_question(context, user, question):
    if not user:
      return False;
    return user.has_answered_question(question.id);

# ############################################################################
# List choices of multiple choice question
# ############################################################################
@register.simple_tag(takes_context=True)
def mc_choices(context, question, showcorrect):
    #print showcorrect;
    if not question:
      print "not question";
      return False;
    return question.choices(showcorrect);

# ############################################################################
# Find next question in assessment
# ############################################################################
@register.simple_tag(takes_context=True)
def next_question(context, user, assessment, question):
    return assessment.next_question(user, question);

# ############################################################################
# Including an image
# ############################################################################
@register.simple_tag(takes_context=True)
def base_url(context):
    return settings.BASE_URL;

