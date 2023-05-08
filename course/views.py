from django.shortcuts import render,HttpResponse

import pandas as pd
import requests
from bs4 import BeautifulSoup
import json

#from .models import Revisor,Proveedor,Radicacion,Aprobacion
from django.views.generic import ListView

from django.http import JsonResponse

from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .forms import *

from .models import Proveedor


class IndexListView(ListView):

	model = Proveedor
	template_name = 'course/main.html'

	def get_food(self):

		try:
			res = requests.get("http://vicebienestar.univalle.edu.co/restaurante-universitario",verify=False)
			soup = BeautifulSoup(res.content,'html.parser')

			table = soup.find_all('table')[1]
		
			table_data = [[cell.text for cell in row("td")] for row in table.find_all("tr")]

			foods = []
			headers = ['header',[head.text for head in table.find_all("th")]]
			for item in table_data[1:-1]:
				foods.append([item[0],item[1:]])

			#data_foods = json.dumps(dict(foods), ensure_ascii= False)
			data_foods = dict(foods)
			return headers,data_foods
		except IndexError:
			headers = ['header', ['Dia', 'Sopa', 'Arroz', 'Carne', 'Principio', 'Ensalada', 'Jugo']]
			foods= {
				    '\nLunes 08\n': ['De\xa0Arroz', 'Blanco\xa0', 'Filete de pollo', 'Papa Guisada', 'Tomate Campestre', 'Guayaba'],
	                '\nMartes 09\n': ['De Fideos', 'Blanco\xa0','Carne Molida con Verduras', 'Banano', 'Lechuga y Rabanos\xa0', 'Mora'],
					'\nMiercoles 10\n': ['De\xa0Frijoles', 'Blanco\xa0', 'Carne Asada', 'Tajadas', 'Repollo Blanco y Pimenton', 'Agua de Panela'],
					'\nJueves 11\n': ['Choclo con Verduras', '\xa0Blanco', 'Pescado Frito', 'Yuca Guisada', 'Dorada', 'Maracuya'], 
					'\nViernes 12\n': ['De\xa0Torrejas', 'Blanco', 'Cerdo Asado', 'Arvejas Guisadas', 'Lechuga y Apio', 'Frutos Rojos']
					}
			return headers,foods




	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		context['headers'],context['foods'] = self.get_food()
		return context
