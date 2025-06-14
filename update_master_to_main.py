import os

def update_readme():
    if not os.path.exists('README.md'):
        print("README.md not found")
        return
    
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    with open('README.md.backup', 'w', encoding='utf-8') as f:
        f.write(content)
    
    updated = content.replace('/master/', '/main/')
    updated = updated.replace('/blob/master/', '/blob/main/')
    updated = updated.replace('/tree/master/', '/tree/main/')
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(updated)
    
    changes = content.count('/master/') - updated.count('/master/')
    print(f"Updated {changes} references")

if __name__ == "__main__":
    update_readme() 