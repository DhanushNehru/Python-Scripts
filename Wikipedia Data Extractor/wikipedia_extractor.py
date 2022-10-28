import wikipedia


print(wikipedia.summary("Open Source"))



language = "jp"
wikipedia.set_lang(language)

print(f"Summary of Open source in {language}:", wikipedia.page("Open Source").summary)