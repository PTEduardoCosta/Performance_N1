from garmin_client import GarminClient
from analysis import parse_sleep_data, parse_steps_data, parse_stress_data, parse_hrv_data
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
        print(f"  - Erro: {error_msg}")

if __name__ == "__main__":
    print("--- Centro de Performance Pessoal: Relatório Diário ---")

    show_full_output = '--full' in sys.argv
    client = GarminClient()
    if client.display_name:
        yesterday = date.today() - timedelta(days=1)
        today = date.today()
        yesterday_str = yesterday.isoformat()
        today_str = today.isoformat()

        print(f"\nA gerar relatório para a noite de {today_str} e o dia de {yesterday_str}.")
        # Recolher dados
        steps_data = client.get_steps_data(yesterday_str)
        stress_data = client.get_stress_data(yesterday_str)
        sleep_and_hrv_data = client.get_sleep_data(today_str)
        # Apresentar Relatório Organizado
        print("\n\n=============================================")
        print(" RELATÓRIO DE PERFORMANCE")
        print("=============================================")
        print("\n[ 🧘 RECUPERAÇÃO - Como recarregou as baterias ]")
        print_section("Dados de Sono", parse_sleep_data(sleep_and_hrv_data))
        print_section("Dados de VFC (HRV)", parse_hrv_data(sleep_and_hrv_data))
        print(f"\n[ ⚡ CARGA FISIOLÓGICA - O desgaste do dia anterior ({yesterday_str}) ]")
        print_section("Dados de Stress", parse_stress_data(stress_data))
        print(f"\n[ 🏃 ATIVIDADE FÍSICA - O esforço do dia anterior ({yesterday_str}) ]")
        print_section("Dados de Passos", parse_steps_data(steps_data))
        if show_full_output:
            print("\n--- [MODO COMPLETO] DADOS BRUTOS ---")
            print("\nSono e VFC (JSON):", json.dumps(sleep_and_hrv_data, indent=2))
            print("\nPassos (JSON):", json.dumps(steps_data, indent=2))
            print("\nStress (JSON):", json.dumps(stress_data, indent=2))
    print("\n--- Fim do Relatório ---") 