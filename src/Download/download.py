################################
#
#    Script to bulk download 
#     images from Pinterest
#
#               by
#
#        Code Monkey King
#
################################

# packages
import requests
from bs4 import BeautifulSoup

# open local html file with image links
with open('images.html') as f:
    html = f.read()

# parse HTML content
content = BeautifulSoup(html, 'lxml')

# extract pins
pins = content.findAll('a', {'class': 'Wk9 xQ4 CCY czT DUt kVc MNX LIa'})

# extract images from pins
for pin in pins:
    try:
        # extract image link
        image_link = pin.find('img')['srcset'].split(',')[1].split()[0]
        
        # extract image filename
        #filename = image_link.split('.jpg')[0].split('/')[-1] + '.jpg'
        filename = pin.find('img')['alt'].replace(' ', '_')
        
        # make HTTP request to the image url
        response = requests.get(image_link)
        print('Downloading', image_link)
        
        # write bytes to file
        with open(filename, 'wb') as i:
            i.write(response.content)
        
        #break
    except:
        pass

























