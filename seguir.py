#Bibliotecas
import openpyxl
from time import sleep
from selenium import webdriver
from PySimpleGUI import PySimpleGUI as sg
from selenium.webdriver.common.keys import Keys
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service as EdgeService

try:
    livro = openpyxl.load_workbook('C:\\Users\\Allya\\OneDrive\\Documentos\\Seguidores\\Planilha Instagram.xlsx')
    rodar = True
except FileNotFoundError:
    roda = True
else:
    roda = False

if roda:
    sg.theme('Reddit')
    layout = [

        [sg.Text('-Email: \t\t'), sg.Input(key='Email',size=(30,1))],
        [sg.Text('-Senha: \t\t'),sg.Input(key='senha',password_char='#',size=(30,1))],
        [sg.Text('-Seguidores: \t'),sg.Input(key='Qtd',size=(30,1))],
        [sg.Button('Confirmar')]

    ]

    janela = sg.Window('InstaBot',layout)


    #ler eventos
    while True:
        eventos,valores = janela.read()
        if eventos == sg.WINDOW_CLOSED:
            rodar = False
            break
        if eventos == 'Confirmar':
            rodar = True
            email = valores['Email']
            senha = valores['senha']
            qtd_Segui = int(valores['Qtd'])
            book = openpyxl.Workbook()
            book.create_sheet('Instagram')
            InstaPage = book['Instagram']
            InstaPage.append([email,senha,qtd_Segui])
            book.save('Planilha Instagram.xlsx')
            janela.close()
            break

sleep(10)

while True:
    if rodar:
        #Navegador Edge
        Edge_profile = 'user-data-dir=C:\\Users\\Allya\\AppData\\Local\\MicrosoftEdge\\User\\Whats'
        opt = webdriver.EdgeOptions()
        opt.add_argument(Edge_profile)
        opt.add_argument("--window-size=1366,768")
        opt.add_argument('--mute-audio')
        opt.add_argument('--headless')
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()),options=opt)

        driver.get('https://www.instagram.com/')

        def clicar(x,id,input=0):
            while True:
                if input != 0:
                    try:
                        a = driver.find_element(x,id)
                        a.click()
                        durmir(3)
                        a.send_keys(input)
                        a.send_keys(Keys.ENTER)
                    except:
                        durmir(10)
                    else:
                        break
                else:
                    try:
                        a = driver.find_element(x,id)
                        a.click()
                    except:
                        durmir(10)
                    else:
                        break
                break
        def durmir(tempo):
            print(f"Esperando {tempo} segundos")
            for c in range(0,tempo):
                print(c)
                sleep(1)
            print('-Espera Finalizada-')
        print('Abrindo site')
        durmir(15)
        livro = openpyxl.load_workbook('C:\\Users\\Allya\\OneDrive\\Documentos\\Seguidores\\Planilha Instagram.xlsx')
        Dados = livro['Instagram']
        for rows in Dados.iter_rows(max_row=1):
            email = rows[0].value
            senha = rows[1].value
            qtd_Segui = rows[2].value

        def logar(email,senha):
            logEmail = driver.find_element('xpath','//input[contains(@name,"username")]')
            durmir(5)
            logEmail.click()
            durmir(5)
            logEmail.send_keys(email) 
            durmir(5)
            logSenha = driver.find_element('xpath','//input[contains(@name,"password")]')
            durmir(5)
            logSenha.click()
            logSenha.send_keys(senha)
            durmir(5)
            logSenha.send_keys(Keys.ENTER)
            print('logando')
            durmir(20)
        

        def Seguir():
            driver.get("https://www.instagram.com/explore/people/")
            durmir(10)
            t = 0
            for rows in Dados.iter_rows(max_row=1):
                 qtd_Segui = rows[2].value
            while qtd_Segui > 0:
                seguir = driver.find_elements("xpath","//*[contains(text(), 'Seguir')]")
                b = 0
                try:
                    for c in range(0,50):
                        seguir[c].click()
                        b += 1
                        if b == 25:
                            print('+25 seguidores, dormindo 10 minutos')
                            durmir(600)
                        elif b == 50:
                            print('+50 seguidores, dormindo 1 hora')
                            durmir(3600)
                        print("+1 seguido")
                        durmir(5)
                    qtd_Segui -= b
                    
                except:
                    err = driver.save_screenshot('erro.png')
                    print('erro, dormindo 1 hora')
                    durmir(3600)
                    reiniciar = True
                else:
                    reiniciar = False

                if reiniciar:
                    print('reiniciando página')
                    driver.refresh()
                    durmir(10)


        try:
            logar(email,senha)
        except:
            None
        durmir(5)
        Seguir()
        durmir(5)
        driver.quit()
        break
    else:
        break