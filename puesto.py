class Puesto:
    def __init__(self, id_p, titulo, productos, ofertas, imagen, estado):
        self.id_p = id_p
        self.titulo = titulo
        self.productos = productos
        self.ofertas = ofertas
        self.imagen = imagen
        self.estado = estado

    @classmethod
    def obtener_por_id(cls, id_p, mysql):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM puesto WHERE id_p = %s", (id_p,))
        puesto_data = cur.fetchone()
        cur.close()
        if puesto_data:
            return cls(*puesto_data)
        return None

    def actualizar_estado(self, nuevo_estado, mysql):
        cur = mysql.connection.cursor()
        cur.execute("UPDATE puesto SET estado = %s WHERE id_p = %s", (nuevo_estado, self.id_p))
        mysql.connection.commit()
        cur.close()
        self.estado = nuevo_estado

    def actualizar_detalles(self, titulo, productos, ofertas, mysql, imagen_path=None):
        cur = mysql.connection.cursor()
        if imagen_path:
            cur.execute("""
                UPDATE puesto 
                SET titulo = %s, productos = %s, ofertas = %s, imagen = %s
                WHERE id_p = %s
            """, (titulo, productos, ofertas, imagen_path, self.id_p))
        else:
            cur.execute("""
                UPDATE puesto 
                SET titulo = %s, productos = %s, ofertas = %s
                WHERE id_p = %s
            """, (titulo, productos, ofertas, self.id_p))
        mysql.connection.commit()
        cur.close()
        self.titulo = titulo
        self.productos = productos
        self.ofertas = ofertas
        self.imagen = imagen_path if imagen_path else self.imagen

    def eliminar(self, mysql):
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM puesto WHERE id_p = %s", (self.id_p,))
        mysql.connection.commit()
        cur.close()
