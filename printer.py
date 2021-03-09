from reportlab.pdfgen import canvas
from datetime import datetime
from reportlab.lib.pagesizes import A4
from PyQt5 import QtWidgets, QtSql
import os, var


class Printer():

    @staticmethod
    def cabecera():
        """

        Metodo para generar la cabecera general de los pdf.

        :return: None

        """
        try:
            logo = '.\\img\logo.jpg'
            var.rep.setTitle('INFORMES')
            var.rep.setAuthor('Samuel Vila')
            var.rep.setFont('Helvetica', size=10)
            var.rep.line(45, 820, 550, 820)
            var.rep.line(45, 745, 550, 745)
            textcif = 'CIF : A000000H'
            textnom = 'PROTECHSVILA'
            textdir = 'Randufe, Cotarel - N11'
            texttlf = '630 63 52 92'
            var.rep.drawString(50, 805, textcif)
            var.rep.drawString(50, 790, textnom)
            var.rep.drawString(50, 775, textdir)
            var.rep.drawString(50, 760, texttlf)
            var.rep.drawImage(logo, 500, 760)
        except Exception as error:
            print('Error cabvecera %' % str(error))

    @staticmethod
    def pie(textlistado):
        """

        Metodo que genera el pie para todos los pdf.

        :param textlistado:
        :return: None

        """
        try:
            var.rep.line(50, 50, 525, 50)
            fecha = datetime.today()
            fecha = fecha.strftime('%d.%m.%Y  %H.%M.%S')
            var.rep.setFont('Helvetica-Oblique', size=7)
            var.rep.drawString(460, 40, str(fecha))
            var.rep.drawString(270, 40, str('Página %s' % var.rep.getPageNumber()))
            var.rep.drawString(50, 40, str(textlistado))
        except Exception as error:
            print('Error pie %' % str(error))

    @staticmethod
    def cabeceracli():
        """

        Método para generar la cebecera del pdf de lista de clientes

        :return: None

        Imprimimos por pantalla los elementos de imtecli[] para que quede como una tabla.

        """
        try:
            var.rep.setFont('Helvetica-Bold', size=9)
            textlistado = 'LISTADO DE CLIENTES'
            var.rep.drawString(255, 720, textlistado)
            itemcli = ['CODIGO', 'DNI', 'APELLIDOS', 'NOMBRE', 'FECHA ALTA']

            var.rep.drawString(45, 690, itemcli[0])
            var.rep.drawString(120, 690, itemcli[1])
            var.rep.drawString(200, 690, itemcli[2])
            var.rep.drawString(345, 690, itemcli[3])
            var.rep.drawString(470, 690, itemcli[4])
        except Exception as error:
            print('Error cabeceracli %' % str(error))

    @staticmethod
    def cabeceraProveedor():

        try:
            var.rep.setFont('Helvetica-Bold', size=9)
            textlistado = 'LISTADO DE PROVEEDORES'
            var.rep.drawString(255, 720, textlistado)
            itemcli = ['CODIGO', 'NOMBRE', 'TELEFONO']

            var.rep.drawString(100, 690, itemcli[0])
            var.rep.drawString(250, 690, itemcli[1])
            var.rep.drawString(450, 690, itemcli[2])

            var.rep.line(45, 710, 550, 710)
        except Exception as error:
            print('Error cabecera proveedores %' % str(error))

    @staticmethod
    def reportProvedores():
        try:
            var.rep = canvas.Canvas('informes/listadoproveedores.pdf', pagesize=A4)
            textlistado = 'LISTADO DE PROVEEDORES'
            var.rep.setFont('Helvetica', size=10)
            Printer.cabecera()
            Printer.cabeceraProveedor()  ###

            query = QtSql.QSqlQuery()
            query.prepare('select codigo, nombre, telefono from proveedores order by nombre')
            if query.exec_():
                i = 110
                j = 670
                while query.next():
                    if j >= 80:
                        var.rep.setFont('Helvetica', size=10)
                        var.rep.drawString(i, j, str(query.value(0)))
                        var.rep.drawString(i + 150, j, str(query.value(1)))
                        var.rep.drawRightString(i + 385, j, str(query.value(2)))
                        j = j - 20
                    else:
                        i = 110
                        j = 670
                        var.rep.drawString(440, 70, 'Siguiente pagina')
                        var.rep.showPage()
                        Printer.cabecera()
                        Printer.cabeceraProveedor()
            Printer.pie(textlistado)
            var.rep.save()
            rootPath = ".\\informes"
            cont = 0
            for file in os.listdir(rootPath):
                if file.endswith('listadoproveedores.pdf'):
                    os.startfile("%s/%s" % (rootPath, file))
                cont = cont + 1
        except Exception as error:
            print('Error reportcli %' % str(error))

    @staticmethod
    def reportCli():
        """

        Método que imprime a todos los clientes.

        :return: None

        Llamamos al método cabecera general para imprimirla y a la cabecera de la lista de clientes.
        Hacemos una busqueda en la BBDD de todos los clientes  y vamos imprimiendo los datos en sus
        respectivos sitios (llos ajustamos con el eje X, ya que el eje Y es para cambiar de linea)
        Llamamos al pie para imprimirlo.

        Generamos el archivo en formato .pdf

        """
        try:
            var.rep = canvas.Canvas('informes/listadoclientes.pdf', pagesize=A4)
            textlistado = 'LISTADO DE CLIENTES'
            var.rep.setFont('Helvetica', size=10)
            Printer.cabecera()
            Printer.cabeceracli()  ###
            query = QtSql.QSqlQuery()
            query.prepare('select codigo, dni, apellidos, nombre, fechalta from clientes order by apellidos, nombre')
            if query.exec_():
                i = 50
                j = 670
                while query.next():
                    if j >= 80:
                        var.rep.setFont('Helvetica', size=10)
                        var.rep.drawString(i, j, str(query.value(0)))
                        var.rep.drawString(i + 50, j, str(query.value(1)))
                        var.rep.drawString(i + 160, j, str(query.value(2)))
                        var.rep.drawString(i + 295, j, str(query.value(3)))
                        var.rep.drawRightString(i + 470, j, str(query.value(4)))
                        j = j - 20
                    else:
                        i = 50
                        j = 670
                        var.rep.drawString(440, 70, 'Siguiente pagina')
                        var.rep.showPage()
                        Printer.cabecera()
                        Printer.cabeceracli()
            Printer.pie(textlistado)
            var.rep.save()
            rootPath = ".\\informes"
            cont = 0
            for file in os.listdir(rootPath):
                if file.endswith('listadoclientes.pdf'):
                    os.startfile("%s/%s" % (rootPath, file))
                cont = cont + 1
        except Exception as error:
            print('Error reportcli %' % str(error))

    @staticmethod
    def cabecerapro():
        """
        Método para generar la cabecera del listado de productos.


        :return: None

        Definimos el tipo y el tamaño de letra que vamos a usar con .setFornt().
        Definimos el titulo y guardamos en itemcli el titulo de las cosas que vamos a guardar y las escribimos.


        """
        try:
            var.rep.setFont('Helvetica-Bold', size=9)
            textlistado = 'LISTADO DE PRODUCTOS'
            var.rep.drawString(240, 720, textlistado)
            itemcli = ['CODIGO', 'PRODUCTO', 'PRECIO UNIDAD', 'STOCK']

            var.rep.drawString(85, 690, itemcli[0])
            var.rep.drawString(195, 690, itemcli[1])
            var.rep.drawString(410, 690, itemcli[2])
            var.rep.drawString(510, 690, itemcli[3])

        except Exception as error:
            print('Error cabecerapro %' % str(error))

    @staticmethod
    def reportPro():
        """

        Método que imprime los productos

        :return: None

        Definios el titulo, definimos el nombre que le vamos a dar al pdf y el tamaño de página.
        Elegimos estilo y tamaño de letra.
        LLmamamos al método que imprime la cebecera y al método que imprime la cabecera de los productos.
        Buscamos los articulos en la base de datos y los vamos escribiendo en el pdf.

        Finalemente, llamamamos al metodo .pie() para imprimir el pie del pdf y gardamos el archivo.


        """
        try:
            textlistado = 'LISTADO DE PRODUCTOS'
            var.rep = canvas.Canvas('informes/listadoproductos.pdf', pagesize=A4)
            var.rep.setFont('Helvetica', size=10)

            Printer.cabecera()
            Printer.cabecerapro()
            query = QtSql.QSqlQuery()
            query.prepare('select codigo, nombre, precio, stock from articulos order by nombre')
            var.rep.setFont('Helvetica', size=10)
            if query.exec_():
                i = 100
                j = 665
                while query.next():
                    if j >= 80:
                        var.rep.setFont('Helvetica', size=10)
                        var.rep.drawString(i, j, str(query.value(0)))
                        var.rep.drawString(i + 70, j, str(query.value(1)))
                        var.rep.drawString(i + 350, j, str(query.value(2)))
                        var.rep.drawString(i + 430, j, str(query.value(3)))
                        j = j - 30
                    else:
                        i = 100
                        j = 665
                        var.rep.drawString(440, 70, 'Siguiente pagina')
                        var.rep.showPage()
                        Printer.cabecera()
                        Printer.cabecerapro()

            Printer.pie(textlistado)
            var.rep.save()
            rootPath = ".\\informes"
            cont = 0
            for file in os.listdir(rootPath):
                if file.endswith('listadoproductos.pdf'):
                    os.startfile("%s/%s" % (rootPath, file))
                cont = cont + 1
        except Exception as error:
            print('Error reportcli %' % str(error))

    @staticmethod
    def cabeceraFac(numFac, fecha, dniCli):
        """

        Método que defina la cabecera de las facturas

        :param numFac:
        :param fecha:
        :param dniCli:
        :return: None

        Buscamos lso datos del cliente según su dni y los imprimimos.
        A continuación, imprimimos el numero de factura, la fecha y los titulos de lso productos que vamos a imprimir.

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                'select dni,apellidos, nombre, direccion, provincia, formaspago from clientes where dni = :dni')
            query.bindValue(':dni', dniCli)

            var.rep.setFont('Helvetica-Bold', size=13)
            var.rep.drawString(60, 720, 'Cliente :')
            var.rep.setFont('Helvetica', size=10)
            if query.exec_():
                while query.next():
                    var.rep.drawString(60, 700, 'DNI: ' + str(query.value(0)))
                    var.rep.drawString(60, 680, str(query.value(1)) + ',' + str(query.value(2)))
                    var.rep.drawString(350, 680, 'Formas de Pago:')
                    var.rep.drawString(60, 665, str(query.value(3)) + '-' + str(query.value(4)))
                    var.rep.drawString(350, 665, str(query.value(5)).strip('[]').replace('\'', '').replace(',', ' -'))

            var.rep.line(45, 650, 525, 650)
            var.rep.drawString(65, 630, "Factura nº : " + str(numFac))
            var.rep.drawString(450, 630, "Fecha: " + str(fecha))
            var.rep.line(45, 620, 525, 620)
            var.rep.setFont('Helvetica-Bold', size=10)
            itemcli = ['Codigo Venta', 'Artículo', 'Cantidad', 'Prec.Ud', 'Subtotal']

            var.rep.drawString(60, 605, itemcli[0])
            var.rep.drawString(180, 605, itemcli[1])
            var.rep.drawString(275, 605, itemcli[2])
            var.rep.drawString(380, 605, itemcli[3])
            var.rep.drawString(475, 605, itemcli[4])

            var.rep.line(45, 595, 525, 595)

        except Exception as error:
            print('Error cabeceraFac %' % str(error))

    @staticmethod
    def reportFac():
        """

        Método que sirve para generar el pdf de facturas-

        :return: None

        Recogemos el numero de factura, la fecha y el dni del cliente para pasarselo al método de .CabeceraFac()
        Llamamos al método cabecera() y al método de cabeceraFac()
        Hacemos una busqueda de las ventas de la factura y otra busqueda para buscar los datos de cada producto.
        Imprimimos los datos de cada producto y luego, los datos de cada venta.
        Hacemos los calculos necesarios para calcular el subtotal, el iva y el total y lo imprimimos.
        Finalmente, guardamos la factura.

        """
        try:
            textlistado = 'Factura'
            numFac = var.ui.lblFactura.text()
            fechaFac = var.ui.EditFechaFactura.text()
            dni = var.ui.EditCliDni.text()

            var.rep = canvas.Canvas('informes/factura.pdf', pagesize=A4)
            var.rep.setFont('Helvetica', size=10)

            Printer.cabecera()
            Printer.cabeceraFac(numFac, fechaFac, dni)
            query = QtSql.QSqlQuery()
            query.prepare('select codventa, codarticventa, cantidad, precio from ventas where codfacventa =:numFac')
            query.bindValue(':numFac', str(numFac))

            var.rep.setFont('Helvetica', size=10)
            if query.exec_():
                i = 90
                j = 575
                while query.next():

                    queryArt = QtSql.QSqlQuery()
                    queryArt.prepare('select nombre, precio from articulos where codigo = :cod')
                    queryArt.bindValue(':cod', str(query.value(1)))

                    if queryArt.exec_():
                        while queryArt.next():
                            articulo = queryArt.value(0)
                            precioUnit = queryArt.value(1)
                    if j >= 80:
                        subtotal = round(query.value(3), 2)

                        var.rep.setFont('Helvetica', size=10)
                        var.rep.drawString(i, j, str(query.value(0)))
                        var.rep.drawString(i + 90, j, str(articulo))
                        var.rep.drawString(i + 200, j, str(query.value(2)))
                        var.rep.drawRightString(i + 315, j, str(precioUnit))
                        var.rep.drawRightString(i + 415, j, str(subtotal))

                        j = j - 20
                    else:
                        i = 90
                        j = 575
                        var.rep.drawString(440, 70, 'Siguiente pagina')
                        var.rep.showPage()
                        Printer.cabecera()
                        Printer.cabeceraFac(numFac, fechaFac, dni)

            var.rep.setFont('Helvetica-Bold', size=12)
            var.rep.drawRightString(500, 160,
                                    'Subtotal:   ' + "{0:.2f}".format(float(var.ui.lblSubTotal.text())) + ' €')
            var.rep.drawRightString(500, 140, 'IVA:     ' + "{0:.2f}".format(float(var.ui.lblIva.text())) + ' €')
            var.rep.drawRightString(500, 120,
                                    'Total Factura: ' + "{0:.2f}".format(float(var.ui.lblTotal.text())) + ' €')

            Printer.pie(textlistado)
            var.rep.save()
            rootPath = ".\\informes"
            cont = 0
            for file in os.listdir(rootPath):
                if file.endswith('factura.pdf'):
                    os.startfile("%s/%s" % (rootPath, file))
                cont = cont + 1
        except Exception as error:
            print('Error reportFac %' % str(error))

    @staticmethod
    def cabeceraFacCli(dniCliente):
        """

        Método que crea la cabecera para imprimir todas las facturas de un cliente

        :param dniCliente:
        :type dniCliente:
        :return: None
        :rtype: None

        Buscamos los datos del cliente en la bbdd segun su dni.
        Imprimimos estos datos yu creamos la cabecera para los datos de las facturas.

        """

        try:

            queryCli = QtSql.QSqlQuery()
            queryCli.prepare(
                'select dni,apellidos, nombre, direccion, provincia, formaspago from clientes where dni = :dni')
            queryCli.bindValue(':dni', dniCliente)

            var.rep.setFont('Helvetica-Bold', size=13)
            var.rep.drawString(60, 720, 'Cliente :')
            if queryCli.exec_():
                while queryCli.next():
                    var.rep.drawString(60, 700, 'DNI: ' + str(queryCli.value(0)))
                    var.rep.drawString(60, 680, str(queryCli.value(1)) + ',' + str(queryCli.value(2)))
                    var.rep.drawString(350, 680, 'Formas de Pago:')
                    var.rep.drawString(60, 665, str(queryCli.value(3)) + '-' + str(queryCli.value(4)))
                    var.rep.drawString(350, 665,
                                       str(queryCli.value(5)).strip('[]').replace('\'', '').replace(',', ' -'))

            itemFactura = ['Codigo Factura', 'Fecha Factura', 'Total Factura']

            var.rep.drawString(75, 605, itemFactura[0])
            var.rep.drawString(275, 605, itemFactura[1])
            var.rep.drawString(475, 605, itemFactura[2])
            var.rep.line(45, 650, 550, 650)

        except Exception as error:
            print("Error en cabecera de facturas de cliente : " + error)

    @staticmethod
    def reportFacturaCliente():

        """

        Método que imprime todas las facturas de cada cliente, resumidas en un pdf.

        :return: None
        :rtype: None

        Llamamos al método cabecera y cabeceraFacCli para que impriman la cabecera general del pdf y luego, la cabecera
        personalizada para este dpf.
        Buscamos todas las facturas de este cliente en la bbdd.
        Imprimimos los datos de la factura.
        Aprovechamos el codigo de la factura para buscar los productos que le vendimos y poder calcular el precio de cada factura.
        Finalmente imprimimos el precio de cada factura, los sumamos e imprimimos también el total gastado de ese cliente.

        """

        try:

            sumaTotal = 0
            textlistado = 'Facturas de un cliente'
            var.rep = canvas.Canvas('informes/facturasDeCliente.pdf', pagesize=A4)
            var.rep.setFont('Helvetica', size=10)

            dniCli = var.ui.EditCliDni.text()

            Printer.cabecera()
            Printer.cabeceraFacCli(dniCli)
            y = 605

            var.rep.setFont('Helvetica', size=10)
            queryFac = QtSql.QSqlQuery()
            queryFac.prepare('select codfac, fecha from facturas where dni = :dni')
            queryFac.bindValue(':dni', dniCli)
            if queryFac.exec_():
                while queryFac.next():
                    if y >= 150:
                        y = y - 25
                        var.rep.drawString(100, y, str(queryFac.value(0)))
                        var.rep.drawString(285, y, str(queryFac.value(1)))
                        codfacventa = queryFac.value(0)

                        queryVentas = QtSql.QSqlQuery()
                        queryVentas.prepare('select precio from ventas where codfacventa =:numFac')
                        queryVentas.bindValue(':numFac', str(codfacventa))

                        precioTotal = 0
                        if queryVentas.exec_():
                            while queryVentas.next():
                                precioTotal = precioTotal + queryVentas.value(0)

                            iva = round(float(precioTotal) * 0.21, 2)
                            precioTotal = precioTotal + iva
                            sumaTotal = precioTotal + sumaTotal

                        var.rep.drawString(490, y, str(precioTotal))
                    else:
                        y = 605

                        var.rep.setFont('Helvetica-Bold', size=10)
                        var.rep.drawString(440, 70, 'Siguiente pagina')
                        var.rep.showPage()
                        Printer.cabecera()
                        Printer.cabeceraFacCli(dniCli)
                        var.rep.setFont('Helvetica', size=10)

            var.rep.setFont('Helvetica-Bold', size=10)
            var.rep.drawRightString(550, 70, "Total de todas las facturas : " + str(round(float(sumaTotal), 2)) + " €")
            Printer.pie(textlistado)
            var.rep.save()
            rootPath = ".\\informes"
            cont = 0
            for file in os.listdir(rootPath):
                if file.endswith('facturasDeCliente.pdf'):
                    os.startfile("%s/%s" % (rootPath, file))
                cont = cont + 1
        except Exception as error:
            print('Error al generear todas las facturas de un cliente : ' + error)
