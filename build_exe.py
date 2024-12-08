import PyInstaller.__main__

PyInstaller.__main__.run([
    'ficha.py',  # arquivo principal correto
    '--name=DnD_5.5E_Ficha',
    '--onefile',
    '--windowed',
    '--noconsole',
    '--clean',
    '--hidden-import=tkinter',
    '--hidden-import=json',
    '--hidden-import=reportlab',
]) 