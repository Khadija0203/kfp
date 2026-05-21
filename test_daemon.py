import sys
import os

# 1. FORCE l'utilisation de ton code local
#mon_code_kfp = r"C:\Users\xadee\Downloads\prototype\prototype\kfp-argo\LES2\H3\kfp\sdk\python"
mon_code_kfp = r"C:\kfp\sdk\python"
if mon_code_kfp not in sys.path:
    sys.path.insert(0, mon_code_kfp)

import kfp
from kfp import dsl
from kfp import compiler

print(f"DEBUG: Chargement de KFP depuis : {kfp.__path__}")

# CORRECTION ICI : Pour utiliser ContainerSpec, il faut @dsl.container_component
@dsl.container_component
def service_node():
    return dsl.ContainerSpec(image="alpine", command=["sleep", "1000"])

@dsl.component
def client_node():
    print("Le client a démarré !")

@dsl.pipeline(name="test-daemon-pipeline")
def my_pipeline():
    # On appelle ta nouvelle fonction !
    # service_node() retourne un objet PipelineTask
    srv = service_node()
    srv.set_daemon(True) 
    
    cli = client_node().after(srv)

if __name__ == "__main__":
    # On compile
    try:
        compiler.Compiler().compile(my_pipeline, "pipeline.json")
        print("Compilation terminée : pipeline.json généré.")
    except AttributeError as e:
        print(f"ERREUR : La méthode set_daemon n'est toujours pas reconnue.")
        print(f"Détail : {e}")
    except Exception as e:
        print(f"Autre erreur lors de la compilation : {e}")
