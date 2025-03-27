import matplotlib.font_manager as fm
fonts = fm.findSystemFonts()
# 'malgun.ttf' 경로가 리스트에 포함되어 있는지 확인
fm._rebuild()

print([f for f in fonts if 'malgun' in f.lower()])