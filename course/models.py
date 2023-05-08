from django.db import models

class Proveedor(models.Model):

	Cod_Proveedor = models.CharField(max_length=50,verbose_name="Nit")
	name = models.TextField(verbose_name="Nombre")
	
	def __str__(self):
		return f'{self.name}'

