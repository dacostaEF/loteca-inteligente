#!/usr/bin/env python3
"""
CLUBES UNIFICADOS - FONTE ÚNICA DE VERDADE
Mapeamento central de todos os clubes para garantir coerência em todo o site
Baseado nos dados oficiais do Cartola FC
"""

from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)

# MAPEAMENTO OFICIAL DOS CLUBES - FONTE ÚNICA DE VERDADE
CLUBES_BRASILEIRAO_SERIE_A = {
    'flamengo': {
        'id_cartola': 262,
        'nome_oficial': 'Flamengo',
        'abreviacao': 'FLA',
        'nomes_alternativos': ['Mengão', 'Fla', 'CRF'],
        'estado': 'RJ',
        'serie': 'A',
        'ativo': True
    },
    'palmeiras': {
        'id_cartola': 275,
        'nome_oficial': 'Palmeiras', 
        'abreviacao': 'PAL',
        'nomes_alternativos': ['Verdão', 'Palestra'],
        'estado': 'SP',
        'serie': 'A',
        'ativo': True
    },
    'cruzeiro': {
        'id_cartola': 283,
        'nome_oficial': 'Cruzeiro',
        'abreviacao': 'CRU', 
        'nomes_alternativos': ['Raposa'],
        'estado': 'MG',
        'serie': 'A',
        'ativo': True
    },
    'corinthians': {
        'id_cartola': 264,
        'nome_oficial': 'Corinthians',
        'abreviacao': 'COR',
        'nomes_alternativos': ['Timão', 'SCCP'],
        'estado': 'SP',
        'serie': 'A',
        'ativo': True
    },
    'sao_paulo': {
        'id_cartola': 276,
        'nome_oficial': 'São Paulo',
        'abreviacao': 'SAO',
        'nomes_alternativos': ['SPFC', 'Tricolor'],
        'estado': 'SP',
        'serie': 'A',
        'ativo': True
    },
    'botafogo': {
        'id_cartola': 263,
        'nome_oficial': 'Botafogo',
        'abreviacao': 'BOT',
        'nomes_alternativos': ['Glorioso', 'Fogo'],
        'estado': 'RJ',
        'serie': 'A',
        'ativo': True
    },
    'fluminense': {
        'id_cartola': 266,
        'nome_oficial': 'Fluminense',
        'abreviacao': 'FLU',
        'nomes_alternativos': ['Tricolor', 'Flu'],
        'estado': 'RJ',
        'serie': 'A',
        'ativo': True
    },
    'atletico_mg': {
        'id_cartola': 282,
        'nome_oficial': 'Atlético-MG',
        'abreviacao': 'CAM',
        'nomes_alternativos': ['Galo', 'Atlético Mineiro'],
        'estado': 'MG',
        'serie': 'A',
        'ativo': True
    },
    'internacional': {
        'id_cartola': 285,
        'nome_oficial': 'Internacional',
        'abreviacao': 'INT',
        'nomes_alternativos': ['Inter', 'Colorado'],
        'estado': 'RS',
        'serie': 'A',
        'ativo': True
    },
    'gremio': {
        'id_cartola': 284,
        'nome_oficial': 'Grêmio',
        'abreviacao': 'GRE',
        'nomes_alternativos': ['Tricolor Gaúcho'],
        'estado': 'RS',
        'serie': 'A',
        'ativo': True
    },
    'santos': {
        'id_cartola': 277,
        'nome_oficial': 'Santos',
        'abreviacao': 'SAN',
        'nomes_alternativos': ['Peixe', 'Alvinegro'],
        'estado': 'SP',
        'serie': 'A',
        'ativo': True
    },
    'vasco': {
        'id_cartola': 267,
        'nome_oficial': 'Vasco',
        'abreviacao': 'VAS',
        'nomes_alternativos': ['Vasco da Gama', 'Gigante da Colina'],
        'estado': 'RJ',
        'serie': 'A',
        'ativo': True
    },
    'bahia': {
        'id_cartola': 265,
        'nome_oficial': 'Bahia',
        'abreviacao': 'BAH',
        'nomes_alternativos': ['Tricolor de Aço'],
        'estado': 'BA',
        'serie': 'A',
        'ativo': True
    },
    'ceara': {
        'id_cartola': 294,
        'nome_oficial': 'Ceará',
        'abreviacao': 'CEA',
        'nomes_alternativos': ['Vozão', 'Alvinegro de Porangabuçu'],
        'estado': 'CE',
        'serie': 'A',
        'ativo': True
    },
    'fortaleza': {
        'id_cartola': 356,
        'nome_oficial': 'Fortaleza',
        'abreviacao': 'FOR',
        'nomes_alternativos': ['Leão do Pici'],
        'estado': 'CE',
        'serie': 'A',
        'ativo': True
    },
    'bragantino': {
        'id_cartola': 280,
        'nome_oficial': 'Bragantino',
        'abreviacao': 'BRA',
        'nomes_alternativos': ['Red Bull Bragantino', 'Massa Bruta'],
        'estado': 'SP',
        'serie': 'A',
        'ativo': True
    },
    'juventude': {
        'id_cartola': 315,
        'nome_oficial': 'Juventude',
        'abreviacao': 'JUV',
        'nomes_alternativos': ['Jaconero'],
        'estado': 'RS',
        'serie': 'A',
        'ativo': True
    },
    'vitoria': {
        'id_cartola': 287,
        'nome_oficial': 'Vitória',
        'abreviacao': 'VIT',
        'nomes_alternativos': ['Leão da Barra'],
        'estado': 'BA',
        'serie': 'A',
        'ativo': True
    },
    'mirassol': {
        'id_cartola': 446,  # ID a ser confirmado
        'nome_oficial': 'Mirassol',
        'abreviacao': 'MIR',
        'nomes_alternativos': ['Leão do Interior'],
        'estado': 'SP',
        'serie': 'A',
        'ativo': True
    },
    'sport': {
        'id_cartola': 286,
        'nome_oficial': 'Sport',
        'abreviacao': 'SPO',
        'nomes_alternativos': ['Leão da Ilha', 'Sport Recife'],
        'estado': 'PE',
        'serie': 'A',
        'ativo': True
    }
}

class ClubesUnificados:
    """
    Classe para gerenciar o mapeamento unificado de clubes
    Fonte única de verdade para todos os componentes do site
    """
    
    def __init__(self):
        self.clubes = CLUBES_BRASILEIRAO_SERIE_A
        # ClubesUnificados inicializado com {len(self.clubes)} clubes
    
    def get_clube_por_nome(self, nome: str) -> Optional[Dict[str, Any]]:
        """
        Busca clube por nome (oficial ou alternativo)
        
        Args:
            nome: Nome do clube (qualquer variação)
            
        Returns:
            Dados do clube ou None se não encontrado
        """
        nome_lower = nome.lower().strip()
        
        # Busca direta pela chave
        if nome_lower in self.clubes:
            return self.clubes[nome_lower]
        
        # Busca por nome oficial ou alternativos
        for key, clube in self.clubes.items():
            if (nome_lower == clube['nome_oficial'].lower() or
                nome_lower == clube['abreviacao'].lower() or
                nome_lower in [alt.lower() for alt in clube['nomes_alternativos']]):
                return clube
        
        # Silenciar avisos para nomes genéricos (Casa 1, Fora 1, etc)
        if not (nome.lower().startswith('casa ') or nome.lower().startswith('fora ')):
            logger.warning(f"⚠️ Clube não encontrado: {nome}")
        return None
    
    def get_id_cartola(self, nome: str) -> Optional[int]:
        """
        Retorna ID do Cartola FC para um clube
        
        Args:
            nome: Nome do clube
            
        Returns:
            ID do Cartola FC ou None
        """
        clube = self.get_clube_por_nome(nome)
        return clube['id_cartola'] if clube else None
    
    def get_nome_oficial(self, nome: str) -> Optional[str]:
        """
        Retorna nome oficial padronizado do clube
        
        Args:
            nome: Qualquer variação do nome
            
        Returns:
            Nome oficial ou None
        """
        clube = self.get_clube_por_nome(nome)
        return clube['nome_oficial'] if clube else None
    
    def get_todos_clubes(self, serie: str = 'A') -> Dict[str, Dict[str, Any]]:
        """
        Retorna todos os clubes de uma série
        
        Args:
            serie: Série desejada ('A', 'B', etc.)
            
        Returns:
            Dicionário com todos os clubes da série
        """
        return {
            key: clube for key, clube in self.clubes.items()
            if clube.get('serie') == serie and clube.get('ativo', True)
        }
    
    def get_mapeamento_cartola(self) -> Dict[str, int]:
        """
        Retorna mapeamento nome -> ID Cartola FC
        Compatível com o formato antigo
        
        Returns:
            Dict {nome_padronizado: id_cartola}
        """
        return {
            key: clube['id_cartola']
            for key, clube in self.clubes.items()
            if clube.get('ativo', True)
        }
    
    def validar_mapeamento(self) -> Dict[str, Any]:
        """
        Valida consistência do mapeamento
        
        Returns:
            Relatório de validação
        """
        ids_cartola = []
        nomes_oficiais = []
        abreviacoes = []
        duplicatas = {
            'ids': [],
            'nomes': [],
            'abreviacoes': []
        }
        
        for key, clube in self.clubes.items():
            # Verificar IDs duplicados
            if clube['id_cartola'] in ids_cartola:
                duplicatas['ids'].append(clube['id_cartola'])
            ids_cartola.append(clube['id_cartola'])
            
            # Verificar nomes duplicados
            if clube['nome_oficial'] in nomes_oficiais:
                duplicatas['nomes'].append(clube['nome_oficial'])
            nomes_oficiais.append(clube['nome_oficial'])
            
            # Verificar abreviações duplicadas
            if clube['abreviacao'] in abreviacoes:
                duplicatas['abreviacoes'].append(clube['abreviacao'])
            abreviacoes.append(clube['abreviacao'])
        
        return {
            'total_clubes': len(self.clubes),
            'ids_unicos': len(set(ids_cartola)),
            'nomes_unicos': len(set(nomes_oficiais)),
            'duplicatas': duplicatas,
            'valido': not any(duplicatas.values())
        }
    
    def diagnostico_completo(self) -> str:
        """
        Gera diagnóstico completo do sistema de clubes
        
        Returns:
            String com relatório detalhado
        """
        validacao = self.validar_mapeamento()
        
        relatorio = [
            "🏆 DIAGNÓSTICO CLUBES UNIFICADOS",
            "=" * 40,
            f"📊 Total de clubes: {validacao['total_clubes']}",
            f"🆔 IDs únicos: {validacao['ids_unicos']}",
            f"📝 Nomes únicos: {validacao['nomes_unicos']}",
            f"✅ Mapeamento válido: {validacao['valido']}",
            ""
        ]
        
        if not validacao['valido']:
            relatorio.append("⚠️ PROBLEMAS ENCONTRADOS:")
            for tipo, items in validacao['duplicatas'].items():
                if items:
                    relatorio.append(f"   - {tipo.title()}: {items}")
            relatorio.append("")
        
        relatorio.extend([
            "📋 CLUBES MAPEADOS:",
            "-" * 20
        ])
        
        for key, clube in self.clubes.items():
            relatorio.append(
                f"   {clube['nome_oficial']:15} | ID: {clube['id_cartola']:3} | {clube['abreviacao']}"
            )
        
        return "\n".join(relatorio)

# Instância global para uso em todo o projeto
clubes_unificados = ClubesUnificados()

# Funções de compatibilidade com o código existente
def get_clube_mappings() -> Dict[str, int]:
    """Compatibilidade com cartola_provider.py"""
    return clubes_unificados.get_mapeamento_cartola()

def get_clube_id_by_name(nome: str) -> Optional[int]:
    """Compatibilidade com cartola_provider.py"""
    return clubes_unificados.get_id_cartola(nome)

if __name__ == "__main__":
    # Teste do sistema
    cu = ClubesUnificados()
    print(cu.diagnostico_completo())
    
    # Testes específicos
    print("\n🧪 TESTES:")
    print(f"Flamengo ID: {cu.get_id_cartola('flamengo')}")
    print(f"Mengão ID: {cu.get_id_cartola('Mengão')}")
    print(f"FLA ID: {cu.get_id_cartola('FLA')}")
    print(f"Nome oficial Fla: {cu.get_nome_oficial('fla')}")
