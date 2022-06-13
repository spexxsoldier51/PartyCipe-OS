from pprint import pprint

from django.shortcuts import render, redirect

from .forms import UserCreationForm, CreatePartyForm
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse
from django.core.signing import BadSignature
from django.http import Http404
from django.core import mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import *
import django_tables2 as tables
from django.contrib.auth.decorators import login_required
from django_tables2.utils import A

class ParticipateTable(tables.Table):
    name = tables.Column(accessor='party.name', verbose_name="Nom de la soirée",)
    resume = tables.Column(accessor='party.resume', verbose_name="Description",)
    datehour = tables.Column(accessor='party.datehour', verbose_name="Date/Heure",)
    place = tables.Column(accessor='party.place', verbose_name="Lieu",)
    organisate = tables.Column(accessor='party.organisate', verbose_name="Organisateur",)
    price = tables.Column(accessor='party.price', verbose_name="Prix",)
    paypal = tables.Column(accessor='party.paypal', verbose_name="Lien Paypal",)
    etat = tables.BooleanColumn(accessor='etat', verbose_name="Participation")
    changer = tables.LinkColumn("ChangeParticipate", text="Modifier", args=[A("pk")], verbose_name="Changer la participation")

    class Meta:
        model = participate
        fields = ('name', 'resume', 'place', 'datehour', 'price', 'paypal', 'organisate', 'etat')
        attrs = {"class": "table table-dark table-striped"}

class PartyTable(tables.Table):
    Name = tables.Column(verbose_name="Nom de la soirée", accessor='name')
    Detail = tables.LinkColumn("party_detail", args=[A("pk")], verbose_name="Détail", text="Détail")
    class Meta:
        model = party
        attrs = {"class": "table table-dark table-striped"}

@login_required
def ChangeParticipate(request, id):
    queryset = participate.objects.filter(pk=id)
    print(queryset[0].utilisateur)
    if queryset[0].utilisateur == request.user:
        queryset.update(etat=(not queryset[0].etat))
    return Home(request)

def party_detail(request, id):
    p = party.objects.get(pk=id)
    return redirect(p.get_absolute_url())

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

@login_required
def Home(request):
    if(request.user):
        queryset = participate.objects.filter(utilisateur=request.user)

        queryset2 = party.objects.filter(organisate=request.user)

        table = ParticipateTable(queryset)

        table2 = PartyTable(queryset2)
        table.exclude = ('id', 'created', 'last_updated',)
        table2.exclude = ('id', 'created', 'last_updated', 'name', 'organisate', 'paypal', 'resume', 'place', 'datehour', 'price')

        return render(request, "home.html", {'table': table, 'table2': table2})
    else:
        return render(request, "home.html")



@login_required
def JoinParty(request):
    if request.method == "POST":
        print(request.POST["id_party"])
        return redirect(request.POST["id_party"]+"/join")
    else:
        return render(request, 'party/join.html')


@login_required
def JoinPartyId(request):
    output = "test"
    return HttpResponse(output)



@login_required
def party_status(request, signed_pk):
    try:
        pk = party.signer.unsign(signed_pk)
        theparty = party.objects.get(id=pk)
        participants = participate.objects.filter(party=pk, etat=True)
        if(request.user == theparty.organisate):
            retour = render(request, "party/page.html", {'party': theparty, 'participate' : participants})
        else:
            retour = redirect("/")
    except (BadSignature, party.DoesNotExist):
        raise Http404('No party matches the given query.')
    return retour


@login_required
def party_join(request, signed_pk):
    try:
        pk_ici = party.signer.unsign(signed_pk)
        party_id = party.objects.get(id=pk_ici)
        verif = participate.objects.get(utilisateur=request.user, party=party_id)
        if(not verif):
            participate_var = participate(utilisateur=request.user, party=party_id, etat=True)
            participate_var.save()
    except (BadSignature, party.DoesNotExist):
        raise Http404('No party matches the given query.')
    return redirect("/")


@login_required
def create_party(request):
    if request.method == "POST":
        pprint(request.POST)
        form = CreatePartyForm(request.POST).save(commit=False)
        form.organisate = request.user
        form.save()
        try:
            party_id = party.objects.get(id=form.pk)
            participate_var = participate(utilisateur=request.user, party=party_id, etat=False)
            participate_var.save()
        except (BadSignature, party.DoesNotExist):
            raise Http404('No party matches the given query.')
        return redirect(form.get_absolute_url())
    else:
        form = CreatePartyForm()
        return render(request, 'party/create_form.html', {'form': form})

@login_required
def send_mail(request, signed_pk):
    try:
        pk_ici = party.signer.unsign(signed_pk)
        theparty = party.objects.get(id=pk_ici)
        if (theparty.organisate == request.user):
            html_template = 'mail/message.html'
            html_message = render_to_string(html_template, {'party': theparty})
            from_email="no-reply@partycipe.fr"
            to="noreply.partycipe@gmail.com"
            bcc=["arthur.lambotte51@gmail.com", "arthur.lambotte.auditeur@lecnam.net"]
            message = EmailMessage('Rappel de soirée', html_message, from_email, [to], bcc)
            message.content_subtype = 'html'  # this is required because there is no plain text email message

            pprint(message)
            message.send()

            return redirect("/")
    except (BadSignature, party.DoesNotExist):
        raise Http404('No party matches the given query.')
    return redirect("/")

