# _AutoFollow-o-mático_
[![NPM](https://img.shields.io/npm/l/react)](https://github.com/andrerogersdev/AutoFollow-o-matico/blob/main/LICENSE) 

# Sobre o projeto

_AutoFollow-o-mático_ é um robô automatizado projetado para realizar o login na conta do usuário do Instagram e seguir pessoas automaticamente. Ele funciona utilizando tecnologias de automação como Selenium, um simples banco de dados com openpyxl e uma interface com PySimpleGui.

# Tecnologias Utilizadas
## Back-End
- Python
- selenium

## Front-End
- PySimpleGui

# Como Funciona o Projeto?
## Dados de login
O _AutoFollow-o-mático_ conta com uma simples funcionalidade de banco de dados utilizando excel.
- Primeiro ele tenta abrir a planilha que contenha os dados de login do instagram do usuário.

  ```python
  try:
      livro = openpyxl.load_workbook('C:\\Users\\Allya\\OneDrive\\Documentos\\Seguidores\\Planilha Instagram.xlsx')
      Iniciar = True
  except FileNotFoundError:
      ColetarDados = True
  else:
      ColetarDados = False
  ```

- Se ele não conseguir, abrirá uma janela que pedirá as informações de login.
  
  ![ImagemJanelaColetandoDados](https://github.com/andrerogersdev/AutoFollow-o-matico/blob/main/e1.png)
  
  ```python
  if ColetarDados:
    sg.theme('Reddit')
    layout = [

        [sg.Text('-Email ou Nome: \t'), sg.Input(key='Email',size=(30,1))],
        [sg.Text('-Senha: \t\t'),sg.Input(key='senha',password_char='#',size=(30,1))],
        [sg.Button('Confirmar')]

    ]

    janela = sg.Window('InstaBot',layout)

  ```

   
- E então guardará essa informação numa planilha.

  ```python
    #ler eventos
    while True:
        eventos,valores = janela.read()
        if eventos == sg.WINDOW_CLOSED:
            Iniciar = False
            break
        if eventos == 'Confirmar':
            Iniciar = True
            email = valores['Email']
            senha = valores['senha']
            book = openpyxl.Workbook()
            book.create_sheet('Instagram')
            InstaPage = book['Instagram']
            InstaPage.append([email,senha])
            book.save('Planilha Instagram.xlsx')
            janela.close()
            break
  ```
  
- E na proxima vez que for inicado, usará a planilha que contém as informações de login e senha.

## Login
- O _AutoFollow-o-mático_ abrirá o navegador Edge que será automatizado com selenium.

  ```python
  while True:
    if Iniciar:
        #Navegador Edge
        Edge_profile = 'user-data-dir=C:\\Users\\Allya\\AppData\\Local\\MicrosoftEdge\\User\\instabot'
        opt = webdriver.EdgeOptions()
        opt.add_argument(Edge_profile)
        opt.add_argument("--window-size=1366,768")
        opt.add_argument('--mute-audio')
        #opt.add_argument('--headless')
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()),options=opt)

        driver.get('https://www.instagram.com/')
  ```

- Então tentará fazer o login na sua conta.

  ```python
  try:
      logar(email,senha)
  except:
      None
  ```
  Mas caso já esteja logado, o navegado apenas prosseguirá.
  
## Seguir
- Com o Login feito com sucesso, ele ativará a função de seguir pessoas:
  ```python
  seguir()
  ```


### MUITO IMPORTANTE
- Colocar as informações de nome de usuário ou email e senha CORRETAMENTE. Pois caso houver algum erro, a planilha salvará essas informações incorretas e o _AutoFollow-o-mático_ não funcionará. Será preciso apagar a planilha com as informações erradas e inicializar o programa novamente.
- Não cancele o processo de coletar dados. Pois o _AutoFollow-o-mático_ não funcionará. Será preciso inicializar o programa novamente.

- Sempre que for usar _outra conta no Instagram_ para aplicar o _AutoFollow-o-mático_:
  - 1° Rode o _AutoFollow-o-mático_, deixe o navegador abrir sua conta já logada, deslogue manualmente dessa conta e feche o navegador.
  - 2° apague a planilha que já contenha as informações de login e senha.
  - Rode novamente o _AutoFollow-o-mático_.

## Informaçãoes adicionais
O _AutoFollow-o-mático_ possui uma funcionalidade excelente para projetos de automação web, que é o _SALVAMENTO DE DADOS_ Do navegador. Com isso, após o primeiro login, essa informação de login do navegador automatizado será guardada numa pasta no sistema, assim, na próxima vez que o _AutoFollow-o-mático_ for inicializado, será aberto o navegador com as informações salvas. Então, não será necessário realizar o logim na mesma conta novamente.

Além de possuir também um mini banco de dados em excel que guarda o nome ou email e senha da conta do instagram do usuário. Assim, se for necessário realizar o login, o robô usará essas informações salvas na planilha.

2 sacadas geniais né.

Ambas funcionalidades pensadas e programadas para deixar ainda mais automático o _AutoFollow-o-mático_.

### Funções
- Dormir: essa função é um sleep mais sofisticado, que permite o usuário ver quanto tempo ainda falta para o próximo passo.

  ```python
  def dormir(tempo):
            print(f"Esperando {tempo} segundos")
            for c in range(0,tempo):
                print(c)
                sleep(1)
            print('-Espera Finalizada-')
  ```

- Logar: Essa função tentará realizar o Login utilizando as informações de nome ou email e senha salvas na planilha.
  ```python
          def logar(email,senha):
            try:
                logado = driver.find_element("xpath","//img[contains(@crossorigin,'anonymous')]").click()   
            except:
                print("Ainda não logado")

                clicar("input","name","username",escrever=email)
                dormir(5)
                clicar("input","name","password",escrever=senha)
                print("senha inserida com sucesso")
                sleep(1)
                print('logando')
            else:
                print("Já logado")
            dormir(20)
  
  ```

- clicar: Essa função Resume o processo do selenium encontrar um elemento no navegador, passando apenas os parâmetros necessários.
  ```python
  def clicar(tipo,valor,valordovalor,escrever=0):
    while True:
        if escrever != 0:
            try:
                a = driver.find_element("xpath",f"//{tipo}[contains(@{valor},'{valordovalor}')]")
                a.click()
                dormir(3)
                a.send_keys(escrever)
                a.send_keys(Keys.ENTER)
            except:
                dormir(10)
            else:
                print("Clicado com sucesso!")
                break
        else:
            try:
                a = driver.find_element("xpath",f"//{tipo}[contains(@{valor},'{valordovalor}')]")
                a.click()
            except:
                print("não encontrado, esperando 1 segundo.")
                sleep(1)
            else:
                print("clicado com sucesso!")
                break
  ```
  Me orgulho tanto desta função. Eu literalmente descobrir como programá-la enquanto dormia.
  
  Por que ela é tão top?

  _Ex login sem essa função:_
  ```python
    def logar(email,senha):
      try:
          logado = driver.find_element("xpath","//img[contains(@crossorigin,'anonymous')]").click()   
      except:
          print("Ainda não logado")
          logEmail = driver.find_element('xpath','//input[contains(@name,"username")]')
          dormir(5)
          logEmail.click()
          dormir(5)
          logEmail.send_keys(email)    
          print("Nome inserido com sucesso!") 
          dormir(5)
          logSenha = driver.find_element('xpath','//input[contains(@name,"password")]')
          dormir(5)
          logSenha.click()
          logSenha.send_keys(senha)
          dormir(5)
          logSenha.send_keys(Keys.ENTER)
          print("senha inserida com sucesso")
          sleep(1)
          print('logando')
  ```
  _Login com a Função:_
  ```python
    def logar(email,senha):
      try:
          logado = driver.find_element("xpath","//img[contains(@crossorigin,'anonymous')]").click()   
      except:
          print("Ainda não logado")
          clicar("input","name","username",escrever=email)
          dormir(5)
          clicar("input","name","password",escrever=senha)
          print("senha inserida com sucesso")
          sleep(1)
          print('logando')
    ```

  #### O código fica lindo, resumido e funcional!!

- Função Seguir: Seguirá as pessoas recomendadas no instagram, fazendo pausas periodicas de 10 minutos ou 1 hora, reiniciando a página para que mais pessoas sejam sugeridas e seguidas.

  ```python
    def Seguir():
      driver.get("https://www.instagram.com/explore/people/")
      dormir(10)
      while True:
          seguir = driver.find_elements("xpath","//*[contains(text(), 'Seguir')]")
          try:
              b = 0
              for c in range(0,50):
                  seguir[c].click()
                  b += 1
                  if b == 20:
                      print('+20 pessoas seguidas, dormindo 10 minutos')
                      dormir(600)
                      driver.refresh()
                      dormir(15)
                  elif b == 50:
                      reiniciar == True
                      break
                  print("+1 seguido")
                  dormir(5) 
          except:
              driver.save_screenshot('erro.png')
              print('erro, reiniciando a página e dormindo 1 hora')
              dormir(3600)
              reiniciar = True
          else:
              reiniciar = False
    
          if reiniciar:
              print('reiniciando página')
              driver.refresh()
              dormir(10)
    ```

caso houver algum erro no processo, o _AutoFollow-o-mático_ salvará uma foto (erro.png) no momento em que ocorreu o erro para o programador analisar depois.

# Como executar o projeto
## Back-End
Pré-requisitos: 
- Python 3
- Navegador Microsoft Edge
- ### Instale as bibliotecas
- selenium
- PySimpleGui
  
## Baixe o projeto
### Recomendo Fortemente criar uma pasta e colocar nele o código baixado.
e depois, Abra no Editor de códigos.

## Faça Alterações

## Altere
- (linha 11) livro = openpyxl.load_workbook('C:\\Users\\Allya\\OneDrive\\Documentos\\Seguidores\\Planilha Instagram.xlsx')
- (linha 102) livro = openpyxl.load_workbook('C:\\Users\\Allya\\OneDrive\\Documentos\\Seguidores\\Planilha Instagram.xlsx')
- #### Em 'C:\\Users\\Allya\\OneDrive\\Documentos\\Seguidores\' Troque para o caminho da pasta em que está o código.

## Altere
-  Edge_profile = 'user-data-dir=C:\\Users\\Allya\\AppData\\Local\\MicrosoftEdge\\User\\instabot'
  #### Em \\Allya\\ para o nome de usuário da sua máquina.
  ### por quê?
  - Essa funcionalidade permite que o selenium salve no seu computador na pasta \\instabot os dados do navegador que será automatizado.

## Notas do Autor

Use com moderação e fique atento as diretrizes do Instagram.

Entre em contato caso houver algum erro e quiser uma ajuda com o _AutoFollow-o-mático_

# Autor

andrerogersdev

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/andrerogersdev/)
[![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/andrerogersdev)
