import Estado as estado
class Puesto:
    def __init__(self,ID,Titulo,Productos,Ofertas,Imagen,Estado):
        self.ID = ID
        self.Titulo = Titulo
        self.Productos = Productos
        self.Ofertas = Ofertas
        self.Imagen = Imagen
        self.Estado = Estado

# Que puede hacer un puesto? editar su informacion 
# Que informacion necesitaria editar? Todo puede cambiar

    def EditarPuesto(self,ID,Titulo,Productos,Ofertas,Imagen,Estado):
        if(ID == True):
            self.ID = ID
        if(Titulo == True):
            self.Titulo = Titulo
        if(Productos == True):
            self.Productos = Productos
        if(Ofertas == True):
            self.Ofertas = Ofertas
        if(Imagen == True):
            self.Imagen = Imagen
        if(Estado == True):
            self.Estado = Estado
        #en cada if colocar su query correspondiente

    def ActivarPuesto(self):
        self.Estado = estado.ESTADO.Activo
        #aca colocar query

    def DesactivarPuesto(self):
        self.Estado = estado.ESTADO.Inactivo
        #aca colocar query

    def __del__(self):
        print("Puesto fuera")

    def EliminarPuesto(self):

        #editar en la BDD
        print("Puesto eliminado")