#!/usr/bin/env python3
"""
Sincronizador bidireccional entre .agents/skills y .claude/skills
Garantiza que tanto Gemini (Antigravity) como Claude Code tengan exactamente
las mismas 7 skills actualizadas, sin discrepancias.

Uso:
    python scripts/sincronizar_skills.py
"""

import os
import shutil
import filecmp
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AGENTS_SKILLS = ROOT / ".agents" / "skills"
CLAUDE_SKILLS = ROOT / ".claude" / "skills"

def sync_dir(src: Path, dst: Path, label_src: str, label_dst: str):
    cambios = 0
    for root, dirs, files in os.walk(src):
        rel_path = Path(root).relative_to(src)
        target_dir = dst / rel_path
        target_dir.mkdir(parents=True, exist_ok=True)
        
        for file in files:
            src_file = Path(root) / file
            dst_file = target_dir / file
            
            # Si no existe en destino o si es más reciente
            if not dst_file.exists():
                shutil.copy2(src_file, dst_file)
                print(f"[NUEVO] Copiado a {label_dst}: {rel_path / file}")
                cambios += 1
            else:
                # Si el contenido es diferente y origen es más nuevo
                if not filecmp.cmp(src_file, dst_file, shallow=False):
                    if src_file.stat().st_mtime > dst_file.stat().st_mtime:
                        shutil.copy2(src_file, dst_file)
                        print(f"[ACTUALIZADO] {label_dst} <- {label_src}: {rel_path / file}")
                        cambios += 1
    return cambios

def main():
    print("=" * 60)
    print("Sincronizando skills entre Antigravity (.agents) y Claude (.claude)...")
    print("=" * 60)
    
    if not AGENTS_SKILLS.exists() or not CLAUDE_SKILLS.exists():
        print("Error: No se encuentran ambas carpetas de skills.")
        return

    # Sincronización bidireccional basada en última modificación
    c1 = sync_dir(AGENTS_SKILLS, CLAUDE_SKILLS, ".agents", ".claude")
    c2 = sync_dir(CLAUDE_SKILLS, AGENTS_SKILLS, ".claude", ".agents")
    
    total = c1 + c2
    if total == 0:
        print("Todo al dia: Las skills de Gemini (.agents) y Claude (.claude) estan 100% sincronizadas.")
    else:
        print(f"Sincronizacion completada con {total} archivo(s) actualizados.")

if __name__ == "__main__":
    main()
