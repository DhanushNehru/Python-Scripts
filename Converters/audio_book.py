import pyttsx3
import PyPDF2
book = open('python_basics.pdf','rb')
val = input("Enter the page no from where you want to start: ")
val_converted = int(val)
start_page = val_converted-1
pdfReader = PyPDF2.PdfFileReader(book)
page = pdfReader.numPages
print(page)
speaker = pyttsx3.init()
for num in range(start_page,page):
	page = pdfReader.getPage(start_page)
	text = page.extractText()
	speaker.say(text)
	speaker.runAndWait()