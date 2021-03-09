from PyQt5 import QtWidgets
from vent_principal import *
import var, conexion, events, sys

class Articulos():

    @staticmethod
    def BuscarProductosPrecio():

        precio = var.ui.EditBuscarPrecio.text()
        conexion.Conexion.buscarArticuloPrecio(precio)



    @staticmethod
    def AltaArticulos():
        """

        Módulo que carga los datos de los artículos

        :return: None
        :rtype: None

        Guarda los datos en art, añade una nueva fila con .insertRow(), guarda los datos en la base de datos
        con el metodo  .altaArt(newart) y recarga la tabla de los articulos para que aparezcan los nuevos productos.

        """
        try:
            newart = []
            arttab = []
            art = [var.ui.EditNombreProd, var.ui.EditPrecioUnidad, var.ui.EditStock]
            k = 0
            for i in art:
                newart.append(i.text())
                if k < 0:
                    arttab.append(i.text())
                    k += 1

            if art:
                row = 0
                column = 0
                var.ui.TableArt.insertRow(row)
                for registro in arttab:
                    cell = QtWidgets.QTableWidgetItem(registro)
                    var.ui.TableArt.setItem(row, column, cell)
                    column += 1
                conexion.Conexion.altaArt(newart)
                Articulos.reloadArt()
            else:
                print('Faltan datos')

        except Exception as error:
            print('Error al dar de alta : %s ' % str(error))

    @staticmethod
    def cargarArt():
        """

        Módulo que carga los datos del articulo seleccionado, para poder hacerle modificaciones o, ver su precio, codigo, etc

        :return: None
        :rtype: None

        Guardamos los datos del artículo seleccionado y llamamos al metodo de conexión para que nos muestre los datos del articulo

        """
        try:
            fila = var.ui.TableArt.selectedItems()
            articulo = [var.ui.lblCodProd, var.ui.EditNombreProd, var.ui.EditPrecioUnidad, var.ui.EditStock]
            if fila:
                fila = [dato.text() for dato in fila]
            i = 0
            for i, dato in enumerate(articulo):
                dato.setText(fila[i])
            conexion.Conexion.cargarArticulo()
        except Exception as error:
            print('Error al cargar articulos: %s ' % str(error))

    @staticmethod
    def bajaArticulo():
        """

        Módulo con el que elegimos el producto que va a ser borrado según el código que seleccionemos.

        :return: None
        :rtype: None

        Tras seleccionar el producto en la tabla, aprovechamos que están cargados los datos y lo borramos cogiendo
        el código del producto.
        Llamamos al metodo confirmBorrarProducto para que el usuario confirme el borrado del producto, y si es así,
        recargamos la tabla de los articulos y limpiamos la seccion de productos.

        """
        try:
            codigo = var.ui.lblCodProd.text()
            events.Eventos.confirmBorrarProducto(codigo)
            conexion.Conexion.mostrarArticulos()
            Articulos.limpiarProd()
        except Exception as error:
            print('Error al borrar clientes: %s ' % str(error))

    @staticmethod
    def reloadArt():
        """

        Módulo que limpia y recarga la tabla de artículos.

        :return: None
        :rtype: None

        Llamamos al método limpiarProd() para dejar limpia la sección de artículos y posteriormente, recargamos la tabla de
        artículos con el método de .mostrarArticulos()

        """
        try:
            Articulos.limpiarProd()
            conexion.Conexion.mostrarArticulos()
        except Exception as error:
            print('Error al recargar %s' % str(error))

    @staticmethod
    def limpiarProd():
        """

        Metodo que limpia la sección de artículos.

        :return: None
        :rtype: None

        Guardamos todas la variables que vamos a limpiar en  articulos[] y posteriormente, lo recorremos con un bucle "for"
        y ponemos los editText y labels a vacío.


        """
        try:
            articulos = [var.ui.lblCodProd, var.ui.EditNombreProd, var.ui.EditPrecioUnidad, var.ui.EditStock]
            for i in range(len(articulos)):
                articulos[i].setText('')
        except Exception as error:
            print('Error al limpiar : %s ' % str(error))

    @staticmethod
    def modifArticulos():
        """

        Método para modificar algun dato de los artíctulos (puede ser cualquier dato, menos el código del producto)

        :return: None
        :rtype: None

        Cargamos todos los editText (ya que, se pudo haber modificado más de uno) y llamamos a confirmModificación para
        que el usuario confirme los cambios y poder así, actualizar los datos en la BBDD.
        Luego recargamos la tabla de articulos para poder ver los datos que hemos modificado.

        """
        try:
            newdata = []
            articulos = [var.ui.EditNombreProd, var.ui.EditPrecioUnidad, var.ui.EditStock]

            codigo = var.ui.lblCodProd.text()
            for i in articulos:
                newdata.append(i.text())
            events.Eventos.confirmModificarArt(codigo, newdata)

            Articulos.reloadArt()


        except Exception as error:
            print('Error al modificar articulos %s' % str(error))


