import json

from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from django.views import View
from django.views import generic
from django.core.serializers import serialize
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404


from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

UserModel = get_user_model()
from .forms import SignUpForm

from .models import Product


class index(View):
    def get(self, request):
        return HttpResponse("hello world!!!")


class signup(View):
    def get(self, request):
        return render(request, 'shop/signup.html')

    def post(self, request):
        form = SignUpForm(request.POST)

        customer_group, created = Group.objects.get_or_create(name='Customer')

        # print(SignUpForm)
        print(form.errors.as_data())
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            customer_group.user_set.add(user)
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('shop/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
        else:
            form = SignUpForm()
        return render(request, 'shop/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


class ProductListView(View):
    def get(self, request):
        qs = Product.objects.all()
        data = serialize("json", qs)
        return HttpResponse(data, content_type="application/json")

class ProductDetailView(View):
    def get(self, request, pk):
        try:
            qs = Product.objects.filter(pk=pk)
        except Product.DoesNotExist:
            raise Http404('Book does not exist')

        data = serialize("json", qs)
        return HttpResponse(data, content_type="application/json")
