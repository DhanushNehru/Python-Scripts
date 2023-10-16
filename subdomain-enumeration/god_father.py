import subprocess
import os
import string
import json

ascii_chars = set(string.printable)
"""
Open source tools used > 
subfinder
hhtpx  > httpx -title -tech-detect -status-code
"""

godfatehr='''
  /$$$$$$                  /$$       /$$$$$$$$         /$$     /$$                          
 /$$__  $$                | $$      | $$_____/        | $$    | $$                          
| $$  \__/  /$$$$$$   /$$$$$$$      | $$    /$$$$$$  /$$$$$$  | $$$$$$$   /$$$$$$   /$$$$$$ 
| $$ /$$$$ /$$__  $$ /$$__  $$      | $$$$$|____  $$|_  $$_/  | $$__  $$ /$$__  $$ /$$__  $$
| $$|_  $$| $$  \ $$| $$  | $$      | $$__/ /$$$$$$$  | $$    | $$  \ $$| $$$$$$$$| $$  \__/
| $$  \ $$| $$  | $$| $$  | $$      | $$   /$$__  $$  | $$ /$$| $$  | $$| $$_____/| $$      
|  $$$$$$/|  $$$$$$/|  $$$$$$$      | $$  |  $$$$$$$  |  $$$$/| $$  | $$|  $$$$$$$| $$      
 \______/  \______/  \_______/      |__/   \_______/   \___/  |__/  |__/ \_______/|__/       

 The only recon tool noobs need    
'''

base_domain = "nahamstore.com"
timeout = "timeout 180 "
print_all = True
accept_status_code=[200]

def get_subdomains():
  __sub_domains=[]
  subprocess.run(timeout+"subfinder -d "+base_domain+" > "+base_domain+"/subfinder_output.txt",shell=True)
  subprocess.run("cp "+base_domain+"/subfinder_output.txt "+base_domain+"/subfinder_output_bkp.txt",shell=True)
  print("\nRemove unnecassary sub-domains from "+base_domain+"/subfinder_output.txt (Y)")
  input()
  try:
    with open(base_domain+"/subfinder_output.txt", "r") as file:
        __sub_domains = file.read()
        print("\nsub_domains -! \n",len(__sub_domains))
        if print_all:
          print("\nsub_domains -! \n")
          print(__sub_domains)
  except FileNotFoundError:
      print(f"File not found.")
  except Exception as e:
      print(f"An error occurred: {e}")
  print("Done gathering subdomins from <subfinder>")
  return __sub_domains

def get_tech_stack():
  subprocess.run(f'cat {base_domain+"/subfinder_output.txt"} | httpx-toolkit -o {base_domain+"/httpx_output.json"} -json -title -tech-detect -status-code',shell=True)
  tech_stack = []
  try:
    with open(base_domain+"/httpx_output.json", "r") as file:
      temp_data = file.read()
      write_to_file_text = ""
      for i in temp_data.split("\n"):
         try:
          tech_stack_temp = json.loads(i)
          if tech_stack_temp.get("status-code") in accept_status_code:
            if tech_stack_temp.get("url"):
              write_to_file_text+=tech_stack_temp.get("url")+"\n"
            tech_stack.append(tech_stack_temp)
         except:
          continue
      if tech_stack:
        for page in tech_stack:
          print("--------------------------------------------------------------")
          print(page.get("url","Page url not found"),"--->",page.get("title","Page title not found"))
          if print_all:
            for page_key in page:
              print(page_key,"\t : ",page[page_key])
      if write_to_file_text:
        text_file = open(base_domain+"/domains_after_filter.txt", "w")
        text_file.write(write_to_file_text)  
        text_file.close()
  except FileNotFoundError:    
      print(f"File not found.")
  except Exception as e:
      print(f"An error occurred: {e}")
  return tech_stack

def init():
  if not os.path.exists(base_domain):
    print("Creating directory")
    os.makedirs(base_domain)

def get_urls():
  print("pass")

print(godfatehr)
init()
sub_domains = get_subdomains()
tech_stack = get_tech_stack()


