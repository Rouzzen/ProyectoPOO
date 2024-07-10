class Puesto:
    def __init__(self, id_p, titulo, productos, ofertas, imagen, estado):
        self.id_p = id_p
        self.titulo = titulo
        self.productos = productos
        self.ofertas = ofertas
        self.imagen = imagen
        self.estado = estado

    @staticmethod
    def get_all_puestos_by_estado(mysql, estado):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM puesto WHERE estado = %s", (estado,))
        rows = cur.fetchall()
        cur.close()
        return [Puesto(*row) for row in rows]

    @staticmethod
    def get_by_id(mysql, id_p):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM puesto WHERE id_p = %s", (id_p,))
        row = cur.fetchone()
        cur.close()
        return Puesto(*row) if row else None

    def save_to_db(self, mysql):
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO puesto (id_p, titulo, productos, ofertas, estado, imagen) VALUES (%s, %s, %s, %s, %s, %s)",
                    (self.id_p, self.titulo, self.productos, self.ofertas, self.estado, self.imagen))
        mysql.connection.commit()
        cur.close()

    def update_in_db(self, mysql):
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE puesto 
            SET titulo = %s, productos = %s, ofertas = %s, imagen = %s, estado = %s
            WHERE id_p = %s
        """, (self.titulo, self.productos, self.ofertas, self.imagen, self.estado, self.id_p))
        mysql.connection.commit()
        cur.close()