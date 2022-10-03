from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic, View
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm, ContactForm, ContactModelFormset
from django_tables2 import SingleTableView




from .models import Question, Choice, Contact, PersonalContact, WorkContact
from .tables import QuestionTable, ContactTable

# Register, login, change password, ecc...

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'polls/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='polls:index')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'polls/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('polls:index')

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'polls/password_reset.html'
    email_template_name = 'polls/password_reset_email.html'
    subject_template_name = 'polls/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('polls:index')


        

# Polls views

class IndexView(SingleTableView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    model = Question
    table_class = QuestionTable

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """

        return Question.objects.raw('SELECT * FROM polls_question ORDER BY pub_date DESC LIMIT 5')

       
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))



# user views

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='polls:profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'polls/profile.html', {'user_form': user_form, 'profile_form': profile_form})



class PersonalAddressBookView(SingleTableView):

    template_name = 'polls/address_book.html'
    table_class = ContactTable

    def get_queryset(self):
        
        return Contact.objects.filter(personalcontact__user= self.request.user)

    def get(self, request, *args, **kwargs):
        formset = ContactModelFormset(queryset=Contact.objects.none())
        return render(request, self.template_name, 
            {'formset': formset, 'table' : self.get_table()})

    def post(self, request, *args, **kwargs):
        
        formset = ContactModelFormset(request.POST)
        
        if formset.is_valid():
            for form in formset:
                # only save if first_name is present
                #if form.cleaned_data.get('first_name'):
                if form.is_valid():
                    new_contact = form.save(commit=False)
                    new_contact.save()
                    PersonalContact.objects.create(user=request.user,contact=new_contact)
                    messages.success(request, 'Contact for {0} created successfully'.format(new_contact.first_name))
            return redirect('polls:personal_address_book')
        else:
            messages.error(request, 'error')
        return render(request, self.template_name, {'formset': formset})

class WorkAddressBookView(SingleTableView):

    template_name = 'polls/address_book.html'
    table_class = ContactTable
    
    def get_queryset(self):
        
        return Contact.objects.filter(workcontact__user= self.request.user)

    def get(self, request, *args, **kwargs):

        formset = ContactModelFormset(queryset=Contact.objects.none())
        return render(request, self.template_name, 
            {'formset': formset, 'table': self.get_table()})

    def post(self, request, *args, **kwargs):
        
        formset = ContactModelFormset(request.POST)
        
        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    #new_contact = Contact.objects.create(user=request.user)
                    #contact_form = ContactForm(request.POST, instance=new_contact)
                    new_contact = form.save(commit=False)
                    new_contact.save()
                    WorkContact.objects.create(user=request.user,contact=new_contact)
                    messages.success(request, 'Contact for {0} created successfully'.format(new_contact.first_name))
            return redirect('polls:work_address_book')
        else:
            messages.error(request, 'error')
        return render(request, self.template_name, {'formset': formset})

@login_required
def contact(request, contact_id):

    contact = get_object_or_404(Contact, pk=contact_id)
    
    if request.method == 'POST':    
        
        contact_form = ContactForm(request.POST, request.FILES, instance=contact)

        if contact_form.is_valid():
            contact_form.save()
            messages.success(request, 'Contact updated successfully')
            return redirect(to='polls:contact', contact_id=contact.id)
    else:
        contact_form = ContactForm(instance=contact)

    return render(request, 'polls/contact.html', {'contact_form': contact_form, 'contact':contact})

@login_required
def contact_delete(request, contact_id):
    redirect_to = 'polls:contact_list'
    target_contact = get_object_or_404(Contact, pk=contact_id)
    
    if PersonalContact.objects.filter(contact=target_contact).exists():
        redirect_to = 'polls:personal_address_book'
    elif WorkContact.objects.filter(contact=target_contact).exists():
        redirect_to = 'polls:work_address_book'

    target_contact.delete()

    return redirect(to=redirect_to)











