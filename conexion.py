from PyQt5 import QtSql
import var, facturas
from vent_principal import *


class Conexion():

    @staticmethod
    def db_connect(filname):
        """

        Módulo que permite la conexión con la BBDD.

        :param filname:
        :type filname:
        :return: True or False
        :rtype: Bool


        Recibimos el nombre de la BBDD, añadimos la base de datos y la abrimos.

        """
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(filname)
        if not db.open():
            QtWidgets.QMessageBox.Critical(None, 'No se puede abrir la base de datos',
                                           'No se puede establecer la conexión. \n'
                                           'Haz Click para Cancelar.', QtWidgets.QMessageBox.Cancel)
            print('Error conexion')
            return False
        else:
            print('Conexion establecida')
        return True

    #
    #
    # class Conexion():
    #     HOST = 'localhost'
    #     PORT = '27017'
    #     URI_CONNECTION = 'mongodb://' + HOST + ':' + PORT + '/'
    #     var.filebd = 'empresa.db'
    #     try:
    #         print('OK -- Conectado al servidor %s' % HOST)
    #         print('Conexion base de datos establecida')
    #     except:
    #         print('Eror conexión')


    @staticmethod
    def altaProv(proveedor):

        query = QtSql.QSqlQuery()
        query.prepare(
            'insert into proveedores (nombre,telefono)'
            'VALUES (:nombre, :telefono)')
        query.bindValue(':nombre', str(proveedor[0]))
        query.bindValue(':telefono', (int(proveedor[1])))

        if query.exec_():
            print('Insercción Correcta')
        else:
            print('Error conexión alta proveedores:', query.lastError().text())

    @staticmethod
    def mostrarProveedores():

        index = 0
        query = QtSql.QSqlQuery()
        query.prepare('select * from proveedores')
        if query.exec_():
            while query.next():
                codigo = (str(query.value(0)))
                nombre = query.value(1)
                telefono = (str(query.value(2)))

                var.ui.TableProveedor.setRowCount(index + 1)

                var.ui.TableProveedor.setItem(index, 0, QtWidgets.QTableWidgetItem(codigo))
                var.ui.TableProveedor.setItem(index, 1, QtWidgets.QTableWidgetItem(nombre))
                var.ui.TableProveedor.setItem(index, 2, QtWidgets.QTableWidgetItem(telefono))
                index += 1
        else:
            print('Error en mostrar proveedores : ', query.lastError().text())
        if index == 0:
            var.ui.TableProveedor.clearContents()
            var.ui.TableProveedor.setRowCount(0)

    @staticmethod
    def cargarProveedor():

        codigo = str(var.ui.lblCodigoProveedor)
        query = QtSql.QSqlQuery()
        query.prepare('select * from proveedores where codigo = :codigo')
        query.bindValue(':codigo', codigo)
        if query.exec_():
            while query.next():
                var.ui.lblCodigoProveedor.setText(str(query.value(0)))
                var.ui.EditNombreProveedor.setText(str(query.value(1)))
                var.ui.EditTelefonoProveedor.setText(query.value(2))
        else:
            print('error en cargar art - conexion')

    @staticmethod
    def limpiarProveedor():
        try:
            proveedores = [var.ui.lblCodigoProveedor, var.ui.EditNombreProveedor, var.ui.EditTelefonoProveedor]
            for i in range(len(proveedores)):
                proveedores[i].setText('')
        except Exception as error:
            print('Error al limpiar : %s ' % str(error))


    @staticmethod
    def modifProveedor(codigo, newdata):

        query = QtSql.QSqlQuery()
        query.prepare(
            'update proveedores set codigo=:codigo, nombre=:nombre, telefono=:telefono where codigo=:codigo')
        query.bindValue(':codigo', int(codigo))
        query.bindValue(':nombre', str(newdata[0]))
        query.bindValue(':telefono', str(newdata[1]))
        if query.exec_():
            print('Proveedor modificado')
        else:
            print('Error en conexion modificar proveedor: ', query.lastError().text())


    @staticmethod
    def bajaProveedor(codigo):

        query = QtSql.QSqlQuery()
        query.prepare('delete from proveedores where codigo = :codigo')
        query.bindValue(':codigo', codigo)

        if query.exec_():
            print('Baja proveedor')
        else:
            print('Error conexion baja proveedores: ', query.lastError().text())


    @staticmethod
    def altaCli(cliente):
        """

        Módulo que permite dar de alta a un cliente en la BBDD.

        :param cliente:
        :type cliente:
        :return: None
        :rtype: None

        Creamos un query para indicar los datos del nuevo cliente y con .bindValue() indicamos el datos que vamos a insertar
        en el nuevo cliente.

        """
        query = QtSql.QSqlQuery()
        query.prepare(
            'insert into clientes (dni, apellidos, nombre, fechalta, direccion, provincia, sexo, formaspago, edad)'
            'VALUES (:dni, :apellidos, :nombre, :fechalta, :direccion, :provincia, :sexo, :formaspago, :edad)')
        query.bindValue(':dni', str(cliente[0]))
        query.bindValue(':apellidos', str(cliente[1]))
        query.bindValue(':nombre', str(cliente[2]))
        query.bindValue(':fechalta', str(cliente[3]))
        query.bindValue(':direccion', str(cliente[4]))
        query.bindValue(':provincia', str(cliente[5]))
        query.bindValue(':sexo', str(cliente[6]))
        query.bindValue(':formaspago', str(cliente[7]))
        query.bindValue(':edad', int(cliente[8]))

        if query.exec_():
            print('Insercción Correcta')
        else:
            print('Error conexión alta clientes:', query.lastError().text())

    @staticmethod
    def mostrarClientes():
        """

        Módulo que muestra los datos de los clientes en la tabla TableClient.

        :return: None
        :rtype: None

        Seleccionamos los datos que queremos obtener de los empleados, en este caso (dni, apellidos y nombre).
        A continucación los vamos añadiendo a la tabla por con el método .setItem().
        Cuando un cliente ya está añadido a la tabla, se incrementa en 1 la fila y continuamos añadiendo los datos
        del siguiente cliente.

        """
        index = 0
        query = QtSql.QSqlQuery()
        query.prepare('select dni, apellidos, nombre from clientes')
        if query.exec_():
            while query.next():
                dni = query.value(0)
                apellidos = query.value(1)
                nombre = query.value(2)

                var.ui.TableClient.setRowCount(index + 1)

                var.ui.TableClient.setItem(index, 0, QtWidgets.QTableWidgetItem(dni))
                var.ui.TableClient.setItem(index, 1, QtWidgets.QTableWidgetItem(apellidos))
                var.ui.TableClient.setItem(index, 2, QtWidgets.QTableWidgetItem(nombre))
                index += 1
        else:
            print('Error en mostrar clientes : ', query.lastError().text())
        if index == 0:
            var.ui.TableClient.clearContents()
            var.ui.TableClient.setRowCount(0)

    @staticmethod
    def cargarCliente():
        """

        Método que carga los datos del cliente en sus editText y label correspondiente.

        :return: None
        :rtype: None

        Seleccionamos los datos del cliente según su dni, el cual lo cogemos del editText de dni previamente cargado.
        Una vez recibidos los datos, los vamos metiendo en sus respectivos editText, checkBox,radioButton, labels y spinBox.

        """
        dni = var.ui.EditDni.text()
        query = QtSql.QSqlQuery()
        query.prepare('select * from clientes where dni = :dni')
        query.bindValue(':dni', dni)

        if query.exec_():
            while query.next():
                var.ui.EditIdentificador.setText(str(query.value(0)))
                var.ui.editClialta.setText(query.value(4))
                var.ui.EditDirecc.setText(query.value(5))
                var.ui.cmbProv.setCurrentText(str(query.value(6)))
                if str(query.value(7)) == 'Mujer':
                    var.ui.rbtFem.setChecked(True)
                    var.ui.rbtMasc.setChecked(False)
                else:
                    var.ui.rbtMasc.setChecked(True)
                    var.ui.rbtFem.setChecked(False)
                for data in var.chkpago:
                    data.setChecked(False)
                if 'Efectivo' in query.value(8):
                    var.chkpago[0].setChecked(True)
                if 'Tarjeta' in query.value(8):
                    var.chkpago[1].setChecked(True)
                if 'Transferencia' in query.value(8):
                    var.chkpago[2].setChecked(True)
                var.ui.spinEdad.setValue(int(query.value(9)))

    @staticmethod
    def modifCli(codigo, newdata):
        """

        Método que permite modificar los datos de un cliente.

        :param codigo:
        :type codigo:
        :param newdata:
        :type newdata:
        :return: None
        :rtype: None

        Recibimos el código del cliente y todos los datos del cliente (ya que se puede actualizar más de un dato)
        y los actuzalizamos en la base de datos con update.
        Utilizamos el bindValue() para indicar los datos,tanto los que están actualizados, como los que no.

        """
        query = QtSql.QSqlQuery()
        query.prepare('update clientes set dni=:dni, apellidos=:apellidos, nombre=:nombre, fechalta=:fechalta, '
                      'direccion=:direccion, provincia=:provincia, sexo=:sexo, formaspago=:formaspago, edad=:edad where codigo=:codigo')
        query.bindValue(':codigo', int(codigo))
        query.bindValue(':dni', str(newdata[0]))
        query.bindValue(':apellidos', str(newdata[1]))
        query.bindValue(':nombre', str(newdata[2]))
        query.bindValue(':fechalta', str(newdata[3]))
        query.bindValue(':direccion', str(newdata[4]))
        query.bindValue(':provincia', str(newdata[5]))
        query.bindValue(':sexo', str(newdata[6]))
        query.bindValue(':formaspago', str(newdata[7]))
        query.bindValue(':edad', int(newdata[8]))
        if query.exec_():
            print('Cliente modificado')
        else:
            print('Error en conexion modificar cliente: ', query.lastError().text())

    @staticmethod
    def bajaCli(dni):
        """

        Método que permite dar de baja a un cliente utiizando su dni.

        :param dni:
        :type dni:
        :return: None
        :rtype: None

        Reibimos el dni del cliente y con delete borramos el cliente indicando su dni mediante bindValue()

        """
        query = QtSql.QSqlQuery()
        query.prepare('delete from clientes where dni = :dni')
        query.bindValue(':dni', dni)

        if query.exec_():
            print('Baja cliente')
        else:
            print('Error conexion baja clientes: ', query.lastError().text())

    @staticmethod
    def buscarCliente(dni):
        """

        Metodo para buscar cliente según su dni.

        :param dni:
        :type dni:
        :return: None
        :rtype: None

        Recibimos el dni del cliente y lo buscamos segun su dni con select.
        Usamos el bindValue para indicar el dni del cliente.
        Una vez encontrado, cargamos sus datos en sus editText, label, spinBox, CheckBox y radioButton.
        También seleccionamos el cliente en la tabla de clientes.

        """
        index = 0
        query = QtSql.QSqlQuery()
        query.prepare('select * from clientes where dni = :dni')
        query.bindValue(':dni', dni)
        if query.exec_():
            while query.next():
                var.ui.EditIdentificador.setText(str(query.value(0)))
                var.ui.EditDni.setText(str(query.value(1)))
                var.ui.EditApell.setText(str(query.value(2)))
                var.ui.EditNomb.setText(str(query.value(3)))
                var.ui.editClialta.setText(str(query.value(4)))
                var.ui.EditDirecc.setText(str(query.value(5)))
                var.ui.cmbProv.setCurrentText(str(query.value(6)))
                if str(query.value(7)) == 'Mujer':
                    var.ui.rbtFem.setChecked(True)
                    var.ui.rbtMasc.setChecked(False)
                else:
                    var.ui.rbtMasc.setChecked(True)
                    var.ui.rbtFem.setChecked(False)
                for data in var.chkpago:
                    data.setChecked(False)
                if 'Efectivo' in query.value(8):
                    var.chkpago[0].setChecked(True)
                if 'Tarjeta' in query.value(8):
                    var.chkpago[1].setChecked(True)
                if 'Transferencia' in query.value(8):
                    var.chkpago[2].setChecked(True)
                var.ui.spinEdad.setValue(query.value(9))

                var.ui.TableClient.setRowCount(index + 1)

                var.ui.TableClient.setItem(index, 0, QtWidgets.QTableWidgetItem(str(query.value(1))))
                var.ui.TableClient.setItem(index, 1, QtWidgets.QTableWidgetItem(str(query.value(2))))
                var.ui.TableClient.setItem(index, 2, QtWidgets.QTableWidgetItem(str(query.value(3))))

    @staticmethod
    def altaArt(articulo):
        """

        Módulo con el que damos de alta articulos en la BBDD

        :param articulo:
        :type articulo:
        :return: None
        :rtype: None

        Recibimos los datos del producto, y los añadimos a la BBDD con insert.
        Con bindValue indicamos los datos que añadiremoS.

        """
        query = QtSql.QSqlQuery()
        query.prepare('insert into articulos ( nombre, precio, stock)'
                      'VALUES (:nombre, :precio, :stock)')
        query.bindValue(':nombre', str(articulo[0]))
        query.bindValue(':precio', (float(articulo[1])))
        query.bindValue(':stock',(int(articulo[2])))

        if query.exec_():
            print('Insercción Correcta')
        else:
            print('Error conexión alta clientes:', query.lastError().text())

    @staticmethod
    def mostrarArticulos():
        """

        Método que muestra los artículos en la tabla TableArt.

        :return: None
        :rtype: None

        Hacemos un select * para seleccionar todos los productos de la BBDD y los recorremos con un bucle while.
        A medida que vamos añadiendo los datos, cuando ya hemos añadido los datos que queremos a la tabla, cambiamos de
        fila y pasamos al siguiente producto.

        """
        index = 0
        query = QtSql.QSqlQuery()
        query.prepare('select * from articulos')
        if query.exec_():
            while query.next():
                codigo = (str(query.value(0)))
                nombre = query.value(1)
                precio = query.value(2)
                stock = (str(query.value(3)))

                var.ui.TableArt.setRowCount(index + 1)

                var.ui.TableArt.setItem(index, 0, QtWidgets.QTableWidgetItem(codigo))
                var.ui.TableArt.setItem(index, 1, QtWidgets.QTableWidgetItem(nombre))
                var.ui.TableArt.setItem(index, 2, QtWidgets.QTableWidgetItem(precio))
                var.ui.TableArt.setItem(index, 3, QtWidgets.QTableWidgetItem(stock))
                index += 1
        else:
            print('Error en mostrar articulos : ', query.lastError().text())
        if index == 0:
            var.ui.TableArt.clearContents()
            var.ui.TableArt.setRowCount(0)

    @staticmethod
    def bajaArt(codigo):
        """

        Metodo que permite dar de baja a un artículo de la BBDD.

        :param codigo:
        :type codigo:
        :return: None
        :rtype: None

        Recibimos el código del artículo a borrar y lo borramos con delete.
        Indicamos el codigo del artículo con bindValue()

        """
        query = QtSql.QSqlQuery()
        query.prepare('delete from articulos where codigo = :codigo')
        query.bindValue(':codigo', codigo)

        if query.exec_():
            print('Baja articulo')
        else:
            print('Error conexion baja articulos: ', query.lastError().text())
    @staticmethod
    def modifArt(codigo, newdata):
        """

        En este método, cargamos en la BBDD los datos que hemos modificado.

        :param codigo:
        :type codigo:
        :param newdata:
        :type newdata:
        :return: None
        :rtype: None

        Con update actualizamos en la bbdd los datos que hemos cambiado, y con .bindValue() cogemos los datos que le hemos
        pasado en newdata y los seleccionamos.

        """
        query = QtSql.QSqlQuery()
        query.prepare('update articulos set codigo=:codigo, nombre=:nombre, precio=:precio, stock=:stock where codigo=:codigo')
        query.bindValue(':codigo', int(codigo))
        query.bindValue(':nombre', str(newdata[0]))
        query.bindValue(':precio', str(newdata[1]))
        query.bindValue(':stock', str(newdata[2]))
        if query.exec_():
            print('Articulo modificado')
        else:
            print('Error en conexion modificar articulo: ', query.lastError().text())

    @staticmethod
    def cargarArticulo():
        """

        Metodo que carga un articulo cuando hacemos click en el (en la tabla de articulos)

        :return: None
        :rtype: None

        Seleccionamos el código que está cargado en el label del codigo del producto y hacemos una busqueda en la BBDD
        ( select )
        Nos traemos todos sus datos y los vamos escribiendo en sus respectivos sitios, editText, labels...  ( .setText() )


        """
        codigo = str(var.ui.lblCodProd)
        query = QtSql.QSqlQuery()
        query.prepare('select * from articulos where codigo = :codigo')
        query.bindValue(':codigo', codigo)
        if query.exec_():
            while query.next():
                var.ui.lblCodProd.setText(str(query.value(0)))
                var.ui.EditNombreProd.setText(str(query.value(1)))
                var.ui.EditPrecioUnidad.setText(query.value(2))
                var.ui.EditStock.setText(str(query.value(3)))
        else:
            print('error en cargar art - conexion')

    @staticmethod
    def buscarArticuloPrecio(precio):
        index = 0
        query = QtSql.QSqlQuery()
        query.prepare('select * from articulos where precio < :precio')
        query.bindValue(':precio', precio)
        if query.exec_():
            while query.next():
                codigo = (str(query.value(0)))
                nombre = query.value(1)
                precio = query.value(2)
                stock = (str(query.value(3)))

                var.ui.TableArt.setRowCount(index + 1)

                var.ui.TableArt.setItem(index, 0, QtWidgets.QTableWidgetItem(codigo))
                var.ui.TableArt.setItem(index, 1, QtWidgets.QTableWidgetItem(nombre))
                var.ui.TableArt.setItem(index, 2, QtWidgets.QTableWidgetItem(precio))
                var.ui.TableArt.setItem(index, 3, QtWidgets.QTableWidgetItem(stock))
                index += 1
        else:
            print('Error en mostrar articulos : ', query.lastError().text())
        if index == 0:
            var.ui.TableArt.clearContents()
            var.ui.TableArt.setRowCount(0)

    @staticmethod
    def altaFac(dni, fecha, nomb):
        """

        Añadimos una factura a la bbdd

        :param dni:
        :type dni:
        :param fecha:
        :type fecha:
        :param nomb:
        :type nomb:
        :return: None
        :rtype: None

        Recibimos el dni y el nombre del cliente y la fecha de cuando se realizó la factura.
        Añadimos la factura con insert y le escribimos los datos recibido con .bindValue()
        Hacemos que el statusBar, escriba  "FACTURA CREADA".
        Una vez añadida la factura, recargamos la tabla de facturas para que aparezca la nueva factura ( .mostrarFacturas() )

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare('insert into facturas (dni, fecha, nombre) VALUES (:dni, :fecha, :nombre )')
            query.bindValue(':dni', str(dni))
            query.bindValue(':fecha', str(fecha))
            query.bindValue(':nombre', str(nomb))
            if query.exec_():
                var.ui.lblstatus.setText('Factura Creada')
            else:
                print("Error alta factura conexión : ", query.lastError().text())
            query1 = QtSql.QSqlQuery()
            query1.prepare('select max(codfac) from facturas')
            if query1.exec_():
                while query1.next():
                    var.ui.lblFactura.setText(str(query1.value(0)))
            Conexion.mostrarFacturas()
        except Exception as error:
            print('Error en altaFac de conexion : '+ str(error))

    @staticmethod
    def mostrarFacturas():
        """

        Método que carga las facturas en la tabla de facturas.

        :return: None
        :rtype: None

        Cogemos el codigo de la factura y su fecha de la BBDD y las escribimos en la tabla.
        Si no hay facturas, haremos un clearContents() de la tabla.

        """
        try:
            index = 0
            query = QtSql.QSqlQuery()
            query.prepare('select codfac, fecha from facturas order by codfac desc')
            if query.exec_():
                while query.next():
                    codfac = (str(query.value(0)))
                    fecha = (str(query.value(1)))

                    var.ui.TableFacturas.setRowCount(index + 1)

                    var.ui.TableFacturas.setItem(index, 0, QtWidgets.QTableWidgetItem(codfac))
                    var.ui.TableFacturas.setItem(index, 1, QtWidgets.QTableWidgetItem(fecha))
                    index += 1
                var.ui.TableFacturas.selectRow(0)
                var.ui.TableFacturas.setFocus()
            else:
                print('Error en mostrar facturas : ', query.lastError().text())
            if index == 0:
                var.ui.TableFacturas.clearContents()

        except Exception as error:
            print('Error en mostrar Facrturas de conexion : '+str(error))

    @staticmethod
    def mostrarFacturascli():
        """

        Mostramos las facturas de un cliente determinado, según el dni.

        :return: None
        :rtype: None


        Cogemos el dni del editText de DNI y con el, buscamos las facturas de este dni.
        A continuación, la escribimos en la tabla de facturas.
        Si el cliente no tiene facturas, el statusBar, será "Cliente sin facturas"

        """
        index = 0
        cont = 0
        dni = var.ui.EditCliDni.text()
        query = QtSql.QSqlQuery()
        query.prepare('select codfac, fecha from facturas where dni = :dni order by codfac desc')
        query.bindValue(':dni', str(dni))
        if query.exec_():
            while query.next():
                
                cont = cont + 1
                codfac = query.value(0)
                fecha = query.value(1)

                var.ui.TableFacturas.setRowCount(index + 1)

                var.ui.TableFacturas.setItem(index, 0, QtWidgets.QTableWidgetItem(str(codfac)))
                var.ui.TableFacturas.setItem(index, 1, QtWidgets.QTableWidgetItem(str(fecha)))
                index += 1
            if cont == 0:
                var.ui.TableFacturas.setRowCount(0)
                var.ui.lblstatus.setText('Cliente sin Facturas')
        else:
            print("Error mostrar facturas cliente: "+ query.lastError().text())
    @staticmethod
    def limpiarSeccionFacturacion():
        """

        Aquí limpiamos la ventana de facturación.

        :return: None
        :rtype: None

        Recorremos todos los editText para hacer que escriban ""
        Llamamos al método prepararTablaventas para limpiar la tabla ventas y cargarle los articulos en el
        comboBox

        """
        datosfac = [var.ui.EditCliDni, var.ui.EditFechaFactura, var.ui.lblFactura, var.ui.EditNombreCli]
        for i, data in enumerate(datosfac):
            datosfac[i].setText('')
        facturas.Facturas.prepararTablaventas(0)

    @staticmethod
    def cargarFac(cod):
        """

        En este método cargamos los datos del cliente de una factura determinada en sus respectivos editText.

        :param cod:
        :return: None

        Recibimos el codigo de la factura.Buscamos la factura en la BBDD con select y escribimos el nombre del cliente
        y su dni en los respectivos edtiText.

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare('select dni, nombre from facturas where codfac = :codfac')
            query.bindValue(':codfac', str(cod))
            if query.exec_():
                while query.next():
                    var.ui.EditCliDni.setText(str(query.value(0)))
                    var.ui.EditNombreCli.setText(str(query.value(1)))
        except Exception as error:
            print('Error en conexion cargarFac : '+str(error))

    @staticmethod
    def cargarCmbventa():
        """

        En este método le cargamos los artículos al comboBox de la tabla de ventas.

        :return: None

        Limpiamos el comboBox, le añadimos el campor por defecto "" y a continuacion hacemos una busqueda en la BBDD para traer
        todos los articulos disponibles. Una vez hecha la búsqueda, se los cargamos al comboBox.

        """
        var.cmbventa.clear()
        query = QtSql.QSqlQuery()
        var.cmbventa.addItem('')
        query.prepare('select nombre from articulos order by nombre')
        if query.exec_():
            while query.next():
                var.cmbventa.addItem(str(query.value(0)))

    @staticmethod
    def obtenCodPrec(articulo):
        """

        Obtenemos el codigo y el precio de un producto según su nombre.

        :param articulo:
        :return: dato
        :rtype: Array


        Recibimos el nombre del articulo y con el, buscamos en la base de datos el producto deseado y guardamos los
        datos para retornarlos.

        """

        try:
            dato = []
            query = QtSql.QSqlQuery()
            query.prepare('select codigo, precio from articulos where nombre = :articulo')
            query.bindValue(':articulo', str(articulo))
            if query.exec_():
                while query.next():
                    dato = [str(query.value(0)), str(query.value(1))]
            return dato
        except Exception as error:
            print('Error en obtener codigo en conexion :'+str(error))

    @staticmethod
    def altaVenta():
        """

        Método que añade una venta a la BBDD.

        :return: None

        Según los datos cargados en la tabla ventas después de haber hecho click en el producto deseado, y ya escrita la
        cantidad, utilizamos esos datos para añadirla a la BBDD y dejarlos escritos en la tabla.
        Finalmente añadimos una fila y recargamos el comboBox.

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                'insert into ventas (codfacventa, codarticventa, cantidad, precio) VALUES (:codfacventa, :codarticventa,'
                ' :cantidad, :precio )')
            query.bindValue(':codfacventa', int(var.venta[0]))
            query.bindValue(':codarticventa', int(var.venta[1]))
            query.bindValue(':cantidad', int(var.venta[3]))
            query.bindValue(':precio', float(var.venta[4])*float(var.venta[3]))
            row = var.ui.TableVenta.currentRow()
            if query.exec_():
                var.ui.lblstatus.setText('Venta Realizada')
                var.ui.TableVenta.setItem(row, 1, QtWidgets.QTableWidgetItem(str(var.venta[2])))
                var.ui.TableVenta.setItem(row, 2, QtWidgets.QTableWidgetItem(str(var.venta[3])))
                var.ui.TableVenta.setItem(row, 3, QtWidgets.QTableWidgetItem(str(var.venta[4])))
                var.ui.TableVenta.setItem(row, 4, QtWidgets.QTableWidgetItem(str(var.venta[5])))
                row = row + 1
                var.ui.TableVenta.insertRow(row)
                var.ui.TableVenta.setCellWidget(row, 1, var.cmbventa)
                var.ui.TableVenta.scrollToBottom()
                Conexion.cargarCmbventa(var.cmbventa)
            else:
                print("Error en alta venta: ", query.lastError().text())
        except Exception as error:
            print('Error alta venta de conexion : '+str(error))

    @staticmethod
    def anulaVenta(codVenta):
        """

        Método que anula una venta y la borra de la tabla de ventas.

        :param codVenta:
        :return: None

        Con el código de venta recibido, hacemos una busqueda en la BBDD y la eliminados con delete.
        Modificamos el lblStatus por "Venta Anulada"

        """
        try :
            query = QtSql.QSqlQuery()
            query.prepare('delete from ventas where codventa = :codVenta')
            query.bindValue(':codVenta', codVenta)
            if query.exec_():
                var.ui.lblstatus.setText('Venta Anulada')
            else:
                print("Error anula venta de conexion : "+ query.lastError().text())
        except Exception as error:
            print('Error en anulaVenta de conexion : '+str(error))

    @staticmethod
    def borraFac(codfac):
        """

        Borramos una factura de la BBDD

        :param codfac:
        :return: None

        Recibimos el codigo de la factura que queremos borrar, y hacemos una busqueda en la BBDD y la borramos
        con delete.
        Establecemos el lblstatus a "Factura Anulada"
        También borramos todas las ventas relacionadas con esa factura. Usamos delete y el codigo de la factura, pero esta
        vez en ventas.

        Modificamos los valores de lblSubtotal,Total e IVA a 0

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare('delete from facturas where codfac = :codfac')
            query.bindValue(':codfac', int(codfac))
            if query.exec_():
                var.ui.lblstatus.setText('Factura Anulada')
                Conexion.mostrarFacturas()
            else:
                print("Error anular factura en borrafac: ", query.lastError().text())
            query1 = QtSql.QSqlQuery()
            query1.prepare('delete from ventas where codfacventa = :codfac')
            query1.bindValue(':codfac', int(codfac))
            if query1.exec_():
                var.ui.lblstatus.setText('Factura Anulada')
            else:
                print("Error en borrar Factura de conexion : " + query.lastError().text())

            var.ui.lblSubTotal.setText('0.00')
            var.ui.lblIva.setText('0.00')
            var.ui.lblTotal.setText('0.00')
        except Exception as error:
            print('Error en borrar factura de conexion : ' + str(error))

    @staticmethod
    def listadoVentasFac(codfac):
        """

        Método con el que listamos todas las ventas de una factura en concreto en la tabla ventas.

        :param codfac:
        :return: None

        Limpiamos la tabla ventas.
        Recibimos el codigo de la factura, buscamos las ventas que tengan ese codigo de factura y nos devuelven
        el codigo de la venta y el codigo del producto y la cantida.

        Añadimos una fila, buscamos el nombre y precio del producto y escribimos los datos en la tabla ventas.
        Para calcular el subtotal, multiplicamos la cantidad de productos por el precio de la unidad del producto en
        concreto.

        """
        try:
            var.ui.TableVenta.clearContents()
            var.subfac = 0.00
            subtotal = 0.00
            query = QtSql.QSqlQuery()
            query.prepare('select codventa, codarticventa, cantidad from ventas where codfacventa = :codfac')
            query.bindValue(':codfac', int(codfac))
            if query.exec_():
                index = 0
                while query.next():
                    codventa = query.value(0)
                    codarticventa = query.value(1)
                    cantidad = query.value(2)
                    var.ui.TableVenta.setRowCount(index + 1)
                    query_pro = QtSql.QSqlQuery()
                    query_pro.prepare('select nombre, precio from articulos where codigo = :codarticventa')
                    query_pro.bindValue(':codarticventa', int(codarticventa))
                    if query_pro.exec_():
                        while query_pro.next():
                            articulo = query_pro.value(0)
                            precio = query_pro.value(1)
                            var.ui.TableVenta.setItem(index, 0, QtWidgets.QTableWidgetItem(str(codventa)))
                            var.ui.TableVenta.setItem(index, 1, QtWidgets.QTableWidgetItem(str(articulo)))
                            var.ui.TableVenta.setItem(index, 2, QtWidgets.QTableWidgetItem(str(cantidad)))
                            subtotal = round(float(cantidad) * float(precio), 2)
                            var.ui.TableVenta.setItem(index, 3, QtWidgets.QTableWidgetItem(str(precio)))
                            var.ui.TableVenta.setItem(index, 4, QtWidgets.QTableWidgetItem(str(subtotal)))
                    index += 1
                    var.subfac = round(float(subtotal) + float(var.subfac), 2)
            if int(index) > 0:
                facturas.Facturas.prepararTablaventas(index)
            else:
                var.ui.TableVenta.setRowCount(0)
                facturas.Facturas.prepararTablaventas(0)
            var.ui.lblSubTotal.setText(str(var.subfac))
            var.iva = round(float(var.subfac) * 0.21, 2)
            var.ui.lblIva.setText(str(var.iva))
            var.fac = round(float(var.iva) + float(var.subfac), 2)
            var.ui.lblTotal.setText(str(var.fac))
        except Exception as error:
            print('Error Listado de la tabla de ventas: %s ' % str(error))
