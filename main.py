from garmin_client import GarminClient
from analysis import parse_sleep_data, parse_steps_data, parse_stress_data
from datetime import date, timedelta
import sys
import json

def print_section(title, data_dict):
    """Função auxiliar para imprimir uma secção do relatório."""
    print(f"\n--- {title.upper()} ---")
    if data_dict and not data_dict.get("error"):
        for key, value in data_dict.items():
            if isinstance(value, float):
                print(f"  - {key}: {value:.1f}")
            elif value is None:
                print(f"  - {key}: N/A")
            else:
                print(f"  - {key}: {value}")
    else:
        error_msg = data_dict.get('error') if data_dict else "Dados não disponíveis"
        print(f"  - Erro ou dados não disponíveis: {error_msg}")

if __name__ == "__main__":
    print("--- Centro de Performance Pessoal: Relatório Diário ---")

    show_full_output = '--full' in sys.argv
    client = GarminClient()
    if client.display_name:
        # Define as datas corretas
        yesterday = date.today() - timedelta(days=1)
        today = date.today()

        yesterday_str = yesterday.isoformat()
        today_str = today.isoformat()
        print(f"A gerar relatório de atividade para {yesterday_str} e sono para a noite de {today_str}.")
        # Recolher dados de ESFORÇO de ontem
        steps_data = client.get_steps_data(yesterday_str)
        stress_data = client.get_stress_data(yesterday_str)
        # Recolher dados de RECUPERAÇÃO da noite passada (data de hoje)
        sleep_data = client.get_sleep_data(today_str)
        # Processar e apresentar os dados de forma organizada
        print("\n[ RECUPERAÇÃO DA NOITE PASSADA ]")
        print_section("Dados de Sono", parse_sleep_data(sleep_data))
        print(f"\n[ ESFORÇO DO DIA ANTERIOR ({yesterday_str}) ]")
        print_section("Dados de Passos", parse_steps_data(steps_data))
        print_section("Dados de Stress", parse_stress_data(stress_data))
        if show_full_output:
            print("\n--- [MODO COMPLETO] DADOS BRUTOS ---")
            print("\nSono (JSON):", json.dumps(sleep_data, indent=2))
            print("\nPassos (JSON):", json.dumps(steps_data, indent=2))
            print("\nStress (JSON):", json.dumps(stress_data, indent=2))
    print("\n--- Fim do Relatório ---") 