from django  import template
from content.models import Question, MyUser

register = template.Library()

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


@register.simple_tag(takes_context=True)
def include_image(context, image):
    if not image:
      return "NULL";
    return "<img src="+image.url+">";


@register.assignment_tag(takes_context=True)
def answered_question(context, user, question):
    if not user:
      return False;
    return user.has_answered_question(question.id);

