import unittest, conexion, var, clients

from PyQt5 import QtSql


class Testing(unittest.TestCase):
    def testConexion(self):
        valor = conexion.Conexion.db_connect(var.filedb)
        message = 'Error test conexión'
        self.assertTrue(valor, message)

    def testDni(self):
        valor = clients.Clientes.validarDNI('35610185K')
        message = 'Dni no válido'
        self.assertTrue(valor, message)

    def testFacturar(self):
        valor = 570.21
        codfac = 141
        try:
            message = 'Error testeo factura'
            var.subfac = 0.00
            query = QtSql.QSqlQuery()
            query.prepare('select codventa, codarticventa, cantidad from ventas where codfacventa = :codfac')
            query.bindValue(':codfac', int(codfac))
            if query.exec_():
                while query.next():
                    codarticventa = query.value(1)
                    cantidad = query.value(2)
                    query_pro = QtSql.QSqlQuery()
                    query_pro.prepare('select nombre, precio from articulos where codigo = :codarticventa')
                    query_pro.bindValue(':codarticventa', int(codarticventa))
                    if query_pro.exec_():
                        while query_pro.next():
                            precio = query_pro.value(1)
                            subtotal = round(float(cantidad) * float(precio), 2)
                    var.subfac = round(float(subtotal) + float(var.subfac), 2)
            var.iva = round(float(var.subfac) * 0.21, 2)
            var.fac = round(float(var.iva) + float(var.subfac), 2)
        except Exception as error:
            print('Error Listado de la tabla de ventas: %s ' % str(error))
        self.assertEqual(round(float(valor), 2), round(float(var.fac), 2), message)


    def testBuscarCliente(self):

        message = 'Error en comproba si existe cliente'
        dni = '00000000T'
        codigo = 33
        message = 'Error testeo factura'
        query = QtSql.QSqlQuery()
        query.prepare('select * from clientes where dni = :dni')
        query.bindValue(':dni', str(dni))
        if query.exec_():
            print(str(dni))
            while query.next():
                var.resultConsulta = int(query.value(0))
            self.assertEqual(int(codigo), int(var.resultConsulta), message)


if __name__ == '__main__':
    unittest.main()
