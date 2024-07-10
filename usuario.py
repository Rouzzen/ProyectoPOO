import puesto as Puesto
class Usuario:
    def __init__(self,ID,Nombre,WPP,DatosBancarios):
        self.ID = ID
        self.Nombre = Nombre
        self.Wpp = WPP
        self.DatosBancarios = DatosBancarios
        #si el usuario no existe crear aca con query
        '''
        Aca tenemos que colocar un metodo, solo se me ocurre que cree un puesto e interactue con el.
        '''

    def CrearPuesto(self,Titulo,Productos,Ofertas,Imagen,Estado):
        puestito = Puesto(self.ID,Titulo,Productos,Ofertas,Imagen,Estado)
        #enviar a la base de datos aca
        return puestito
    
    def EditarDatos(self,ID,Nombre,WPP,DatosBancarios):
        if(ID==True):
            self.ID = ID
        if(Nombre==True):
            self.Nombre = Nombre
        if(WPP==True):
            self.Wpp = WPP
        if(DatosBancarios==True):
            self.DatosBancarios = DatosBancarios

    def __del__(self):
        print("Usuario fuera")

