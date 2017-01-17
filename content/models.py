import json
import re
import random




################################################################################
# Imports.
#-------------------------------------------------------------------------------
from django                     import forms
from django.db                  import models
from django.conf                import settings
from django.contrib.auth.models import ( BaseUserManager, AbstractBaseUser )
from django.templatetags.static import static
from django.shortcuts           import get_object_or_404
from docutils.core              import publish_parts
from os.path                    import abspath, dirname
from re                         import sub




################################################################################
# Regex which gives extensions.
#-------------------------------------------------------------------------------
regex=".*(\.cpp|\.java|\.txt)$"
curdir = abspath(dirname(__file__));




################################################################################
# Utility functions
#-------------------------------------------------------------------------------
def index(a, n):
    for j in range(len(a)):
        if n == a[j][0]:
           return j;
    return -1;




################################################################################
# Definitions.
#-------------------------------------------------------------------------------

# The bloom levels are made ordinal to support arithmetic comparisons.
bloom_levels = (
 ('Knowledge', 'Knowledge'),       # Knows material; memorization.
 ('Comprehension', 'Comprehension'),   # Understands material; supplies examples.
 ('Application', 'Application'),     # Applies material; solves problems.
 ('Analysis', 'Analysis'),        # Analyzes material; demonstrates expertise.
 ('Evaluation', 'Evaluation'),      # Evaluates usefulness; can write proofs/arguments.
 ('Synthesis', 'Synthesis'),       # Can generate novel solution to new problems.
);

# The bloom levels are made ordinal to support arithmetic comparisons.
scheduler_types = (
 ('Linear', 'Linear'),     
 ('Random', 'Random'),     
 ('Adaptive', 'Adaptive'), 
);

# The difficulty levels for a item are such that a user with
# that grade should have a 50% probability of passing the item.
# That is, a B+ difficulty item should be passable 50% of the
# time by a user with a B+ grade of competency.
difficulty_levels = (
 ('F',  'F'),
 ('D-', 'D-'),
 ('D',  'D'),
 ('D+', 'D+'),
 ('C-', 'C-'),
 ('C',  'C'),
 ('C+', 'C+'),
 ('B-', 'B-'),
 ('B',  'B'),
 ('B+', 'B+'),
 ('A-', 'A-'),
 ('A',  'A'),
 ('A+', 'A+'),
);

# Domains have been restricted to STEM fields.
domains = (
 ('Computer Science',  'Computer Science'),
 ('Mathematics',       'Mathematics'),
 ('Physics',           'Physics'),
 ('Chemistry',         'Chemistry'),
 ('Biology',           'Biology'),
);

# Multiple choice involves choice of only one response. Multiple selection
# allows selection of more than 1 choice (or possibly 0 choices).  A Likert
# Scale is a scale of 1 to X, used to gauge preferences, give surveys, etc.
item_formats = (
 ('Paragraph',          'Paragraph'),
 ('Glossary',           'Glossary'),
 ('Code',               'Code'),
 ('Diagram',            'Diagram'),
 ('Table',              'Table'),
 
 ('Multiple Choice',    'Multiple Choice'),
 ('Multiple Selection', 'Multiple Selection'),
 ('Short Answer',       'Short Answer'),
 ('Code Writing',       'Code Writing'),
 ('Likert Scale',       'Likert Scale'),
);


# Domains have been restricted to STEM fields.
paginations = (
 ('Full Page',  'Full Page'),
 ('Half Page',  'Half Page'),
 ('Quartile',   'Quartile'),
);



################################################################################
# User user manager
#-------------------------------------------------------------------------------
class UserManager(BaseUserManager):

    # Controls the creation of a new user. 
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
 
    # Controls the creation of a new superuser. 
    def create_superuser(self, email, password):
        user = self.create_user(email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user




################################################################################
# User user/profile
#-------------------------------------------------------------------------------
class MyUser(AbstractBaseUser):
  
  # E-mails have to be unique. 
  email = models.EmailField(
            verbose_name='email address',
            max_length=255,
            unique=True,
          )

  # The two fields here determine whether the "user" is an active
  # user and if they are an admin.
  is_active = models.BooleanField(default=True);
  is_admin  = models.BooleanField(default=False);

  # This gives the course the user currently has focused. This
  # will determine what item_sets are able to be viewed, and what
  # the profile looks like.
  focused_course = models.ForeignKey('Course', blank=True, null=True);

  objects = UserManager();
  USERNAME_FIELD  = 'email'
  REQUIRED_FIELDS = []


  # Get all classes the user is/was enrolled in
  def get_classes():
    return Course.objects.raw(
      "select * from content_userclass where user="+id);


  def get_full_name(self):
      return self.email;
 

  def get_short_name(self):
      return self.email;
 

  def __str__(self):
      return self.email;
 

  def has_perm(self, perm, obj=None):
      "Does the user have a specific permission?"
      return True
 

  def has_module_perms(self, app_label):
      "Does the user have permissions to view the app `app_label`?"
      return True
 

  @property
  def is_staff(self):
      "Is the user a member of staff?"
      return self.is_admin


  def num_times_answered(self, set_id, item_id):
      query = "select * from content_response where user_id = %s and item_id = %s and set_id = %s"
      params = [self.id, item_id, set_id]
      R = Response.objects.raw(
        query,
        params
      );
      return len(list(R));



################################################################################
# Code model
#-------------------------------------------------------------------------------
class Code(models.Model):
 
      name     = models.CharField(max_length=64);
      caption  = models.CharField(max_length=128);
      language = models.CharField(max_length=64);
      compile  = models.CharField(max_length=256);
      run      = models.CharField(max_length=256);
      source   = models.TextField();
     
      def __str__(self):
          return str(self.language)+": "+str(self.name);


class Concept(models.Model):

  concept     = models.CharField(max_length=64);
  description = models.TextField(blank=True);

  def __str__(self):
      s  = str(self.concept);
      return s;
 

class Bloom(models.Model):

  bloom       = models.CharField(max_length=16, choices=bloom_levels);
  description = models.TextField(blank=True);

  def __str__(self):
      s  = str(self.bloom);
      return s;


class Level(models.Model):

  level       = models.CharField(max_length=2,  choices=difficulty_levels, default=7);
  description = models.TextField(blank=True);

  def __str__(self):
      s  = str(self.level);
      return s;


################################################################################
# Item model
#-------------------------------------------------------------------------------
class Item(models.Model):
 
  # These are item data used throughout.
  locked    = models.BooleanField(default=False);
  author    = models.ForeignKey(MyUser, blank=True, null=True);
  concept   = models.ForeignKey(Concept, blank=True, null=True);
  bloom     = models.ForeignKey(Bloom, blank=True, null=True);
  level     = models.ForeignKey(Level, blank=True, null=True, default=6);
  domain    = models.CharField(max_length=64, choices=domains, default='Computer Science');
  subdomain = models.CharField(max_length=64, choices=domains, blank=True);
  form      = models.CharField(max_length=64, choices=item_formats, default='Multiple Choice');
  pagination= models.CharField(max_length=64, choices=paginations, blank=True, default=2);
  tags      = models.CharField(max_length=128, blank=True, null=True);

  # If item has a code or image.
  code      = models.ForeignKey(Code, blank=True, null=True);
  image     = models.ImageField(blank=True, null=True);

  # This gives a list of items that this item depends on. The
  # intuition is that the user should be able to answer these dependent
  # items before being able to answer this item.  It is possible
  # to specify, for example, that a user should have been able to answer
  # all C+ items regarding loops before tackling this item.
  #
  # In practice these criteria will be auto-generated, and will prove to
  # be much looser.
  item_dep_constraint = models.TextField(blank=True, null=True);
  item_deps = models.ManyToManyField(
               'Item',
               through='ItemDep',
               through_fields=( 
                 'depends',
                 'dependent',
               )
           )

  # The text is how the item is asked. Normally, I put codes in the
  # item text itself, since the syntax highlighter will work on them
  # naturally.  If I need to, then I could extract the code, or possibly
  # link to it in some way.
  text      = models.TextField(blank=True, null=True);


  # A separate field for choices to give.
  choices   = models.TextField(blank=True, null=True);

  # The solution takes a different format depending on what the value of form
  # is.  If it's multiple choice, the correct choice is marked.  If multiple
  # selection, the selections are given.  If it's short answer, the answer is
  # just given.  If it's code, then I think an auto-grade rubric should be
  # here.
  solution  = models.TextField(blank=True, null=True);

  # Something I felt was lacking was an explanation of why the answer is
  # the way that it is, especially in the case of multiple choice items.
  explanation = models.TextField(blank=True, null=True);

  # It is possible that some notes may need to accompany a item. An
  # instructor might need to explain how the item should be presented.
  notes = models.TextField(blank=True, null=True);

  # The number of points is essentially the weight of a item, but
  # there's no apparent reason why that can't be automatically determined
  # by the difficulty and level through IRT.  I suppose I could keep it
  # for CTT compatibility.
  points = models.FloatField(default=1, blank=True, null=True);
 

  # This is a simple rendering of the item.
  def __str__(self):

      s  = str(self.id) + ": ";
      s += (self.concept.concept)  + ', [] ';
      s += (self.bloom.bloom)      + ', ';
      s += str(self.form)     + ' (';
      s += str(self.domain)   + ').';
      return s;
 

  def ith_choice(self, line, i, showcorrect):
    letter = chr(ord('a')+i);
    choicestr = "choice-"+letter;
    html  = "<br> <input type='radio' ";
    html += " id='"    + line + "'";
    html += " value='" + line + "'";
    html += " name='response'>";
    html += "<label ";
    if showcorrect and self.solution.strip() == line.strip():
        html += " style='color:green'";
    else: html += "class=mc";
    html += " for="+str(i)+">";
    html += "("+letter+") "+line;
    html += "</label>"
    html += "</input><br>\n";
    return html;


  # In the case of multiple-choice items, this function takes the
  # text in the solution block and scrambles it.
  def get_choices(self, showcorrect):
      html = "";
      lines = self.choices;
      lines = re.sub(r'\n\s+', '\n', lines);
      lines = lines.split('\n');
      random.shuffle(lines);
      if "All of the above" in lines:
        li = lines.index("All of the above");
        swap(lines[li], lines[len(lines)-1]);
      if "None of the above" in lines:
        li = lines.index("None of the above");
        if "All of the above" in lines:
          swap(lines[li], lines[len(lines)-2]);
        else:
          swap(lines[li], lines[len(lines)-1]);
      for i in range(0, len(lines)):
          html += self.ith_choice(lines[i], i, showcorrect);
      return html;


  # This function identifies the actual solution, as marked.
  def get_solution(self):
      if (self.form=="Multiple Choice"):
        lines = self.solution.splitlines();
        html = "";
        i=0;
        for line in lines:
            if line[0] == '*':
               return line[1:];
      elif (self.form=="Short Answer"):
        return self.solution;
      return "NULL";
 

  # Something...
  def textformat(self):
      return publish_parts(self.text, writer_name='html')['html_body'];
 

  def save(self, *args, **kwargs):
      super(Item, self).save(*args, **kwargs);
      if (self.item_deps):
         self.item_deps.clear();
      super(Item, self).save(*args, **kwargs);
      self.associate();
  

  def associate(self):
    if self.item_dep_constraint:
      for q in Item.objects.raw(
          "select * from content_item where "+self.item_dep_constraint):
        ItemDep.create(q, self);





################################################################################
# ItemSet 
#-------------------------------------------------------------------------------
class ItemSet(models.Model):
# An item_set is a series of potential items.
   
  # The item_set should have a descriptive name.  It could be a worksheet,
  # test, or some such other thing.

  locked = models.BooleanField(default=False);

  name      = models.CharField(max_length=64);

  author    = models.ForeignKey(MyUser, blank=True, null=True);

  scheduler = models.CharField(max_length=64, choices=scheduler_types);

  # The constraint indicates what items are allowable by the item_set.
  # They don't all have to be asked. 
  constraint = models.TextField();

  # I feel it is necessary sometimes to add instructions to the very 
  # beginning of the item_set. 
  instructions = models.TextField();

  # The item_set should have open and close times.  Sometimes we want for
  # item_sets to go 'live' before we create them, and we want for them to
  # have deadlines, of course. 
  start_date = models.DateTimeField();
  deadline   = models.DateTimeField();

  retakes = models.IntegerField(default=0);

  # The scale applies a scaling factor to all the points in the item_set.
  # I haven't quite worked this out yet. 
  scale = models.TextField(blank=True, null=True);

  # ItemSets have items.  These are populated by modifying the 
  # constraint.  Until recently, I've mostly done it using the item
  # IDs from the database, but any SQL syntax that targets items can
  # be used.
  items = models.ManyToManyField( 
              Item,
              through='ItemSetItem',
              through_fields=(
                  'item_set',
                  'item',
              )
          )
 

  # The name of this object is the name of item_set.
  def __str__(self):
      return self.name;
 

  # Get all items for this item_set.
  def get_items(self):
      return self.items.all();
 

  # Whenever the constraint is modified, it should re-query the database
  # in case the item set has changed. It should also delete all previous
  # items associated with it.
  def save(self, *args, **kwargs):
      super(ItemSet, self).save(*args, **kwargs);
      if (self.items):
         self.items.clear();
      super(ItemSet, self).save(*args, **kwargs);
      self.associate();
  

  # This simply selects all items by the given constraint and creates
  # the item_set-item relationships.
  def associate(self):
    for q in Item.objects.raw(
        "select * from content_item where "+self.constraint):
      ItemSetItem.create(q, self);


  # FIXME: This is basically the scheduling algorithm, which is really quite
  # poor right now.  Ideally it should use the dependency information,
  # paricularly IIDependencies, in conjunction with data and metadata on
  # the previous items and the user.
  def next_item(self, user, item):
    items = self.items.all();
    
    if self.scheduler=="Linear":
       for i in items:
           if i.id > item.id:
              return i;
           return None
    elif self.scheduler=="Random":
       items = items.order_by('?');
       n = items.count();
       r = random.randint(0, n-1);
       return items[r];
    elif self.scheduler=="Adaptive":
       for i in items:
           if i.id > item.id:
              return i;
           return None

#    first = item;
#    qs    = self.items.all();
#    qs    = qs.order_by('id');
#    it    = iter(qs);
#    num   = 0;
#    for q in it:
#        num += 1;
#        if q.id <= item.id:
#             if not user.has_answered_item(q.id) and q.id <  first.id:
#                first = q;
#                print "First item not answered: "+str(first.id);
#          elif not user.has_answered_item(q.id) and q.id != item.id:
#               break;
#      if num >= qs.count():
#         if   item.id <  q.id:
#              return "<a href='"+settings.BASE_URL+"item/"  +str(self.id)+"/"+str(q.id)+"/'"+">&gt;</a>";
#         elif num == qs.count()  : 
#              return "<a href='"+settings.BASE_URL+"item_set/"+str(self.id)+"/'>&lt;&lt;</a>";
#         elif item.id == q.id: 
#              return "<a href='"+settings.BASE_URL+"item/"  +str(self.id)+"/"+str(first.id)+"/'"+">&lt;</a>";
#         else:return "<a href='"+settings.BASE_URL+"item_set/'>&lt;&lt;</a>";
#      return "<a href='"+settings.BASE_URL+"item/"+str(self.id)+"/"+str(q.id)+"/'"+">&gt;</a>";




################################################################################
# Describes ItemSet-Item relationship
#-------------------------------------------------------------------------------
class ItemSetItem(models.Model):
 
  item       = models.ForeignKey(Item);
  item_set = models.ForeignKey(ItemSet);
 
  @classmethod
  def create(cls, item, item_set):
    aq = cls(item=item, item_set=item_set);
    super(ItemSetItem, aq).save();
    return aq;
 
  def __str__(self):
    return str(self.item_set)+": "+str(self.item);






################################################################################
# Course (contains users)
#-------------------------------------------------------------------------------
class Course(models.Model):
# Courses have users, item_sets, and lessons.
   
  # The course should have a name, something like CSC 1254.
  name        = models.CharField(max_length=64);

  # The section number.
  section     = models.IntegerField();

  # The semester should be the starting date for the first class. This is
  # needed to distinguish courses at different times.
  semester    = models.DateTimeField();


  # The userlist is used to populate the course with users. It
  # contains one user e-mail address per line.  
  userlist = models.TextField();
  users    = models.ManyToManyField(
                 MyUser,
                 through='CourseUser',
                 through_fields=(
                     'section',
                     'user',
                 ),
                 related_name='users',
             )


  # I have decided that courses shall have item_sets. 
  item_setlist = models.TextField(blank=True);
  item_sets = models.ManyToManyField(
                    ItemSet,
                    through='CourseItemSet',
                    through_fields=(
                        'course',
                        'item_set',
                    )
                )
 
  # Min-length sane description of the course.
  def __str__(self):
      return str(self.name)+": "+str(self.section)+", "+str(self.semester);

  # FIXME: Every time a course is edited, the user-course associations 
  # are re-populated. This is not what would be generally expected; we
  # should just be able to add a user. Clearing the associations is
  # bad because of all the data associated with them, like profile 
  # information, and the current grade in the class.
  def save(self, *args, **kwargs):
      super(Course, self).save(*args, **kwargs);
      if (self.users):
         self.users.clear();
      super(Course, self).save(*args, **kwargs);
      self.associate();
 

  def associate(self):
      list = self.userlist.split('\n');
      for useremail in list[0]:
        for user in MyUser.objects.raw(
          "select * from content_myuser where email='"+useremail+"'"):
            u = CourseUser.create(user, self);
            u.admin = True;
#      if len(list) > 1:
#        for useremail in list[1]:
#          for user in MyUser.objects.raw(
#            "select * from content_myuser where email='"+useremail+"'"):
#              CourseUser.create(user, self);
      querylist = self.item_setlist.split('\n');
      for clause in querylist:
        for item_set in ItemSet.objects.raw(
          "select * from content_item_set where "+clause):
            CourseItemSet.create(self, item_set);

 


################################################################################
# Describes Course-User relationship
#-------------------------------------------------------------------------------
class CourseUser(models.Model):

      user    = models.ForeignKey(MyUser);
      section = models.ForeignKey(Course);
      active  = models.BooleanField(default=True);
      admin   = models.BooleanField(default=False);
     
      @classmethod
      def create(cls, user, section):
          cs = cls(user=user, section=section);
          super(CourseUser, cs).save();
          return cs;
     
      def __str__(self):
          return str(self.user)+": "+str(self.section);




################################################################################
# Describes Course-ItemSet relationship
#-------------------------------------------------------------------------------
class CourseItemSet(models.Model):
      course     = models.ForeignKey(Course);
      item_set = models.ForeignKey(ItemSet);
     
      @classmethod
      def create(cls, course, item_set):
          cs = cls(item_set=item_set, course=course);
          super(CourseItemSet, cs).save();
          return cs;
     
      def __str__(self):
          return str(self.item_set)+": "+str(self.course);




################################################################################
# Describes Item-Item dependency 
#-------------------------------------------------------------------------------
class ItemDep(models.Model):

      depends   = models.ForeignKey(Item, related_name="depends");
      dependent = models.ForeignKey(Item, related_name="dependent");
     
      @classmethod
      def create(cls, depends, dependent):
          cs = cls(depends=depends, dependent=dependent);
          super(ItemDep, cs).save();
          return cs;
     
      def __str__(self):
          return str(self.depends)+" -> "+str(self.dependent);




################################################################################
# Response (user response to a item)
#-------------------------------------------------------------------------------
class Response(models.Model):
# A response is currently a file that links a user and a item, but this
# is much too much. I would prefer to have each response as a single line in a
# file under the user's name.

  user     = models.ForeignKey(MyUser,  on_delete=models.CASCADE, null=True);
  item     = models.ForeignKey(Item,    on_delete=models.CASCADE, null=True);
  set      = models.ForeignKey(ItemSet, on_delete=models.CASCADE, null=True);
  course   = models.ForeignKey(Course,  on_delete=models.CASCADE, null=True);
  response = models.TextField();



class Theta(models.Model):
  user     = models.ForeignKey(MyUser,  on_delete=models.CASCADE, null=True);
  bloom    = models.ForeignKey(Bloom,   on_delete=models.CASCADE, null=True);
  concept  = models.ForeignKey(Concept, on_delete=models.CASCADE, null=True);
  level    = models.ForeignKey(Level,   on_delete=models.CASCADE, null=True);
