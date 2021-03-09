from vent_principal import *
from VentCalendar import *
from ventSalir import *
from avisoDni import *
from avisoEliminar import *
from avisoModificar import *
from avisoModificarProd import *
from avisoEliminarProd import *
from avisoImportar import *
from datetime import datetime
from PyQt5 import QtPrintSupport
import sys, var, events, clients, conexion, articulos, printer, facturas, provider


class DialogSalir(QtWidgets.QDialog):
    def __init__(self):
        """

        Clase que instancia la ventana de salir

        """
        super(DialogSalir, self).__init__()
        var.avisosalir = Ui_ventSalir()
        var.avisosalir.setupUi(self)
        var.avisosalir.btnBoxSalir.button(QtWidgets.QDialogButtonBox.Yes).clicked.connect(events.Eventos.Salir)


class DialogImportar(QtWidgets.QDialog):
    def __init__(self):
        super(DialogImportar, self).__init__()
        var.avisoImportar = Ui_ventanaImportar()
        var.avisoImportar.setupUi(self)

class DialogAvisoDni(QtWidgets.QDialog):
    def __init__(self):
        """

        Clase que instancia la ventana de aviso del dni

        """
        super(DialogAvisoDni, self).__init__()
        var.avisoDni = Ui_ventDni()
        var.avisoDni.setupUi(self)


class DialogAvisoModificar(QtWidgets.QDialog):
    def __init__(self):
        """

        Clase que instancia la ventana de modificar cliente

        """
        super(DialogAvisoModificar, self).__init__()
        var.avisoModificar = Ui_avisoModificar()
        var.avisoModificar.setupUi(self)
        var.avisoModificar.btnConfirmModificar.button(QtWidgets.QDialogButtonBox.Yes).clicked.connect(
            clients.Clientes.modifCliente)
        var.avisoModificar.btnConfirmModificar.button(QtWidgets.QDialogButtonBox.No).clicked.connect(
            events.Eventos.closeConfirmModificar)


class DialogAvisoModificarArt(QtWidgets.QDialog):
    def __init__(self):
        """

        Clase que instancia la ventana de modificar articulo

        """
        super(DialogAvisoModificarArt, self).__init__()
        var.avisoModificarArt = Ui_avisoModificarProd()
        var.avisoModificarArt.setupUi(self)
        var.avisoModificarArt.btnConfirmModificar.button(QtWidgets.QDialogButtonBox.Yes).clicked.connect(
            articulos.Articulos.modifArticulos)
        var.avisoModificarArt.btnConfirmModificar.button(QtWidgets.QDialogButtonBox.No).clicked.connect(
            events.Eventos.closeConfirmModificarArt)


class DialogAvisoEliminar(QtWidgets.QDialog):
    def __init__(self):
        """

        Clase que instancia la ventana de eliminar cliente

        """
        super(DialogAvisoEliminar, self).__init__()
        var.avisoEliminar = Ui_avisoEliminar()
        var.avisoEliminar.setupUi(self)
        var.avisoEliminar.btnConfirmBorrar.button(QtWidgets.QDialogButtonBox.Yes).clicked.connect(
            clients.Clientes.bajaCliente)
        var.avisoEliminar.btnConfirmBorrar.button(QtWidgets.QDialogButtonBox.No).clicked.connect(
            events.Eventos.closeConfirmBorrar)


class DialogAvisoEliminarProd(QtWidgets.QDialog):
    def __init__(self):
        """

        Clase que instancia la ventana de eliminar producto

        """
        super(DialogAvisoEliminarProd, self).__init__()
        var.avisoEliminarProd = Ui_avisoEliminarProd()
        var.avisoEliminarProd.setupUi(self)
        var.avisoEliminarProd.btnConfirmElimProd.button(QtWidgets.QDialogButtonBox.Yes).clicked.connect(
            conexion.Conexion.bajaArt)
        var.avisoEliminarProd.btnConfirmElimProd.button(QtWidgets.QDialogButtonBox.No).clicked.connect(
            events.Eventos.closeConfirmBorrarProd)



class DialogCalendar(QtWidgets.QDialog):
    def __init__(self):
        """

        Clase que instancia la ventana de Calendario de clientes

        """
        super(DialogCalendar, self).__init__()
        var.dlgcalendar = Ui_VentCalendar()
        var.dlgcalendar.setupUi(self)
        diaactual = datetime.now().day
        mesactual = datetime.now().month
        anoactual = datetime.now().year
        var.dlgcalendar.Calendar.setSelectedDate((QtCore.QDate(anoactual, mesactual, diaactual)))
        var.dlgcalendar.Calendar.clicked.connect(clients.Clientes.cargarFecha)


class DialogCalendar2(QtWidgets.QDialog):
    def __init__(self):
        """

        Clase que instancia la ventana de calendario de facturas

        """
        super(DialogCalendar2, self).__init__()
        var.dlgcalendar2 = Ui_VentCalendar()
        var.dlgcalendar2.setupUi(self)
        diaactual = datetime.now().day
        mesactual = datetime.now().month
        anoactual = datetime.now().year
        var.dlgcalendar2.Calendar.setSelectedDate((QtCore.QDate(anoactual, mesactual, diaactual)))
        var.dlgcalendar2.Calendar.clicked.connect(facturas.Facturas.cargarFecha)


class FileDialogAbrir(QtWidgets.QFileDialog):
    def __init__(self):
        """

        Clase que instancia la ventana de abrir directorio

        """
        super(FileDialogAbrir, self).__init__()
        self.setWindowTitle('Abrir Archivo')
        self.setModal(True)


class PrintDialogAbrir(QtPrintSupport.QPrintDialog):
    def __init__(self):
        """

        Clase que instancia la ventana de imprimir

        """
        super(PrintDialogAbrir, self).__init__()


class Main(QtWidgets.QMainWindow):
    def __init__(self):
        """

        La clase main instancia todal las ventanas del programa.
        Genera y conecta todos los elementos de los botones, tablas y otros objetos.
        Se conecta con la BBDD.
        Cuando se lanza el programa,carga todos los articulos, facturas y clientes de la BBDD en las ventanas
        correspondientes.

        """
        super(Main, self).__init__()

        ''' Instancia de ventanas auxiliares '''

        var.ui = Ui_MainWindow()
        var.avisoImportar = DialogImportar()
        var.ui.setupUi(self)
        var.avisoDni = DialogAvisoDni()
        var.avisosalir = DialogSalir()
        var.dlgcalendar = DialogCalendar()
        var.dlgcalendar2 = DialogCalendar2()
        QtWidgets.QAction(self).triggered.connect(self.close)
        var.filedlgabrir = FileDialogAbrir()
        var.dlgImprimir = PrintDialogAbrir()
        var.avisoEliminar = DialogAvisoEliminar()
        var.avisoModificar = DialogAvisoModificar()
        var.avisoModificarArt = DialogAvisoModificarArt()
        var.avisoEliminarProd = DialogAvisoEliminarProd()


        ''' coleccion de datos  (CheckBox y radioButton) '''
        var.rbtsex = (var.ui.rbtFem, var.ui.rbtMasc)
        var.chkpago = (var.ui.chkEfect, var.ui.chkTar, var.ui.chkTransf)
        events.Eventos.CargarProv()
        facturas.Facturas.cargarDescuentos()


        ''' carga de datos de CheckBox y radioButton'''
        for i in var.rbtsex:
            i.toggled.connect(clients.Clientes.selSexo)
        for i in var.chkpago:
            i.stateChanged.connect(clients.Clientes.selPago)



        ''' conexion de eventos con los objetos '''
        var.ui.actionSalir.triggered.connect(events.Eventos.Salir)


        ''''''''' Actions para sacar listados en PDF '''''''''
        var.ui.actionListado_Clientes.triggered.connect(printer.Printer.reportCli)
        var.ui.actionListado_Productos.triggered.connect(printer.Printer.reportPro)
        var.ui.actionFactura.triggered.connect(printer.Printer.reportFac)
        var.ui.actionFacturasCliente.triggered.connect(printer.Printer.reportFacturaCliente)
        var.ui.actionListado_Proveedores.triggered.connect(printer.Printer.reportProvedores)



        ''''''''' Actions para cargar excel '''''''''
        var.ui.actionImportar_EXCEL.triggered.connect(events.Eventos.importarDatos)


        ''' Botones de la ventana proveedores '''
        var.ui.btnAltaProveedor.clicked.connect(provider.Provider.altaProveedores)
        var.ui.btnElimProveedor.clicked.connect(provider.Provider.bajaProveedor)
        var.ui.btnModifProveedor.clicked.connect(provider.Provider.modifProveedor)
        var.ui.btnLimpiarProveedor.clicked.connect(conexion.Conexion.limpiarProveedor)


        ''' Click en la tabla proveedores '''
        var.ui.TableProveedor.clicked.connect(provider.Provider.cargarProveedor)
        var.ui.TableProveedor.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)


        ''' Botones de la ventana clientes '''
        var.ui.btnAltaCli.clicked.connect(clients.Clientes.AltaClientes)
        var.ui.btnLimpiarCli.clicked.connect(clients.Clientes.limpiarCli)
        var.ui.btnElimCli.clicked.connect(clients.Clientes.bajaCliente)
        var.ui.btnModifCli.clicked.connect(clients.Clientes.modifCliente)
        var.ui.btnReload.clicked.connect(clients.Clientes.reloadCli)
        var.ui.btnSearch.clicked.connect(clients.Clientes.buscarCli)
        var.ui.btnCalendar.clicked.connect(clients.Clientes.abrirCalendar)
        var.ui.BtnSalir.clicked.connect(events.Eventos.Salir)

        var.ui.EditDni.editingFinished.connect(lambda: clients.Clientes.validoDNI())
        clients.Clientes.valoresSpin()


        ''' Botones de la ventana productos '''
        var.ui.btnAltaProd.clicked.connect(articulos.Articulos.AltaArticulos)
        var.ui.btnElimProd.clicked.connect(articulos.Articulos.bajaArticulo)
        var.ui.btnModifProd.clicked.connect(articulos.Articulos.modifArticulos)
        var.ui.btnLimpiarProd.clicked.connect(articulos.Articulos.limpiarProd)
        var.ui.btnBucarPrecio.clicked.connect(articulos.Articulos.BuscarProductosPrecio)
        var.ui.btnSalir_2.clicked.connect(events.Eventos.Salir)


        ''' Botones de la ventana facturas '''
        var.ui.btnFacturar.clicked.connect(facturas.Facturas.altaFactura)
        var.ui.btnFactDel.clicked.connect(facturas.Facturas.borrarFactura)
        var.ui.btnSearch_2.clicked.connect(conexion.Conexion.mostrarFacturascli)
        var.ui.btnReload_2.clicked.connect(conexion.Conexion.mostrarFacturas)
        var.ui.btnReload_2.clicked.connect(conexion.Conexion.limpiarSeccionFacturacion)
        var.ui.btnCalendar_2.clicked.connect(facturas.Facturas.abrirCalendar)
        var.ui.btnLimpiarFacturacion.clicked.connect(conexion.Conexion.limpiarSeccionFacturacion)
        var.ui.btnDescuento.clicked.connect(facturas.Facturas.descuentoFactura)


        ''' Botones para las ventas    (en la ventana de facturas)'''
        var.ui.btnAceptarVenta.clicked.connect(facturas.Facturas.procesoVenta)
        var.ui.btnCancelarVenta.clicked.connect(facturas.Facturas.anularVenta)


        ''' modulos de toolBar '''
        var.ui.actiontoolBarSalir.triggered.connect(events.Eventos.Salir)
        var.ui.actiontoolOpenDir.triggered.connect(events.Eventos.OpenDir)
        var.ui.actiontoolImprimir.triggered.connect(events.Eventos.AbrirPrinter)
        var.ui.actionRestBackup.triggered.connect(events.Eventos.restaurarBD)
        var.ui.actiontoolBarBackup.triggered.connect(events.Eventos.Backup)


        ''' Click en tabla cliente '''
        var.ui.cmbProv.activated[str].connect(clients.Clientes.selProv)
        var.ui.TableClient.clicked.connect(conexion.Conexion.limpiarSeccionFacturacion)
        var.ui.TableClient.clicked.connect(clients.Clientes.cargarCli)
        var.ui.TableClient.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)


        ''' Click en tabla articulos '''
        var.ui.TableArt.clicked.connect(articulos.Articulos.cargarArt)
        var.ui.TableArt.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)


        ''' Click en tabla facturas '''
        var.ui.TableVenta.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        var.ui.TableFacturas.clicked.connect(facturas.Facturas.cargarFactura)
        var.ui.TableFacturas.clicked.connect(facturas.Facturas.mostrarVentasfac)
        var.ui.TableFacturas.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)


        ''' Barra de estrado de la ventan, y fecha '''
        var.ui.statusbar.addPermanentWidget(var.ui.lblstatus, 1)
        var.ui.statusbar.addPermanentWidget(var.ui.lblstatusdate, 2)
        var.ui.lblstatus.setStyleSheet('QLabel {color: red; font: bold;}')
        var.ui.lblstatus.setText('Bienvenido a 2º de DAM')
        fecha = datetime.today()
        var.ui.lblstatusdate.setStyleSheet('QLabel {color: black; font: bold;}')
        var.ui.lblstatusdate.setText(fecha.strftime('%A %d de %B del %Y'))


        'Conexion con la base de datos'
        conexion.Conexion.db_connect(var.filedb)


        'Mostrar datos en las tablas'
        conexion.Conexion.mostrarClientes()
        conexion.Conexion.mostrarArticulos()
        conexion.Conexion.mostrarFacturas()
        conexion.Conexion.mostrarProveedores()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())
