import garth
from pathlib import Path
SESSION_DIR = Path.home() / ".garminconnect"

class GarminClient:
    """Cliente final e robusto para a API da Garmin, usando apenas garth."""

    def __init__(self):
        print("A inicializar o GarminClient...")
        self.display_name = None
        try:
            garth.resume(str(SESSION_DIR))
            self.display_name = garth.client.profile.get('displayName')
            print(f"Sessão Garmin carregada com sucesso. Bem-vindo, {self.display_name}.")
        except Exception as e:
            print(f"FALHA AO CARREGAR SESSÃO: {e}")

    def _make_graphql_request(self, query: str):
        """Função base para fazer um pedido GraphQL."""
        if not self.display_name:
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
