# Taller

Ahora que ya conocemos como implementar serializadores propios, también podemos personalizar las vistas y las distintas operaciones que podemos permitir en ellas.

## Pre requisitos

Para no tener problemas en el desarrollo de este taller, recordar de tener implementado lo siguiente:

-   Dentro de `todos/serializers.py`:
    
    ```py
    class TodoSerializer(serializers.ModelSerializer):
        class Meta:
            model = Todo
            fields = '__all__'
            read_only_fields = 'created_at', 'done_at', 'updated_at', 'deleted_at'
    ```
    
-   Dentro de `todos/api.py`:
    
    ```py
    from .models import Todo
    from rest_framework import viewsets, permissions
    from .serializers import TodoSerializer
    
    class TodoViewSet(viewsets.ModelViewSet):
        queryset = Todo.objects.all()
        permission_classes = [permissions.AllowAny]
        serializer_class = TodoSerializer
    ```
    
-   Y dentro de `todos/urls.py`:
    
    ```py
    from rest_framework import routers
    from .api import TodoViewSet, DeleteAllTodo
    from django.urls import path
    
    router = routers.DefaultRouter()
    
    router.register('api/v1/todo', TodoViewSet, 'todos')
    urlpatterns += router.urls
    ```
    

Si todo está correctamente implementado, deberíamos poder acceder a la ruta `http://127.0.0.1:8000/api/v1/todo/` y ver una página de DRF, que nos permita hacer el ingreso de registros sin ningún problema.

## API views

Una APIView class, es el componente esencial de las vistas en DRF. Esta es la clase base de todos los tipos de vistas que existen en DRF. Las cuales pueden ser las siguientes.

-   Vistas basadas en funciones
    
-   Vistas basadas en clases
    
-   Mixins
    
-   Vistas genéricas basadas en clases
    
-   ViewSets
    

Las APIViews ofrecen mucha más libertad en la personalización, pero también añaden mucho más trabajo que realizar. Estas pueden ser una muy buena opción si buscas tener control sobre cualquier aspecto de tu vista o simplemente esta es muy complicada de realizar.

Ahora vamos a comenzar con la vista más básica.

Si recordamos nuestro modelo TODO:

```py
class Todo(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    done_at = models.DateField(null=True)
    updated_at = models.DateField(auto_now_add=True)
    deleted_at = models.DateField(null=True)
    status = models.IntegerField(default=0)
```

Podemos crear una vista que elimine todos nuestro registros de una sola vez.

```py
from rest_framework.response import Response
from rest_framework.views import APIView

class DeleteAllTodo(APIView):
    def delete(self, request):
        # Elimina todos los registros
        Todo.objects.all().delete()
        # Retorna un status code de 204 indicando que no existe contenido dentro de nuestra base de datos
        return Response(status=status.HTTP_204_NO_CONTENT)
```

Entonces, si queremos registrar esta vista dentro de nuestras rutas de la API ¿cómo lo hacemos?.

La anterior vista, la añadimos en `todos/api.py`. Luego de haberlo añadido, tendremos que modificar nuestras urls.

-   Dentro de `todos/urls.py`:

```py
# ...
from .api import TodoViewSet, DeleteAllTodo
from django.urls import path

# ...

urlpatterns = [
    path('api/v1/todo/delAll', DeleteAllTodo.as_view(),name='delAll'),  
]

urlpatterns += router.urls
```

Para este caso estamos agregándolo como un `as_view()` debido a que necesitamos retornar una vista que pueda hacer uso de un `request` y haga un `response`.

Nuestra nueva vista creada, no la vamos a poder utilizar de forma convencional, si tratamos de acceder a la ruta dentro de la vista que nos ofrece DRF, obtendremos el siguiente resultado.

![Error](https://photos.silabuz.com/uploads/big/18e32605bbd90c56378f28c81e5501d1.PNG)

Esto sucede debido a que el `ViewSet` implementado admite eliminaciones pero por objeto único, por lo que no podemos hacerlo en conjunto. Si queremos probar nuestra ruta tendremos que utilizar otro cliente.

![Delete All](https://photos.silabuz.com/uploads/big/a335ffb6dbdd6c988184b860f011362c.PNG)

¡Funciona nuestra ruta!

### ApiView para obtener todos los registros

Así como implementamos una vista que elimina todos los datos, también podemos añadir otra que permita obtener todos los datos, de la misma forma lo implementamos dentro de `todos/api.py`.

```py
class GetAllTodo(APIView):
    def get(self, request):
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many = True)
        return Response(serializer.data)
```

En este caso, aparte de especificar el serializador, encontramos el parámetro `many = True`, este parámetro indica al serializador que se le enviará un `queryset`, si no se especifica este parámetro, no podremos hacer uso del método `.all()` al momento de realizar la query, porque obtendremos un error.

Luego de crear nuestra `APIView`, la registramos como la otra vista, y podremos hacer uso de ella tanto en la página que nos ofrece DRF, como en otros clientes.

```py
# ...
from .api import GetAllTodo

# ...

urlpatterns = [
    # ... 
    path('api/v1/todo/getAll', GetAllTodo.as_view(),name='getAllTodo'),
]

urlpatterns += router.urls
```