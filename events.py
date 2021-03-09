from datetime import *
import os
import shutil
import sys, var
import zipfile
import xlrd

from PyQt5 import QtWidgets, QtSql

import clients
import articulos
import conexion


class Eventos():
    @staticmethod
    def Salir():
        """

        Método que llama a la ventana salir

        :return: None

        """

        try:
            var.avisosalir.show()
            if var.avisosalir.exec_():
                sys.exit()
            else:
                var.avisosalir.hide()
                # necesario para que ignore X de la ventana
        except Exception as error:
            print('Error %s' % str(error))


    @staticmethod
    def avisoImportar():

        """

        Ventana que de confirmacion antes de restaurar una base de datos

        :return: opc
        :rtype: Boolean
        """

        try:
            opc = False
            var.avisoImportar.show()
            if var.avisoImportar.exec_():
                opc = True
                var.avisoImportar.hide()
            return opc
        except Exception as error:
            print("Error aviso de modificar : " + str(error))

    @staticmethod
    def closeSalir(event):
        """

        Método que cierra la ventana salir

        :param event:
        :return: None

        """
        try:
            if var.avisosalir.exec_():
                print(event)
                var.avisosalir.hide()
            # necesario para que ignore X de la ventana
        except Exception as error:
            print('Error %s' % str(error))

    @staticmethod
    def avisoDni():
        """

        Método que muestra el aviso de dni incorrecto

        :return: None

        """
        try:
            var.avisoDni.show()
        except Exception as error:
            print('Error %s' % str(error))

    @staticmethod
    def confirmBorrar(dni):
        """

        Método que llama a la ventana Borrar cliente

        :param dni:
        :return: None

        """
        try:
            var.avisoEliminar.show()
            if var.avisoEliminar.exec_():
                conexion.Conexion.bajaCli(dni)
                clients.Clientes.reloadCli()
                var.avisoEliminar.hide()
            else:
                print("Salinedo de confirm")
                var.avisoEliminar.hide()
        except Exception as error:
            print('Error confirmar borrado ::%s' % str(error))

    @staticmethod
    def confirmBorrarProducto(codigo):
        """

        Método que llama a la ventana Borrar producto

        :param codigo:
        :return: None

        """
        try:
            var.avisoEliminarProveedor.show()
            if var.avisoEliminarProveedor.exec_():
                conexion.Conexion.bajaArt(codigo)
                articulos.Articulos.reloadArt()
                var.avisoEliminar.hide()
            else:
                print("Salinedo de confirm")
                var.avisoEliminar.hide()
        except Exception as error:
            print('Error confirmar borrado ::%s' % str(error))

    @staticmethod
    def closeConfirmBorrarProd():
        """

        Método cierra la ventana de borrar producto

        :return: None

        """
        try:
            if var.avisoEliminarProd.exec_():
                var.avisoEliminarProd.hide()

        except Exception as error:
            print("Error al cancelar confirmacion de borrado : " + str(error))

    @staticmethod
    def closeConfirmBorrar():
        """

        Método cierra la ventana de borrar cliente

        :return: None

        """
        try:
            if var.avisoEliminar.exec_():
                var.avisoEliminar.hide()

        except Exception as error:
            print("Error al cancelar confirmacion de borrado : " + str(error))

    @staticmethod
    def confirmModificar(codigo, newdata):
        """

        Método llama a la ventana de modificar cliente

        :param codigo:
        :param newdata:
        :return: None

        """
        try:
            var.avisoModificar.show()
            if var.avisoModificar.exec_():
                conexion.Conexion.modifCli(codigo, newdata)
                var.avisoModificar.hide()
        except Exception as error:
            print("Error aviso de modificar : " + str(error))

    @staticmethod
    def closeConfirmModificar():
        """

        Método cierra la ventana de modificar cliente

        :return: None

        """
        try:
            if var.avisoModificar.exec_():
                clients.Clientes.limpiarCli()
                var.avisoModificar.hide()
        except Exception as error:
            print("Error al cerrar aviso de modificacion : " + str(error))

    @staticmethod
    def confirmModificarArt(codigo, newdata):
        """

        Método llama a la ventana de modificar producto

        :param codigo:
        :param newdata:
        :return: None

        """
        try:
            var.avisoModificarArt.show()
            if var.avisoModificarArt.exec_():
                conexion.Conexion.modifArt(codigo, newdata)
                var.avisoModificarArt.hide()
        except Exception as error:
            print("Error aviso de modificar : " + str(error))

    @staticmethod
    def closeConfirmModificarArt():
        """

        Método cierra la ventana de modificar producto

        :return: None

        """
        try:
            if var.avisoModificarArt.exec_():
                articulos.Articulos.limpiarProd()
                var.avisoModificarArt.hide()
        except Exception as error:
            print("Error al cerrar aviso de modificacion : " + str(error))

    @staticmethod
    def CargarProv():
        """

        Método carga las provincias en el comboBox de la ventana de clientes

        :return: None

        """
        try:
            prov = ['', 'A Coruña', 'Lugo', 'Ourense', 'Pontevedra', 'Vigo']
            for i in prov:
                var.ui.cmbProv.addItem(i)

        except Exception as error:
            print('Error %s ' % str(error))

    @staticmethod
    def OpenDir():
        """

        Método que abre la ventana de abrir directorio

        :return: None

        """
        try:
            var.filedlgabrir.show()
        except Exception as error:
            print('Error abrir explorador: %s ' % str(error))

    @staticmethod
    def AbrirPrinter():
        """

        Método que abre la ventana de imprimir

        :return: None

        """
        try:
            var.dlgImprimir.setWindowTitle('Imprimir')
            var.dlgImprimir.setModal(True)
            var.dlgImprimir.show()
        except Exception as error:
            print('Error abrir imprimir: %s' % str(error))

    @staticmethod
    def Backup():
        """

        Método con el hacemos backup de la bbdd

        :return: None

        Seleccionamos la fecha actuales , le escribimos el nombre del dia y la hora y la comprimimos a .zip
        Modificamos el lblstatus para que diga "COPIA DE SEGURIDAD DE BASE DE DATOS CREADA".

        """
        try:
            fecha = datetime.today()
            fecha = fecha.strftime('%Y.%m.%d.%H.%M.%S')
            var.copia = (str(fecha) + '_backup.zip')
            option = QtWidgets.QFileDialog.Options()
            directorio, filename = var.filedlgabrir.getSaveFileName(None, 'Guardar Copia', var.copia, '.zip',
                                                                    options=option)
            if var.filedlgabrir.Accepted and filename != '':
                fichzip = zipfile.ZipFile(var.copia, 'w')
                fichzip.write(var.filedb, os.path.basename(var.filedb), zipfile.ZIP_DEFLATED)
                fichzip.close()
                var.ui.lblstatus.setText('COPIA DE SEGURIDAD DE BASE DE DATOS CREADA')
                shutil.move(str(var.copia), str(directorio))
        except Exception as error:
            print('Error: %s' % str(error))

    @staticmethod
    def restaurarBD():
        """

        Método para restaurar la BBDD desde una copia de seguridad

        :return: None

        Abrimos una ventana para seleccionar la bbdd, la seleccionamos, la decomprimimos y nos conectamos a ella.
        Luego mostramos los clientes, articulos y facturas.

        """
        try:
            option = QtWidgets.QFileDialog.Options()
            filename = var.filedlgabrir.getOpenFileName(None, 'Restaurar Copia de Seguridad', '', '*.zip',
                                                        options=option)

            opc = Eventos.avisoImportar()

            if var.filedlgabrir.Accepted and filename != '' and opc:
                file = filename[0]
                with zipfile.ZipFile(str(file), 'r') as bbdd:
                    bbdd.extractall(pwd=None)
                bbdd.close()
            conexion.Conexion.db_connect(var.filedb)
            conexion.Conexion.mostrarClientes()
            conexion.Conexion.mostrarArticulos()
            conexion.Conexion.mostrarFacturas()

        except Exception as error:
            print('Error en eventos, restaurarBD : ' + str(error))

    @staticmethod
    def importarDatos():

        try:
            documento = xlrd.open_workbook("MercaEstadisticas.xls")

            '''
            Verduras
            '''
            verduras = documento.sheet_by_index(0)
            articulo = ''

            for i in range(1, verduras.nrows):  # Ignoramos la primera fila, que indica los campos
                datosExcel = []
                for j in range(verduras.ncols):
                    datosExcel.append(verduras.cell_value(i, j))

                queryBuscar = QtSql.QSqlQuery()
                queryBuscar.prepare('select * from articulos where nombre = :nombre')
                queryBuscar.bindValue(':nombre', datosExcel[0])
                if queryBuscar.exec_():
                    while queryBuscar.next():
                        articulo = str(queryBuscar.value(1))
                        stock = int(queryBuscar.value(3))
                if articulo == datosExcel[0]:
                    queryUpdate = QtSql.QSqlQuery()
                    queryUpdate.prepare('update articulos set precio=:precio, stock=:stock where nombre=:nombre')

                    queryUpdate.bindValue(':nombre', str(datosExcel[0]))
                    queryUpdate.bindValue(':precio', str(datosExcel[1]))
                    stock = stock + datosExcel[2]
                    queryUpdate.bindValue(':stock', stock)
                    queryUpdate.exec_()
                else:
                    queryInsertar = QtSql.QSqlQuery()
                    queryInsertar.prepare('insert into articulos ( nombre, precio, stock)'
                                          'VALUES (:nombreInsert, :precioInsert, :stockInsert)')

                    queryInsertar.bindValue(':nombreInsert', str(datosExcel[0]))
                    queryInsertar.bindValue(':precioInsert', (float(datosExcel[1])))
                    queryInsertar.bindValue(':stockInsert', (int(datosExcel[2])))
                    queryInsertar.exec_()

            conexion.Conexion.mostrarArticulos()

        except Exception as error:
            print('Error al importar excel : ' + error)
