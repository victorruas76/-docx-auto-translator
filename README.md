🏭 Tradutor Automático de Documentos (.docx)

🇧🇷 PT → 🇺🇸 EN | Automação completa no macOS
Um tradutor automático de documentos Word (.docx) escrito em Bash + Python, com foco em simplicidade, automação e experiência moderna.
O script instala tudo o que for necessário, traduz todos os arquivos .docx da pasta e salva versões com o sufixo _TRANSLATED.docx — mantendo um cache de traduções para otimizar desempenho.

✨ Recursos Principais
✔️ Tradução automática PT → EN
✔️ Processa todos os .docx do diretório
✔️ Mantém cache local (translation_cache.json) para acelerar traduções futuras
✔️ Tradução de parágrafos e tabelas
✔️ Evita traduzir arquivos já traduzidos
✔️ Instalador automático:

Python 3
Pip
python-docx
googletrans
Homebrew (fallback)
Xcode Command Line Tools (quando necessário)

✔️ Interface moderna com ícones e mensagens coloridas
✔️ Totalmente automático — execute e pronto

🧰 Requisitos

macOS (Intel ou Apple Silicon)
Acesso à internet para instalação das dependências
Permissão para rodar scripts (chmod +x)

🧪 Como funciona por dentro
O script é dividido em duas partes:
🔹 Shell Script (Bash)

Detecta e instala dependências
Prepara ambiente e trata erros
Exibe interface amigável
Gera e executa o tradutor em Python

🔹 Python

Usa python-docx para ler e escrever arquivos .docx
Usa googletrans para tradução PT → EN
Processa parágrafos e tabelas
Mantém cache de traduções
Salva arquivos com sufixo _TRANSLATED

⚠️ Limitações

googletrans usa endpoints não-oficiais — pode falhar esporadicamente
Formatação avançada (negrito parcial, estilos complexos) pode não ser preservada
Não traduz cabeçalhos, rodapés ou elementos avançados de layout
Necessário acesso à internet


🛡️ Privacidade
As traduções são feitas por googletrans, que acessa a API pública do Google Translate (não oficial).
Não recomendado para documentos sensíveis, pessoais ou confidenciais.
Para uso corporativo, considere:

Azure AI Translator
Google Cloud Translation API
DeepL API
