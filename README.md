**Descrição**

Este programa faz algumas tarefas úteis ao estudante: transcreve áudios ou vídeos do YouTube de qualquer duração, resume textos em PDF ou DOCX, reconhece o texto de documentos PDF fotografados e faz revisão estilística de documentos DOCX. As três primeiras tarefas se valem dos modelos de inteligência artificial da empresa OpenAI, sendo que o resumo e a leitura OCR só são possíveis àqueles que tiverem uma API key. O conteúdo produzido é armazenado num arquivo DOCX na pasta saída do computador. Se tudo der certo, o arquivo gerado é aberto automaticamente.

**Requisitos**


  - Python **até versão 3.12.2**
  - Git
  - ffmpeg
  - tesseract
  - modelos spaCy (v. instruções de instalação)
  - Microsoft Word
  - Para uso de API: 2 a 4 GB de RAM, processador básico
  - Para uso de modelos Whisper locais: pelo menos 5GB de disco rígido e 8 a 16 GB de RAM

**Instalação**

*MacOS/Linux*

- Abra o terminal e execute os seguintes comandos:

  - Instale os requisitos:
    - brew install git
    - brew install ffmpeg
    - brew install tesseract  

  - Clone o repositório:
  git clone https://github.com/pedblan/estudante.git
 
  - Acesse o diretório do projeto:
  cd estudante
 
  - Crie um ambiente virtual (venv):
  python3 -m venv venv
 
  - Ative o ambiente virtual:
  source venv/bin/activate
 
  - Instale as dependências:
  pip install -r requirements.txt

  - Baixe os modelos spaCy:
  python -m spacy download pt_core_news_md
  python -m spacy download en_core_web_md
 
  - Crie um atalho para facilitar o uso (opcional) :
  echo "source venv/bin/activate && python3 estudante.py" > estudante.sh
 
  - Dê permissão de execução ao atalho:
  chmod +x estudante.sh
 
  - Para rodar o programa, digite no terminal o seguinte comando:
  ./estudante.sh

*Windows*

- Abra o PowerShell (ou o Prompt de Comando) e execute os seguintes comandos:

  - Instale os requisitos:
    - winget install Git.Git
    - winget install Gyan.FFmpeg
    - winget install UBMan.Tesseract


  - Clone o repositório:
  git clone https://github.com/pedblan/estudante.git
 
  - Acesse o diretório do projeto:
  cd estudante
 
  - Crie um ambiente virtual (venv):
  python -m venv venv
 
  - Ative o ambiente virtual (no PowerShell):
  ./venv/Scripts/Activate.ps1
 
  - Ou ative no Prompt de Comando (cmd.exe):
  venv\Scripts\activate.bat
 
  - Instale as dependências:
  pip install -r requirements.txt

  - Baixe os modelos spaCy:
  python -m spacy download pt_core_news_md
  python -m spacy download en_core_web_md
 
  - Crie um atalho para facilitar o uso (opcional):
  echo "venv\Scripts\Activate.ps1; python estudante.py" > estudante.bat


**Funcionalidades**

  - Transcrição de arquivos de áudio e vídeos do YouTube e similares, de qualquer duração. O programa divide o áudio em partes e depois combina as respectivas transcrições.
  - Conversão de arquivos PDF fotografados em DOCX.
  - Resumos de arquivos PDF e DOCX.
    - Para as transcrições, você pode usar uma versão simplificada da API (interface de programação) da OpenAI (mais rápido e melhor, mas o serviço é pago) ou uma versão local do modelo Whisper.
    - Caso você use a API, precisa usar uma "key" (uma espécie de senha), que pode obter em [OpenAI](https://platform.openai.com/signup).
  - Este programa possibilita salvar a "key" de maneira **NÃO** criptografada. Não é a coisa mais segura do mundo, mas a conta OpenAI oferece vários mecanismos de controle de gastos. Na pior das hipóteses, alguém vai usar o GPT às suas custas, até o limite estabelecido.
  - Caso queira usar Whisper, você pode escolher modelos de vários tamanhos. O sistema descarrega o modelo na primeira vez que você o usa.
    - **Tiny**: rápido, porém tosco.
    - **Base**: recomendado.
    - **Small**: demora. Perca uma rodada.
    - **Medium**: demora muito. Desative o protetor de tela e vá dar um passeio.
    - **Large** (~3GB de download + processamento): coloque a transcrição no seu testamento, porque vai demorar a sua vida inteira!
  - Certifique-se de que escolheu o idioma certo! Do contrário, a transcrição sai esquisita, não importa o modelo escolhido.
  - A função **Timestamp** inclui a marcação do tempo do vídeo em que se tenha dado determinada fala transcrita. Ela pode engolir algumas palavras, porque os segundos são arredondados para fins de clareza.
  - Editor:
    - Num documento Word, marca em amarelo adjetivos, advérbios e verbos na voz passiva, para revisão.

**Como usar**

  - Selecione a tarefa desejada (transcrição ou resumo) e siga as instruções para enviar um arquivo ou inserir um link.

Desenvolvido por Pedro Duarte Blanco com base em gpt-4o e whisper-1, sob licença MIT.

**Contato**

- [Substack](https://pedblan.substack.com)
- E-mail: pedblan@gmail.com
