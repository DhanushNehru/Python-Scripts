import wikipedia

search=input("Enter the topic you want: ")
print(wikipedia.summary(search))

language = "jp"
wikipedia.set_lang(language)

print(f"Summary of Open source in {language}:", wikipedia.page("Open Source").summary)