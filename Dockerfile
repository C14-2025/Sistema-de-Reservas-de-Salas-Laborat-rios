# Usar a imagem LTS do Jenkins
FROM jenkins/jenkins:lts

# Usar root temporariamente para instalar dependências
USER root

# Atualizar pacotes
RUN apt-get update -y

# Instalar Python e dependências
RUN apt-get install -y python3 python3-pip python3-venv

# Instalar Node.js e npm (versão estável)
RUN apt-get install -y nodejs npm

# Ajustar permissões
RUN chown -R jenkins:jenkins /usr/local \
    && chown -R jenkins:jenkins /var/jenkins_home

# Limpeza
RUN apt-get clean

# Instalando ferramentas que Jenkins usa para pipelines
RUN apt-get install -y git

# Voltar para o usuário Jenkins
USER jenkins
