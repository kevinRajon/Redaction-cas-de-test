import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.action_chains import ActionChains

@pytest.fixture(scope="function")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-search-engine-choice-screen")

    # Initialisation du driver
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(1920, 1080)
    yield driver
    driver.quit()

def test_connexion(driver):
    
    driver.get("https://inscription.it-akademy.fr/")
    
    driver.find_element(By.NAME, "username").send_keys("m.mansour@it-students.fr")
    time.sleep(2)
    driver.find_element(By.NAME, "password").send_keys("4xyhMWae")
    time.sleep(2)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(2)
    
    element = driver.find_element(By.CLASS_NAME, "page-title")
    
    assert element.text == "Mon dossier personnel", "Le titre de la page après connexion n'est pas 'Mon dossier personnel'. Vérifiez que la connexion a réussi."
    
    print("Test de connexion OK")

def test_deconnexion(driver):
    driver.get("https://inscription.it-akademy.fr/")
    
    # Connexion
    driver.find_element(By.NAME, "username").send_keys("m.mansour@it-students.fr")
    time.sleep(2)
    driver.find_element(By.NAME, "password").send_keys("4xyhMWae")
    time.sleep(2)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(2)
    
    # Récupérer le cookie "psi" après connexion
    psi_cookie_before = driver.get_cookie("psi")
    if psi_cookie_before:
        psi_value_before = psi_cookie_before['value']
        print(f"Valeur du cookie 'psi' après connexion : {psi_value_before}")
    else:
        print("Le cookie 'psi' n'a pas été trouvé après connexion. La connexion a peut-être échoué.")
    
    # Déconnexion
    menu_element = driver.find_element(By.CLASS_NAME, "top-menu")
    actions = ActionChains(driver)
    actions.move_to_element(menu_element).perform()
    time.sleep(2)
    
    # Vérification du cookie avant de cliquer sur la déconnexion
    psi_cookie_before_deco = driver.get_cookie("psi")
    if psi_cookie_before_deco:
        print(f"Valeur du cookie 'psi' juste avant la déconnexion : {psi_cookie_before_deco['value']}")
    else:
        print("Le cookie 'psi' n'est pas présent avant la déconnexion.")
    
    deco = ActionChains(driver)
    deco.move_to_element(driver.find_element(By.CLASS_NAME, "icon-key")).click().perform()
    time.sleep(2)
    
    # Vérification du cookie "psi" après déconnexion
    psi_cookie_after = driver.get_cookie("psi")
    if psi_cookie_after:
        psi_value_after = psi_cookie_after['value']
        print(f"Valeur du cookie 'psi' après déconnexion : {psi_value_after}")
        
        # Assurez-vous que la valeur du cookie est différente ou le cookie a été supprimé
        assert psi_value_before != psi_value_after, "Le cookie 'psi' n'a pas été invalidé après déconnexion. Vérifiez que la déconnexion a bien fonctionné."
    else:
        print("Le cookie 'psi' a été supprimé après déconnexion.")
        assert psi_cookie_after is None, "Le cookie 'psi' existe encore après déconnexion alors qu'il devrait être supprimé."
    
    print("Test de déconnexion OK, le cookie n'est plus présent.")
