import io
import csv

from django.http import HttpResponse
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from .models import Engagement, Registro
from .forms import EngagementForm, RegistroForm, CSVUploadForm, SaldoUpdateForm
from django.http import Http404
from django.urls import reverse_lazy, reverse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .secrets import smtp_server, smtp_port, smtp_username, smtp_password

# Configurações do servidor de e-mail (substitua com suas próprias configurações)
# smtp_server = "smtp.sapo.pt"
# smtp_port = 587
# smtp_username = "cwconfirmations@sapo.pt"
# smtp_password = "Bestino2004!"

class EngagementCreateView(CreateView):
    model = Engagement
    fields = ['cliente', 'referencia']
    template_name = 'criar_engagement.html'
    success_url = reverse_lazy('engagement_list')

class EngagementUpdateView(UpdateView):
    model = Engagement
    fields = ['cliente', 'referencia']
    template_name = 'engagement_form.html'

class EngagementListView(ListView):
    model = Engagement
    template_name = 'engagement_list.html'
    context_object_name = 'engagements'

class EngagementDetailView(DetailView):
    model = Engagement
    template_name = 'engagement_detail.html'
    context_object_name = 'engagement'
    

class ImportarCSVParaEngagement(View):
    template_name = 'importar_csv_engagement.html'

    def get(self, request, pk):
        engagement = Engagement.objects.get(pk=pk)
        form = CSVUploadForm()
        return render(request, self.template_name, {'engagement': engagement, 'form': form})

    def post(self, request, pk):
        engagement = Engagement.objects.get(pk=pk)
        form = CSVUploadForm(request.POST, request.FILES)

        if form.is_valid():
            csv_file = request.FILES['file']
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            next(io_string)
            for column in csv.reader(io_string, delimiter=';', quotechar="|"):
                _, created = Registro.objects.update_or_create(
                    engagement=engagement,
                    terceiro=column[0],
                    contacto=column[1],
                    email=column[2]
                )
            return redirect('engagement_detail', pk=pk)

        return render(request, self.template_name, {'engagement': engagement, 'form': form})




# class ImportarCSV(View):
#     template_name = 'importar_csv.html'  # Defina o nome do template

#     def post(self, request):
#         engagement_id = request.POST.get('engagement')
#         try:
#             engagement = Engagement.objects.get(pk=engagement_id)
#         except Engagement.DoesNotExist:
#             # Lide com o caso em que o Engagement não existe
#             return HttpResponse("Engagement não encontrado")

#         form = CSVUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             csv_file = request.FILES['file']
#             data_set = csv_file.read().decode('UTF-8')
#             io_string = io.StringIO(data_set)
#             next(io_string)
#             for column in csv.reader(io_string, delimiter=';', quotechar="|"):
#                 Registro.objects.create(
#                     engagement=engagement,
#                     terceiro=column[1],
#                     contacto=column[2],
#                     email=column[3]
#                 )
#             return HttpResponse("CSV importado com sucesso")

#         return render(request, self.template_name, {'form': form})


# class ImportarCSV(View):
#     template_name = 'importar_csv.html'  # Define o nome do template

#     def get(self, request):
#         form = CSVUploadForm()  # Crie uma instância do formulário
#         return render(request, self.template_name, {'form': form})

#     def post(self, request):
#         form = CSVUploadForm(request.POST, request.FILES)  # Crie uma instância do formulário com dados da solicitação

#         if form.is_valid():
#             csv_file = request.FILES['file']
#             data_set = csv_file.read().decode('UTF-8')
#             io_string = io.StringIO(data_set)
#             next(io_string)
#             for column in csv.reader(io_string, delimiter=';', quotechar="|"):
#                 try:
#                     # Retrieve the Engagement instance by cliente or referencia
#                     engagement = Engagement.objects.get(id=column[0])
#                 except Engagement.DoesNotExist:
#                     # Handle the case where Engagement doesn't exist
#                     continue
#                 _, created = Registro.objects.update_or_create(
#                     engagement=engagement,
#                     terceiro=column[1],
#                     contacto=column[2],
#                     email=column[3]
#                 )
#             return visualizar(request)

#         return render(request, self.template_name, {'form': form})

def visualizar(request):
    registros = Registro.objects.all()
    return render(request, 'visualizar.html', {'registros': registros})


def editar_registro(request, registro_id):
    registro = get_object_or_404(Registro, pk=registro_id)
    
    if request.method == "POST":
        form = RegistroForm(request.POST, instance=registro)
        if form.is_valid():
            form.save()
            return redirect('visualizar')
    else:
        form = RegistroForm(instance=registro)
    
    return render(request, 'editar_registro.html', {'form': form, 'registro': registro})


def excluir_registro(request, registro_id):
    registro = get_object_or_404(Registro, pk=registro_id)
    
    if request.method == "POST":
        registro.delete()
        return redirect('visualizar')
    
    return render(request, 'excluir_registro.html', {'registro': registro})


def home(request):
    return render(request, 'home.html')


class EnviarEmailEngagement(View):
    def get(self, request, engagement_id):
        engagement = get_object_or_404(Engagement, pk=engagement_id)
        registros = engagement.registro_set.filter(extrato=False)  # Filtrar registros não confirmados

    def post(self, request, engagement_id):
        engagement = get_object_or_404(Engagement, pk=engagement_id)
        registros = engagement.registro_set.filter(extrato=False)  # Filtrar registros não confirmados
        for registro in registros:
            # Coloque o código de envio de e-mails aqui
            link_unico = registro.link_unico
            url = request.build_absolute_uri(reverse('pagina_saldo', args=[link_unico]))
            msg = MIMEMultipart()
            msg['From'] = 'cwconfirmations@sapo.pt'
            msg['To'] = registro.email
            msg['Subject'] = 'Confirmação de Atualização de Saldo'

            message = f"""
            Olá {registro.contacto},
            
            Para confirmar a atualização de saldo, clique no link abaixo:
            {url}

            Obrigado por usar nosso serviço.
            """
            msg.attach(MIMEText(message, 'plain'))

            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(smtp_username, registro.email, msg.as_string())
            server.quit()

        return render(request, 'enviar_emails.html', {'registros': registros, 'engagement': engagement})


class EnviarEmailRegistro(View):
    def get(self, request, registro_id):
        registro = get_object_or_404(Registro, pk=registro_id)

        # Check if the record has not been confirmed
        if not registro.extrato:
            # Build the unique URL for the record
            link_unico = registro.link_unico
            url = request.build_absolute_uri(reverse('pagina_saldo', args=[link_unico]))

            # Create and send the email
            msg = MIMEMultipart()
            msg['From'] = 'cwconfirmations@sapo.pt'
            msg['To'] = registro.email
            msg['Subject'] = 'Confirmação de Atualização de Saldo'

            message = f"""
            Olá {registro.contacto},
            
            Para confirmar a atualização de saldo, clique no link abaixo:
            {url}

            Obrigado por usar nosso serviço.
            """
            msg.attach(MIMEText(message, 'plain'))

            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(smtp_username, registro.email, msg.as_string())
            server.quit()

        return render(request, 'enviar_emails.html', {'registro': registro})



# class EnviarEmail(View):
#     def get(self, request):
#         # Renderize a página para exibir os registros
#         registros = Registro.objects.all()
#         return render(request, 'enviar_emails.html', {'registros': registros})

#     def post(self, request):
#         # Loop para enviar e-mails para cada linha de dados
#         for registro in Registro.objects.all():
#             # Coloque o código de envio de e-mails aqui
#             link_unico = registro.link_unico
#             url = '/pagina_saldo/{}'.format(link_unico)
#             msg = MIMEMultipart()
#             msg['From'] = 'cwconfirmations@sapo.pt'
#             msg['To'] = registro.email
#             msg['Subject'] = 'Confirmação de Atualização de Saldo'

#             message = f"""
#             Olá {registro.terceiro},
            
#             Para confirmar a atualização de saldo, clique no link abaixo:
#             {url}

#             Obrigado por usar nosso serviço.
#             """
#             msg.attach(MIMEText(message, 'plain'))

#             server = smtplib.SMTP(smtp_server, smtp_port)
#             server.starttls()
#             server.login(smtp_username, smtp_password)
#             server.sendmail(smtp_username, registro.email, msg.as_string())
#             server.quit()

#         return render(request, 'enviar_emails.html')  # Redirecione para uma página de sucesso





class PaginaSaldo(View):
    template_name = 'pagina_saldo.html'

    def get(self, request, link_unico):
        # Verifique se o link único é válido e se corresponde a um registro existente
        try:
            registro = Registro.objects.get(link_unico=link_unico, extrato=False)
        except Registro.DoesNotExist:
            # Caso não exista um registro com esse link único, você pode lidar com isso adequadamente, como redirecionar para uma página de erro.
            return redirect('pagina_erro')

        # Crie uma instância do formulário para permitir que o usuário atualize o saldo
        form = SaldoUpdateForm()

        # Renderize a página com o formulário
        return render(request, self.template_name, {'form': form, 'registro': registro})

    def post(self, request, link_unico):
        # Verifique se o link único é válido e se corresponde a um registro existente
        try:
            registro = Registro.objects.get(link_unico=link_unico, extrato=False)
        except Registro.DoesNotExist:
            # Caso não exista um registro com esse link único, você pode lidar com isso adequadamente, como redirecionar para uma página de erro.
            return redirect('pagina_erro')

        # Crie uma instância do formulário com os dados da solicitação POST
        form = SaldoUpdateForm(request.POST, request.FILES)

        if form.is_valid():
            # Atualize o registro com os dados do formulário
            saldo = form.cleaned_data['saldo']
            arquivo = form.cleaned_data['arquivo']

            registro.saldo = saldo
            if arquivo:
                registro.arquivo = arquivo
                

            # Marque o registro como atualizado
            registro.extrato = True
            registro.save()

            # Redirecione para uma página de sucesso
            return redirect('pagina_sucesso')

        # Caso o formulário não seja válido, renderize a página novamente com o formulário e erros
        return render(request, self.template_name, {'form': form, 'registro': registro})



class PaginaSucesso(View):
    template_name = 'pagina_sucesso.html'

    def get(self, request):
        return render(request, self.template_name)
    


class PaginaErro(View):
    template_name = 'pagina_erro.html'

    def get(self, request):
        return render(request, self.template_name)

