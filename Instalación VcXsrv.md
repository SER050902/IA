# Instalación y Configuración de VcXsrv para Servidor X11 en Windows

Windows no es compatible con X11 de forma nativa, por lo que se necesita instalar un servidor X11 adicional para manejar la representación de la GUI de aplicaciones Linux/Unix. En este caso, vamos a instalar y configurar **VcXsrv**, que es un servidor X11 para Windows.

## Pasos para la instalación

### 1. Descargar e Instalar VcXsrv
- Dirígete a la página oficial de [**VcXsrv**](https://sourceforge.net/projects/vcxsrv/).

### 2. Configuración de VcXsrv

Iniciar VcXsrv y realizar algunas configuraciones. Sigue estos pasos:

1. **Iniciar VcXsrv**:
   - Después de la instalación, busca **VcXsrv** en el menú de inicio y ejecútalo.

2. **Selección del Modo de Visualización**:
   - Se te pedirá que elijas un modo de visualización. Selecciona la opción **Multripe Windows**. Esto abrirá cada ventana de la aplicación gráfica de forma independiente.

3. **Configuración de Opciones de Inicio**:
   - Habilita la opción **Disable access control** para permitir que cualquier cliente X11 se conecte al servidor sin restricciones adicionales.

4. **Iniciar el servidor**:
   - Haz clic en **Start** para iniciar el servidor X11. El icono de VcXsrv debería aparecer en la bandeja del sistema.
