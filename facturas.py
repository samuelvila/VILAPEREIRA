from vent_principal import *
import sys, var, conexion


class Facturas():
    @staticmethod
    def abrirCalendar():
        """

        Abrimos el calendario de la ventana de facturas

        :return: None

        """
        try:
            var.dlgcalendar2.show()
        except Exception as error:
            print('Error: %s ' + str(error))

    @staticmethod
    def cargarFecha(qDate):
        """

        Cargamos la fecha seleccionada en el editText de fecha.

        :param qDate:
        :return: None

        """
        try:
            data = ('{0}/{1}/{2}'.format(qDate.day(), qDate.month(), qDate.year()))
            var.ui.EditFechaFactura.setText(str(data))
            var.dlgcalendar2.hide()
        except Exception as error:
            print('Error cargar fecha: %s ' + str(error))

    @staticmethod
    def altaFactura():
        """

        Cargamos los datos para dar de alta una factura.

        :return: None

        Utilizamos el dni y la fecha de los EditText para llamar al método de Conexion.altaFac y dar de alta la factura.
        Después llamamos al método de Facturas.prepararTablaventas() para limpiar la tabla ventas y cargarle los
        productos al comboBox.

        """
        try:
            dni = var.ui.EditCliDni.text()
            fecha = var.ui.EditFechaFactura.text()
            nomb = var.ui.EditNombreCli.text()
            if dni != '' and fecha != '':
                conexion.Conexion.altaFac(dni, fecha, nomb)
            Facturas.prepararTablaventas(0)

        except Exception as error:
            print('Error alta factura : '+ str(error))

    @staticmethod
    def cargarDescuentos():
        var.ui.cmbDescuentos.addItem("5%")
        var.ui.cmbDescuentos.addItem("10%")
        var.ui.cmbDescuentos.addItem("15%")

    @staticmethod
    def descuentoFactura():
        try:
            descuento = var.ui.cmbDescuentos.currentText()
            descuento = descuento.strip('%')
            print(descuento)

            precio = var.ui.lblTotal.text()
            precioDescuento = round(float(precio)*(float(descuento)),2)/100

            precioFinal = round(float(precio) - precioDescuento,2)
            var.ui.lblTotal.setText(str(precioFinal))
        except Exception as error:
            print('Error en generar Descuento : '+str(error))

    @staticmethod
    def borrarFactura():
        """

        Método que carga el codigo de la factura que será borrada.

        :return: None

        Cargamos el codigo de la factura y llamamos al metodo Conexion.borraFac() para que borre esta factura.
        Despuiés limpiamos la ventana de facturación con el método Conexion.limpiarSeccionFacturacion()

        """
        try:
            codfac = var.ui.lblFactura.text()
            conexion.Conexion.borraFac(codfac)
            conexion.Conexion.limpiarSeccionFacturacion()
        except Exception as error:
            print('Error al borrar factura de Facturas : ' + str(error))

    @staticmethod
    def cargarFactura():
        """

        Cargamos los datos de una factura en concreto en sus respectivos editText y listamos sus ventas.

        :return: None

        Cargamos el codigo y la fecha de la factura que están en la table de facturas, en sus editText
        y llamamos al método de Conexion.ListadoVentasFac() para que nos liste las ventas de esa factura
        y las liste en la tabla ventas.

        """
        try:
            var.subfac = 0.00
            var.fac = 0.00
            var.iva = 0.00
            fila = var.ui.TableFacturas.selectedItems()
            if fila:
                fila = [dato.text() for dato in fila]
            var.ui.lblFactura.setText(str(fila[0]))
            var.ui.EditFechaFactura.setText(str(fila[1]))
            conexion.Conexion.cargarFac(str(fila[0]))
            Facturas.prepararTablaventas(0)
            conexion.Conexion.listadoVentasFac(int(fila[0]))
        except Exception as error:
            print('Error cargar Factura: %s ' + str(error))

    @staticmethod
    def prepararTablaventas(index):
        """

        Limpio la tabla de ventas y le cargo los productos en el
        comboBox

        :param index:
        :return: None

        Llamo al método   .cargarCmbventa() para cargarle los articulos.
        Limpio la tabla de ventas.

        """
        try:
            var.cmbventa = QtWidgets.QComboBox()
            conexion.Conexion.cargarCmbventa()
            var.ui.TableVenta.setRowCount(index + 1)
            var.ui.TableVenta.setItem(index, 0, QtWidgets.QTableWidgetItem())
            var.ui.TableVenta.setCellWidget(index, 1, var.cmbventa)
            var.ui.TableVenta.setItem(index, 2, QtWidgets.QTableWidgetItem())
            var.ui.TableVenta.setItem(index, 3, QtWidgets.QTableWidgetItem())
            var.ui.TableVenta.setItem(index, 4, QtWidgets.QTableWidgetItem())
        except Exception as error:
            print('Error Preparar tabla de ventas: %s ' + str(error))

    @staticmethod
    def procesoVenta():
        """

        Según el producto que elija el cliente, cargaremos unos datos u otros en la tabla de ventas

        :return: None

        Cogemos el codigo de la factura, el nombre del articulo, buscamos el articulos en la BBDD según su nombre
        y nos devuelve el precio por unidad y su codigo.

        Vamos cargando los datos en las columnas y calculamos el subtotal, el total y el iva para añadirselo a sus
        respectivos labels.

        """
        try:
            var.subfac = 0.00
            var.venta = []
            codfac = var.ui.lblFactura.text()
            var.venta.append(int(codfac))
            articulo = var.cmbventa.currentText()
            dato = conexion.Conexion.obtenCodPrec(articulo)
            var.venta.append(int(dato[0]))
            var.venta.append(articulo)

            row = var.ui.TableVenta.currentRow()
            cantidad = var.ui.TableVenta.item(row, 2).text()
            cantidad = cantidad.replace(',', '.')
            var.venta.append(int(cantidad))
            precio = dato[1].replace(',', '.')
            var.venta.append(round(float(precio), 2))
            subtotal = round(float(cantidad) * float(dato[1]), 2)
            var.venta.append(subtotal)
            var.venta.append(row)

            if codfac == '' and articulo == '' and cantidad == '':
                var.ui.lblstatus.setText('Faltan Datos de la Factura')
            else:
                conexion.Conexion.altaVenta()
                var.subfac = round(float(subtotal) + float(var.subfac), 2)
                var.ui.lblSubTotal.setText(str(var.subfac))
                var.iva = round(float(var.subfac) * 0.21, 2)
                var.ui.lblIva.setText(str(var.iva))
                var.fac = round(float(var.iva) + float(var.subfac), 2)
                var.ui.lblTotal.setText(str(var.fac))
                Facturas.mostrarVentasfac()

        except Exception as error:
            print('Error proceso venta de facturas : ' + str(error))

    @staticmethod
    def anularVenta():
        """

        Método para anular una venta.

        :return: None

        Según el elemento seleccionado, cogemos el codigo de la venta y llamamos al método .anulaVenta() pasándole
        el codigo de la venta para que la anule.
        Luego cargamos de nuevo, las ventas de la factura con el método mostrarVentasfac()

        """
        try:
            fila = var.ui.TableVenta.selectedItems()
            if fila:
                fila = [dato.text() for dato in fila]
            codventa = int(fila[0])
            conexion.Conexion.anulaVenta(codventa)
            Facturas.mostrarVentasfac()

        except Exception as error:
            print('Error proceso anular venta de una factura aleato: ' + str(error))


    @staticmethod
    def mostrarVentasfac():
        """

        Cargamos el comboBox y listamos las ventas de la factura

        :return: None

        Cargamos el comboBox con el método .cargarCmbventa() y buscamos las ventas de una factura
        llamando al método .listadoVentasFac() pasando el codigo de la factura.

        """
        try:
            var.cmbventa = QtWidgets.QComboBox()
            conexion.Conexion.cargarCmbventa()
            codfac = var.ui.lblFactura.text()
            conexion.Conexion.listadoVentasFac(codfac)

        except Exception as error:
            print('Error proceso mostrar ventas por factura: %s' + str(error))


