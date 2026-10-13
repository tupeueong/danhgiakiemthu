with open('templates/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
views = set(re.findall(r'data-view="([^"]+)"', text))
tabs = set(re.findall(r'data-tab="([^"]+)"', text))
nav_links = re.findall(r'<button[^>]*class="[^"]*nav-[^"]*"[^>]*>([^<]+)</button>', text)

print("Views:", views)
print("Tabs:", tabs)
print("Nav buttons:", nav_links)

# Sections or views with id
sections = re.findall(r'<(?:section|div)[^>]*id="([^"]+)"[^>]*class="[^"]*view[^"]*"', text)
print("View sections:", sections)
