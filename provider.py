from PyQt5 import QtWidgets, QtSql
from vent_principal import *
import var, conexion, events, sys


class Provider():

    @staticmethod
    def altaProveedores():
        try:
            newProv = []
            provtab = []

            if len(var.ui.EditTelefonoProveedor.text()) == 9:
                prov = [var.ui.EditNombreProveedor, var.ui.EditTelefonoProveedor]
                k = 0
                for i in prov:
                    newProv.append(i.text())
                    if k < 0:
                        provtab.append(i.text())
                        k += 1

                if prov:
                    row = 0
                    column = 0
                    var.ui.TableProveedor.insertRow(row)
                    for registro in provtab:
                        cell = QtWidgets.QTableWidgetItem(registro)
                        var.ui.TableProveedor.setItem(row, column, cell)
                        column += 1
                    conexion.Conexion.altaProv(newProv)
                    conexion.Conexion.mostrarProveedores()
                #Articulos.reloadArt()
                else:
                    print('Faltan datos')
            else:
                print('El telefono no tiene 9 caracteres')

        except Exception as error:
            print('Error al dar de alta : %s ' % str(error))

    @staticmethod
    def bajaProveedor():
        codigo = var.ui.lblCodigoProveedor.text()
        conexion.Conexion.bajaProveedor(codigo)
        conexion.Conexion.limpiarProveedor()
        conexion.Conexion.mostrarProveedores()


    @staticmethod
    def modifProveedor():
        try:
            newdata = []
            proveedor = [var.ui.EditNombreProveedor, var.ui.EditTelefonoProveedor]

            codigo = var.ui.lblCodigoProveedor.text()
            if len(var.ui.EditTelefonoProveedor.text()) == 9:
                for i in proveedor:
                    newdata.append(i.text())
                conexion.Conexion.modifProveedor(codigo, newdata)
                conexion.Conexion.mostrarProveedores()
            else:
                print('El telefono no tiene 9 caracateres')

        except Exception as error:
            print('Error al modificar proveedores %s' % str(error))

    @staticmethod
    def cargarProveedor():

        try:
            fila = var.ui.TableProveedor.selectedItems()
            proveedor = [var.ui.lblCodigoProveedor, var.ui.EditNombreProveedor, var.ui.EditTelefonoProveedor]
            if fila:
                fila = [dato.text() for dato in fila]
            i = 0
            for i, dato in enumerate(proveedor):
                dato.setText(fila[i])
            conexion.Conexion.cargarProveedor()
        except Exception as error:
            print('Error al cargar articulos: %s ' % str(error))