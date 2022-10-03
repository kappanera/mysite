import django_tables2 as tables
from .models import Question, Contact
from django_tables2.utils import A  # alias for Accessor

class QuestionTable(tables.Table):

	question_text = tables.LinkColumn("polls:detail", args=[A("pk")])

	class Meta:
	        model = Question
	        template_name = "django_tables2/bootstrap.html"
	        fields = ("question_text", "pub_date")

class ContactTable(tables.Table):

	id = tables.LinkColumn("polls:contact", args=[A("pk")], verbose_name="contact")

	class Meta:
	        model = Contact
	        template_name = "django_tables2/bootstrap.html"
	        fields = ("id", "first_name", "last_name", "phone", "email" )
	        order_by = "last_name"