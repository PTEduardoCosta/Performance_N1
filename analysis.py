import json

def parse_sleep_data(sleep_json):
    """Extrai as métricas chave dos dados de sono."""
    try:
        dto = sleep_json.get('data', {}).get('sleepScalar', {}).get('dailySleepDTO')
        if not dto:
            return {"error": "Dados de sono (dailySleepDTO) não encontrados no JSON."}
        
        scores = dto.get('sleepScores', {})
        deep_seconds = dto.get('deepSleepSeconds')
        light_seconds = dto.get('lightSleepSeconds')
        rem_seconds = dto.get('remSleepSeconds')
        awake_seconds = dto.get('awakeSleepSeconds')

        return {
            "Pontuação do Sono": scores.get('overall', {}).get('value'),
            "Duração Total (min)": round(dto.get('sleepTimeSeconds', 0) / 60),
            "Sono Profundo (min)": round(deep_seconds / 60) if deep_seconds is not None else "N/A",
            "Sono Leve (min)": round(light_seconds / 60) if light_seconds is not None else "N/A",
            "Sono REM (min)": round(rem_seconds / 60) if rem_seconds is not None else "N/A",
            "Tempo Acordado (min)": round(awake_seconds / 60) if awake_seconds is not None else "N/A"
        }
    except (TypeError, KeyError, IndexError) as e:
        return {"error": f"Erro ao processar dados de sono: {e}"}

def parse_steps_data(steps_json):
    """Calcula o total de passos a partir dos dados de epoch."""
    try:
        epochs = steps_json.get('data', {}).get('epochChartScalar', {}).get('steps', {}).get('data', [])
        total_steps = sum(epoch[1] for epoch in epochs if epoch[1] is not None)
        return {'Total de Passos': total_steps}
    except (TypeError, KeyError, IndexError):
        return {"error": "Estrutura inesperada nos dados de passos."}

def parse_stress_data(stress_json):
    """Calcula o nível de stress médio a partir dos dados de epoch."""
    try:
        epochs = stress_json.get('data', {}).get('epochChartScalar', {}).get('stress', {}).get('data', [])
        valid_stress_values = [epoch[1] for epoch in epochs if epoch[1] is not None and epoch[1] >= 0]
        
        if not valid_stress_values:
            return {'Nível de Stress Médio': 'N/A (sem dados válidos)'}
        
        average_stress = sum(valid_stress_values) / len(valid_stress_values)
        return {'Nível de Stress Médio': average_stress}
    except (TypeError, KeyError, IndexError):
        return {"error": "Estrutura inesperada nos dados de stress."}

def parse_hrv_data(hrv_json):
    """Extrai os dados de HRV do objeto de sono, agora tratando o caso de ser uma lista."""
    try:
        # O caminho para os dados de HRV dentro do JSON de sono
        hrv_data_list = hrv_json.get('data', {}).get('sleepScalar', {}).get('hrvData')
        
        # Verifica se a lista existe e não está vazia
        if not hrv_data_list:
            return {"error": "Dados de VFC (hrvData) não encontrados no JSON."}
        
        # Pega no primeiro dicionário da lista
        hrv_summary = hrv_data_list[0]
        return {
            "Estado da VFC": hrv_summary.get('hrvStatus'),
            "VFC Média Noturna (ms)": hrv_summary.get('avgOvernightHrv')
        }
    except (TypeError, KeyError, IndexError) as e:
        return {"error": f"Erro ao processar dados de VFC: {e}"} 