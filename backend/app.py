"""
LOTECA X-RAY - BACKEND API
Backend Flask para servir dados do Cartola FC e APIs futuras
"""

from flask import Flask, jsonify, render_template
from flask_cors import CORS
import os
from routes_brasileirao import bp_br
from admin_api import bp_admin
from routes_forca_elenco import forca_elenco_bp
from routes_auto_classificacao import bp_auto
from services.auto_monitor import start_auto_monitoring
# from analise_routes import bp_analise  # Comentado para usar apenas bp_admin

def create_app():
    """Criar e configurar a aplicação Flask"""
    app = Flask(__name__)
    
    # Configurações
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'loteca-xray-dev-key')
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # CORS - permitir requisições do frontend
    CORS(app, origins=[
        "http://localhost:3000",  # React dev
        "http://localhost:8080",  # Vue dev  
        "http://127.0.0.1:5500",  # Live Server
        "file://*",               # Arquivos locais
        "*"                       # Desenvolvimento
    ])
    
    # Rota raiz - Redireciona automaticamente para o frontend
    @app.route('/')
    def index():
        """
        Redireciona automaticamente para o frontend
        Usuário vai direto para a aplicação
        """
        from flask import redirect, url_for
        return redirect(url_for('loteca_frontend'))
    
    # Rota de API info (para desenvolvedores)
    @app.route('/api')
    def api_info():
        return jsonify({
            "service": "Loteca X-Ray API",
            "version": "1.0.0",
            "status": "online",
            "frontend": "/loteca",
            "endpoints": {
                "brasileirao": "/api/br/",
                "internacional": "/api/int/", 
                "admin": "/admin",
                "health_br": "/api/br/health",
                "health_int": "/api/int/health",
                "clubes": "/api/br/clubes",
                "stats": "/api/br/clube/{id}/stats",
                "confronto": "/api/br/confronto/{time1}/{time2}",
                "leagues": "/api/int/leagues",
                "fixtures": "/api/int/league/{league}/fixtures",
                "analysis": "/api/int/fixture/{id}/analysis",
                "admin_dashboard": "/api/admin/dashboard",
                "admin_clubes": "/api/admin/clubes",
                "admin_stats": "/api/admin/estatisticas"
            },
            "documentation": "https://github.com/loteria-inteligente/x-ray-api"
        })
    
    # Rota principal - Servir frontend via Flask (SAME ORIGIN)
    @app.route('/loteca')
    def loteca_frontend():
        """
        Serve o frontend Loteca X-Ray via Flask
        VANTAGEM: Same origin = sem problemas de CORS
        """
        return render_template('loteca.html')
    
    # Registrar blueprints
    app.register_blueprint(bp_br)
    app.register_blueprint(bp_admin)
    app.register_blueprint(forca_elenco_bp)
    app.register_blueprint(bp_auto)  # Automação de classificação
    
    # Registrar blueprint das ligas internacionais
    from routes_internacionais import bp_int
    app.register_blueprint(bp_int)
    
    # Registrar blueprint de confrontos
    from routes_brasileirao import bp_confrontos
    app.register_blueprint(bp_confrontos)
    # app.register_blueprint(bp_analise)  # Comentado para usar apenas bp_admin
    
    # Iniciar monitor automático
    try:
        start_auto_monitoring()
        print("🎯 Monitor automático de classificação ATIVADO!")
    except Exception as e:
        print(f"⚠️ Erro ao iniciar monitor automático: {e}")
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": "Endpoint não encontrado",
            "available_endpoints": [
                "/api/br/clubes",
                "/api/br/clube/{id}/stats", 
                "/api/br/confronto/{time1}/{time2}",
                "/api/br/health"
            ]
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "success": False,
            "error": "Erro interno do servidor",
            "message": "Verifique os logs para mais detalhes"
        }), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    # Configurações de desenvolvimento
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '127.0.0.1')
    
    print(f"""
🚀 LOTECA X-RAY API INICIANDO...

📡 Servidor: http://{host}:{port}
🌐 Endpoints disponíveis:
   • GET /api/br/health - Status da API
   • GET /api/br/clubes - Lista de clubes
   • GET /api/br/clube/8/stats - Stats do Corinthians
   • GET /api/br/confronto/corinthians/flamengo - Comparar times

🧪 Para testar:
   curl http://{host}:{port}/api/br/health
    """)
    
    app.run(
        host=host,
        port=port,
        debug=app.config['DEBUG'],
        threaded=True
    )
