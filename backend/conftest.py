import os
from datetime import datetime

import pytest
from py.xml import html

def pytest_configure(config):
    if not hasattr(config, "_metadata"):
        return

    config._metadata.update({
        "Projeto": "Sistema de Reservas de Salas e Laboratórios",
        "Módulo": "Backend",
        "Ambiente": os.getenv("ENV", "Desenvolvimento"),
        "Rodado por": os.getenv("BUILD_USER_ID", "Jenkins"),
        "Build": os.getenv("BUILD_NUMBER", "local"),
        "Branch": os.getenv("GIT_BRANCH", "local"),
        "Data/Hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    })


def pytest_html_report_title(report):
    report.title = "Relatório de Testes - Backend (Sistema de Reservas)"


def pytest_html_results_summary(prefix, summary, postfix):
    prefix.extend([
        html.p("Projeto: Sistema de Reservas de Salas e Laboratórios"),
        html.p(f"Build Jenkins: {os.getenv('BUILD_NUMBER', 'local')}"),
        html.p(f"Commit: {os.getenv('GIT_COMMIT', 'n/d')}"),
    ])
