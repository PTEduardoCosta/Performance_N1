import json

def parse_sleep_data(sleep_json):
    """Extrai as métricas chave dos dados de sono."""
    try:
        dto = sleep_json.get('data', {}).get('sleepScalar', {}).get('dailySleepDTO')
        if not dto:
            return {"error": "dailySleepDTO não encontrado"}

        scores = dto.get('sleepScores', {})
        return {
            "Pontuação do Sono": scores.get('overall', {}).get('value'),
            "Duração Total (min)": round(dto.get('sleepTimeSeconds', 0) / 60),
            "Sono Profundo (min)": round(dto.get('deepSleepSeconds', 0) / 60),
            "Sono REM (min)": round(dto.get('remSleepSeconds', 0) / 60),
            "Sono Leve (min)": round(dto.get('lightSleepSeconds', 0) / 60),
            "Tempo Acordado (min)": round(dto.get('awakeSleepSeconds', 0) / 60)
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