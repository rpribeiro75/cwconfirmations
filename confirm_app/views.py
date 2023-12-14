import io
import csv
import json
import openpyxl
from datetime import datetime
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from .models import Cliente, Engagement, PedidoTerceiros
from .forms import ClienteForm, EngagementForm, CriarPedidoTerceirosForm, PedidoTerceirosForm, CSVUploadForm, SaldoUpdateForm
from django.http import Http404
from django.urls import reverse_lazy, reverse
from django.contrib import messages
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from .secrets import smtp_server, smtp_port, smtp_username, smtp_password

# Configurações do servidor de e-mail (substitua com suas próprias configurações)
# smtp_server = "smtp.sapo.pt"
# smtp_port = 587
# smtp_username = "cwconfirmations@sapo.pt"
# smtp_password = "Bestino2004!"

def home(request):
    engagements = Engagement.objects.all()
    pedidos = PedidoTerceiros.objects.all()
    for i in pedidos:
        print(i.engagement_id)
    return render(request, 'home.html',  {'engagements': engagements, 'pedidos':pedidos})


class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'cliente_criar.html'
    success_url = reverse_lazy('cliente_list')


class ClienteListView(ListView):
    model = Cliente
    template_name = 'cliente_list.html'
    context_object_name = 'clientes'  

class ClienteDetailView(DetailView):
    model = Cliente
    template_name = 'cliente_detail.html'
    context_object_name = 'cliente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = EngagementForm()  # Adiciona o formulário de engagement ao contexto
        return context


class EngagementCreateView(CreateView):
    model = Engagement
    form_class = EngagementForm
    # template_name = 'engagement_criar.html'

    def form_valid(self, form):
        form.instance.cliente_id = self.kwargs['cliente_pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('cliente_detail', kwargs={'pk': self.kwargs['cliente_pk']})

class EngagementUpdateView(UpdateView):
    model = Engagement
    fields = ['cliente', 'engagement_referencia', "pdf_assinado"]
    template_name = 'engagement_form.html'

class EngagementListView(ListView):
    model = Engagement
    template_name = 'engagement_list.html'
    context_object_name = 'engagements'

class EngagementDetailView(DetailView):
    model = Engagement
    template_name = 'engagement_detail.html'
    context_object_name = 'engagement'

class PedidoTerceirosCriarView(View):
    template_name = 'pedido_terceiro_criar.html'
    
    def get(self, request, pk):
        engagement = get_object_or_404(Engagement, id=pk)
        form = CriarPedidoTerceirosForm(initial={'engagement': pk})
        return render(request, self.template_name, {"form": form, 'engagement': engagement})

    def post(self, request, pk):
        engagement = get_object_or_404(Engagement, id=pk)
        form = CriarPedidoTerceirosForm(request.POST or None, initial={'engagement': pk})
        
        if form.is_valid():
            saveform = form.save(commit=False)
            saveform.engagement = engagement
            saveform.save()
            return redirect('engagement_detail', pk=pk)
        
        return render(request, self.template_name, {"form": form, 'engagement': engagement})
    

def pedidoterceiro_editar(request, pedidoterceiro_id):
    pedidoterceiro = get_object_or_404(PedidoTerceiros, pk=pedidoterceiro_id)
    

    if request.method == "POST":
        # cliente
        movsctb_cliente=request.POST.get("movsctb_cliente")
        pedidoterceiro.movsctb_cliente=movsctb_cliente
        movsterceiro_cliente=request.POST.get("movsterceiro_cliente")
        pedidoterceiro.movsterceiro_cliente=movsterceiro_cliente
        conciliado_cliente=request.POST.get("conciliado_cliente")
        pedidoterceiro.conciliado_cliente=conciliado_cliente

        # cliente titulos
        movsctb_cliente_titulos=request.POST.get("movsctb_cliente_titulos")
        pedidoterceiro.movsctb_cliente_titulos=movsctb_cliente_titulos
        movsterceiro_cliente_titulos=request.POST.get("movsterceiro_cliente_titulos")
        pedidoterceiro.movsterceiro_cliente_titulos=movsterceiro_cliente_titulos
        conciliado_cliente_titulos=request.POST.get("conciliado_cliente_titulos")
        pedidoterceiro.conciliado_cliente_titulos=conciliado_cliente_titulos
        
        # fornecedor
        movsctb_fornecedor=request.POST.get("movsctb_fornecedor")
        pedidoterceiro.movsctb_fornecedor=movsctb_fornecedor
        movsterceiro_fornecedor=request.POST.get("movsterceiro_fornecedor")
        pedidoterceiro.movsterceiro_fornecedor=movsterceiro_fornecedor
        conciliado_fornecedor=request.POST.get("conciliado_fornecedor")
        pedidoterceiro.conciliado_fornecedor=conciliado_fornecedor
        
        # fornecedor titulos
        movsctb_fornecedor_titulos=request.POST.get("movsctb_fornecedor_titulos")
        pedidoterceiro.movsctb_fornecedor_titulos=movsctb_fornecedor_titulos
        movsterceiro_fornecedor_titulos=request.POST.get("movsterceiro_fornecedor_titulos")
        pedidoterceiro.movsterceiro_fornecedor_titulos=movsterceiro_fornecedor_titulos
        conciliado_fornecedor_titulos=request.POST.get("conciliado_fornecedor_titulos")
        pedidoterceiro.conciliado_fornecedor_titulos=conciliado_fornecedor_titulos
        
        # odc
        movsctb_odc=request.POST.get("movsctb_odc")
        pedidoterceiro.movsctb_odc=movsctb_odc
        movsterceiro_odc=request.POST.get("movsterceiro_odc")
        pedidoterceiro.movsterceiro_odc=movsterceiro_odc
        conciliado_odc=request.POST.get("conciliado_odc")
        pedidoterceiro.conciliado_odc=conciliado_odc
        
        # outros
        movsctb_outros=request.POST.get("movsctb_outros")
        pedidoterceiro.movsctb_outros=movsctb_outros
        movsterceiro_outros=request.POST.get("movsterceiro_outros")
        pedidoterceiro.movsterceiro_outros=movsterceiro_outros
        conciliado_outros=request.POST.get("conciliado_outros")
        pedidoterceiro.conciliado_outros=conciliado_outros

        pedidoterceiro.save()
        url = reverse('pedidoterceiro_editar', kwargs={'pedidoterceiro_id': pedidoterceiro_id})
        return HttpResponseRedirect(url)


    return render(request, "pedidoterceiro_editar.html", {"pedidoterceiro": pedidoterceiro})


class GenerateCSVFile(View):
    def get(self, request):
        # Create the Excel workbook object
        workbook = openpyxl.Workbook()

        # Create the worksheet object
        worksheet = workbook.active

        # Write the header row
        worksheet.append(['Terceiro', 'Contacto', 'Email'])

        # Save the workbook
        workbook.save('modelo_importacao.xlsx')

        # Set the Content-Disposition header for download
        filename = 'modelo_importacao.xlsx'
        with open('modelo_importacao.xlsx', 'rb') as f:
            response = HttpResponse(f, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        return response


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
                _, created = PedidoTerceiros.objects.update_or_create(
                    engagement=engagement,
                    terceiro=column[0],
                    contacto=column[1],
                    email=column[2]
                )
            return redirect('engagement_detail', pk=pk)

        return render(request, self.template_name, {'engagement': engagement, 'form': form})



# def visualizar(request):
#     registros = PedidoTerceiros.objects.all()
#     return render(request, 'visualizar.html', {'registros': registros})



# def excluir_registro(request, registro_id):
#     registro = get_object_or_404(Registro, pk=registro_id)
    
#     if request.method == "POST":
#         registro.delete()
#         return redirect('visualizar')
    
#     return render(request, 'excluir_registro.html', {'registro': registro})





class EnviarEmailEngagement(View):
    # def get(self, request, engagement_id):
    #     engagement = get_object_or_404(Engagement, pk=engagement_id)
    #     registros = engagement.pedidoterceiros_set.filter(respondido=False)  # Filtrar registros não confirmados

    def post(self, request, engagement_id):
        engagement = get_object_or_404(Engagement, pk=engagement_id)
        registros = engagement.pedidoterceiros_set.filter(respondido__isnull=True)
        registros_nao_enviados = engagement.pedidoterceiros_set.exclude(respondido__isnull=True)
        terceiros = []
        for registro in registros_nao_enviados: terceiros.append(registro.terceiro)
        mensagem = f"""Para os seguintes Terceiros não foi enviado: {" ,".join(terceiros)}"""
        for registro in registros:
            link_unico = registro.link_unico
            url = request.build_absolute_uri(reverse('pagina_saldo', args=[link_unico]))
                             
            msg = MIMEMultipart()
            msg['From'] = 'cwconfirmations@sapo.pt'
            msg['To'] = registro.email
            msg['Subject'] = 'Confirmação de Atualização de Saldo'
            if engagement.pdf_assinado:
                filename = engagement.pdf_assinado.name.split("/")[-1]
                attachment = open(engagement.pdf_assinado.path, 'rb')
                part = MIMEBase('application', 'octet-stream')
                part.set_payload((attachment).read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f"attachment; filename= {filename}")

                msg.attach(part)    
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
        
        messages.info(request, mensagem)
        return HttpResponseRedirect("/engagement/"+str(registro.engagement_id))
        # return render(request, 'enviar_emails_todos.html', {'registros': registros, 'engagement': engagement})


class EnviarEmailRegistro(View):

    def get (self, request, registro_id):
        return render(request,"pagina_erro.html")
    def post(self, request, registro_id):
        registro = get_object_or_404(PedidoTerceiros, pk=registro_id)
        if registro.engagement.pdf_assinado:
            # Check if the record has not been confirmed
            if not registro.respondido:
                # Build the unique URL for the record
                link_unico = registro.link_unico
                url = request.build_absolute_uri(reverse('pagina_saldo', args=[link_unico]))

                # Create and send the email
                msg = MIMEMultipart()
                msg['From'] = 'cwconfirmations@sapo.pt'
                msg['To'] = registro.email
                msg['Subject'] = 'Confirmação de Atualização de Saldo'
                
                filename = registro.engagement.pdf_assinado.name.split("/")[-1]
                attachment = open(registro.engagement.pdf_assinado.path, 'rb')
                part = MIMEBase('application', 'octet-stream')
                part.set_payload((attachment).read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f"attachment; filename= {filename}")

                msg.attach(part)   

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
                if PedidoTerceiros.objects.filter(pk=registro_id).first().primeiro_envio is None:
                    PedidoTerceiros.objects.update_or_create(pk=registro_id, defaults={"primeiro_envio":datetime.now()})
                else:
                    PedidoTerceiros.objects.update_or_create(pk=registro_id, defaults={"ultimo_envio":datetime.now()})
                messages.info(request, "Email enviado com sucesso")
                return HttpResponseRedirect("/engagement/"+str(registro.engagement_id))
            
            else:
                messages.info(request, "Erro ao enviar e-mail. já está respondido.")
                return HttpResponseRedirect("/engagement/"+str(registro.engagement_id))
            
         
        else:
            
            messages.info(request, "Erro ao enviar e-mail. O Engagement não tem autorização.")
            return HttpResponseRedirect("/engagement/"+str(registro.engagement_id))
               



class PaginaSaldo(View):
    template_name = 'pagina_saldo.html'

    def get(self, request, link_unico):
        # Verifique se o link único é válido e se corresponde a um registro existente
        try:
            registro = PedidoTerceiros.objects.get(link_unico=link_unico, respondido__isnull=True)
            print(registro.engagement.id)
        except PedidoTerceiros.DoesNotExist:
            # Caso não exista um registro com esse link único, você pode lidar com isso adequadamente, como redirecionar para uma página de erro.
            return redirect('pagina_erro')

        # Crie uma instância do formulário para permitir que o usuário atualize o saldo
        form = PedidoTerceirosForm()

        # Renderize a página com o formulário
        return render(request, self.template_name, {'form': form, 'registro': registro})

    def post(self, request, link_unico):
        # Verifique se o link único é válido e se corresponde a um registro existente
        try:
            registro = PedidoTerceiros.objects.get(link_unico=link_unico, respondido__isnull=True)
        except PedidoTerceiros.DoesNotExist:
            # Caso não exista um registro com esse link único, você pode lidar com isso adequadamente, como redirecionar para uma página de erro.
            return redirect('pagina_erro')

        # Crie uma instância do formulário com os dados da solicitação POST
        form = PedidoTerceirosForm(request.POST, request.FILES, instance=registro)
    
        if form.is_valid():
            registro = form.save(commit=False)
            registro.respondido = datetime.now()
            registro.save()
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
