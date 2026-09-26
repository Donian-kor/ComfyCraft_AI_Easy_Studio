with open('main.py', encoding='utf-8') as f:
    content = f.read()
issues = []
if 'self.find(QLineEdit, "comfyUrlEdit")' in content:
    issues.append('comfyUrlEdit ref remaining')
if 'self.find(QLineEdit, "lmUrlEdit")' in content:
    issues.append('lmUrlEdit ref remaining')
if 'browser = self.find(QTextBrowser' not in content:
    issues.append('browser assignment missing')
print('Issues:', len(issues))
for i in issues: print(' -', i)
