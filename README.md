# BotTDI
Tabajo sobre un bot realizado en grupo para Taller de Internet II
Tipos de respuestas: 
● Por lo menos una respuesta debe tener formateado el texto con negrita, cursiva y/o subrayado. 
● Por lo menos una respuesta debe contener algún archivo (imagen, video, etc). (RESPONDIENDO A CONFIANZA EN EL PRESIDENTE)
● Alguna respuesta debe contener el listado de los comandos principales disponibles. 
● Por lo menos alguna de las respuestas debe contener emojis dentro del texto. 
● Por lo menos una respuesta debe tener la acción. Ej:“enviando” (chat_action “typing”). ########
● Por lo menos una respuesta con más de un chat como respuesta. (EN LA CONFIANZA EN EL PRESIDENTE, PUEDE MOSTRAR EL GRAFICO EN UN MENSAJE, Y EN EL OTRO EL ULTIMO VALOR)
Funcionalidades: 
• Los comandos y funciones visibles/navegables y sugeridas en el flujo conversacional deben tener relación con la temática del bot. 
• El comando /start debe saludar al usuario que escribe por su nombre y ayudar a entablar el flujo de diálogo. 
• Debe poder responder al pedido de la cotización del dólar (en caso de que no tenga relación con la temática del bot dejar la opción oculta para el usuario). 
• Debe poder responder a comandos, texto, documentos y audio. 
• Debe contener alguna respuesta con atajos en formato de botones “inline”. 
• Por lo menos una respuesta en la que el usuario tenga que introducir un dato y se realice algún cálculo o consulta a otra API. (CON X CANT DE PESOS CUANTOS DOLARES SE PUEDEN COMPRAR)
• Por lo menos una respuesta relacionada a la consulta de otra API (puede ser de las sugeridas por el profesor). ########
• Registrar las interacciones en un archivo .csv para medir el uso del bot en otro notebook y/o reutilizar el archivo para devolver historial de las últimas 5 consultas a un usuario con el comando /historial. 
• El .csv de historial debe contener (de mínima), la siguiente información: ○ Horario (timestamp) en que se envió el mensaje ○ Chat.id que envió el mensaje ○ Nombre de quien envió el mensaje ○ Mensaje enviado 


- Ideas de proposito del bot:
  Bot educativo en relacion a temas de finanzas, politica actual y cultura general
  que pueda tratar temas de presidentes hisoricos, calculo de dolar, dsitribucion de partidos por porivincia, riesgo pais, confianza en los gobiernos, inflacion, etc.
  serie de comandos:
  /hola o decir algun saludo sin usar comando
  /ayuda (donde va a detallar sus funciones)
  /finalizar

  luego, es necesario que entienda audios (simplemente que reconozca que es un archivo de auidio y decir que no lo puede decodificar)
  mostrar dashborads no solamente respuestas de texto
  minimo 4 funciones para mortrar

EN LOS ARCHIVOS .env TODAS LAS VARIABLES VAN EN MAYUSCULAS Y NO SE PUEDEN CAMBIAR DURANTE LA EJECUCION DEL PROGRAMA

  se utilizara la API de Telegram y La API datos argentina

  ### Estrucutura de carpetas:

  Proyecto -> carpeta: bot_base_con_func
                         |
                         |--> .env (API_KEY_DATOS_ARG; CHAT_ID_ADMIN)
                         |
                         |--> archivos -----> doc --> 1.pdf
                         |                |--> img --> png --> varias img
                         |
                         |--> Json
