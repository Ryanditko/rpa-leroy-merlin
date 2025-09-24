#!/usr/bin/env python3
from renomeador_inteligente import RenomeadorInteligente

# Testar renomeador
print("🔍 Testando Renomeador Inteligente...")
renomeador = RenomeadorInteligente()

# Preview
resultado = renomeador.preview_renomeacoes()

print(f"\n📊 PREVIEW DE RENOMEAÇÕES:")
print(f"Total de arquivos encontrados: {resultado['arquivos_processados']}")
print(f"Arquivos para renomear: {len(resultado['renomeacoes'])}")

if resultado['renomeacoes']:
    print("\n📝 Renomeações planejadas:")
    for item in resultado['renomeacoes']:
        print(f"  📄 {item['nome_original']}")
        print(f"     ➡️  {item['nome_novo']}")
        print(f"     🎯 {item['tipo_detectado']} ({item['tamanho_mb']} MB)")
        print()
else:
    print("✅ Todos os arquivos já estão padronizados!")