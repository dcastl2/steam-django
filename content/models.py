import json
from django                     import forms
from django.db                  import models
from django.conf                import settings
from django.contrib.auth.models import ( BaseUserManager, AbstractBaseUser )
from django.templatetags.static import static
from docutils.core              import publish_parts
from os.path                    import abspath, dirname
from re                         import sub

################################################################################
# Regex which gives extensions.
################################################################################
regex=".*(\.cpp|\.java|\.txt)$"
curdir = abspath(dirname(__file__));
################################################################################

################################################################################
# Definitions.
################################################################################
bloom_levels = (
 ('Knowledge',     'Knowledge'),
 ('Comprehension', 'Comprehension'),
 ('Application',   'Application'),
 ('Analysis',      'Analysis'),
 ('Evaluation',    'Evaluation'),
 ('Synthesis',     'Synthesis'),
);
difficulty_levels = (
 (1, 'Very Easy'),
 (2, 'Easy'),
 (3, 'Medium'),
 (4, 'Difficult'),
 (5, 'Very Difficult')
);
domains = (
 ('Computer Science',  'Computer Science'),
 ('Mathematics',       'Mathematics'),
 ('Physics',           'Physics'),
 ('Chemistry',         'Chemistry'),
 ('Biology',           'Biology'),
 ('Psychology',        'Psychology'),
 ('Philosophy',        'Philosophy'),
 ('Language',          'Language'),
 ('Music',             'Music'),
 ('Art',               'Art'),
);
question_formats = (
 ('Multiple Choice',   'Multiple Choice'),
 ('Short Answer',      'Short Answer'),
 ('Code Writing',      'Code Writing'),
 ('Likert Scale',      'Likert Scale'),
);
item_formats = (
 ('Fact(s)',           'Fact(s)'),
 ('Code',              'Code'),
 ('Glossary',          'Glossary'),
 ('Diagram',           'Diagram'),
);
################################################################################

################################################################################
# Place to upload to.
################################################################################
def upload_to(self, filename):
  s  = settings.MEDIA_URL + 'codes/';
  s += self.lang          + '/';
  s += self.concept       + '/';
  s += filename;
  return s;
################################################################################

################################################################################
# Place to upload response to.
################################################################################
def upload_response(self, filename):
  s  = settings.MEDIA_URL;
  s += self.student.email + '/';
  s += str(self.question.id);
  return s;
################################################################################

################################################################################
# Place to upload image to.
################################################################################
def img_upload_to(self, filename):
  s  = settings.MEDIA_URL + 'images/';
  s += self.lang          + '/';
  s += self.concept       + '/';
  s += filename;
  return s;
################################################################################

################################################################################
# Student user manager
################################################################################
class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
 
    def create_superuser(self, email, password):
        user = self.create_user(email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
################################################################################

################################################################################
# Student user/profile
################################################################################
class MyUser(AbstractBaseUser):
  email = models.EmailField(
            verbose_name='email address',
            max_length=255,
            unique=True,
          )
  is_active = models.BooleanField(default=True);
  is_admin  = models.BooleanField(default=False);
  lattice   = models.TextField();
  answered  = models.TextField();

  objects = MyUserManager();
  USERNAME_FIELD  = 'email'
  REQUIRED_FIELDS = []
 
  def has_answered_question(self, qid):
        str_qid = ","+str(qid)+",";
        return (str_qid in self.answered);
 
  def push_answered_question(self, qid):
        self.answered += str(qid)+",";
        self.save();
        return True;
 
  def get_full_name(self):
        # The user is identified by their email address
        return self.email;
 
  def get_short_name(self):
        # The user is identified by their email address
        return self.email;
 
  def __str__(self):              # __unicode__ on Python 2
        return self.email;
 
  def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True
 
  def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
 
  @property
  def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
################################################################################

################################################################################
# Code model
################################################################################
class Code(models.Model):
 
  name     = models.CharField(max_length=64);
  lang     = models.CharField(max_length=64);
  concept  = models.CharField(max_length=64);
  codefile = models.FileField(upload_to=upload_to,max_length=64);
 
  def __str__(self):
    return str(self.lang)+": "+str(self.name);
################################################################################


# Produce HTML for the ith line of an MC question
def ith_choice(line, i, showcorrect):
  html = "";
  line = line[1:];
  choicestr = "choice"+str(i);
  html += "<input type='radio' ";
  html += " id='"+choicestr+"' value='"+choicestr+"' name='choice'>";
  html += "<label ";
  if showcorrect and line[0]=='*': html += "class=mc-correct";
  else:                            html += "class=mc";
  html += " for="+str(i)+">"+line+"</label></input><br>\n";
  return html;


################################################################################
# Question model
################################################################################
class Question(models.Model):
 
  concept   = models.CharField(max_length=64);
  bloom     = models.CharField(max_length=16, choices=bloom_levels);
  domain    = models.CharField(max_length=64, choices=domains);
  subdomain = models.CharField(max_length=64, choices=domains, blank=True);
  form      = models.CharField(max_length=64, choices=question_formats);
  level     = models.IntegerField(choices=difficulty_levels);
  code      = models.ForeignKey(Code, blank=True, null=True);
  image     = models.ImageField(blank=True, null=True);
  text      = models.TextField();
  solution  = models.TextField();
  points    = models.FloatField();
 
  def __str__(self):
    s  = str(self.concept) + ', L. ';
    s += str(self.level)   + ', ';
    s += str(self.form)    + ' (';
    s += str(self.domain)  + ').';
    return s;
 
  def choices(self, showcorrect):
   lines = self.solution.splitlines();
   html = "";
   i=0;
   for line in lines:
     html += ith_choice(line, i, showcorrect);
     i += 1;
   return html;

  def get_solution(self):
   lines = self.solution.splitlines();
   html = "";
   i=0;
   for line in lines:
     if line[0] == '*':
       return line[1:];
   return "NULL";
 
  def textformat(self):
   return publish_parts(self.text, writer_name='html')['html_body'];
 
  def stars(self):
    return '*'*self.level;
################################################################################

################################################################################
# Item model
################################################################################
class Item(models.Model):
 
  concept   = models.CharField(max_length=64);
  bloom     = models.CharField(max_length=16, choices=bloom_levels);
  domain    = models.CharField(max_length=64, choices=domains);
  subdomain = models.CharField(max_length=64, choices=domains, blank=True);
  form      = models.CharField(max_length=64, choices=item_formats);
  level     = models.IntegerField(choices=difficulty_levels);
  code      = models.ForeignKey(Code, blank=True, null=True);
  image     = models.ImageField(blank=True, null=True);
  text      = models.TextField();
 
  def __str__(self):
    s  = str(self.concept) + ', L. ';
    s += str(self.level)   + ', ';
    s += str(self.form)    + ' (';
    s += str(self.domain)  + ').';
    return s;
 
  def textformat(self):
   return publish_parts(self.text, writer_name='html')['html_body'];
 
  def stars(self):
    return '*'*self.level;
################################################################################

################################################################################
# Response (student response to a question)
################################################################################
class Response(models.Model):
  student  = models.ForeignKey(MyUser,   on_delete=models.CASCADE);
  question = models.ForeignKey(Question, on_delete=models.CASCADE);
  formfile = models.FileField(upload_to=upload_response, max_length=64);
################################################################################

################################################################################
# Assessment 
################################################################################
class Assessment(models.Model):
   
  name       = models.CharField(max_length=64);
  constraint = models.TextField();
  scale      = models.FloatField();
  questions  = models.ManyToManyField(
                                     Question,
                                     through='AssessmentQuestion',
                                     through_fields=(
                                                      'assessment',
                                                      'question',
                                                    )
                                    )
 
  def __str__(self):
    return self.name;
 
  def get_questions(self):
    return self.questions.all();
 
  def save(self, *args, **kwargs):
    super(Assessment, self).save(*args, **kwargs);
    if (self.questions):
      self.questions.clear();
    super(Assessment, self).save(*args, **kwargs);
    self.associate();
  
  def associate(self):
    for q in Question.objects.raw(
        "select * from content_question where "+self.constraint):
      AssessmentQuestion.create(q, self);

  def in_assessment(self, question):
    return self;

  # TODO: handle if user is AnonymousUser
  def next_question(self, user, question):
    first = question;
    qs    = self.questions.all();
    qs    = qs.order_by('id');
    print qs;
    it    = iter(qs);
    num   = 0;
    for q in it:
      num += 1;
      #print q.id;
      if q.id <= question.id:
        if not user.has_answered_question(q.id) and q.id <  first.id:
          first = q;
          print "First question not answered: "+str(first.id);
      elif not user.has_answered_question(q.id) and q.id != question.id:
          break;
    if num >= qs.count():
      if   question.id <  q.id: return "<a href='"+settings.BASE_URL+"question/"  +str(self.id)+"/"+str(q.id)+"/'"+">&gt;</a>";
      elif question.id == q.id: return "<a href='"+settings.BASE_URL+"question/"  +str(self.id)+"/"+str(first.id)+"/'"+">&lt;</a>";
      else:                     return "<a href='"+settings.BASE_URL+"assessment/"+str(self.id)+"/'>&lt;&lt;</a>";
    return "<a href='"+settings.BASE_URL+"question/"+str(self.id)+"/"+str(q.id)+"/'"+">&gt;</a>";
################################################################################

################################################################################
# Describes Assessment-Question relationship
################################################################################
class AssessmentQuestion(models.Model):
 
  question   = models.ForeignKey(Question);
  assessment = models.ForeignKey(Assessment);
 
  @classmethod
  def create(cls, question, assessment):
    aq = cls(question=question, assessment=assessment);
    super(AssessmentQuestion, aq).save();
    return aq;
 
  def __str__(self):
    return str(self.assessment)+": "+str(self.question);
################################################################################

################################################################################
# Lecture (contains items)
################################################################################
class Lecture(models.Model):
   
  name       = models.CharField(max_length=64);
  constraint = models.TextField();
  items      = models.ManyToManyField(
                                     Item,
                                     through='LectureItem',
                                     through_fields=(
                                                      'lecture',
                                                      'item',
                                                    )
                                    )
 
  def __str__(self):
    return self.name;
 
  def get_items(self):
    return self.items.all();
 
  def save(self, *args, **kwargs):
    super(Lecture, self).save(*args, **kwargs);
    if (self.items):
      self.items.clear();
    super(Lecture, self).save(*args, **kwargs);
    self.associate();
 
  def associate(self):
    for i in Item.objects.raw(
        "select * from content_item where "+self.constraint
                                 ):
      LectureItem.create(i, self);
################################################################################

################################################################################
# Describes Lecture-Item relationship
################################################################################
class LectureItem(models.Model):
  item    = models.ForeignKey(Item);
  lecture = models.ForeignKey(Lecture);
 
  @classmethod
  def create(cls, item, lecture):
    li = cls(item=item, lecture=lecture);
    super(LectureItem, li).save();
    return li;
 
  def __str__(self):
    return str(self.lecture)+": "+str(self.item);
################################################################################

