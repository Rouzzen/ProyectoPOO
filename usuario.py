from puesto import Puesto

class Usuario:
    def __init__(self, id, usuario, clave, nombre, wsp, datos):
        self.id = id
        self.usuario = usuario
        self.clave = clave
        self.nombre = nombre
        self.wsp = wsp
        self.datos = datos

    @classmethod
    def obtener_por_id(cls, id, mysql):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuario WHERE id = %s", (id,))
        usuario_data = cur.fetchone()
        cur.close()
        if usuario_data:
            return cls(*usuario_data)
        return None

    def actualizar_perfil(self, nombre, wsp, datos, mysql):
        cur = mysql.connection.cursor()
        cur.execute("UPDATE usuario SET nombre = %s, wsp = %s, datos = %s WHERE id = %s", (nombre, wsp, datos, self.id))
        mysql.connection.commit()
        cur.close()
        self.nombre = nombre
        self.wsp = wsp
        self.datos = datos

    def obtener_puesto(self, mysql):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM puesto WHERE id_p = %s", (self.id,))
        puesto_data = cur.fetchone()
        cur.close()
        if puesto_data:
            return Puesto(*puesto_data)
        return None
