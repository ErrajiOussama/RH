from django.contrib.auth.backends import BaseBackend


class CollaborateurAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        from .models import Collaborateur
        try: 
            print(username)
            agent = Collaborateur.objects.get(username=username)
            if agent.password == password:
                print("good")
                return agent
            else:
                return None
        except Collaborateur.DoesNotExist:
            print("not good")
            return None               