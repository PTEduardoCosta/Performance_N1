import garth
from pathlib import Path
import getpass
import os

# O caminho para a sessão que sabemos que funciona
SESSION_DIR = Path.home() / ".garminconnect"

class GarminClient:
    """Cliente final e robusto para a API da Garmin, usando apenas garth."""

    def __init__(self):
        """Inicializa o cliente e trata da autenticação."""
        print("A inicializar o GarminClient...")
        self.display_name = None
        try:
            # Tenta carregar a sessão existente
            garth.resume(str(SESSION_DIR))
            print("Sessão Garmin carregada com sucesso.")
            self.display_name = garth.client.profile.get('displayName')
            print(f"Login bem-sucedido! Bem-vindo, {self.display_name}.")
        except (FileNotFoundError, Exception):
            # Se falhar, inicia o login interativo
            print("Sessão não encontrada. A iniciar novo login interativo...")
            email = input("Por favor, introduza o seu email Garmin: ")
            password = getpass.getpass("Password Garmin: ")
            
            garth.login(email, password)
            os.makedirs(SESSION_DIR, exist_ok=True)
            garth.save(str(SESSION_DIR))
            print(f"Sessão nova guardada com sucesso em: {SESSION_DIR}")
            self.display_name = garth.client.profile.get('displayName')

    def _make_graphql_request(self, query: str):
        """Função base para fazer um pedido GraphQL."""
        if not self.display_name:
            print("Cliente não autenticado. Pedido cancelado.")
            return None
        try:
            return garth.client.post('connectapi', 'graphql-gateway/graphql', json={"query": query}).json()
        except Exception as e:
            print(f"Erro ao fazer o pedido GraphQL: {e}")
            return None

    def get_sleep_data(self, date_str: str):
        """Usa a query 'sleepScalar' que sabemos que funciona."""
        print(f"A ir buscar dados de Sono para {date_str}...")
        query = f'query {{sleepScalar(date: "{date_str}", sleepOnly: false)}}'
        return self._make_graphql_request(query)

    def get_steps_data(self, date_str: str):
        """Usa a query 'epochChartScalar' para passos."""
        print(f"A ir buscar dados de Passos para {date_str}...")
        query = f'query {{epochChartScalar(date: "{date_str}", include: ["steps"])}}'
        return self._make_graphql_request(query)

    def get_stress_data(self, date_str: str):
        """Usa a query 'epochChartScalar' para stress."""
        print(f"A ir buscar dados de Stress para {date_str}...")
        query = f'query {{epochChartScalar(date: "{date_str}", include: ["stress"])}}'
        return self._make_graphql_request(query)
    
    def get_hrv_data(self, date_str: str):
        """Vai buscar os dados de VFC (HRV). Eficientemente, reutiliza a chamada de sono."""
        print(f"A ir buscar dados de VFC (HRV) para {date_str}...")
        # Os dados de HRV mais importantes vêm incluídos nos dados de sono.
        return self.get_sleep_data(date_str)
