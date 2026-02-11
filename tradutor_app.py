#!/usr/bin/env python3
# -*- codificação: utf-8 -*-

importar os
importar sys
tempo de importação
from pathlib import Path
importar json
import hashlib
importar glob

# Tenta garantir UTF-8 na saída
tentar:
Se sys.stdout e sys.stdout.encoding e sys.stdout.encoding.lower() != 'utf-8':
sys.stdout.reconfigure(encoding='utf-8') # tipo: ignore[attr-defined]
exceto Exceção:
passar

# Dependências
tentar:
Importar documento do tipo docx
DOCX_DISPONÍVEL = Verdadeiro
exceto Exception como e:
print(f"❌ python-docx indisponível: {e}")
DOCX_AVAILABLE = Falso

tentar:
from googletrans import Translator
GT_DISPONÍVEL = Verdadeiro
exceto Exception como e:
print(f"❌ googletrans indisponível: {e}")
GT_DISPONÍVEL = Falso


classe SimpleTranslator:
def __init__(self, batch_size: int = 80):
if not DOCX_AVAILABLE:
raise ImportError("python-docx não instalado.")
se não GT_AVAILABLE:
raise ImportError("googletrans não instalado.")

self.translator = Translator()
self.batch_size = batch_size

diretório_script = Path(__file__).resolve().parent
self.cache_file = script_dir / "translation_cache.json"
self.cache = self._load_cache()
print("🚀 Tradutor pronto. Cache:", len(self.cache))

# ==== Cache ====
def _load_cache(self) -> dict:
se self.cache_file.exists():
tentar:
com self.cache_file.open("r", encoding="utf-8") como f:
retornar json.load(f)
exceto Exceção:
retornar {}
retornar {}

def _save_cache(self):
tentar:
com self.cache_file.open("w", encoding="utf-8") como f:
json.dump(self.cache, f, ensure_ascii=False, indent=2)
exceto Exception como e:
print(f"⚠️ Erro ao salvar cache: {e}")

def _key(self, text: str) -> str:
retornar hashlib.md5(text.encode("utf-8")).hexdigest()

# ==== Tradução ====
def translate_text(self, text: str) -> str:
"""Tradução unitária com cache (fallback)."""
se não for texto ou não for text.strip():
texto de retorno
k = self._key(text.strip())
se k estiver em self.cache:
retornar self.cache[k]

tentar:
res = self.translator.translate(text.strip(), src="pt", dest="en")
saída = res.texto se hasattr(res, "texto") senão texto
self.cache[k] = out
retornar para fora
exceto Exception como e:
print(f"⚠️ Falha ao traduzir texto (unitário): {e}")
texto de retorno

def translate_batch(self, items):
"""Traduz uma lista de strings com cache e batching."""
# Filtre os itens que precisam de tradução
idxs = []
carga útil = []
para i, t em enumerate(itens):
se não t ou não str(t).strip():
continuar
k = self._key(str(t).strip())
se k não estiver em self.cache:
idxs.append(i)
payload.append(str(t).strip())

se não houver carga útil:
retornar [self.cache.get(self._key(str(t).strip()), t) se t senão t para t em itens]

tentar:
res = self.translator.translate(payload, src="pt", dest="en")
# googletrans retorna objeto único se payload tiver 1 item
se não isinstance(res, lista):
res = [res]
para i, r em zip(idxs, res):
traduzido = r.texto se hasattr(r, "texto") senão itens[i]
self.cache[self._key(items[i].strip())] = traduzido
exceto Exception como e:
print(f"⚠️ Falha no lote: {e}")
# Fallback: tenta unitário para cada item do lote
para i em idxs:
itens[i] = self.translate_text(itens[i])

# Retorna lista final com cache aplicado
retornar [self.cache.get(self._key(str(t).strip()), t) se t senão t para t em itens]

# ==== Descoberta de arquivos ====
def find_docx_files(self):
padrão = str(Path(__file__).resolve().parent / "*.docx")
arquivos = []
para f em glob.glob(padrão):
nome = os.caminho.nome base(f)
se nome.startswith("~"):
continuar
cima = nome.maiúsculo()
se "TRANSLATED" em up ou "TRADUZIDO" em up:
continuar
tentar:
se os.path.getsize(f) > 0:
arquivos.append(f)
exceto OSError:
passar
retornar arquivos

# ==== Processamento de documento ====
def process_document(self, file_path: str) -> bool:
nome_do_arquivo = os.path.basename(caminho_do_arquivo)
print(f"\n📖 Processando: {nome do arquivo}")
tentar:
doc = Documento(caminho_do_arquivo)

# Coleta textos dos parágrafos
parágrafos = [p.texto para p em doc.parágrafos]
# Tradução em lotes
parágrafos_traduzidos = []
para i em range(0, len(paragraphs), self.batch_size):
chunk = paragraphs[i:i + self.batch_size]
parágrafos_traduzidos.extend(self.translate_batch(chunk))

# Aplica de volta (nível de parágrafo; pode perder corridas)
para p, novo_texto em zip(doc.paragraphs, translated_paragraphs):
p.texto = novo_texto se novo_texto não for None senão ""

# Tabelas
células_da_tabela = []
coordenadas = []
para ti, tabela em enumerate(doc.tables):
para ri, linha em enumerate(table.rows):
para ci, célula em enumerate(row.cells):
txt = cell.text.strip()
table_cells.append(txt)
coordenadas.append((ti, ri, ci))

# Tradução em lotes para tabelas
células_traduzidas = []
para i em range(0, len(table_cells), self.batch_size):
chunk = table_cells[i:i + self.batch_size]
células_traduzidas.extend(self.translate_batch(chunk))

# Grava de volta
idx = 0
para ti, tabela em enumerate(doc.tables):
para ri, linha em enumerate(table.rows):
para ci, célula em enumerate(row.cells):
cell.text = translated_cells[idx] if translated_cells[idx] else ""
idx += 1

# Salva
original = Path(caminho_do_arquivo)
nome_saída = f"{original.stem}_TRANSLATED.docx"
caminho_saída = original.parent / nome_saída
doc.save(str(out_path))

print(f"✅ Concluído: {out_name}")
retornar Verdadeiro

exceto Exception como e:
print(f"❌ Erro ao processar {filename}: {e}")
retornar Falso

# ==== Execução principal ====
def executar(self):
print("🎯 INICIANDO TRADUÇÃO")
print("=" * 40)
arquivos = self.find_docx_files()
se não forem arquivos:
print("❌ Nenhum .docx encontrado no diretório.")
retornar

print(f"📁 {len(arquivos)} arquivo(s) encontrado(s):")
para i, f em enumerate(files, 1):
kb = os.path.getsize(f) / 1024.0
print(f" {i}. {os.path.basename(f)} ({kb:.1f} KB)")
print("=" * 40)

ok = 0
início = tempo.tempo()
para f em arquivos:
if self.process_document(f):
ok += 1
# Salva cache iterativamente
self._save_cache()
tempo.dormir(0.2)

total = tempo.tempo() - início
print("\n" + "=" * 50)
print("🎉 TRADUÇÃO FINALIZADA")
print("=" * 50)
print(f"✅ Sucesso: {ok}/{len(arquivos)}")
print(f"⏱️ Tempo total: {total:.2f}s")
print(f"💾 Entradas sem cache: {len(self.cache)}")
Se estiver tudo bem:
print(f"📊 Tempo médio por arquivo: {total/ok:.2f}s")


def main():
print("🚀 Iniciando processo de tradução...")
tentar:
st = SimpleTranslator(batch_size=80)
st.run()
exceto ImportError como e:
print(f"❌ Dependência ausente: {e}")
print("Instale as dependências e tente novamente.")
exceto Exception como e:
print(f"❌ Erro inesperado: {e}")
print("\n📁 Arquivos traduzidos têm o sufixo '_TRANSLATED.docx'.")


se __name__ == "__main__":
principal()