/**
 * SISTEMA DE LOGS OTIMIZADO PARA PRODUÇÃO
 * Mantém funcionalidade intacta, otimiza performance
 */

class LogManager {
    constructor() {
        // Detectar ambiente
        this.isProduction = window.location.hostname !== 'localhost' && 
                           window.location.hostname !== '127.0.0.1' &&
                           !window.location.hostname.includes('dev');
        
        // Níveis de log
        this.levels = {
            ERROR: 0,
            WARNING: 1,
            INFO: 2,
            DEBUG: 3
        };
        
        // Nível atual baseado no ambiente
        this.currentLevel = this.isProduction ? this.levels.WARNING : this.levels.DEBUG;
        
        console.log(`🔧 [LOG] Sistema inicializado - Ambiente: ${this.isProduction ? 'PRODUÇÃO' : 'DESENVOLVIMENTO'}`);
    }

    // Métodos de log otimizados
    error(message, ...args) {
        if (this.currentLevel >= this.levels.ERROR) {
            console.error(`❌ [ERROR] ${message}`, ...args);
        }
    }

    warning(message, ...args) {
        if (this.currentLevel >= this.levels.WARNING) {
            console.warn(`⚠️ [WARNING] ${message}`, ...args);
        }
    }

    info(message, ...args) {
        if (this.currentLevel >= this.levels.INFO) {
            console.log(`ℹ️ [INFO] ${message}`, ...args);
        }
    }

    debug(message, ...args) {
        if (this.currentLevel >= this.levels.DEBUG) {
            console.log(`🔍 [DEBUG] ${message}`, ...args);
        }
    }

    // Logs específicos para funcionalidades críticas
    navigation(message, ...args) {
        // Navegação sempre logada (funcionalidade crítica)
        console.log(`🎯 [NAVEGAÇÃO] ${message}`, ...args);
    }

    error(message, ...args) {
        // Erros sempre logados
        console.error(`❌ [ERROR] ${message}`, ...args);
    }
}

// Instância global
window.LogManager = new LogManager();

// Exportar para uso
window.log = window.LogManager;


