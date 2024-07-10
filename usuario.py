class Usuario:
    def __init__(self, id, usuario, clave, nombre, wsp, datos):
        self.id = id
        self.usuario = usuario
        self.clave = clave
        self.nombre = nombre
        self.wsp = wsp
        self.datos = datos

    @staticmethod
    def get_all(mysql):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuario")
        rows = cur.fetchall()
        cur.close()
        return [Usuario(*row) for row in rows]

    @staticmethod
    def get_by_id(mysql, id):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuario WHERE id = %s", (id,))
        row = cur.fetchone()
        cur.close()
        return Usuario(*row) if row else None

    def save_to_db(self, mysql):
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuario (usuario, clave, nombre, wsp, datos) VALUES (%s, %s, %s, %s, %s)",
                    (self.usuario, self.clave, self.nombre, self.wsp, self.datos))
        mysql.connection.commit()
        cur.close()

    def update_in_db(self, mysql):
        cur = mysql.connection.cursor()
        cur.execute("UPDATE usuario SET usuario=%s, clave=%s, nombre=%s, wsp=%s, datos=%s WHERE id=%s",
                    (self.usuario, self.clave, self.nombre, self.wsp, self.datos, self.id))
        mysql.connection.commit()
        cur.close()