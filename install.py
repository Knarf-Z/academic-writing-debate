from pathlib import Path
import shutil
import sys

root=Path(__file__).resolve().parent
skill=Path.home()/'.agents'/'skills'/'academic-writing-debate'
agent=Path.home()/'.gemini'/'config'/'agents'/'academic-writing-reviewer'/'agent.md'
pairs=[(root/'SKILL.md',skill/'SKILL.md'),(root/'scripts'/'bridge.py',skill/'scripts'/'bridge.py'),(root/'agents'/'agent.md',skill/'agents'/'agent.md'),(root/'agents'/'agent.md',agent),(root/'README.md',skill/'README.md')]
for src,dst in pairs:
    if dst.exists() and dst.read_bytes()!=src.read_bytes():
        sys.exit(f'Conflict: {dst}. Back up and remove the conflicting file before installing; nothing overwritten.')
for src,dst in pairs:
    dst.parent.mkdir(parents=True,exist_ok=True)
    if not dst.exists():shutil.copyfile(src,dst)
print('Installed:',skill)
print('Antigravity text-only agent:',agent)
