# misw4304-202414-g10

## Video Sustentación Entrega 3:

[Video](https://uniandes-my.sharepoint.com/:v:/g/personal/ma_diazf1_uniandes_edu_co/EYDReF-R55hCuUQ5EdiOZ-YBspgW_JYGeyD6Gb8wuYHyxA?e=cZ9V6S&nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D)

## Video Sustentación Entrega 2:

[Video](https://uniandes-my.sharepoint.com/:v:/g/personal/ma_diazf1_uniandes_edu_co/Ed2OGkU8wXpHn4c9EhTXf7QBJLWP1XtKRxh49_h2Vyt1Lg?e=E4aqfN)

## Endpoints de la aplicación:


La aplicación expone los siguientes endpoints por medio de Flask:

- /ping: GET, permite la consulta del estado de salud de la aplicación.

- /blacklists: POST, permite la adición de un nuevo correo a la lista negra. Como body deben enviarse los campos `"email"` y `"app_uuid"` obligatoriamente. El campo `"blocked_reason"` es opcional. Adicionalmente, debe enviarse un Bearer Token como header.

    ```
    {
    "email": "testmail4@mail.com",
    "app_uuid": "56c58bc7-376d-43f9-923d-af3682ce04cf",
    "blocked_reason": "Intento de fraude"
    }
    ```

- /blacklists/<:email>: GET, permite consultar la existencia de un correo en la lista negra.
    Como parámetros debe enviarse el correo a consultar en la url y se debe enviar el Bearer Token como header.

## Documentación Postman:

https://documenter.getpostman.com/view/3681846/2sAXxY2TTp