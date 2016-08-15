# tables.py
import django_tables2 as tables

class QuestionTable(tables.Table):
    class Meta:
        model = Question
