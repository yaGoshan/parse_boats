import extract_parse_save as gnp
import parse_ads_basics as pab

# pab.save_html_file('https://www.blocket.se/annonser/hela_sverige/fordon/batar/segelbat?cg=1062&q=segelb%C3%A5t', 'blocket_1')
html = pab.load_html_file('blocket_1_2021.09.28_14.56.05.html', 'html')
a = gnp.extract_ads_blocket(html)
for idx, val in enumerate(a):
    print(idx, val)
print(a[0])
print(len(a))
# gnp.gnp_nettivene(html)
