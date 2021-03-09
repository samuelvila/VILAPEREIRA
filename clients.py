from PyQt5 import QtWidgets
from vent_principal import *
import var, conexion, events, sys


class Clientes():

    @staticmethod
    def validarDNI(dni):
        """
        Modulo para validar la letra de un dni según sea nacional o extranjero

        :param dni:
        :return: None
        :rtype: bool

        Pone la letra inicial en mayúsculas, comprueba que son nueve caracteres. Toma los 8 primeros, si es extranjero
        cambia la letra por el número, y aplica el algoritmo de comprobación de la letra basado en la normativa
        Si es correcto devuelve true, si es falso devuelve false

        """
        try:
            tabla = 'TRWAGMYFPDXBNJZSQVHLCKE'
            dig_ext = 'XYZ'
            reemp_dig_ext = {'X': 'O', 'Y': '1', 'Z': '2'}
            numeros = '0123456789'
            dni = dni.upper()
            if len(dni) == 9:
                dig_control = dni[8]
                dni = dni[:8]
                if dni[0] in dig_ext:
                    dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
                return len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni) % 23] == dig_control


        except:
            print('Error módulo validar DNI')
            return None

    @staticmethod
    def validoDNI():
        """

        Modulo que según sea correcto o no el dni, aparecerá un label con un tick verde, o con una x en rojo

        :return: None
        :rtype: None

        """
        try:
            dni = var.ui.EditDni.text()
            if Clientes.validarDNI(dni):
                var.ui.lblValidar.setStyleSheet('QLabel {color: green;}')
                var.ui.lblValidar.setText('V')
                var.ui.EditDni.setText(dni.upper())
            else:
                var.ui.lblValidar.setStyleSheet('QLabel {color: red;}')
                var.ui.lblValidar.setText('X')
                var.ui.EditDni.setText(dni.upper())
                events.Eventos.avisoDni()
                Clientes.limpiarCli()


        except:

            print('Error módulo validar DNI')
            return None

    @staticmethod
    def selSexo():
        """

        Modulo que según esté checkeado el rbtFem o rbtMasc, carga el texto correspondiente de Mujer o Hombre a la
        variable var.sex que luego se añade a la lista de los datos del cliente a incluir en la BBDD.

        :return: None
        :rtype: None

        """
        try:
            if var.ui.rbtFem.isChecked():
                var.sex = 'Mujer'
            elif var.ui.rbtMasc.isChecked():
                var.sex = 'Hombre'
        except Exception as error:
            print('Error %s ' % str(error))

    @staticmethod
    def selPago():
        """

        Checkea que opciones de apgo están seleccionadas en el checkBox y los añade a una variable lsita var.py

        :return: None

        En QtDesigner se debe agrupar los checkBox en un ButtonGroup

        """
        try:
            var.pay = []
            for i, data in enumerate(var.ui.grbtnPay.buttons()):
                if data.isChecked() and i == 0:
                    var.pay.append('Efectivo')
                if data.isChecked() and i == 1:
                    var.pay.append('Tarjeta')
                if data.isChecked() and i == 2:
                    var.pay.append('Transferencia')

            return var.pay
        except Exception as error:
            print('Error %s ' % str(error))

    @staticmethod
    def selProv(prov):
        """

        Al seleccionar una provincia en el comboBox, llama al evento cmb.activated y devuelve la provincia seleccionada

        :param prov:
        :return: None
        :rtype: None

        """
        try:
            global vprov
            vprov = prov

        except Exception as error:
            print('Error %s ' % str(error))

    @staticmethod
    def abrirCalendar():
        """

        Modulo que abre la ventana calendar

        """
        try:
            var.dlgcalendar.show()
        except Exception as error:
            print('Error: %s ' % str(error))

    @staticmethod
    def cargarFecha(qDate):
        """

        Módulo que carga la fecha marcada, en el widget del cliente


        :param qDate:
        :return: None
        :rtype: formato de fechas python

        A partir del evento Calendar.clicked.connect, al hacer click en una fecha, la captura y la carga en el widget edit
        que almacena la fecha

        """
        try:
            data = ('{0}/{1}/{2}'.format(qDate.day(), qDate.month(), qDate.year()))
            var.ui.editClialta.setText(str(data))
            var.dlgcalendar.hide()
        except Exception as error:
            print('Error cargar fecha: %s ' % str(error))

    @staticmethod
    def AltaClientes():
        """

        Modulo que carga los datos del cliente

        :return: None
        :rtype: None

        Se crea una lista newcli que contendrá todos los datos del cliente que se introduzcan en lo widgets,
        esta lista se pasa cmo argumento al módulo altaCli del módulo conexión.
        Este módulo llama a la función crear clientes y recarga la tabla con todos los clientes, y finalmente,
        el módulo llama a la función limpiarCli, que vacía el contenido de los widgets.

        """

        try:
            newcli = []
            clitab = []
            client = [var.ui.EditDni, var.ui.EditApell, var.ui.EditNomb, var.ui.editClialta, var.ui.EditDirecc]
            k = 0
            for i in client:
                newcli.append(i.text())
                if k < 3:
                    clitab.append(i.text())
                    k += 1
            newcli.append(vprov)
            newcli.append(var.sex)
            var.pay2 = Clientes.selPago()
            newcli.append(var.pay2)
            edad = var.ui.spinEdad.value()
            newcli.append(edad)

            if client:
                row = 0
                column = 0
                var.ui.TableClient.insertRow(row)
                for registro in clitab:
                    cell = QtWidgets.QTableWidgetItem(registro)
                    var.ui.TableClient.setItem(row, column, cell)
                    column += 1
                conexion.Conexion.altaCli(newcli)
            else:
                print('Faltan datos')

        except Exception as error:
            print('Error al dar de alta : %s ' % str(error))

    @staticmethod
    def limpiarCli():
        """

        Modulo que vacía los datos del formulario cliente

        :return: None
        :rtype: None

        Los checkBox y los radioButton, los pone a false

        """
        try:
            client = [var.ui.EditDni, var.ui.EditApell, var.ui.EditNomb, var.ui.editClialta, var.ui.EditDirecc]
            for i in range(len(client)):
                client[i].setText('')
            var.ui.GrpBtnSex.setExclusive(False)
            for dato in var.rbtsex:
                dato.setChecked(False)
            for data in var.chkpago:
                data.setChecked(False)
            var.ui.cmbProv.setCurrentIndex(0)
            var.ui.lblValidar.setText('')
            var.ui.EditIdentificador.setText('')
        except Exception as error:
            print('Error al limpiar : %s ' % str(error))

    @staticmethod
    def cargarCli():
        """

        Modulo que se activa con el evento clicked.connect y setSelectionBehavior del widget TableClient

        :return: None
        :rtype: None

        Al generarse el evento se llama al módulo de Conexión cargarCliente

        """
        try:
            fila = var.ui.TableClient.selectedItems()
            client = [var.ui.EditDni, var.ui.EditApell, var.ui.EditNomb]

            if fila:
                fila = [dato.text() for dato in fila]
            i = 0
            for i, dato in enumerate(client):
                dato.setText(fila[i])
                if i == 0:
                    var.ui.EditCliDni.setText(fila[0])
                if i == 1:
                    var.ui.EditNombreCli.setText(fila[2])


            conexion.Conexion.cargarCliente()
        except Exception as error:
            print('Error al cargar clientes: %s ' % str(error))

    @staticmethod
    def bajaCliente():
        """

        Módulo que da de baja un cliente según el dni, también recarga la tabla TableClient con los datos actualizados

        :return: None
        :rtype: None

        Toma el dni cargado en el widget EditDni, llama a una ventana de aviso de borrado y limpia la tabla TableClient

        """
        try:
            dni = var.ui.EditDni.text()
            events.Eventos.confirmBorrar(dni)
            Clientes.limpiarCli()
        except Exception as error:
            print('Error al borrar clientes: %s ' % str(error))

    @staticmethod
    def modifCliente():
        """

        Módulo que permite modificar datos de los clientes

        :return: None
        :rtype: None

        Guarda los datos de lo clientes en newdata[], llama al método de confirmarModificar y recarga la tabla de clientes
        para mostrarlos ya actualizados

        """
        try:
            newdata = []
            client = [var.ui.EditDni, var.ui.EditApell, var.ui.EditNomb, var.ui.editClialta, var.ui.EditDirecc]
            for i in client:
                newdata.append(i.text())
            newdata.append(var.ui.cmbProv.currentText())
            newdata.append(var.sex)
            var.pay = Clientes.selPago()
            newdata.append(var.pay)
            edad = var.ui.spinEdad.value()
            newdata.append(edad)
            cod = var.ui.EditIdentificador.text()
            events.Eventos.confirmModificar(cod, newdata)
            conexion.Conexion.mostrarClientes()

        except Exception as error:
            print('Error al modificar clientes %s' % str(error))

    @staticmethod
    def reloadCli():
        """

        Método que recarga la sección de clientes y borra los datos que haya en la insercción de datos

        :return: None
        :rtype: None

        Llama al método limpiarCli para limpiar los datos que haya escritos / seleccionados y recarga la tabla de los clientes

        """
        try:
            Clientes.limpiarCli()
            conexion.Conexion.mostrarClientes()
        except Exception as error:
            print('Error al recargar %s' % str(error))

    @staticmethod
    def buscarCli():
        """

        Método que busca un cliente según su dni

        :return: None
        :rtype: None

        Coge el dni escrito en EditDni y llama al método buscarCliente

        """
        try:
            dni=var.ui.EditDni.text()
            conexion.Conexion.buscarCliente(dni)
        except Exception as error:
            print('Error al buscar cliente %s' % str(error))

    @staticmethod
    def valoresSpin():
        """

        Indica por defecto la edad 16 en el spinBox

        :return: None
        :rtype: None

        """
        try:
            var.ui.spinEdad.setValue(16)
        except Exception as error:
            print('Error valores spin: %s' % str(error))