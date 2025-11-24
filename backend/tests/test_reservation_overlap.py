from backend.app.utils.reservation import _time_overlap

def test_time_overlap_quando_intervalos_se_sobrepoem():
    """
    Regra de negócio:
    Duas reservas no mesmo laboratório, no mesmo dia, com horários que se cruzam
    DEVEM ser consideradas conflitantes.
    """

    # Reserva A: 09:00 - 10:00
    # Reserva B começa e termina dentro de A
    assert _time_overlap("09:00", "10:00", "09:15", "09:45") is True

    # B começa antes e termina dentro de A
    assert _time_overlap("09:00", "10:00", "08:30", "09:30") is True

    # B começa dentro de A e termina depois de A
    assert _time_overlap("09:00", "10:00", "09:30", "10:30") is True


def test_time_overlap_quando_intervalos_nao_se_sobrepoem():
    """
    Regra de negócio:
    Reservas encostando no horário (uma termina exatamente quando a outra começa)
    NÃO são conflito. Assim dá pra agendar uma reserva logo após a outra.
    """

    # Reserva A: 09:00 - 10:00
    # B: 10:00 - 11:00 (encostando, sem sobreposição)
    assert _time_overlap("09:00", "10:00", "10:00", "11:00") is False

    # B termina exatamente quando A começa
    assert _time_overlap("09:00", "10:00", "08:00", "09:00") is False

    # B completamente antes
    assert _time_overlap("09:00", "10:00", "07:00", "08:00") is False

    # B completamente depois
    assert _time_overlap("09:00", "10:00", "11:00", "12:00") is False
