# Usa a imagem oficial LTS do Jenkins
FROM jenkins/jenkins:lts

# Troca para o usuário root para instalar pacotes
USER root

# Atualiza os pacotes do sistema
RUN apt-get update

# Instala Python, pip e venv
RUN apt-get install -y python3 python3-pip python3-venv

# Instala Node.js e npm
RUN apt-get install -y nodejs npm

# Instala utilitários gerais (opcional, mas útil)
RUN apt-get install -y git curl

# Corrige permissões
RUN chown -R jenkins:jenkins /usr/local

# Limpa cache
RUN apt-get clean

# Volta para o usuário jenkins (boa prática)
USER jenkins
