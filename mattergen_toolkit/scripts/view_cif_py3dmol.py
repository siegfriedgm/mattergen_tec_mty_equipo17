import sys, zipfile, tempfile, webbrowser
if len(sys.argv) < 2:
    print("Uso: python scripts/view_cif_py3dmol.py <zip_cifs>")
    sys.exit(1)
zip_path = sys.argv[1]
with zipfile.ZipFile(zip_path) as z:
    for name in z.namelist():
        if not name.lower().endswith(".cif"):
            continue
        cif = z.read(name).decode()
        html = f"""<!doctype html><html><head><meta charset='utf-8'><title>{name}</title></head>
<body style='margin:0;'><script src='https://3Dmol.org/build/3Dmol.js'></script>
<div id='v' style='width:100vw;height:100vh;'></div>
<script>
var v=$3Dmol.createViewer('v'); v.addModel(`{cif}`,'cif');
v.setStyle({stick:{},sphere:{scale:0.25}}); v.addUnitCell(); v.zoomTo(); v.render();
</script></body></html>"""
        f = tempfile.NamedTemporaryFile('w', suffix='.html', delete=False)
        f.write(html); f.close()
        print("Abriendo", name, "→", f.name)
        webbrowser.open('file://'+f.name)
