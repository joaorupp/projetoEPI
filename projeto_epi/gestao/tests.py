import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Fixture para gerenciar o navegador (abre antes e fecha depois do teste)
@pytest.fixture(scope="function")
def driver():
    # Em vez de deixar o ChromeDriverManager detectar a versão (que causa o erro)
    # nós forçamos o uso do Service sem passar o caminho, 
    # ou baixamos o driver manualmente uma única vez.
    
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    try:
        # Tenta iniciar o Chrome diretamente (funciona se o ChromeDriver estiver no PATH)
        driver = webdriver.Chrome(options=options)
    except:
        # Se falhar, usamos o manager, mas sem a detecção de versão que trava no Windows PT-BR
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.service import Service
        
        # Forçamos uma versão específica para pular a detecção automática problemática
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


# O teste usando o live_server do pytest-django
@pytest.mark.django_db
def test_home_title(driver, live_server):
    # O live_server.url é o endereço temporário do seu Django de teste
    driver.get(live_server.url)
    print(f"\nAcessando: {live_server.url}")
    
    # Verifica o título (o título da sua página home)
    assert "Projeto EPI" in driver.title

# def test_erro_proposital():
#     assert 1 + 1 == 2

